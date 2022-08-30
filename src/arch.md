# Arch Linux Hacks

### install archlinux as a unprivileged user 

```bash
function unprivileged_arch_install_to() {
  newroot=$1; shift
  pacman_args=("${@:-base}")
  mkdir -m 0755 -p "$newroot"/var/{cache/pacman/pkg,lib/pacman,log} "$newroot"/{dev,run,etc/pacman.d}
  mkdir -m 1777 -p "$newroot"/tmp
  mkdir -m 0555 -p "$newroot"/{sys,proc}
  unshare --fork -r --pid pacman -r "$newroot" -Sy "${pacman_args[@]}"
}
```


### find and download old kernels

https://wiki.archlinux.org/title/Arch_Linux_Archive#Historical_Archive

```bash
# on a fresh system do
pacman -S python-pip python-internetarchive
pip install setuptools

# find package identifier
ia search identifier:'archlinux_pkg_linux'
ia search subject:"archlinux package" subject:'linux'

# show all versions of found identifier
ia list archlinux_pkg_linux

# mtime is linux epoch
ia list archlinux_pkg_linux -c mtime,name

ia download archlinux_pkg_linux linux-5.9.arch1-1-x86_64.pkg.tar.zst
```
