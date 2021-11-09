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
