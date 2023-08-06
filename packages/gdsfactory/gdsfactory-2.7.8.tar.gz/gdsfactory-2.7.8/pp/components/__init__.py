""" NOTE: import order matters.
Only change the order if you know what you are doing

isort:skip_file
"""
import dataclasses
from pp.tech import LIBRARY

# level 0 components
from pp.components.array import array
from pp.components.array import array_2d
from pp.components.array_with_fanout import array_with_fanout
from pp.components.array_with_fanout import array_with_fanout_2d
from pp.components.array_with_via import array_with_via
from pp.components.array_with_via import array_with_via_2d
from pp.components.straight import straight
from pp.components.straight_heater import straight_heater
from pp.components.straight_heater import straight_with_heater
from pp.components.straight_pin import straight_pin
from pp.components.straight_array import straight_array

from pp.components.bend_circular import bend_circular
from pp.components.bend_circular import bend_circular180
from pp.components.bend_circular_heater import bend_circular_heater
from pp.components.bend_s import bend_s
from pp.components.bezier import bezier
from pp.components.bend_euler import bend_euler
from pp.components.bend_euler import bend_euler180
from pp.components.bend_euler import bend_euler_s

from pp.components.coupler90 import coupler90
from pp.components.coupler90bend import coupler90bend
from pp.components.coupler_straight import coupler_straight
from pp.components.coupler_symmetric import coupler_symmetric
from pp.components.coupler_asymmetric import coupler_asymmetric
from pp.components.hline import hline

# basic shapes
from pp.components.circle import circle
from pp.components.compass import compass
from pp.components.cross import cross
from pp.components.crossing_waveguide import crossing
from pp.components.crossing_waveguide import crossing45
from pp.components.crossing_waveguide import compensation_path
from pp.components.ellipse import ellipse
from pp.components.rectangle import rectangle
from pp.components.ring import ring
from pp.components.extension import extend_ports
from pp.components.taper import taper
from pp.components.taper import taper_strip_to_ridge
from pp.components.taper_from_csv import taper_0p5_to_3_l36
from pp.components.text import text
from pp.components.L import L
from pp.components.C import C
from pp.components.bbox import bbox
from pp.components.nxn import nxn
from pp.components.ramp import ramp
from pp.components.die import die
from pp.components.die_bbox import die_bbox

# optical test structures
from pp.components.version_stamp import version_stamp
from pp.components.version_stamp import qrcode
from pp.components.manhattan_font import manhattan_text
from pp.components.logo import logo
from pp.components.align import align_wafer
from pp.components.cutback_bend import cutback_bend90
from pp.components.cutback_bend import cutback_bend180
from pp.components.cutback_component import cutback_component
from pp.components.cutback_component import cutback_component_flipped

from pp.components.pcm.litho_calipers import litho_calipers
from pp.components.pcm.litho_steps import litho_steps
from pp.components.pcm.verniers import verniers
from pp.components.litho_ruler import litho_ruler


from pp.components.grating_coupler.elliptical import grating_coupler_elliptical_te
from pp.components.grating_coupler.elliptical import grating_coupler_elliptical_tm
from pp.components.grating_coupler.elliptical2 import grating_coupler_elliptical2
from pp.components.grating_coupler.uniform import grating_coupler_uniform
from pp.components.grating_coupler.uniform_optimized import (
    grating_coupler_uniform_optimized,
)
from pp.components.grating_coupler.grating_coupler_tree import grating_coupler_tree
from pp.components.grating_coupler.elliptical_trenches import grating_coupler_te
from pp.components.grating_coupler.elliptical_trenches import grating_coupler_tm
from pp.components.grating_coupler.grating_coupler_loss import grating_coupler_loss
from pp.components.delay_snake import delay_snake
from pp.components.delay_snake2 import delay_snake2
from pp.components.delay_snake3 import delay_snake3
from pp.components.spiral import spiral
from pp.components.spiral_inner_io import spiral_inner_io_euler
from pp.components.spiral_inner_io import spiral_inner_io
from pp.components.spiral_inner_io import spiral_inner_io_with_gratings
from pp.components.spiral_external_io import spiral_external_io
from pp.components.spiral_circular import spiral_circular
from pp.components.cdc import cdc
from pp.components.dbr import dbr
from pp.components.dbr2 import dbr2

# electrical
from pp.components.wire import wire_corner
from pp.components.wire import wire_straight
from pp.components.wire_sbend import wire_sbend
from pp.components.electrical.pad import pad
from pp.components.electrical.pad import pad_array
from pp.components.electrical.pad import pad_array_2d
from pp.components.via import via
from pp.components.via import via1
from pp.components.via import via2
from pp.components.via import via3
from pp.components.via_stack import via_stack
from pp.components.via_stack_with_offset import via_stack_with_offset
from pp.components.electrical.pads_shorted import pads_shorted

# electrical PCM
from pp.components.resistance_meander import resistance_meander
from pp.components.via_cutback import via_cutback

# level 1 components
from pp.components.cavity import cavity
from pp.components.coupler import coupler
from pp.components.coupler_ring import coupler_ring
from pp.components.coupler_adiabatic import coupler_adiabatic
from pp.components.coupler_full import coupler_full
from pp.components.disk import disk
from pp.components.ring_single import ring_single
from pp.components.ring_single_array import ring_single_array
from pp.components.ring_double import ring_double
from pp.components.mmi1x2 import mmi1x2
from pp.components.mmi2x2 import mmi2x2
from pp.components.mzi import mzi
from pp.components.mzi_phase_shifter import mzi_phase_shifter
from pp.components.mzit import mzit
from pp.components.mzi_lattice import mzi_lattice
from pp.components.mzit_lattice import mzit_lattice
from pp.components.loop_mirror import loop_mirror
from pp.components.fiber import fiber
from pp.components.fiber_array import fiber_array

# level 2 components
from pp.components.awg import awg
from pp.components.component_lattice import component_lattice
from pp.components.component_sequence import component_sequence
from pp.components.splitter_tree import splitter_tree
from pp.components.splitter_chain import splitter_chain


LIBRARY.register(
    [
        array,
        array_2d,
        array_with_fanout,
        array_with_fanout_2d,
        array_with_via,
        array_with_via_2d,
        C,
        L,
        align_wafer,
        awg,
        bbox,
        bend_circular180,
        bend_circular,
        bend_circular_heater,
        bend_euler180,
        bend_euler,
        bend_euler_s,
        bend_s,
        bezier,
        cavity,
        cdc,
        circle,
        compass,
        compensation_path,
        component_lattice,
        component_sequence,
        coupler90,
        coupler90bend,
        coupler,
        coupler_adiabatic,
        coupler_asymmetric,
        coupler_full,
        coupler_ring,
        coupler_straight,
        coupler_symmetric,
        cross,
        crossing45,
        crossing,
        cutback_bend180,
        cutback_bend90,
        cutback_component,
        cutback_component_flipped,
        dbr2,
        dbr,
        delay_snake,
        delay_snake2,
        delay_snake3,
        disk,
        die,
        die_bbox,
        ellipse,
        fiber,
        fiber_array,
        grating_coupler_elliptical2,
        grating_coupler_elliptical_te,
        grating_coupler_elliptical_tm,
        grating_coupler_loss,
        grating_coupler_te,
        grating_coupler_tm,
        grating_coupler_tree,
        grating_coupler_uniform,
        grating_coupler_uniform_optimized,
        hline,
        litho_calipers,
        litho_steps,
        litho_ruler,
        logo,
        loop_mirror,
        manhattan_text,
        mmi1x2,
        mmi2x2,
        mzi,
        mzi_phase_shifter,
        mzi_lattice,
        mzit,
        mzit_lattice,
        nxn,
        pad,
        pad_array,
        pad_array_2d,
        pads_shorted,
        qrcode,
        ramp,
        rectangle,
        ring,
        ring_double,
        ring_single,
        ring_single_array,
        spiral,
        spiral_circular,
        spiral_external_io,
        spiral_inner_io,
        spiral_inner_io_euler,
        spiral_inner_io_with_gratings,
        splitter_chain,
        splitter_tree,
        taper,
        taper_0p5_to_3_l36,
        taper_strip_to_ridge,
        extend_ports,
        resistance_meander,
        via_cutback,
        text,
        via_stack,
        via_stack_with_offset,
        verniers,
        version_stamp,
        via1,
        via2,
        via3,
        via,
        straight,
        straight_array,
        straight_heater,
        straight_pin,
        straight_with_heater,
        wire_straight,
        wire_corner,
        wire_sbend,
    ]
)


def library(component_type: str, **kwargs):
    """Returns a component with settings.
    from TECH.component_settings.component_type

    Args:
        component_type: library
        **kwargs: component_settings

    """
    from pp.tech import TECH
    import pp

    settings = getattr(TECH.component_settings, component_type)
    settings = dataclasses.asdict(settings) if settings else {}
    component_type = settings.pop("component_type", component_type)
    settings.update(**kwargs)

    if isinstance(component_type, pp.Component):
        return component_type
    elif callable(component_type):
        return component_type(**settings)
    elif component_type not in LIBRARY.library.keys():
        raise ValueError(
            f"component_type = {component_type} not in: \n"
            + "\n".join(LIBRARY.library.keys())
        )
    return LIBRARY.library[component_type](**settings)


component_names_skip_test = [
    "text",
    "component_sequence",
    "compensation_path",
    "component_lattice",
    "version_stamp",
    "resistance_meander",
]
component_names_skip_test_ports = ["coupler"]

container_names = ["cavity", "ring_single_dut"]
component_names = (
    set(LIBRARY.factory.keys()) - set(component_names_skip_test) - set(container_names)
)
component_names_test_ports = component_names - set(component_names_skip_test_ports)
circuit_names = {
    "mzi",
    "ring_single",
    "ring_single_array",
    "ring_double",
    "mzit_lattice",
    "mzit",
    "component_lattice",
}

__all__ = list(LIBRARY.factory.keys()) + container_names + ["extend_ports_list"]
component_factory = LIBRARY.factory

if __name__ == "__main__":
    for component_name in component_names:
        try:
            ci = LIBRARY.factory[component_name]()
        except Exception:
            print(f"error building {component_name}")
            raise Exception
    ci.show()
