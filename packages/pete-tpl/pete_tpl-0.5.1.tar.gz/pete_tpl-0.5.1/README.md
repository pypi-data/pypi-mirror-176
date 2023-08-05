# pete_tpl

A Python binding for [libpetetpl](https://github.com/pete-tpl/libpetetpl).

__The project is under development!__

## Development environment

## Installation

```bash
pip install pete-tpl
# Probably reloading of the shell session is needed
# e.g. deactivate && source .venv/bin/activate - in case of virtualenv
petetpl_postinstall.py
```
The second command downloads a shared library. Since the `libpetetpl` library is not implemented in C/C++, it cannot be compiled via Python setup tools.

## Usage

Please check also the [sample file](samples/sample.py).

```python
from pete_tpl import PeteTpl

pete = PeteTpl()

result = pete.render(
    "Hello,{# comment #} {{ user }}! Number is {{ some_number }}\nCalculation: {{ 2 * 9 }}\nPercentage: {{ percentage }}%",
    {
        'user': 'John Doe',
        'some_number': 4443,
        'percentage': 23.41234,
    })

print(result)

# Output:
# Hello, John Doe! Number is 4443
# Calculation: 18
# Percentage: 23.41234%
```