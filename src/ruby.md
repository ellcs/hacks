### ruby - list all instances of class

```ruby
ObjectSpace.each_object(Human) { |humanoid| }
```


### ruby - highorder methods with arguments

```ruby
def with_args(sym, *args)
  Proc.new do |item|
    item.send(sym, *args)
  end
end


[1,2,3,4].map(&with_args(:+, 2))
# => [3, 4, 5, 6]
```

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

### find all ruby classes

```bash
egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"

# count the class occurences
for klass in $(egrep -Hrn "^class (\S)+ " lib | sed -E 's/.+\/.*:.*:(\s)*//' | awk '{print $2}' | grep -vE "^$"); do amount=$(grep -Hrn "$klass" . | wc -l); echo "$klass $amount"; done
```
