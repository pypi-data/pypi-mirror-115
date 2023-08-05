from typing import Tuple

import numpy as np
import pytest

import pp


@pytest.mark.parametrize("x,y,layer", [(1, 8, (1, 0)), (9, 1, (2, 2))])
def test_compute_area(x: int, y: int, layer: Tuple[int, int]) -> None:
    c = pp.components.rectangle(size=(x, y), layer=layer)
    c.write_gds()
    area = pp.drc.compute_area(c, layer)
    assert np.isclose(area, x * y)


if __name__ == "__main__":
    test_compute_area()
