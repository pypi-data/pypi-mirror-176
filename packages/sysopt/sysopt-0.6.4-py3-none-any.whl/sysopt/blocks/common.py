"""Commonly used blocks for model building."""
from typing import Union, List
from sysopt import Block, Signature, Metadata
from numpy import cos, power


class Gain(Block):
    r"""Block for a simple gain stage.

    For each channel (indexed by i), the input-output relationship
    is given by

    math::

        y[i] = p[i] * u[i], i = 0,..., channels - 1

    where :math:`u` are the inputs, :math:`y` are the outputs and :math:`p`
    are the parameters.

    Args:
        channels: Number of gain channels to provide.

    """
    def __init__(self, channels: int):
        super().__init__(
            Metadata(
                inputs=[f'input{i}' for i in range(channels)],
                outputs=[f'output{i}' for i in range(channels)],
                parameters=[f'coefficient{i}' for i in range(channels)]
            ))

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        return [gain * signal for signal, gain in zip(inputs, parameters)]


class Mixer(Block):
    """Provides the output equal to the sum of the inputs.

    Args:
        inputs: number of input channels.

    """
    def __init__(self, inputs: int):
        sig = Signature(
            inputs=inputs,
            outputs=1,
            states=0,
            parameters=0
        )
        super().__init__(sig)

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        return sum(inputs),


class DifferentialAmplifier(Block):
    """Computes `(s_+ - s_-)* 10^({gain/10) + bias`."""
    def __init__(self):
        super().__init__(
            Metadata(
                inputs=['+', '-'],
                parameters=['gain dB', 'bias'],
                outputs=['signal'])
        )

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        gain, bias = parameters
        k = power(10, gain / 10)
        return k * (inputs[0] - inputs[1]) + bias


class ConstantSignal(Block):
    r"""Output constant on each channel.

    For each channel, a constant signal :math:`y[i]` is output equal to the
    corresponding parameter value :math:`p[i]`. That is,

    math::
        y[i](t) = p[i], \text{for all} t

    Args:
        outputs: The number of output channels.

    """
    def __init__(self, outputs: Union[int, List[str]], name=None):

        try:
            params = [f'output[{i}]' for i in range(outputs)]
        except TypeError:
            params = [str(v) for v in outputs]

        super().__init__(
            Metadata(outputs=params, parameters=params), name=name
        )

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        return parameters,


class Oscillator(Block):
    """Cosine oscillator with the given frequency and phase."""

    def __init__(self, name=None):
        metadata = Metadata(
            parameters=['frequency', 'phase'],
            outputs=['signal']
        )
        super().__init__(metadata, name)

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        freq, phase = parameters
        return cos(t * freq + phase),


class LowPassFilter(Block):
    """First order low-pass filter."""
    def __init__(self):
        metadata = Metadata(
            parameters=['cutoff frequency'],
            inputs=['input'],
            outputs=['output'],
            states=['states']
        )
        super().__init__(metadata)

    def initial_state(self, parameters):
        return 0,

    def compute_dynamics(self, t, states, algebraics, inputs, parameters):
        x, = states
        w, = parameters
        u, = inputs
        return (u - x) / w,

    def compute_outputs(self, t, states, algebraics, inputs, parameters):
        x, = states
        return x,


class HighPassFilter(Block):
    """First order highpass filter."""
    def __init__(self, name=None):
        super().__init__(
            metadata_or_signature=Metadata(
                states=['state'],
                inputs=['input'],
                outputs=['output'],
                parameters=['cutoff frequency']
            ),
            name=name
        )

    def initial_state(self, _):
        return [0]

    def compute_dynamics(self,
                         t,
                         states,
                         algebraics,
                         inputs,
                         parameters):
        x, = states
        u, = inputs
        w, = parameters

        return (u - x) / w

    def compute_outputs(self,
                        t,
                        states,
                        algebraics,
                        inputs,
                        parameters):
        x, = states
        u, = inputs
        w, = parameters
        return (u - x) / w

