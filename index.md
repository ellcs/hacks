
### download subtitles with youtube-dl

```
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

```
# don't foget to fetch first
git branch --sort=-committerdate
```

# git pretty oneline with author name

```
git log --pretty="format:%C(Yellow)%H%Creset %Cred%aN%Creset %s"
```

### procfs && working with file descriptors

```
bash -c 'grep heap /proc/$$/maps'
diff /proc/self/fd/3 /proc/self/fd/4 4<<<"$(xxd a)" 3<<<"$(xxd b)"
cat /proc/self/fd/4 4<<<"asdfasdf"
```

### laggy tigervnc session

```
vncviewer -CompressLevel 9 -via ellcs@hostname :1
```

### delete all lines where 'pry' occurs

```
sed -i '/pry/d' **/*.rb
```

### find all ruby classes

```
egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"

# count the class occurences
for klass in $(egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"); do amount=$(grep -Hrn "$klass" . | wc -l); echo "$klass $amount"; done
```


# git push local branch to remote with same name

```
git push -u origin $(git branch | grep '*' | sed 's/* //')
```
