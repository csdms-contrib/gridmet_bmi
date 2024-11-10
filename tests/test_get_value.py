import numpy as np
import numpy.testing as npt

from gridmet_bmi import BmiGridmet


def test_get_initial_value():
    model = BmiGridmet()
    model.initialize()

    grid_id = model.get_var_grid("daily_maximum_temperature")
    size = model.get_grid_size(grid_id)
    vals1 = np.empty(size)
    z0 = model.get_value("daily_maximum_temperature", vals1)
    min = np.nanmin(z0)
    max = np.nanmax(z0)

    npt.assert_almost_equal(min, 266.1, decimal=1)
    npt.assert_almost_equal(max, 304.7, decimal=1)


def test_get_value_copy():
    model = BmiGridmet()
    model.initialize()
    grid_id = model.get_var_grid("daily_maximum_temperature")
    size = model.get_grid_size(grid_id)
    vals1 = np.empty(size)
    vals2 = np.empty(size)
    z0 = model.get_value("daily_maximum_temperature", vals1)
    z1 = model.get_value("daily_maximum_temperature", vals2)

    assert z0 is not z1
    npt.assert_array_almost_equal(z0, z1)


def test_value_size():
    model = BmiGridmet()
    model.initialize()
    grid_id = model.get_var_grid("daily_maximum_temperature")
    size = model.get_grid_size(grid_id)
    vals1 = np.empty(size)
    z = model.get_value("daily_maximum_temperature", vals1)
    assert model.get_grid_size(0) == z.size


# def test_get_value_pointer():
#     model = BmiGridmet()
#     model.initialize()
#
#     grid_id = model.get_var_grid('daily_maximum_temperature')
#     size = model.get_grid_size(grid_id)
#     vals1 = np.empty(size)
#
#     z0 = model.get_value_ptr("daily_maximum_temperature")
#     z1 = model.get_value("daily_maximum_temperature", vals1)
#
#     assert z0 is not z1
#     npt.assert_array_almost_equal(z0, z1)
#
#     for _ in range(3):
#         model.update()
#     z2 = model.get_value_ptr("daily_maximum_temperature")
#     npt.assert_array_equal(z0, z2, verbose=True)
# assert z0 is model.get_value_ptr("daily_maximum_temperature")
