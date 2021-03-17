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
vncviewer -CompressLevel 9 -via ellcs@hostname :1
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
