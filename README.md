# Nagios/Icinga plugin to check bandwidth on devolo's DLAN powerlan adapters
This plugin checks the bandwidth on devolo dlan powerlan adapters. 

My first Nagios/Icinga plugin :)

The plugin uses the build in web interface of the devolos to query the data. To get the bandwidth being used just query the first adapter by it's ip address. The adapter delivers a list of remote stations (identified by their mac address) with current used bandwidths (sending and receiving directions). 

Therefore it's necessary to provide a host ip and a remote mac.

I have 5 devices (dlan 500 Wifi) in my house. All of them are connected through a central "dlan 500 duo+" to my router. The latter doesn't have a web interface, but a mac address, wich can be queried as remote station.  

## Installing
Since this script is written in Python (currently only compatible to 2.7!), it can easily be installed using pip:
```bash
pip install check_dlan_bandwidth
```

## Usage
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
To use this check script you should create a custom command in icinga's commands.conf:
```
object CheckCommand "check_dlan_bandwidth" {
    command = ['/usr/local/bin/check_dlan_bandwidth.py']
}
```


