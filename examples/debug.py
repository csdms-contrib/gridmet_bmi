# import matplotlib.pyplot as plt
from gridmet_bmi import BmiGridmet
import numpy as np
import numpy.testing as npt
import tempfile
import yaml
import datetime


def print_times(x):
    print(x.get_start_time())
    print(x.get_time_step())
    print(x.get_time_units())
    print(x.get_current_time())
    print(x.get_end_time())


x = BmiGridmet()
# x.initialize('gridmet_bmi.yaml')
x.initialize()
print(x.get_input_var_names())
print(x.get_output_var_names())
grid_id = x.get_var_grid('daily_maximum_temperature')
size = x.get_grid_size(grid_id)
shape = np.empty(2, dtype=int)
origin = np.empty(2, dtype=float)
delta = np.empty(2, dtype=float)
x.get_grid_origin(grid_id, origin)
x.get_grid_spacing(grid_id, spacing=delta)
tmp = x.get_grid_shape(grid_id, shape)
print(type(shape), shape[0], shape[1], shape)
tmp2 = np.array([585, 1386])
npt.assert_almost_equal(shape, np.array([585, 1386]))
vals = np.zeros(size)
x.get_value('daily_maximum_temperature', vals)
print(np.nanmin(vals))
print(np.nanmax(vals))
print_times(x)
x.update()
print_times(x)
tmp = 0
x.finalize()
# yamldict = {"_start_date": datetime.date(year=2020, month=1, day=1),
#             "_end_date": datetime.date(year=2020, month=1, day=7)}
# with tempfile.NamedTemporaryFile("w", delete=False) as fp:
#     fp.write((yaml.dump(yamldict, sort_keys=False)))
#     name = fp.name

# print(name)