"""Base classes for block-based modelling."""
from typing import Iterable, Optional, Union, NewType, Tuple, List
from functools import partial
import weakref
from dataclasses import asdict
from sysopt.modelling.types import (Signature, Metadata, Time, States, Parameters,
                                    Inputs, Algebraics, Numeric)

from sysopt.symbolic import SignalReference, restriction_map
from sysopt.exceptions import (
    DanglingInputError, InvalidWire, UnconnectedInputError,
    InvalidComponentError, UnconnectedOutputError, InvalidPort
)


Pin = NewType('Pin', Union['Port', 'Channel'])
Connection = NewType('Connection', Tuple[Pin, Pin])


class Port:
    """Holds a unique identifier for an input/output port on a block.

    Args:
        parent: The owning object.
        size: The number of channels this port has.

    """

    def __init__(self, port_type, parent: 'Block', size: int = 0):
        self._block = weakref.ref(parent)
        self.port_type = port_type
        self._channels = []
        self.size = size
        """(int) Number of 'channel' on this port"""

    def __str__(self):
        return f'{str(self.parent)}->{self.port_type}'

    def __repr__(self):
        return f'Port({self.port_type}, {self.parent}, {self.size})'

    def channel_name(self, i: int):
        try:
            names = getattr(self.block.metadata, self.port_type)
            return names[i]
        except AttributeError:
            return f'{self.port_type}[{i}]'

    @property
    def size(self):
        return len(self._channels)

    @size.setter
    def size(self, value):
        difference = value - self.size
        if difference >= 0:
            offset = self.size
            self._channels += [
                Channel(self, [i + offset]) for i in range(difference)
            ]

    @property
    def block(self):
        return self._block()

    @property
    def parent(self):
        """The block that this port is from."""
        return self._block()

    def __len__(self):
        return self.size

    def __hash__(self):
        return id(self)

    def __contains__(self, item):
        try:
            return item.port is self
        except AttributeError:
            return item is self

    def __getitem__(self, item):
        if isinstance(item, slice):
            self.size = max(item.stop, self.size)
            indices = list(range(item.start or 0, item.stop, item.step or 1))
            return Channel(self, indices)

        elif isinstance(item, int):
            self.size = max(item + 1, self.size)
            return Channel(self, [item])
        elif isinstance(item, str):
            idx = self.parent.find_port_by_name(self.port_type, item)
            if idx >= 0:
                return Channel(self, [idx])
        raise ValueError(f'Can\'t get a lazy ref for [{self.parent} {item}]')

    def __cmp__(self, other):
        return id(self) == id(other)

    def __eq__(self, other):
        try:
            return (self.block == other.block
                    and self.port_type == other.port_type)
        except AttributeError:
            pass
        return self is other

    def __iter__(self):
        return iter(self._channels)

    def __call__(self, t):
        y_t = SignalReference(self)

        if t is y_t.t:
            return y_t
        else:
            return y_t(t)

    @property
    def indices(self) -> List[int]:
        return list(range(self.size))


class Channel:
    """A channel on the associated port."""
    def __init__(self, port: Port, indices: List[int]):
        self.port = port
        self.indices = indices  # type: List[int]

    def __str__(self):
        return f'{str(self.port)}{self.indices}'

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(port={repr(self.port)}, ' \
               f'indices={repr(self.indices)})'

    @property
    def block(self) -> 'ComponentBase':
        return self.port.block

    @property
    def port_type(self):
        return self.port.port_type

    def __call__(self, t):
        y = self.port(t)

        pi = restriction_map(self.indices, y.shape[0])
        return pi(y)

    @property
    def size(self):
        return len(self.indices)

    @property
    def parent(self):
        return self.port.parent

    def __iter__(self):
        return iter(self.indices)


class ComponentBase:
    """Interface definition and recursive search methods for components."""
    _instance_count = 0  # pylint: disable=invalid-name

    def __init__(self, *args, **kwargs):
        pass

    @property
    def parent(self):
        if self._parent:
            return self._parent()
        return None

    @parent.setter
    def parent(self, value: 'Composite'):
        if value is None:
            self._parent = None
        else:
            self._parent = weakref.ref(value)

    def trunk(self):
        node = self
        tree = []
        while node is not None:
            tree.append(node)
            node = node.parent
        return reversed(tree)

    def __str__(self):
        return '/'.join([node.name for node in self.trunk()])

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def __eq__(self, other):
        return id(self) == id(other)

    def compute_dynamics(self,
                         t: Time,
                         states: States,
                         algebraics: Algebraics,
                         inputs: Inputs,
                         parameters: Parameters):
        raise NotImplementedError

    def compute_outputs(self,
                        t: Time,
                        states: States,
                        algebraics: Algebraics,
                        inputs: Inputs,
                        parameters: Parameters) -> Numeric:
        raise NotImplementedError

    def compute_residuals(self,
                          t: Time,
                          states: States,
                          algebraics: Algebraics,
                          inputs: Inputs,
                          parameters: Parameters) -> Numeric:
        raise NotImplementedError

    def initial_state(self, parameters: Parameters) -> Numeric:
        raise NotImplementedError

    def __new__(cls, *args, name=None, **kwargs):  # noqa
        obj = super().__new__(cls)
        obj.inputs = Port('inputs', obj)
        obj.outputs = Port('outputs', obj)
        setattr(obj, '__hash__', lambda arg: id(obj))
        setattr(obj, '_parent', None)
        ComponentBase._instance_count += 1
        setattr(
            obj, 'name',
            name or f'{cls.__name__}_{ComponentBase._instance_count}'
        )

        return obj


class ParameterView:
    """List/dict-like interface for block parameters"""

    def __init__(self, block):
        self.block = weakref.ref(block)

    def __getitem__(self, item):
        parent = self.block()
        if isinstance(item, str):
            if item not in parent.metadata.parameters:
                raise KeyError(item)
            return f'{str(parent)}/{item}'

        if isinstance(item, int):
            return f'{str(parent)}/{parent.metadata.parameters[item]}'
        if isinstance(item, slice):
            return list(self)[item]

        raise KeyError(item)

    def __len__(self):
        return len(self.block().metadata.parameters)

    def __iter__(self):
        parent = self.block()
        for p in parent.metadata.parameters:
            yield f'{str(parent)}/{p}'


class Block(ComponentBase):
    r"""Base class for component models.

    Blocks represent the fundamental components in a model, and
    describe parameter dynamics and/or input-output maps.

    A block is made up of input, output, parameter, states and
    algebraically constrained spaces.
    The dimension of these spaces are defined either implicitly by
    metadata, or explicitly via an instance `sysopt.Signature`.
    Formally, we define these spaces as :math:`U,Y,P,X,Z` respectively.
    Then, a system can be characterised by the functions $f,g,h$ such
    that

    math::
        \dot{x} = f(t, x, z, u, p)
              y = g(t, x, z, y, p)
              0 = h(t, x, z, y, p)

    and with initial conditions :math:`x0(p) = x(0; p)` when it is relevant.

    Args:
        metadata_or_signature: The metadata or signature describing the
            dimensions of the funadmental spaces of this system.

    Attributes:
        signature: An instance of `sysopt.Signature` describing the dimensions
            of input, states, algebraic, output and parameter spaces.
        metadata: An optional instance of `sysopt.Metadata`
            describing the metadata (eg. names) of each term in the input,
            output, states, algebraic and parameter spaces.
        inputs: An instance of `Port` used to define connections.
        outputs: An instance of `Port` used to define connections.

    """

    def __init__(self,
                 metadata_or_signature: Union[Signature, Metadata],
                 name=None
                 ):

        if isinstance(metadata_or_signature, Signature):
            metadata_or_signature = Metadata.from_signature(
                metadata_or_signature
            )

        self.metadata = metadata_or_signature

        self.inputs.size = self.signature.inputs
        self.outputs.size = self.signature.outputs
        super().__init__(name)

    @property
    def parameters(self):
        if not self.metadata.parameters:
            return []

        return ParameterView(self)

    def find_port_by_name(self, var_type, name):
        if var_type not in {'inputs', 'outputs'}:
            raise ValueError(f'{var_type} is not a valid port type')
        try:
            values = asdict(self.metadata)[var_type]
        except KeyError as ex:
            msg = f'{var_type} is not a valid metadata field'
            raise ValueError(msg) from ex
        return values.index(name)

    @property
    def signature(self):
        return self.metadata.signature

    def find_by_type_and_name(self, var_type, var_name: str):
        block_name = str(self)
        if var_name.startswith(f'{block_name}/'):
            name = var_name[len(block_name) + 1:]
            values = asdict(self.metadata)[var_type]
            index = values.index(name)
            if index >= 0:
                return self, index

        return None


class ConnectionList(list):
    """Container for connections between ports.

    Args:
        parent: Composite object that contains this connection list.

    """

    def __init__(self, parent: 'Composite'):
        super().__init__()
        self._parent = weakref.ref(parent)

    def __iadd__(self, other):
        for pair in other:
            self.append(pair)

    @property
    def parent(self):
        return self._parent()

    def append(self, pair):
        composite = self.parent

        def is_valid_source(item):
            if isinstance(item, Channel):
                return is_valid_source(item.port)
            if isinstance(item, Port):
                return item is composite.inputs or (
                    item.parent.parent is composite
                    and item is item.parent.outputs)
            return False

        def is_valid_dest(item):
            if isinstance(item, Channel):
                return is_valid_dest(item.port)
            if isinstance(item, Port):
                return item is composite.outputs or (
                    item.parent.parent is composite
                    and item is item.parent.inputs
                )
            return False

        src, dest = pair
        if not is_valid_source(src):
            raise InvalidWire(
                src, dest, 'Source is not a valid port or channel'
            )
        if not is_valid_dest(dest):
            raise InvalidWire(
                src, dest, 'Destination is not a valid port or channel'
            )
        if src is dest:
            raise InvalidWire(src, dest, 'Cannot connect a port to itself')

        if not src.size and dest.size:
            src.size = dest.size
        elif not dest.size and src.size:
            dest.size = src.size
        elif not src.size and not dest.size:
            raise ConnectionError(
              f'Cannot connect {src} to {dest}, '
              f'both have unknown dimensions. '
              f'Error occurs in Composite {self._parent()} '
              f'when connecting blocks {src.parent} to {dest.parent}.')
        elif src.size != dest.size:
            raise InvalidWire(
                src, dest, f'Cannot connect sizes: {src.size} to {dest.size}'
            )
        super().append((src, dest))


class DiscreteBlock(Block):
    """Interface Definition for discrete time controllers."""

    def __init__(self,
                 metadata_or_signature=Union[Metadata, Signature],
                 clock_hz=100,
                 name=None
                 ):

        assert clock_hz > 0

        self._frequency = clock_hz
        super().__init__(metadata_or_signature, name)

    @property
    def frequency(self):
        return self._frequency

    @property
    def dt(self):
        return 1/self.frequency

    def compute_dynamics(self,
                         t: Time,
                         states: States,
                         algebraics: Algebraics,
                         inputs: Inputs,
                         parameters: Parameters):
        return [0] * self.signature.states

    def compute_state_transition(self,
                                 t, states, algebraics, inputs, parameters):
        raise NotImplementedError



class Composite(ComponentBase):  # noqa
    """Block that consists of a sub-blocks and connections.

    Instances of `sysopt.Block` can be added to a composite block.
    Wires between ports can then be specified to enforce flow between
    different sub-blocks.

    Wires can also define 'forwarding' relationships, for example
    between inputs from the composite block, into inputs on sub-blocks.

    This allows models to be constructed hierarchically, and provides a
    means for encapsulation.

    Args:
        components: A list of components
        wires: A list of connections between component ports.

    """

    def __init__(self,
                 components: Optional[Iterable[Block]] = None,
                 wires: Optional[Iterable[Connection]] = None,
                 name=None
                 ):
        super().__init__(name)

        self._wires = ConnectionList(self)
        self._components = []
        self.components = components or []      # type: Iterable[Block]
        self.wires = wires or []                # type: Iterable[Connection]
        self._input_names = None
        self._output_names = None

    def declare_inputs(self, labels: Optional[List[str]] = None):
        self._input_names = labels.copy()
        self.inputs.size = len(labels)

    def declare_outputs(self, labels: List[str]):
        self._output_names = labels.copy()
        self.outputs.size = len(labels)

    @property
    def wires(self):
        return self._wires

    @wires.setter
    def wires(self, value):
        if isinstance(value, list):
            self._wires.clear()
            self.inputs.size = 0
            self.outputs.size = 0
            for pair in value:
                self._wires.append(pair)
        elif value is self._wires:
            return

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, values):
        for item in values:
            item.parent = self
            self._components.append(item)

    @property
    def parameters(self):
        return [
            p for sub_block in self.components for p in sub_block.parameters
        ]

    def find_by_type_and_name(self, var_type, var_name):
        for component in self.components:
            result = component.find_by_type_and_name(var_type, var_name)
            if result:
                return result

        return None

    def find_port_by_name(self, port_type, name):
        if port_type == 'outputs':
            try:
                return self._output_names.index(name)
            except ValueError as ex:
                raise InvalidPort(
                    name, 'is not a valid output port name for', self
                ) from ex
        elif port_type == 'inputs':
            try:
                return self._input_names.index(name)
            except ValueError as ex:
                raise InvalidPort(
                    name, 'is not a valid input port name for', self
                ) from ex
        raise ValueError(f'Invalid port type {port_type}')

    def check_wiring_or_raise(self):
        ext_inputs, ext_outputs, internal_inputs = _find_unconnected_io(self)

        if ext_inputs:
            raise DanglingInputError(
                self, {str(channel) for channel in ext_inputs}
            )

        if internal_inputs:
            raise UnconnectedInputError(
                str(self), {str(channel) for channel in internal_inputs}
            )

        if not self.outputs:
            raise InvalidComponentError(self, 'has no defined outputs')

        if ext_outputs:
            raise UnconnectedOutputError(self, ext_outputs)


def _find_unconnected_io(composite):
    external_inputs = set(composite.inputs)
    external_outputs = set(composite.outputs)
    internal_inputs = {
        channel for component in composite.components
        for channel in component.inputs
    }

    def src_filter(src, channel):
        if isinstance(src, Channel):
            return channel.port is not src.port or not (
                set(channel.indices).issubset(set(src.indices))
            )
        else:
            return channel.port is not src

    def dest_filter(dest, channel):
        if isinstance(dest, Channel):
            return channel.port is not dest.port or not (
                set(channel.indices).issubset(set(dest.indices))
        )
        else:
            return channel.port is not dest
    for source, destin in composite.wires:

        f_1 = partial(src_filter, source)
        f_2 = partial(dest_filter, destin)
        external_inputs = set(filter(f_1, external_inputs))
        internal_inputs = set(filter(f_2, internal_inputs))
        external_outputs = set(filter(f_2, external_outputs))

    return external_inputs, external_outputs, internal_inputs


