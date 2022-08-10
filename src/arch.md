# Arch Linux Hacks

### install archlinux as a unprivileged user 

```#bash
function unprivileged_arch_install_to() {
  newroot=$1; shift
  pacman_args=("${@:-base}")
  mkdir -m 0755 -p "$newroot"/var/{cache/pacman/pkg,lib/pacman,log} "$newroot"/{dev,run,etc/pacman.d}
  mkdir -m 1777 -p "$newroot"/tmp
  mkdir -m 0555 -p "$newroot"/{sys,proc}
  unshare --fork -r --pid pacman -r "$newroot" -Sy "${pacman_args[@]}"
}
```
