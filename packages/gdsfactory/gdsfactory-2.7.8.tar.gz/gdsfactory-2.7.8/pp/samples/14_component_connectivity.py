"""Lets define the references from a component and then connect them together.
"""


from typing import Optional

import pp
from pp.cell import cell
from pp.component import Component
from pp.components.bend_euler import bend_euler
from pp.components.coupler_ring import coupler_ring as coupler_ring_function
from pp.components.straight import straight as straight_function
from pp.config import call_if_func
from pp.snap import assert_on_2nm_grid
from pp.types import ComponentOrFactory


@cell
def test_ring_single(
    gap: float = 0.2,
    radius: float = 10.0,
    length_x: float = 4.0,
    length_y: float = 0.010,
    coupler_ring: ComponentOrFactory = coupler_ring_function,
    straight: ComponentOrFactory = straight_function,
    bend: Optional[ComponentOrFactory] = None,
    pins: bool = False,
    waveguide: str = "strip",
    **waveguide_settings
) -> Component:
    """Single bus ring made of a ring coupler (cb: bottom)
    connected with two vertical straights (wl: left, wr: right)
    two bends (bl, br) and horizontal straight (wg: top)

    Args:
        gap: gap between for coupler
        radius: for the bend and coupler
        length_x: ring coupler length
        length_y: vertical straight length
        coupler: ring coupler function
        straight: straight function
        bend: 90 degrees bend function
        pins: add pins
        waveguide: for straights
        **waveguide_settings


    .. code::

          bl-wt-br
          |      |
          wl     wr length_y
          |      |
         --==cb==-- gap

          length_x

    """
    assert_on_2nm_grid(gap)

    coupler_ring_component = (
        coupler_ring(
            bend=bend,
            gap=gap,
            radius=radius,
            length_x=length_x,
            waveguide=waveguide,
            **waveguide_settings
        )
        if callable(coupler_ring)
        else coupler_ring
    )
    straight_side = call_if_func(
        straight, length=length_y, waveguide=waveguide, **waveguide_settings
    )
    straight_top = call_if_func(
        straight, length=length_x, waveguide=waveguide, **waveguide_settings
    )

    bend = bend or bend_euler
    bend_ref = (
        bend(radius=radius, waveguide=waveguide, **waveguide_settings)
        if callable(bend)
        else bend
    )

    c = Component()
    cb = c << coupler_ring_component
    wl = c << straight_side
    wr = c << straight_side
    bl = c << bend_ref
    br = c << bend_ref
    wt = c << straight_top
    # wt.mirror(p1=(0, 0), p2=(1, 0))

    wl.connect(port="E0", destination=cb.ports["N0"])
    bl.connect(port="N0", destination=wl.ports["W0"])

    wt.connect(port="E0", destination=bl.ports["W0"])
    br.connect(port="N0", destination=wt.ports["W0"])
    wr.connect(port="W0", destination=br.ports["W0"])
    wr.connect(port="E0", destination=cb.ports["N1"])  # just for netlist

    c.add_port("E0", port=cb.ports["E0"])
    c.add_port("W0", port=cb.ports["W0"])
    if pins:
        pp.add_pins_to_references(c)
    return c


if __name__ == "__main__":
    c = test_ring_single(gap=0.15, length_x=0.2, length_y=0.13)
    c.show()
