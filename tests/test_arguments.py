import unittest
import urllib2
import json
from check_dlan_bandwidth.check_dlan_bandwidth import create_parser


class TestCheckArguments(unittest.TestCase):

    def setUp(self):
        self._parser = create_parser()

    def test_without_parameters(self):
        with self.assertRaises(SystemExit) as ex:
            parsed = self._parser.parse_args([])
        self.assertEqual(ex.exception.code, 2)

    def test_with_all_parameters(self):
        hostname = '127.0.0.1'
        mac_addr = '12:34:56:78:90:AB'
        try:
            parsed = self._parser.parse_args([
                '-H', hostname, '-r', mac_addr, '-u', 'user' , '-p', 'pass'
            ])
            self.assertEqual(parsed.host, hostname)
            self.assertEqual(parsed.remote_mac, mac_addr)
        except SystemExit:
            self.assertFalse(True, msg='Error parsing arguments')
        except Exception, e:
            self.assertFalse(True, msg='Error parsing arguments')
