# refdatatypes

Pyton basic datatypes as a references. Solve problems with static class immutable datatypes.

## Installation
```python
pip3 install refdatatypes
```

## Problem

```python
class A:
    static = 1


class B(A):
    pass


print(f"int {A.static}")  # get 1 correctly
print(f"int {B.static}")  # get 1 correctly

A.static = 5
print(f"int {A.static}")  # get 5 correctly
print(f"int {B.static}")  # get 5 correctly

B.static = 6
print(f"int {A.static}")  # expected 6, but get 5 incorrectly
print(f"int {B.static}")  # get 6 correctly

A.static = 7
print(f"int {A.static}")  # get 7 correctly
print(f"int {B.static}")  # get unchanged 6
```

## Solution
```python
from refdatatypes.refint import RefInt


class AAA:
    static = RefInt(1)


class BBB(AAA):
    pass


print(f"refint {AAA.static.value}")  # get 1 correctly
print(f"refint {BBB.static.value}")  # get 1 correctly

AAA.static.value = 5
print(f"refint {AAA.static.value}")  # get 5 correctly
print(f"refint {BBB.static.value}")  # get 5 correctly

BBB.static.value = 6
print(f"refint {AAA.static.value}")  # get 6 correctly
print(f"refint {BBB.static.value}")  # get 6 correctly

AAA.static.value = 7
print(f"refint {AAA.static.value}")  # get 7 correctly
print(f"refint {BBB.static.value}")  # get 7 correctly
```
