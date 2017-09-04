# Nagios/Icinga plugin to check bandwidth on devolo's DLAN powerlan adapters
This plugin checks the bandwidth on Devolo(tm) dlan powerlan adapters. 

It's my first Nagios/Icinga plugin :)

The plugin uses the build in web interface of the adapters to query the data. To get the bandwidth being used just query the first adapter by it's ip address. The adapter delivers a list of remote stations (identified by their mac address) with current used bandwidths (sending and receiving directions). 

Therefore it's necessary to provide a host ip and a remote mac.

I have 6 devices (5 dlan "500 Wifi" and one "duo+") in my house. All of them are connected through the central "dlan 500 duo+" to my router. The latter doesn't have a web interface, but a mac address, which can be queried as remote station (see parameter -r).  

## Installation
Since this script is written in Python (currently only compatible to 2.7!), it can easily be installed using pip:
```bash
pip install check_dlan_bandwidth
```

This installs the check script, all dependent libs and creates an executable, usually under ``/usr/local/bin``. 

## Usage
On my raspberry pi the script is installed under ``/usr/local/lib/python2.7/dist-packages/check_dlan_bandwidth/check_dlan_bandwidth.py`` and a command line version is created in ``/usr/local/bin/check_dlan_bandwidth``. 

```
check_dlan_bandwidth.py [-h] -H HOST -r REMOTE_MAC -u USER -p PASSWORD
```

Command line arguments
```
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Hostname
  -r REMOTE_MAC, --remote-mac REMOTE_MAC
                        MAC address of remote station
  -u USER, --user USER  Username (same as used for web interface)
  -p PASSWORD, --password PASSWORD
                        Password (same as used for web interface)
```

## Configuration
To use this check script one should create a custom command in icinga's ``commands.conf``:
```
object CheckCommand "check_dlan_bandwidth" {
  command = ["/usr/local/bin/check_dlan_bandwidth"]
  arguments = {
    "-H" = "$address$"
    "-r" = "11:22:33:44:55:66"
    "-u" = "admin"
    "-p" = "my_secret_password"
  }
}

```

.. then make a custom service in ``services.conf`` which automatically applies to all dlan devices:
```
apply Service "DlanBandwidth" {
  import "generic-service"
  check_command = "check_dlan_bandwidth"
  assign where "DLAN-devices" in host.groups
}
```

Note: I've created the hostgroup "DLAN-devices" which contains all my dlan adapters in ``grouops.conf``:
```
object HostGroup "DLAN-devices" {
  display_name = "DLAN devices"
  assign where "Devolo DLAN500 Wifi" in host.templates
}
```
