# simbio-earm

## Installation

```
pip install simbio-earm
```

## Usage

```python
from simbio.models.earm import Albeck11b
from simbio.simulator import Simulator

t = range(100)
Simulator(Albeck11b).run(t).plot()
```
