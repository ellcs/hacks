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
