# Parent Aware

[![Build Status](https://github.com/csm10495/parent_aware/workflows/Release/badge.svg)](https://github.com/csm10495/parent_aware/actions)

A decorator to make objects aware of their parent objects. Particularly useful with dataclasses!

## Example

```
import dataclasses
from parent_aware import parent_aware

@parent_aware
@dataclasses.dataclass
class Child:
    num: int

@parent_aware
@dataclasses.dataclass
class Parent:
    child: Child

c = Child(2)
p = Parent(child=c)

# Automatically a .parents was added on the child!
assert c.parents == [p]

# If you didn't want .parents, use @parent_aware(parents_name='give_a_name_here')
```

## Installation
```
pip install parent_aware
```