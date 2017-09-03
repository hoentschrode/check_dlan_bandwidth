#!/usr/bin/python
# coding=utf-8
import urllib2
import json
import argparse
import nagiosplugin


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
        urllib2.install_opener(opener)

        url = 'http://{0}/cgi-bin/htmlmgr?_file=getjson&service=hpdevices'.format(self._host)
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout=4)

            # Check content type
            content_type = res.info().getheader('Content-Type')
            if content_type is None or not content_type.lower().startswith('application/json'):
                ret = ('HTTP error: Expected json response, got {0}'.format(content_type), None, None)
                return ret

            buf = res.read()
            data = json.loads(buf)

            for entry in data:
                if isinstance(entry, dict):
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


class BandwidthChecker(nagiosplugin.Resource):
    def __init__(self, host, remote_mac, username, password):
        self._host = host
        self._remote_mac = remote_mac
        self._username = username
        self._password = password

    def bandwidth(self):
        bw = DLANBandwidth(self._host, self._remote_mac, self._username, self._password)
        return bw.get_bandwidth()

    def probe(self):
        bandwidth = self.bandwidth()
        return[
            nagiosplugin.Metric('tx', bandwidth[1], min=0, context='bandwidth'),
            nagiosplugin.Metric('rx', bandwidth[2], min=0, context='bandwidth')
        ]


def create_parser():
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
    argp.add_argument('-w', '--warning', default=400,
                      help='Warning level')
    argp.add_argument('-c', '--critical', default=450,
                      help="Critical level")
    return argp


@nagiosplugin.guarded()
def main():
    """
    The all mighty main function
    :return:
    """
    argp = create_parser()

    args = argp.parse_args()

    check = nagiosplugin.Check(
        BandwidthChecker(args.host, args.remote_mac, args.user, args.password),
        nagiosplugin.ScalarContext('bandwidth', args.warning, args.critical, fmt_metric='{value} MBit/s')
    )
    check.main()


if __name__ == '__main__':
    main()
