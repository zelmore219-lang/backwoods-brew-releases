import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from publish_employee import verify_public_feed


class FeedPropagationTests(unittest.TestCase):
 def test_previous_cached_feed_is_retried_until_the_exact_published_payload_arrives(self):
  expected={'schemaVersion':1,'apps':{'employees':{'windows':{'version':'0.4.1'}}}}
  previous={'schemaVersion':1,'apps':{'employees':{'windows':{'version':'0.3.1'}}}}
  with patch('publish_employee.public_bytes',side_effect=[json.dumps(previous).encode(),json.dumps(expected).encode()]) as read,patch('publish_employee.time.sleep'):
   verify_public_feed('https://example.invalid/isolated-test',expected)
   self.assertEqual(read.call_count,2)
 def test_persistent_different_content_is_never_reported_as_verified(self):
  with patch('publish_employee.public_bytes',return_value=b'{"different":"payload"}'),patch('publish_employee.time.sleep'):
   with self.assertRaisesRegex(ValueError,'could not be verified'):verify_public_feed('https://example.invalid/isolated-test',{'expected':'payload'})


if __name__=='__main__':unittest.main()
