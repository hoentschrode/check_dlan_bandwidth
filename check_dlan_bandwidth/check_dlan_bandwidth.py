#!/usr/bin/python
# coding=utf-8
import urllib2
import json
import argparse


VERSION = '0.1'


class DLANBandwidth:
    """
    Read bandwidth between two dlan stations
    """
    def __init__(self, host, remote_mac, username, password):
        """
        Create new bandwidth measure object
        :param host: Hostname/IP of station
        :param remote_mac: MAC address of remote station
        :param username: Username
        :param password: Password
        """
        self._host = host
        self._remote_mac = remote_mac
        self._username = username
        self._password = password

    def get_bandwidth(self):
        """
        Query used bandwidth between stations
        :return: Tuple: (STATUS, tx, rx)
        """
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, 'http://{0}/'.format(self._host), self._username, self._password)
        opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passmgr))

        url = 'http://{0}/cgi-bin/htmlmgr?_file=getjson&service=hpdevices'.format(self._host)
        try:
            req = urllib2.Request(url)
            res = opener.open(req, timeout=4)
            buf = res.read()

            data = json.loads(buf)

            for entry in data:
                if entry.get('loc', None) == u'remote' and entry.get(u'mac', None) == self._remote_mac:
                    ret = ('OK', float(entry['tx']), float(entry['rx']))
                    return ret
        except urllib2.HTTPError, e:
            ret = ('HTTP error {0}'.format(e.code), None, None)
            return ret
        except urllib2.URLError, e:
            ret = ('URL error {0}'.format(e.reason), None, None)
            return ret
        except ValueError, e:
            ret = ('BOGUS data {0}'.format(e.message), None, None)
            return ret
        except Exception, e:
            ret = ('Unknown error {0}'.format(e.message), None, None)
            return ret
        return 'UNKNOWN', None, None


def main():
    """
    The all mighty main function
    :return:
    """
    argp = argparse.ArgumentParser(
        description=u'Check devolo DLAN bandwidth v {0} (c) by Christian Höntsch-Rode'.format(VERSION)
    )
    argp.add_argument('-H', '--host', required=True,
                      help="Hostname")
    argp.add_argument('-r', '--remote-mac', required=True,
                      help="MAC address of remote station")
    argp.add_argument('-u', '--user', required=True,
                      help='Username (same as used for web interface)')
    argp.add_argument('-p', '--password', required=True,
                      help='Password (same as used for web interface)')

    args = argp.parse_args()
    bw = DLANBandwidth(args.host, args.remote_mac, args.user, args.password)
    print bw.get_bandwidth()

if __name__ == '__main__':
    main()
