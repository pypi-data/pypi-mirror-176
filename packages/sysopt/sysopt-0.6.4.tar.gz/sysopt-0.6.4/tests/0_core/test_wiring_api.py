import pytest

from sysopt.blocks.common import Gain, Oscillator, LowPassFilter
from sysopt import Composite
from sysopt import exceptions


def test_wiring_port_to_port_succeeds():
    gain = Gain(channels=1)
    osc = Oscillator()
    
    composite = Composite(components=[gain, osc])
    composite.wires = [
        (gain.outputs, composite.outputs),
        (osc.outputs, gain.inputs)
    ]
    composite.check_wiring_or_raise()
    composite.check_wiring_or_raise()


def test_wiring_channel_to_channel_succeeds():
    gain = Gain(channels=1)
    osc = Oscillator()

    composite = Composite(components=[gain, osc])
    composite.wires = [
        (gain.outputs[0], composite.outputs[0]),
        (osc.outputs[0], gain.inputs[0])
    ]

    composite.check_wiring_or_raise()


def test_wiring_channels_by_name_succeeds():
    gain = Gain(channels=1)
    osc = Oscillator()

    composite = Composite(components=[gain, osc])
    composite.declare_outputs(['output0'])

    composite.wires = [
        (gain.outputs['output0'], composite.outputs['output0']),
        (osc.outputs['signal'], gain.inputs['input0'])
    ]
    composite.check_wiring_or_raise()


def test_forwarding_is_valid():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.wires = [
        (composite.inputs, gain.inputs),
        (gain.outputs, fltr.inputs),
        (fltr.outputs, composite.outputs)
    ]
    composite.check_wiring_or_raise()


def test_forwarding_by_name_is_valid():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.declare_inputs(['in'])
    composite.declare_outputs(['out'])
    composite.wires = [
        (composite.inputs['in'], gain.inputs),
        (gain.outputs, fltr.inputs),
        (fltr.outputs, composite.outputs['out'])
    ]
    composite.check_wiring_or_raise()


def test_unconnected_internal_input_should_throw():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.wires = [
        (gain.outputs, fltr.inputs),
        (fltr.outputs, composite.outputs)
    ]

    with pytest.raises(exceptions.UnconnectedInputError):
        composite.check_wiring_or_raise()


def test_no_forwarded_outputs_should_throw():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.wires = [
        (composite.inputs, gain.inputs),
        (gain.outputs, fltr.inputs)
    ]

    with pytest.raises(exceptions.InvalidComponentError):
        composite.check_wiring_or_raise()


def test_dangling_input_should_throw():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.wires = [
        (gain.outputs, fltr.inputs),
        (fltr.outputs, composite.outputs)
    ]
    composite.declare_inputs(['in'])
    with pytest.raises(exceptions.DanglingInputError):
        composite.check_wiring_or_raise()


def test_wrong_size_should_throw():
    gain_1 = Gain(channels=1)
    gain_2 = Gain(channels=2)

    composite = Composite(components=[gain_1, gain_2])
    with pytest.raises(exceptions.InvalidWire):
        composite.wires = [(gain_2.outputs, gain_1.inputs)]


def test_connecting_to_port_with_invalid_name_should_throw():
    gain = Gain(channels=1)
    fltr = LowPassFilter()

    composite = Composite(components=[gain, fltr])
    composite.declare_inputs(['in'])
    composite.declare_outputs(['out'])

    composite.wires = [
        (composite.inputs['in'], gain.inputs),
        (gain.outputs, fltr.inputs)
    ]
    with pytest.raises(exceptions.InvalidPort):
        composite.wires.append((fltr.outputs, composite.outputs['wrong_name']))


