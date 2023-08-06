# radix-ops

Convert numbers - both integer and floating-point - from one base to another.
Perform arithmetic operations in a given base.

### Installation

```Shell
pip install radix-ops
```

### Usage

```Python
from radix import Num

a = Num(20, 16)    # The number 20 in base 16
b = Num('ff', 16)  # FF or 255 in base 16

print(a.to(2))     # Convert to base 2 (100000)
print(a + b)       # Result in base 16 (11F)
```

### Examples

```Python
>>> from radix import Num
>>> Num(value='FE', base=16).to(base=10)
254
>>> Num(1100, 2).to(10)
12
>>> Num(10.75).to(16)  # When base is 10, it can be omitted.
A.C
>>> Num(10.75).to(2)
1010.11
>>> pi = 3.141592653589793
>>> Num(pi).to(16)
3.243F6A8885
>>> Num(-1001, 2).to(10)
-9
>>> (Num('1a', 16) - Num('ff', 16)) * Num(2, 16)  # (26 - 255) * 2 = -458 = -0x1ca
-1CA
```

### Note

1. Base should be between 2 and 36.

