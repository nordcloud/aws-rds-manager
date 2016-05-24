from unittest import TestCase

import six

if six.PY3:
    from unittest.mock import patch
    from io import StringIO
else:
    from io import BytesIO as StringIO
    from mock import patch

from awsrdsmanager import json_pprint


class TestJson_pprint(TestCase):
    def test_json_pprint(self):
        with patch('sys.stdout', new=StringIO()) as json_output:
            json_pprint({
                'Hello': 'world'
            })
            self.assertEqual(json_output.getvalue().strip(), "{\n    \"Hello\": \"world\"\n}")
