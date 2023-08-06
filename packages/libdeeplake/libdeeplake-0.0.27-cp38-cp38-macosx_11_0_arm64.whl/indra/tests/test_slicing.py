from indra import api
import pytest
from .constants import (
    MNIST_DS_NAME,
)

def check_equality(dsv, ds, slice):
    for i, x in enumerate(slice):
        assert dsv.tensors[1][i] == ds.tensors[1][x]

def test_dataset_slicing():
    ds = api.dataset(MNIST_DS_NAME)
    dsv = ds[0:1000]
    check_equality(dsv, ds, range(0, 1000))
    dsv = ds[0:1000:7]
    check_equality(dsv, ds, range(0, 1000, 7))
    dsv = ds[0:1000:5]
    check_equality(dsv, ds, range(0, 1000, 5))
    dsv = ds[337:5647:13]
    check_equality(dsv, ds, range(337, 5647, 13))

    dsvv = dsv[1:50:6]
    check_equality(dsvv, dsv, range(1, 50, 6))
    dsvv = dsv[[5, 3, 8, 1, 90, 80, 70]]
    check_equality(dsvv, dsv, [5, 3, 8, 1, 90, 80, 70])
    with pytest.raises(IndexError):
        dsvv = dsv[[5, 3, 8, 1, 2000, 90, 80, 70]]

    dsv = ds[[1, 59999, 49999, 4999, 399, 29]]    
    check_equality(dsv, ds, [1, 59999, 49999, 4999, 399, 29])
    dsvv = dsv[[5, 3, 1, 4, 2, 0]]
    check_equality(dsvv, dsv, [5, 3, 1, 4, 2, 0])
    dsvv = dsv[1:5:2]
    check_equality(dsvv, dsv, range(1, 5, 2))