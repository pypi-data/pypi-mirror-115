Examples:

# Creating a firewall named demo1
$ digicloud firewall create demo1 --description "a simple firewall to show how does it work"

# Now we need to add some rules:
$ digicloud firewall rule create  t1 --direction egress --protocol udp --port-range-min 1 --port-range-max 65535
