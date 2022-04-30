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

### default parameters in bash

```bash
# sets x to "/abc" if x is not set
x=${x:-/abc}
```


### find libreoffice files containing a string

This helps you to search for a libreoffice document containing a certian string.
Add it to your `~.bashrc`. Start a terminal within a certian folder you want to
search in and start searching! Make sure you installed `unzip`.

```bash
# Example usages: 
# 
#    find_libre horseshoes
#
#    find_libre "horseshoes with spaces" 
#
#    find_libre "horseshoes somewhere else"  "/home/user"
#
function libre_find() {
  which zipgrep 1>/dev/null || { echo "Please install zipgrep"; exit 1; }
  local search_term="$1"
  local search_path=${2:-$(pwd)}
  find "$search_path" -exec zipgrep -iq "$search_term" {} 2>/dev/null \; -print
}
```
### ghostscript - merge pdf files

```bash
# combine 1.pdf and 2.pdf to out.pdf
gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=out.pdf -dBATCH 1.pdf 2.pdf

# combine matching files to 'candidate_?.pdf', while '?' represents a single char
gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=out.pdf -dBATCH candidate_?.pdf
```