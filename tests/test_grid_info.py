import numpy as np
import numpy.testing as npt
import pytest

from gridmet_bmi import BmiGridmet

grid_id = 0
invalid_grid_id = 12345


def test_grid_var_names():
    model = BmiGridmet()
    model.initialize()

    names = model.get_input_var_names()
    assert names == ("")

    names = model.get_output_var_names()
    assert names == (
        "daily_maximum_temperature",
        "daily_minimum_temperature",
        "precipitation_amount",
    )


def test_grid_var_item_count():
    model = BmiGridmet()
    model.initialize()

    count = model.get_input_item_count()
    assert count == 0

    count = model.get_output_item_count()
    assert count == 3


def test_grid_var_units():
    model = BmiGridmet()
    model.initialize()
    assert model.get_var_units("daily_maximum_temperature") == "K"
    assert model.get_var_units("precipitation_amount") == "mm"


def test_grid_id():
    model = BmiGridmet()
    model.initialize()
    assert model.get_var_grid("daily_maximum_temperature") == grid_id


def test_grid_var_rank():
    model = BmiGridmet()
    model.initialize()
    assert model.get_grid_rank(grid_id) == 2


def test_grid_var_rank_fail():
    model = BmiGridmet()
    model.initialize()
    with pytest.raises(KeyError):
        model.get_grid_rank(invalid_grid_id)


def test_grid_var_size():
    model = BmiGridmet()
    model.initialize()
    assert model.get_grid_size(grid_id) == 810810


def test_grid_var_size_fail():
    model = BmiGridmet()
    model.initialize()
    with pytest.raises(KeyError):
        model.get_grid_size(invalid_grid_id)


def test_grid_var_shape():
    model = BmiGridmet()
    model.initialize()
    shape = np.empty(2, dtype=int)
    tmp2 = np.array([585, 1386])
    npt.assert_equal(model.get_grid_shape(grid_id, shape), tmp2)


def test_grid_var_shape_fail():
    model = BmiGridmet()
    model.initialize()
    shape = np.empty(2, dtype=int)
    with pytest.raises(KeyError):
        model.get_grid_shape(invalid_grid_id, shape)


def test_grid_var_spacing():
    model = BmiGridmet()
    model.initialize()
    shape = np.empty(2, dtype=float)
    tmp2 = np.array([0.041667, 0.041667])
    npt.assert_almost_equal(model.get_grid_spacing(grid_id, shape), tmp2, decimal=4)


def test_grid_var_origin():
    model = BmiGridmet()
    model.initialize()
    shape = np.empty(2, dtype=float)
    tmp2 = np.array([25.066667, -124.77])
    npt.assert_almost_equal(model.get_grid_origin(grid_id, shape), tmp2, decimal=2)


def test_grid_var_type():
    model = BmiGridmet()
    model.initialize()
    assert model.get_var_type("daily_maximum_temperature") == "float64"


def test_grid_type():
    model = BmiGridmet()
    model.initialize()
    assert model.get_grid_type(grid_id) == "uniform_rectilinear"
