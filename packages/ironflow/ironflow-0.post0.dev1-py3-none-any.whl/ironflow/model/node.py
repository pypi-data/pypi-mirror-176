# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.
from __future__ import annotations

from ryvencore import Node as NodeCore
from ryvencore.Base import Event

from ironflow.gui.canvas_widgets import NodeWidget


class Node(NodeCore):
    """
    A parent class for all ironflow nodes. Apart from a small quality-of-life difference where outputs are
    accessible in the same way as inputs (i.e. with a method `output(i)`), the main change here is the `before_update`
    and `after_update` events. Callbacks to happen before and after the update can be added to (removed from) these with
    the `connect` (`disconnect`) methods on the event. Such callbacks need to take the node itself as the first
    argument, and the integer specifying which input channel is being updated as the second argument.

    Also provides a "representation" that gets used in the GUI to give a more detailed look at node data, which defaults
    to showing output channel values.

    Children should specify a title and some combination of initial input, output, and what to do when updated, e.g.:

    >>> class My_Node(Node):
    >>> title = "MyUserNode"
    >>> init_inputs = [
    >>>     NodeInputBP(dtype=dtypes.Integer(default=1), label="foo")
    >>> ]
    >>> init_outputs = [
    >>>    NodeOutputBP(label="bar")
    >>> ]
    >>> color = 'cyan'
    >>>
    >>> def update_event(self, inp=-1):
    >>>     self.set_output_val(0, self.input(0) + 42)

    Note:
        When registering nodes from a module or .py file, only children of this class with names ending in `_Node` will
        get registered.
    """

    main_widget_class = NodeWidget

    color = "#ff69b4"  # Add an abrasive default color -- won't crash if you forget to add one, but pops out a bit

    def __init__(self, params):
        super().__init__(params)

        self.before_update = Event(self, int)
        self.after_update = Event(self, int)
        self.actions = (
            dict()
        )  # Resolves Todo from ryven.NENV, moving it to our node class instead of ryvencore

        self.representation_updated = False
        self.after_update.connect(self._representation_update)

    def place_event(self):
        # place_event() is executed *before* the connections are built
        super().place_event()
        for inp in self.inputs:
            if (
                inp.val is None
            ):  # Don't over-write data from loaded sessions with defaults
                if inp.dtype is not None:
                    inp.update(inp.dtype.default)
                elif "val" in inp.add_data.keys():
                    inp.update(inp.add_data["val"])

    def update(self, inp=-1):
        self.before_update.emit(self, inp)
        super().update(inp=inp)
        self.after_update.emit(self, inp)

    def output(self, i):
        return self.outputs[i].val

    @staticmethod
    def _representation_update(self, inp):
        self.representation_updated = True

    @property
    def representations(self) -> dict:
        return {
            o.label_str if o.label_str != "" else f"output{i}": o.val
            for i, o in enumerate(self.outputs)
            if o.type_ == "data"
        }


class PlaceholderWidgetsContainer:
    """
    An object that just returns None for all accessed attributes so widgets.MyWidget in the non-ironflow nodes files
    just returns None.
    """

    def __getattr__(self, item):
        return None
