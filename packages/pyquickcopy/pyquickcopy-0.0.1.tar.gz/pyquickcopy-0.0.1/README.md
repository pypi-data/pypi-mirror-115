# pyQuickCopy

<badges>[![version](https://img.shields.io/pypi/v/pyquickcopy.svg)](https://pypi.org/project/pyquickcopy/)
[![license](https://img.shields.io/pypi/l/pyquickcopy.svg)](https://pypi.org/project/pyquickcopy/)
[![pyversions](https://img.shields.io/pypi/pyversions/pyquickcopy.svg)](https://pypi.org/project/pyquickcopy/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Python implementation of [QuickCopy](https://github.com/foxe6/QuickCopy/). </i>

# Hierarchy

```
pyquickcopy
'---- QuickCopy()
    |---- copy()
    |---- paste()
    |---- clear()
    '---- loop()
```

# Example

## python
```python
import pyquickcopy


accumulate_list = []


def listener(clipboard):
    # tbd
    # copy a special text to trigger clear accumulate_list
    if "::clear" == clipboard:
        accumulate_list.clear()
        qc.clear()
        qc.copy(clipboard)
        return

    # prevent loop after joining accumulate_list
    if "\n" in clipboard:
        return

    accumulate_list.append(clipboard)
    qc.copy("\n".join(accumulate_list))

    print(accumulate_list)
    print()


qc = pyquickcopy.QuickCopy(
    listener=listener,
    # how frequent the listener is called
    listen_rate=1/10,
    debug=False
)
qc.loop()

```
