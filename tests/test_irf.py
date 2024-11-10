# from io import StringIO


import numpy as np
import numpy.testing as npt

# import yaml
#
# from six.moves import range
from gridmet_bmi import BmiGridmet


def test_component_name():
    model = BmiGridmet()

    name = model.get_component_name()
    assert name == "Gridmet_BMI"
    assert model.get_component_name() is name


def test_start_time():
    model = BmiGridmet()
    model.initialize()

    npt.assert_almost_equal(model.get_start_time(), 0.0)


def test_end_time():
    model = BmiGridmet()
    model.initialize()

    npt.assert_almost_equal(model.get_end_time(), 7.0)


def test_initialize_defaults():
    model = BmiGridmet()
    model.initialize()
    grid_id = model.get_var_grid("daily_maximum_temperature")
    size = model.get_grid_size(grid_id)
    vals = np.empty(size)
    model.get_value("daily_maximum_temperature", vals)
    min = np.nanmin(vals)
    max = np.nanmax(vals)

    npt.assert_almost_equal(min, 266.399, decimal=2)
    npt.assert_almost_equal(max, 305.0, decimal=1)


def test_initialize_from_file():
    import datetime
    import os
    import tempfile

    import yaml

    yamldict = {
        "_start_date": datetime.date(year=2020, month=1, day=1),
        "_end_date": datetime.date(year=2020, month=1, day=7),
    }
    with tempfile.NamedTemporaryFile("w", delete=False) as fp:
        fp.write((yaml.dump(yamldict, sort_keys=False)))
        name = fp.name

    model = BmiGridmet()
    model.initialize(name)

    os.remove(name)
    shape = np.empty(2, dtype=int)
    tmp = model.get_grid_shape(0, shape)
    tmp2 = np.array([585, 1386])
    npt.assert_almost_equal(tmp, tmp2)


def test_update():
    model = BmiGridmet()
    model.initialize()

    for inc in range(6):
        model.update()
        npt.assert_almost_equal(
            model.get_current_time(), (inc + 1) * model.get_time_step()
        )


def test_finalize():
    model = BmiGridmet()
    model.initialize()
    model.update()
    model.finalize()
