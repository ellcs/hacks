### libvirt allow copy-paste on linux

Add this to your domain, power it off and start it again.

```
<devices>
    <controller type='virtio-serial' index='0'/>
    <channel type='spicevmc'>
        <target type='virtio' name='com.redhat.spice.0'/>
    </channel>
</devices>
```

Also install `spice-vdagent` and enable it via systemd.

### vagrant start script

```
Vagrant.configure("2") do |config|
  config.vm.box = "kali-linux-rolling"
  config.vm.hostname = File.split(Dir.pwd).last

  config.vm.provider :libvirt do |libvirt|
    libvirt.uri = 'qemu:///session'
    libvirt.cpus = 6
    libvirt.memory = 1024 * 8
    libvirt.cmd_line = ""
    libvirt.nested = true
    libvirt.video_type = 'virtio'
  end

  config.nfs.verify_installed = false
  config.vm.synced_folder '.', '/vagrant', disabled: true

  #config.vm.provision "shell", inline: "apt update; apt install pwntools; git clone https://github.com/pwndbg/pwndbg; cd pwndbg; ./setup.sh"
end
```

### fix `winrm` timeout with windows vagrant box

It looks as follows:

```
==> default: Waiting for machine to boot. This may take a few minutes...
    default: WinRM address: 192.168.122.42:5985
    default: WinRM username: vagrant
    default: WinRM execution_time_limit: PT2H
    default: WinRM transport: negotiate

==> default: Removing domain...
==> default: Deleting the machine folder
An error occurred executing a remote WinRM command.

Shell: Cmd
Command: hostname
Message: Digest initialization failed: initialization error
```

You might solve this by using `winssh`, if available:

```
  # ...
  config.vm.communicator = "winssh"
  config.winssh.insert_key = false
  # ...
```

### list stored virt-manager connection strings

```bash
dbus-launch gsettings get org.virt-manager.virt-manager.connections uris
['qemu+ssh:///root@192.168.122.181:2022/system', 'qemu+ssh://root@192.168.122.196/system?keyfile=id_rsa', 'qemu:///session']
```

### wrap virsh connection in functions

```bash
function virsh_libvirthost() { 
  virsh -c qemu+ssh://root@192.168.122.105/system $@
}
```

### vagrant libvirt user-session with arch box

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "archlinux/archlinux"

  config.vm.provider :libvirt do |libvirt|
    libvirt.uri = 'qemu:///session'
    libvirt.cpus = 12
    libvirt.memory = 1024 * 8
    libvirt.cmd_line = ""
    libvirt.nested = true
  end
end
```

### qemu with qemu-bridge-helper
```bash
qemu-system-x86_64 -hda output/Arch-Linux-x86_64-cloudimg-ellcs-20220818.0.qcow2 \
  -m 4100 -cpu host -M q35 \
  -enable-kvm -nic bridge,br=virbr0,model=virtio-net-pci
```

### qemu snapshotting

https://web.archive.org/web/20210323214342/https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-qemu-monitor.html#sec-qemu-monitor-snapshots

With running vm:

```
savevm NAME
loadvm NAME
delvm
info snapshots 
```

From bash:

```
qemu-img snapshot -l $img
qemu-img snapshot -c $snapshot_name $img
qemu-img snapshot -d $snapshot_name $img
```

### qemu vm for windows

```
# download and unzip windows vm
wget https://aka.ms/windev_VM_vmware
unzip windev_VM_vmware

# convert to qcow2
qemu-img convert WinDev*.vmdk -O qcow2 

# create qemu script (adjust the disk_name)
cat <<-'EOF' > run.sh
path="$(dirname $(readlink -f "$0"))"
disk_name="WinDev2102Eval-disk1.qcow2"
disk_path="$(pwd)/$disk_name"
monitor="unix:${path}/monitor.sock,server,nowait"

/usr/bin/qemu-system-x86_64 \
  -enable-kvm \
  -M q35 \
  -monitor "$monitor" \
  -vnc :1 \
  -cpu host,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time \
  -smp cpus=7,maxcpus=7 -soundhw ac97 -enable-kvm -m 4100 \
  -hda "$disk_path" \
  -boot once=c,menu=off \
  -nic user,hostfwd=tcp::10022-:22 \
  -device nec-usb-xhci,id=xhci \
  -name 'windows-vm' $*
EOF

# start vm
bash run.sh

# connect via vncviewer
vncviewer :1
```
