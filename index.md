### ruby base64 grepper

```ruby
BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".freeze

# +-------------------------------------------+
# |                                           |
# |            I        II        III         |
# | ascii |876543_21|8765_4321|87_654321|     |
# | b64   |654321|65_4321|6543_21|654321|     |
# |          a       b       c      d         |
# |                                           |
# +-------------------------------------------+
# ASCII-Art as png: https://web.archive.org/web/20210409165509/https://upload.wikimedia.org/wikipedia/commons/7/70/Base64-de.png
#
# Five cases exist:
#  1)  I, II and III are existent   -> given: a,b,c,d
#  2)  I and II are existent        -> given: a,b      partially: c
#  3)  Only I is existent           -> given: a        partially: b
#  4)  II and III are existent      -> given: c, d     partially: b
#  5)  Only III is existent         -> given: d        partially: c
#
# In every case we have either full or partiall information about c xor b. This
# means, we can calculate them. 
#
# Source has been stolen and modified from:
#
# https://web.archive.org/web/20210409165718/https://en.wikibooks.org/wiki/Algorithm_Implementation/Miscellaneous/Base64#Ruby
def encode_regex(str, remove_equals=true)
  candidates = [str.bytes, [nil] + str.bytes, [nil, nil] + str.bytes] 
  candidates.map! do |candidate|
    candidate.each_slice(3).map do |buf|
      symbolic = buf 
      while symbolic.length < 3; symbolic << nil; end

      # replace in both directions
      buf = symbolic.map { |b| ((b.nil?) && 0) || b }

      # basic 3char (8bit) to 4chars (6bit)
      group24 = (buf[0] << 16) | (buf[1] << 8) | buf[2] # current 3 bytes as a 24 bit value
      encoded = ''
      encoded << BASE64_CHARS[(group24 >> 18) & 0x3f] # read the 24 bit value 6 bits at a time
      encoded << BASE64_CHARS[(group24 >> 12) & 0x3f]
      encoded << BASE64_CHARS[(group24 >> 6) & 0x3f]
      encoded << BASE64_CHARS[(group24 >> 0) & 0x3f]

      if symbolic[0].nil? && symbolic[1].nil?
        encoded[0] = '='
        encoded[1] = '=' 
        # encoded[2] 4bits..
        pos = BASE64_CHARS.index(encoded[2])
        possibilities = (4**2).times.map.with_index(0x3f - 16) { |i| BASE64_CHARS[(pos ^ i)] }
        encoded[2] = sprintf("(%s)", possibilities.join("|"))
      elsif symbolic[0].nil?
        encoded[0] = '='
        # encoded[1] first two bits...
        pos = BASE64_CHARS.index(encoded[1])
        possibilities = (2**2).times.map.with_index(0) { |i| BASE64_CHARS[(pos ^ (i << 4))] }
        encoded[1] = sprintf("(%s)", possibilities.join("|"))
      end

      if symbolic[1].nil? && symbolic[2].nil?
        # encoded[1] 4bit...
        encoded[2] = '=' 
        encoded[3] = '='
        pos = BASE64_CHARS.index(encoded[1])
        possibilities = (4**2).times.map.with_index(0x00) { |i| BASE64_CHARS[(pos ^ i)] }
        encoded[1] = sprintf("(%s)", possibilities.join("|"))
      elsif symbolic[2].nil?
        # encoded[3] last two bits...
        # four bits correct; two bits incorrect: 2**2
        encoded[3] = '='
        pos = BASE64_CHARS.index(encoded[2])
        possibilities = (2**2).times.map.with_index(0x00) { |i| BASE64_CHARS[(pos ^ i)] }
        encoded[2] = sprintf("(%s)", possibilities.join("|"))
      end
      encoded
    end.join
  end
  candidates = "(#{candidates.join("|")})"
  candidates = candidates.tr("=", "") if remove_equals
  candidates
end
```


### bash function to archive a page with waybackmachine

```bash
# https://web.archive.org/web/20210323214943/https://gist.github.com/atomotic/721aefe8c72ac095cb6e
function ia-save() {
  curl -s -I "https://web.archive.org/save/$1" | \
  egrep '^location:' | \
  awk '{ print $2 }';
}

# Usage:
ia-save 'https://gist.github.com/atomotic/721aefe8c72ac095cb6e'
```

### ssh with old algos

```
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 123.123.123.123
```

### qemu snapshotting


```
# https://web.archive.org/web/20210323214342/https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-qemu-monitor.html#sec-qemu-monitor-snapshots
savevm NAME
loadvm NAME
delvm
info snapshots 
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


### default parameters in bash

```bash
# sets x to "/abc" if x is not set
x=${x:-/abc}
```


### print space without a space

```bash
python<<<'print("\x20")'

ruby<<<'print("\x20")'

{echo,-e,'\x20'}

{base64,-d}<<<IAo=

{echo,IAo=}|{base64,-d}

{xxd,-r,-p}<<<20

# $'\x20' will be interpreted as ' '
# <<< handles the string right of it, as a filestream
# zsh allows streaming, without program execution
zsh<<<"<<<$'\x20'>/dev/stdout"
zsh<<<"<<<$'\x20'>/proc/self/fd/1"

# use hex and octal
cat<<<$'\x20'
cat<<<$'\040'
```

### radare pwn pattern (debruijn sequence)

```bash
# find offset
ragg2 -P 512 -r | ./narnia1

# query 
ragg -q 0x41414841
```


### download subtitles with youtube-dl

```bash
youtube-dl --list-subs https://www.youtube.com/watch?v=dl78PQGJpiI

youtube-dl --all-subs --skip-download https://www.youtube.com/watch?v=dl78PQGJpiI
```


### gdb (pwndbg) raw stdin input

```bash
# with python3
r < <(python3.9 -c 'import sys; sys.stdout.write("\x41"*50)')

# with python2
r < <(python2.7 -c 'print("\x41"*50)')

# with ruby
r < <(ruby -e 'print("A"*50)')
```

### grep for base64 like strings

```bash
grep -En '[[:alnum:]/+]{20,}' file
```

### gits freshest branch

```bash
# don't foget to fetch first
git branch --sort=-committerdate
```

### git pretty oneline with author name

```bash
git log --pretty="format:%C(Yellow)%H%Creset %Cred%aN%Creset %s"
```

### procfs && working with file descriptors

```bash
bash -c 'grep heap /proc/$$/maps'
diff /proc/self/fd/3 /proc/self/fd/4 4<<<"$(xxd a)" 3<<<"$(xxd b)"
cat /proc/self/fd/4 4<<<"asdfasdf"
```

### laggy tigervnc session

```bash
vncviewer -Shared -CompressLevel 9 -via ellcs@hostname :1
```

### delete all lines where 'pry' occurs

```bash
sed -i '/pry/d' **/*.rb
```

### find all ruby classes

```bash
egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"

# count the class occurences
for klass in $(egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"); do amount=$(grep -Hrn "$klass" . | wc -l); echo "$klass $amount"; done
```

### git push local branch to remote with same name

```bash
git push -u origin $(git branch | grep '*' | sed 's/* //')
```
