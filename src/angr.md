# Angr


# argv

```python
{{#include angr/solve_argv.py}}
```

# stdin

```python
{{#include angr/solve_stdin.py}}
```

# wrapper for stdin and argv

```python
{{#include angr/solve_stdin_argv.py}}
```

# coredump

```python
{{#include angr/solve_coredump.py}}
```


# cfg inspection

https://docs.angr.io/built-in-analyses/cfg

```python
import angr
p = angr.Project('/bin/true', load_options={'auto_load_libs': False})
cfg = p.analyses.CFGFast()
len(cfg.graph.nodes())
len(cfg.graph.edges())

# get the node 
entry_node = cfg.get_any_node(p.entry)

# get successor node of the cfg node `entry`
# -> list[angr.knowledge_plugins.cfg.cfg_node.CFGNode]
succ = cfg.get_successors(entry_node)
# there is only main as successor
main = succ[0]


# opcodes of the cfg node `entry`
entry_node.block.bytes

# number of instructions of the cfg node `entry`
# -> int
entry_node.block.instructions

# all addresses of the cfg node `entry`
# -> list[int]
entry_node.block.instruction_addrs
```

### print all jump gadgets


```python
import angr, angrop

p = angr.Project('/bin/ls', load_options={'auto_load_libs': False})
cfg = p.analyses.CFGFast()
rop = p.analyses.ROP()
rop.find_gadgets()

print("[+] done with angr stuff; filter jmp gadgets")
jump_gadgets = [g for g in rop.gadgets if g.gadget_type == 'jump']

print("[+] print jmp gadgets")
for jmp in jump_gadgets:
	print(f"jmp gadget @ {jmp.addr}")
	print(p.factory.block(jmp.addr).capstone)

import IPython; IPython.embed()
```

### jmp rops

```c
// gcc file.c -o a.out
int multiple_gadgets(int i) {
  if (i > 0) {
    i += 3;
  } else {
    i += 5;
  }
  return i;
}

int main() {
  multiple_gadgets(3);
}
```


```python
import angr, angrop

p = angr.Project('a.out', load_options={'auto_load_libs': False})
cfg = p.analyses.CFGFast()
rop = p.analyses.ROP()
rop.find_gadgets()

multiple_gadgets = cfg.get_any_node(p.entry).successors[0].successors[0].successors[0]
multiple_gadgets.block.pp()
#        multiple_gadgets:
#401119  push    rbp
#40111a  mov     rbp, rsp
#40111d  mov     dword ptr [rbp-0x4], edi
#401120  cmp     dword ptr [rbp-0x4], init
#401124  jle     0x40112c


multiple_gadgets.successors
# [<CFGNode multiple_gadgets+0x13 [9]>, <CFGNode multiple_gadgets+0xd [6]>]

# the second successor gadget seems off; why is it having lower addresses after the ret?
for s in multiple_gadgets.successors:
    s.block.pp()
#40112c  add     dword ptr [rbp-0x4], 0x5
#401130  mov     eax, dword ptr [rbp-0x4]
#401133  pop     rbp
#401134  ret
#
#401130  mov     eax, dword ptr [rbp-0x4]
#401133  pop     rbp
#401134  ret
#401126  add     dword ptr [rbp-0x4], 0x3
#40112a  jmp     0x401130

```
