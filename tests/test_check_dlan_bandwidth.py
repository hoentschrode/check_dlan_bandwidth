import unittest
import urllib2
import json
from mockups import MockResponse
from check_dlan_bandwidth import DLANBandwidth


class TestCheckDLANBandwidth(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCheckDLANBandwidth, self).__init__(*args, **kwargs)
        self._fake_response = None

    def setUp(self):
        urllib2.urlopen = self.mock_urlopen

    def mock_urlopen(self, request, *args, **kwargs):
        return self._fake_response

    def _value_is_wellformed(self, ret):
        """
        Default check if returned value is wellformed
        :param ret: Response tuple
        :return: True if data is wellformed
        """
        return (
            # Return has to be a tuple...
            isinstance(ret, tuple) and
            # ... of 3 elements
            len(ret) == 3 and
            # 1st one is a string
            isinstance(ret[0], str) and
            # 2nd None or float
            (ret[1] is None or isinstance(ret[1], float)) and
            # 3rd None or float
            (ret[2] is None or isinstance(ret[2], float))
        )

    def test_invalid_content_type(self):
        """
        Check for invalid content type
        :return: None
        """

        self._fake_response = MockResponse('', headers={'Content-Type': 'bogus content type'})

        checker = DLANBandwidth('127.0.0.1', 'remote_mac', 'user', 'pass')
        bandwidth = checker.get_bandwidth()

        self.assertTrue(self._value_is_wellformed(bandwidth))

        self.assertTrue(bandwidth[0].startswith('HTTP error'))
        self.assertIsNone(bandwidth[1])
        self.assertIsNone(bandwidth[2])

    def test_bogus_json_content(self):
        """
        Check for bogus json content
        :return: None
        """
        data = {'key': 'value'}
        self._fake_response = MockResponse(json.dumps(data), headers={'Content-Type': 'application/json'})

        checker = DLANBandwidth('127.0.0.1', 'remote_mac', 'user', 'pass')
        bandwidth = checker.get_bandwidth()

        self.assertTrue(self._value_is_wellformed(bandwidth))
        self.assertEqual(bandwidth[0], 'UNKNOWN')
        self.assertIsNone(bandwidth[1])
        self.assertIsNone(bandwidth[2])

    def test_http_error(self):
        """
        Check for HTTP error code 4xx
        :return: None
        """
        self._fake_response = MockResponse('', code=401, headers={'Content-Type': 'application/json'})

        checker = DLANBandwidth('127.0.0.1', 'remote_mac', 'user', 'pass')
        bandwidth = checker.get_bandwidth()

        self.assertTrue(self._value_is_wellformed(bandwidth))
        self.assertEqual(bandwidth[0], 'HTTP error 401')
        self.assertIsNone(bandwidth[1])
        self.assertIsNone(bandwidth[2])

    def test_url_error(self):
        """
        Check for URLerror exception (simulated via 5xx http errors)
        :return: None
        """
        self._fake_response = MockResponse('', code=501, headers={'Content-Type': 'application/json'})

        checker = DLANBandwidth('127.0.0.1', 'remote_mac', 'user', 'pass')
        bandwidth = checker.get_bandwidth()

        self.assertTrue(self._value_is_wellformed(bandwidth))
        self.assertEqual(bandwidth[0], 'URL error faked url error reason')
        self.assertIsNone(bandwidth[1])
        self.assertIsNone(bandwidth[2])

    def test_value_error(self):
        """
        Check for invalid values
        :return:
        """
        mac_addr = '12:34:56:78:90:AB'
        data = [
            {'loc': 'remote', 'mac': mac_addr, 'tx': '0.0', 'rx': 'bogus value'}
        ]
        self._fake_response = MockResponse(json.dumps(data), headers={'Content-Type': 'application/json'})

        checker = DLANBandwidth('127.0.0.1', mac_addr, 'user', 'pass')
        bandwidth = checker.get_bandwidth()

        self.assertTrue(self._value_is_wellformed(bandwidth))
        self.assertTrue(bandwidth[0].startswith('BOGUS data could not convert string to float'))
        self.assertIsNone(bandwidth[1])
        self.assertIsNone(bandwidth[2])
