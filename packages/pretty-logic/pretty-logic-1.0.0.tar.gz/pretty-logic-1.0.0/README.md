# Pretty Logic

Are you tired of your multi-line`or` statements locking ugly? Would you rather use commas between your booleans? This is the package for you.

It's very simple!

### And
```python
from pretty_logic import _and

if _and(True, False, True, True):
    print("This is false")
else:
    print("This is true")
```

### Or
```python
from pretty_logic import _or

if _or(True, False, True, True):
    print("This is true")
else:
    print("This is false")
```
