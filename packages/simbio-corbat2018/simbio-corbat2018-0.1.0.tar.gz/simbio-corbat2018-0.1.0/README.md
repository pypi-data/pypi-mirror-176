# simbio-corbat2018

## Installation

```
pip install simbio-corbat2018
```

## Usage

```python
from simbio.models.corbat2018 import Corbat2018_extrinsic
from simbio.simulator import Simulator

t = range(100)
Simulator(Corbat2018_extrinsic).run(t).plot()
```
