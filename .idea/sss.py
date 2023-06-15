import re
import time

list = {'# /etc/hosts.deny: list of hosts that are _not_ allowed to access the system.\n', '#                  See the manual pages hosts_access(5) and hosts_options(5).\n', '#\n', '# Example:    ALL: some.host.name, .some.domain\n', '#             ALL EXCEPT in.fingerd: other.host.name, .other.domain\n', '#\n', '# If you\'re going to protect the portmapper use the name "rpcbind" for the\n', '# daemon name. See rpcbind(8) and rpc.mountd(8) for further information.\n', '#\n', '# The PARANOID wildcard matches any host whose name does not match its\n', '# address.\n', '#\n', "# You may wish to enable this to ensure any programs that don't\n", '# validate looked up hostnames still leave understandable logs. In past\n', '# versions of Debian this has been the default.\n', '# ALL: PARANOID\n', '\n', 'sshd:192.168.255.255\n'}

for ip in list:
    list={}
    group = re.search(r'(\d+\.\d+\.\d+\.\d+)',ip)
    print(group)
    if group:
        print(group[1])
        list[group[1]]='1'
        print(list)