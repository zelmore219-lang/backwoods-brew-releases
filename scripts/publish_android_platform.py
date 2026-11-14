"""Publish an accepted, signed Employee Android update without changing Windows."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "android-platform-updates" / "employees"
REPO = "zelmore219-lang/backwoods-brew-releases"
FEED_TAG = "employee-updates"
FEED_NAME = "backwoods-employees-updates.json"
PREFIX = f"https://github.com/{REPO}/releases/download/"
FEED_URL = PREFIX + FEED_TAG + "/" + FEED_NAME


def gh(*arguments):
    return subprocess.check_output(["gh", *arguments], text=True)


def api(path):
    return json.loads(gh("api", f"repos/{REPO}/{path}"))


def checksum(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def semver(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("Invalid stable Android version")
    return tuple(map(int, value.split(".")))


def payload_checksum(path):
    result = hashlib.sha256()
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if re.fullmatch(r"META-INF/[^/]+\.(SF|RSA|DSA|EC)|META-INF/MANIFEST.MF", name):
                continue
            result.update(name.encode() + b"\0" + hashlib.sha256(archive.read(name)).digest())
    return result.hexdigest()


def accepted_source(metadata, evidence, windows_provenance):
    semver(metadata["version"])
    source = metadata["sourceSHA"]
    if not re.fullmatch("[a-f0-9]{40}", source):
        raise ValueError("Use the exact accepted source")
    if (evidence.get("headSha") != source or evidence.get("status") != "completed"
            or evidence.get("conclusion") != "success"):
        raise ValueError("The exact source must pass native acceptance")
    jobs = {job["name"]: job for job in evidence.get("jobs", [])}
    if any(jobs.get(name, {}).get("status") != "completed"
           or jobs.get(name, {}).get("conclusion") != "success"
           for name in ("android", "windows")):
        raise ValueError("Android and Windows acceptance must both pass")
    if (windows_provenance.get("sourceSha") != source
            or windows_provenance.get("version") != metadata["version"]
            or windows_provenance.get("windowsAcceptanceRun") != metadata["acceptanceRun"]):
        raise ValueError("Android must use the already accepted Windows release source")


def revised_feed(original, info):
    if original.get("schemaVersion") != 1 or set(original.get("apps", {})) != {"employees"}:
        raise ValueError("Use the separate Employee feed")
    prior = original["apps"]["employees"]["android"]
    if (prior["packageName"] != info["packageName"]
            or prior["certificateSha256"] != info["certificateSha256"]):
        raise ValueError("The installed Android signing identity cannot change")
    if (semver(info["version"]) < semver(prior["version"])
            or type(info["versionCode"]) is not int or info["versionCode"] < prior["versionCode"]):
        raise ValueError("Refusing an Android downgrade")
    if info["versionCode"] == prior["versionCode"]:
        if any(prior.get(key) != value for key, value in info.items()):
            raise ValueError("An existing Android version cannot gain different package bytes")
        return copy.deepcopy(original)
    if semver(info["version"]) <= semver(prior["version"]):
        raise ValueError("A new Android version code needs a newer release version")
    result = copy.deepcopy(original)
    result["apps"]["employees"]["android"] = info.copy()
    result["apps"]["employees"]["notes"] = (
        f"Android {info['version']}: shared-account setup and owner-service discovery repairs. "
        + original["apps"]["employees"].get("notes", "")
    )
    return result


def assemble(metadata):
    if (metadata["app"] != "employees" or metadata["platform"] != "android"
            or metadata["name"] != f"Backwoods-Employees-{metadata['version']}.apk"):
        raise ValueError("Invalid Employee Android package")
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    target = output / metadata["name"]
    with target.open("wb") as stream:
        for part in metadata["parts"]:
            path = (ROOT / part["path"]).resolve()
            if not path.is_relative_to(PACKAGES.resolve()):
                raise ValueError("Package parts must stay in the Android staging folder")
            raw = path.read_bytes()
            if len(raw) != part["size"] or hashlib.sha256(raw).hexdigest() != part["sha256"]:
                raise ValueError("Android package part checksum mismatch")
            stream.write(raw)
    if target.stat().st_size != metadata["size"] or checksum(target) != metadata["sha256"]:
        raise ValueError("Reassembled APK checksum mismatch")
    if payload_checksum(target) != metadata["payloadSHA256"]:
        raise ValueError("The accepted unsigned application payload changed")
    return target


def verify_apk(metadata, target):
    sdk = Path(os.environ.get("ANDROID_HOME", os.environ.get("ANDROID_SDK_ROOT", "/workspace/android-sdk")))
    tools = sdk / "build-tools" / "35.0.0"
    certificates = subprocess.check_output(
        [str(tools / "apksigner"), "verify", "--verbose", "--print-certs", str(target)], text=True)
    match = re.search(r"Signer #1 certificate SHA-256 digest: ([a-f0-9]+)", certificates)
    if not match or match.group(1) != metadata["certificateSha256"]:
        raise ValueError("Signed APK certificate mismatch")
    badging = subprocess.check_output([str(tools / "aapt"), "dump", "badging", str(target)], text=True)
    for expected in (f"name='{metadata['packageName']}'", f"versionCode='{metadata['versionCode']}'",
                     f"versionName='{metadata['version']}'", f"sdkVersion:'{metadata['minSdk']}'"):
        if expected not in badging:
            raise ValueError("Signed APK identity/version/device compatibility mismatch")
    if "application-debuggable" in badging:
        raise ValueError("Do not publish a debug application")
    abis = re.findall(r"'([^']+)'", next(line for line in badging.splitlines() if line.startswith("native-code:")))
    if abis != metadata["abis"]:
        raise ValueError("Signed APK ABI mismatch")


def public_bytes(url):
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "Backwoods-release-verifier"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def verify_public(url, size, digest):
    failure = None
    for delay in (0, 2, 4, 8, 16):
        if delay:
            time.sleep(delay)
        try:
            data = public_bytes(url)
            if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
                raise ValueError("Public APK checksum mismatch")
            return
        except Exception as error:
            failure = error
    raise RuntimeError("Public APK verification failed; no updater was enabled") from failure


def asset(release, name):
    return next((item for item in release["assets"] if item["name"] == name), None)


def ensure_asset(tag, release_id, path):
    current = api(f"releases/{release_id}")
    previous = asset(current, path.name)
    if previous:
        if previous.get("digest") != "sha256:" + checksum(path) or previous["size"] != path.stat().st_size:
            raise ValueError("Refusing to replace an existing release asset")
        return
    # Append this platform only; published Windows assets are never replaced.
    gh("release", "upload", tag, str(path), "--repo", REPO)
    uploaded = asset(api(f"releases/{release_id}"), path.name)
    if (not uploaded or uploaded.get("digest") != "sha256:" + checksum(path)
            or uploaded["size"] != path.stat().st_size):
        raise ValueError("Android release upload failed digest verification")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    metadata = json.loads((PACKAGES / "package.json").read_text())
    target = assemble(metadata)
    verify_apk(metadata, target)
    tag = "employees-" + metadata["version"]
    release = api("releases/tags/" + tag)
    if release["draft"]:
        raise ValueError("The accepted Windows release must already be public")
    provenance = json.loads(public_bytes(PREFIX + tag + "/release-source.json"))
    accepted_source(metadata, json.loads((PACKAGES / "native-acceptance.json").read_text()), provenance)
    raw = public_bytes(FEED_URL)
    original = json.loads(raw)
    channel = api("releases/tags/" + FEED_TAG)
    before = asset(channel, FEED_NAME)
    if not before or before.get("digest") != "sha256:" + hashlib.sha256(raw).hexdigest():
        raise ValueError("The public updater feed is stale; retry after propagation")
    keys = ("version", "versionCode", "packageName", "certificateSha256", "minSdk", "abis", "size", "sha256")
    info = {key: metadata[key] for key in keys}
    info.update(url=PREFIX + tag + "/" + target.name, firstInstallOnly=False)
    updated = revised_feed(original, info)
    print(json.dumps({"verified": True, "version": metadata["version"], "sha256": metadata["sha256"],
                      "windowsPreserved": updated["apps"]["employees"]["windows"] == original["apps"]["employees"]["windows"],
                      "publish": args.publish}), flush=True)
    if not args.publish:
        return
    sums = target.parent / "ANDROID-SHA256SUMS.txt"
    sums.write_text(metadata["sha256"] + "  " + target.name + "\n")
    proof = target.parent / "android-release-source.json"
    proof.write_text(json.dumps({key: metadata[key] for key in metadata if key != "parts"}, indent=2) + "\n")
    for path in (target, sums, proof):
        ensure_asset(tag, release["id"], path)
    after = api(f"releases/{release['id']}")
    for previous in release["assets"]:
        retained = asset(after, previous["name"])
        if not retained or (retained["id"], retained.get("digest")) != (previous["id"], previous.get("digest")):
            raise ValueError("An existing release asset changed concurrently")
    verify_public(info["url"], info["size"], info["sha256"])
    fresh = asset(api("releases/tags/" + FEED_TAG), FEED_NAME)
    if not fresh or (fresh["id"], fresh.get("digest")) != (before["id"], before.get("digest")):
        raise ValueError("The Employee feed changed concurrently; refusing to overwrite it")
    if updated != original:
        feed = target.parent / FEED_NAME
        feed.write_text(json.dumps(updated, indent=2) + "\n")
        try:
            gh("release", "upload", FEED_TAG, str(feed), "--repo", REPO, "--clobber")
        except Exception:
            latest = asset(api("releases/tags/" + FEED_TAG), FEED_NAME)
            if latest and latest.get("digest") == "sha256:" + checksum(feed):
                pass
            elif not latest:
                rollback = target.parent / "rollback" / FEED_NAME
                rollback.parent.mkdir(exist_ok=True)
                rollback.write_bytes(raw)
                gh("release", "upload", FEED_TAG, str(rollback), "--repo", REPO)
                raise
            else:
                raise
    for attempt in range(8):
        if json.loads(public_bytes(FEED_URL)) == updated:
            break
        if attempt == 7:
            raise ValueError("The published Android updater could not be verified")
        time.sleep(4)
    print(json.dumps({"published": True, "version": metadata["version"], "apk": info["url"],
                      "windowsUnchanged": True, "otherApplicationFeedsChanged": False}), flush=True)


if __name__ == "__main__":
    main()
