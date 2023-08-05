# LazImp, The "don't wait for it..." package

LazImp is a package that allows lazy loading of python modules, packages and
symboles for python 3.10+. This package allows you to load modules and packages
only **when** the user use it. From dynamic import to "I only need this
function, not the whole framework", the start-up time is speed-up and delayed
over the execution of the software.

Using LazImp, you will reduce the memory usage and the start-up time of your
software.

## Example

First, you may have long loading or memory heavy modules to expose in your
package api:

```python
# package/heavy_module.py
print('Heavy module is loading...')
from time import sleep

sleep(10)
print('heavy_module loaded')
```

But instead of importing them directly, you can do a lazy import in
the `__init__.py`:

```python
# package/__init__.py of a package
import lazimp

math: lazimp.ModuleType
heavy_module: lazimp.ModuleType

__getattr__ = lazimp.lazy_import(
    'math',
    heavy_module='package',
)
```

Now, when you import the package:

```python
# main.py
import package

print('Before access to heavy_module')
print(package.heavy_module)
print('After access to heavy_module')
print('Before access to math')
print(package.math)
print('After access to math')
```

And the output:

```txt
Before access to heavy_module
Heavy module is loading...
(wait 10 sec)
heavy_module loaded
<module 'heavy_module' from '...'>
After access to heavy_module
Before access to math
# math loaded
<module 'math' (built-in)>
After access to math
```

Without the lazy loading of `heavy_module.py`, the output would have been:

```txt
Heavy module is loading...
(wait 10 sec)
heavy_module loaded  # math loaded too
Before access to heavy_module
<module 'heavy_module' from '...'>
After access to heavy_module
Before access to math
<module 'math' (built-in)>
After access to math
```

## Why this name: LazImp?

`lazimp` is a portmanteau of `lazy` and `imp`.

`imp` was the name of the module `importlib` before python 3.4 and its
deprecation: [What's new in Python 3.4: Deprecations in the Python API](https://docs.python.org/3/whatsnew/3.4.html#deprecations-in-the-python-api)

The name could have been `lazy_import` but the `imp` part was preferred as a
reference to the original module and because an
imp with sunglasses and cocktail is cool 😎, and `lazy` shorten because it
sounded better.