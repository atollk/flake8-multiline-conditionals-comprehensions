# flake8-multiline-conditionals-comprehensions

[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/tox/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/pylint/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/black/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/flake8/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)


flake8 plugin that works on conditional expressions and comprehension 
expressions to enforce each segment to be put on a new line.

## Contents
  * [Options](#options)
  * [Comprehension Errors](#comprehension-errors)
  * [Condition Errors](#condition-errors)

## Options
The flag `--select_c20` can be used to select the set of errors
to include. By default, the active errors are C2000, C2001, C2002,
C2020, C2021, C2023.


## Comprehension Errors

### C2000

A comprehension expression should place each of its generators on a 
separate line.

```python
# Bad
[x+y for x in range(10) for y in range(10)]

# Good
[
    x + y
    for x in range(10)
    for y in range(10)
]
```


### C2001

A multiline comprehension expression should place each of its segments
(map, generator, filter) on a separate line.

```python
# Bad
[x+y for x in range(10) 
for y in range(10) if x+y > 5]

# Good
[
    x + y
    for x in range(10)
    for y in range(10)
    if x + y > 5
]
```


### C2002

A comprehension expression should not contain multiple filters.

```python
# Bad
[x for x in range(10) if x % 2 == 0 if x % 3 == 0]

# Good
[x for x in range(10) if x % 2 == x % 3 == 0]
```

### C2003

A comprehension expression should not span over multiple lines.

```python
# Bad
[x + y 
for x in range(10) ]

# Good
[x+y for x in range(10)]
```

### C2004

A comprehension expression should span over multiple lines.

```python
# Bad
[x for x in range(10)]

# Good
[x 
for x in range(10)]
```



## Condition Errors

### C2020

A multiline conditional expression should place each of its segments
on a separate line.

```python
# Bad
1 
if something() else 0

# Good
1
if something()
else 0
```


### C2021

A conditional expression used for assignment should be surrounded by
parantheses.

```python
# Bad
a = 1 if something() else 0

# Good
a = (1 if something() else 0)
```


### C2022

A conditional expression should not contain further conditional
expressions.

```python
# Bad
1 if x > 0 else -1 if x < 0 else 0

# Good
if x > 0:
    return 1
elif x < 0:
    return -1
else:
    return 0
```


### C2023

A conditional expression should not span over multiple lines.

```python
# Bad
1
if something()
else 0

# Good
1 if something() else 0
```


### C2024

A conditional expression should span over multiple lines.

```python
# Bad
1 if something() else 0

# Good
1
if something()
else 0
```


### C2025

Conditional expressions should not be used.
