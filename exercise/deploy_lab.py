from __future__ import print_function

import libvirt
import subprocess
import sys

def host(command):
    try:
        subprocess.check_output(command, shell=True).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(str(e))


def network(xml):
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    # create a persistent virtual network
    try:
        # create a persistent virtual network
        network = conn.networkDefineXML(xml)
        if network == None:
            print('Failed to define a virtual network', file=sys.stderr)
            exit(1)
        active = network.isActive()
        if active == 1:
            print('The new virtual network is active')
        else:
            print('The new virtual network is not active')
        network.create() # set the network active
        active = network.isActive()
        if active == 1:
            print('The new virtual network is active')
        else:
            print('The new virtual network is not active')
        print('Setting autostart...')
        network.setAutostart(1)
        print('autostart: '+str(network.autostart()))
        conn.close()
    except libvirt.libvirtError as e:
        print(str(e))


def main():
    print('Installing required host packages...')
    cmd = 'yum install -y qemu-kvm libvirt libvirt-python libguestfs-tools virt-install'
    host(cmd)

    net_nat = """<network>
  <name>net_nat</name>
  <uuid>16f4d464-f447-40ea-b257-61a393123abc</uuid>
  <forward mode='nat'/>
  <bridge name='virbr64' stp='on' delay='0'/>
  <mac address='52:54:00:2a:12:ab'/>
  <ip address='192.168.64.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.64.128' end='192.168.64.254'/>
      <host mac='52:54:00:f8:20:20' name='R20' ip='192.168.64.20'/>
      <host mac='52:54:00:f8:21:21' name='R21' ip='192.168.64.21'/>
    </dhcp>
  </ip>
</network>"""

    net_100 = """<network>
  <name>100</name>
  <uuid>2a745b38-d14a-4b11-a6b3-87b96a7d1c0c</uuid>
  <bridge name='virbr100' stp='on' delay='0'/>
  <mac address='52:54:00:df:0f:cc'/>
  <domain name='150'/>
  <ip address='100.100.100.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='100.100.100.128' end='100.100.100.254'/>
    </dhcp>
  </ip>
</network>"""

    print('Installing networks...')
    network(net_100)
    network(net_nat)

    name = 'R20'
    bridge_eth0 = 'virbr64'
    mac_eth0 = '52:54:00:f8:20:20'
    bridge_eth1 = 'virbr100'
    disk_path = '/var/lib/libvirt/images/R20.qcow11'
    kickstart_path = '/root/PycharmProjects/exercise/exercise/r20/anaconda-ks.cfg'
    iso_location = '/home/rafael/Downloads/CentOS-7-x86_64-DVD-1503-01.iso'

    r20_vm = """virt-install \
    --name={0} \
    --arch=x86_64 \
    --vcpus=1 \
    --memory=1024 \
    --os-type=linux \
    --os-variant=rhel7 \
    --hvm \
    --connect=qemu:///system \
    --network bridge={1},model=virtio,mac={2} \
    --network bridge={3},model=virtio \
    --disk path={4},size=16 \
    --initrd-inject={5} \
    --extra-args="ks=file:/anaconda-ks.cfg text console=tty0 utf8 console=ttyS0,115200" \
    --location={6} \
    --accelerate \
    --force""".format(name, bridge_eth0, mac_eth0, bridge_eth1, disk_path, kickstart_path, iso_location)

    name = 'R21'
    bridge_eth0 = 'virbr64'
    mac_eth0 = '52:54:00:f8:21:21'
    bridge_eth1 = 'virbr100'
    disk_path = '/var/lib/libvirt/images/R21.qcow11'
    kickstart_path = '/root/PycharmProjects/exercise/exercise/r21/anaconda-ks.cfg'
    iso_location = '/home/rafael/Downloads/CentOS-7-x86_64-DVD-1503-01.iso'

    r21_vm = """virt-install \
    --name={0} \
    --arch=x86_64 \
    --vcpus=1 \
    --memory=1024 \
    --os-type=linux \
    --os-variant=rhel7 \
    --hvm \
    --connect=qemu:///system \
    --network bridge={1},model=virtio,mac={2} \
    --network bridge={3},model=virtio \
    --disk path={4},size=16 \
    --initrd-inject={5} \
    --extra-args="ks=file:/anaconda-ks.cfg text console=tty0 utf8 console=ttyS0,115200" \
    --location={6} \
    --accelerate \
    --force""".format(name, bridge_eth0, mac_eth0, bridge_eth1, disk_path, kickstart_path, iso_location)

    print('Creating VM for R20... About 15 minutes to completion!')
    host(r20_vm)
    print('Creating VM for R21... About 15 minutes to completion!')
    host(r21_vm)

if __name__ == "__main__":
    main()