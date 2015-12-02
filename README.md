Task:
Deploy two virtual routers (R20 and R21) running quagga in a programmatic manner, establish an EBGP session, and exchange EBGP routes.

Assumptions: 
Host: OS CentOS-7 
Hypervisor: KVM 
Guest VMs OS: CentOS-7 
Hypervisor networks 192.168.64.0/24 and 100.100.100.0/24 doesn't exist in hypervisor. 
Internet access to retrieve the zebra.conf and bgpd.conf files.

Package Structure: 
Directory exercise contains the following: 
Directory r20 which contains the kickstart, bgpd.conf, and zebra.conf files for router 20. 
Directory r21 which contains the kickstart, bgpd.conf, and zebra.conf files for router 21. 
Python script deploy_lab which execute the job.

Instructions: 
1. Place package in root directory (/exercise)
2. On deploy_lab.py file, modify variable iso_location to point to the guest OS (CentOS-7-x86_64-DVD-1503-01.iso); this must be done for each VM construct (r20_vm and r21_vm).
3. Execute python deploy_lab.py as root. 

The script first installs the necessary packages on the host, then the install for each VM (R20 and R21) 

*****Note you must shutdown VM R20 before the script can start executing the creation of VM R21; I'll find a way to fix this...

VMs username is root and the password is pito.

Once both machines are up, execute vtysh to access the router, and execute “show ip bgp summary” and “show ip route bgp” to verify that both routers are exchanging routes.


