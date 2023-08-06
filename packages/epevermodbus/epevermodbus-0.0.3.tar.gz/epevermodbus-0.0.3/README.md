# epevermodbus

To install the package run

```sh
pip install epevermodbus
```

To run the command line utility and see the debug output run the following on the command line

```sh
epevermodbus
```

To use the library within your Python code

```python
from epevermodbus.driver import EpeverChargeController


controller = EpeverChargeController("/dev/ttyUSB0", 1)

controller.get_solar_voltage()
```
