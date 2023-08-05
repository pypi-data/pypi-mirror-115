import pytest
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.num_regression import NumericRegressionFixture

from pp.add_grating_couplers import add_grating_couplers
from pp.add_padding import add_padding_container
from pp.add_pins import add_pins_container
from pp.add_tapers import add_tapers
from pp.add_termination import add_gratings_and_loopback, add_termination
from pp.components.cavity import cavity
from pp.components.extension import extend_ports

# from pp.components.straight import straight
# from pp.components.straight_heater import straight_heater
# from pp.difftest import difftest
from pp.components.mmi2x2 import mmi2x2
from pp.components.mzi_phase_shifter import mzi_phase_shifter
from pp.components.ring_single_dut import ring_single_dut
from pp.components.spiral_inner_io import spiral_inner_io
from pp.rotate import rotate
from pp.routing.add_electrical_pads_shortest import add_electrical_pads_shortest
from pp.routing.add_electrical_pads_top import add_electrical_pads_top
from pp.routing.add_fiber_array import add_fiber_array
from pp.routing.add_fiber_single import add_fiber_single
from pp.routing.fanout2x2 import fanout2x2

container_factory = dict(
    add_electrical_pads_shortest=add_electrical_pads_shortest,
    add_electrical_pads_top=add_electrical_pads_top,
    add_fiber_array=add_fiber_array,
    add_fiber_single=add_fiber_single,
    add_grating_couplers=add_grating_couplers,
    add_padding_container=add_padding_container,
    add_tapers=add_tapers,
    add_termination=add_termination,
    add_pins_container=add_pins_container,
    extend_ports=extend_ports,
    fanout2x2=fanout2x2,
    rotate=rotate,
    cavity=cavity,
    ring_single_dut=ring_single_dut,
)

container_names = set(container_factory.keys()) - set()
component = mzi_phase_shifter(splitter=mmi2x2)


@pytest.mark.parametrize("container_type", container_names)
def test_settings(container_type: str, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    c = container_factory[container_type](component=component)
    data_regression.check(c.get_settings())


@pytest.mark.parametrize("container_type", container_names)
def test_ports(container_type: str, num_regression: NumericRegressionFixture) -> None:
    """Avoid regressions in port names and locations."""
    c = container_factory[container_type](component=component)
    if c.ports:
        num_regression.check(c.get_ports_array())


# @pytest.mark.parametrize("container_type", container_names)
# def test_gds(container_type: str) -> None:
#     """Avoid regressions in GDS geometry shapes and layers."""
#     c = container_factory[container_type](component=component)
#     difftest(c)


# Special test cases for exotic components


def test_add_gratings_and_loopback(data_regression: DataRegressionFixture) -> None:
    """This container requires all ports to face the same direction."""
    c = add_gratings_and_loopback(component=spiral_inner_io())
    data_regression.check(c.get_settings())
