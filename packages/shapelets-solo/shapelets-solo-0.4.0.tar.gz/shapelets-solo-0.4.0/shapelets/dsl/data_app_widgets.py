# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import base64
import uuid
from enum import Enum
from io import BytesIO
from matplotlib.figure import Figure
from os.path import exists as file_exists
from pathlib import Path
from typing import TypeVar, List, Union

from shapelets.dsl.argument_types import (
    ArgumentTypeEnum,
    ArgumentType,
    ArgumentValue,
    SupportedTypes,
    TypeNotSupported
)
from shapelets.dsl.data_app_context import (
    TemporalContext,
    FilteringContext
)
from shapelets.dsl.data_app_events import (
    DSLAlgoReturnType,
    EventProducer
)
from shapelets.dsl.node import (
    Node,
    NodeType
)
from shapelets.model import (
    Collection,
    MetadataType,
    NDArray,
    Sequence,
    View
)


class AttributeNames(Enum):
    ALLOW_MULTI_SELECTION = "allowMultiSelection"
    BINS = "bins"
    CATEGORIES = "categories"
    COLLECTION_ID = "collectionId"
    COLOR = "color"
    CUMULATIVE = "cumulative"
    DATA = "data"
    DATE = "date"
    DEFAULT = "default"
    DISABLED = "disabled"
    DRAGGABLE = "draggable"
    EVENTS = "events"
    EVERY = "every"
    GROUPS = "groups"
    FORMAT = "format"
    HIDDEN = "hidden"
    ID = "id"
    INDEX_BY = "indexBy"
    LABEL = "label"
    LABEL_BY = "labelBy"
    MAX = "max"
    MAX_DATE = "maxDate"
    METADATA_FIELDS = "metadataFields"
    MIN = "min"
    MIN_DATE = "minDate"
    NAME = "name"
    NDARRAY = "NDArray"
    OPERATION = "widget-initializer"
    OPTIONS = "options"
    PLACEHOLDER = "placeholder"
    PLOTS = "plots"
    POINTS = "points"
    PROPERTIES = "properties"
    RANGE = "range"
    REF = "$ref"
    RESIZABLE = "resizable"
    SEQUENCE = "sequence"
    SEQUENCE_ID = "sequenceId"
    SIZE = "size"
    START_DELAY = "startDelay"
    STEP = "step"
    TEXT = "text"
    TIMES = "times"
    TITLE = "title"
    TREND_LINE = "trendLine"
    TYPE = "type"
    TYPE_NOT_SUPPORTED = "only supports int/float types"
    VALUE = "value"
    VALUE_BY = "valueBy"
    VALUES = "values"
    VIEWS = "views"
    WIDGET = "widget"
    WIDGET_REF = "widgetRef"
    X = "x"
    X_AXIS = "xAxis"
    Y_AXIS = "yAxis"


def unique_id_str() -> str:
    return str(uuid.uuid1())


def unique_id_int() -> int:
    return uuid.uuid1().int


class Widget:
    """
    Units defined in Layout
    """

    def __init__(self,
                 widget_type: str,
                 widget_name: str = None,
                 widget_id: str = None,
                 draggable: bool = False,
                 resizable: bool = False,
                 # these are the optional properties:
                 placeholder: str = None,
                 disabled: bool = None,
                 parent_data_app: object = None) -> object:
        # parent_data_app is a reference to the DataApp used as a factory
        # for this widget
        self.parent_data_app = parent_data_app
        self.widget_id = widget_id if widget_id else unique_id_str()
        self.widget_name = widget_name if widget_name else self.widget_id
        self.widget_type = widget_type
        self.placeholder = placeholder
        self.disabled = disabled
        self.draggable = draggable
        self.resizable = resizable

    def to_dict_widget(self):
        properties = {}
        if self.placeholder is not None:
            properties[AttributeNames.PLACEHOLDER.value] = self.placeholder
        widget_dict = {
            AttributeNames.ID.value: self.widget_id,
            AttributeNames.NAME.value: self.widget_name,
            AttributeNames.TYPE.value: self.widget_type,
            AttributeNames.DRAGGABLE.value: self.draggable,
            AttributeNames.RESIZABLE.value: self.resizable,
            AttributeNames.DISABLED.value: False if self.disabled is None else self.disabled,
            AttributeNames.PROPERTIES.value: properties
        }
        return widget_dict


class WidgetNode(Widget, Node):
    OPERATION = AttributeNames.OPERATION.value

    def __init__(self,
                 widget_type: str,
                 widget_name: str,
                 value_type: ArgumentType,
                 value: SupportedTypes,
                 **additional):
        Widget.__init__(self, widget_type, widget_name, **additional)
        Node.__init__(self, WidgetNode.OPERATION, node_type=NodeType.WidgetNode)
        self.value_type = value_type
        self.value = ArgumentValue(value_type, value)

    def __hash__(self):
        return hash((Node.__hash__(self), Widget.__hash__(self)))

    def __eq__(self, other):
        return (isinstance(other, WidgetNode) and
                Node.__eq__(self, other) and
                Widget.__eq__(self, other))

    def __repr__(self):
        s_repr = Node.__repr__(self).replace('Node{id:', 'WidgetNode{id:')
        s_repr += f".{AttributeNames.VALUE.value}: {self.value.to_dict()}"
        return s_repr


class Number(WidgetNode):
    def __init__(self,
                 name: str = None,
                 default_value: TypeVar('N', int, float) = None,
                 value_type: type = float,
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         Number._argument_type(default_value, value_type),
                         default_value,
                         **additional)

    def to_dict_widget(self):
        number_dict = super().to_dict_widget()
        number_dict[AttributeNames.PROPERTIES.value].update(self._argument_value_to_dict())
        return number_dict

    @staticmethod
    def _argument_type(default_value: TypeVar('N', int, float) = None,
                       default_type: type = None) -> ArgumentType:
        if not default_type:
            if not default_value:
                argument_type = ArgumentTypeEnum.DOUBLE
            else:
                if isinstance(default_value, float):
                    argument_type = ArgumentTypeEnum.DOUBLE
                elif isinstance(default_value, int):
                    argument_type = ArgumentTypeEnum.INT
                else:
                    raise TypeNotSupported(AttributeNames.TYPE_NOT_SUPPORTED.value)
        else:
            if default_type is float:
                argument_type = ArgumentTypeEnum.DOUBLE
            elif default_type is int:
                argument_type = ArgumentTypeEnum.INT
            else:
                raise TypeNotSupported(AttributeNames.TYPE_NOT_SUPPORTED.value)
        return ArgumentType(argument_type)

    def _argument_value_to_dict(self) -> dict:
        value_dict = self.value.to_dict()
        keys = list(value_dict.keys())
        del keys[keys.index(ArgumentValue.TYPE_KEY)]
        key = keys[0]
        value = value_dict[key]
        del value_dict[key]
        value_dict[ArgumentValue.VALUE_KEY] = value
        return value_dict


class Text(WidgetNode):

    def __init__(self, title: TypeVar('T', str, Node) = None, text: TypeVar('T', str, Node) = None, **additional):

        super().__init__(self.__class__.__name__, "Text", ArgumentType(ArgumentTypeEnum.STRING), "", **additional)
        self.title = title
        self.text = text

    def to_dict_widget(self):
        text_dict = super().to_dict_widget()

        if self.title is not None:
            if isinstance(self.title, str):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            if isinstance(self.title, Node):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: {
                        AttributeNames.REF.value: f"{self.title.node_id}:{self.title.active_output}"
                    }
                })

        if self.text is not None:
            if isinstance(self.text, str):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT.value: self.text
                })
            if isinstance(self.text, Node):
                text_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TEXT.value: {
                        AttributeNames.REF.value: f"{self.text.node_id}:{self.text.active_output}"
                    }
                })

        return text_dict


class Date(WidgetNode):

    def __init__(self, title: TypeVar('T', str, Node) = None, date: TypeVar('T', float, Node) = None,
                 min_date: TypeVar('T', float, Node) = None, max_date: TypeVar('T', float, Node) = None, **additional):

        super().__init__(self.__class__.__name__, "Date", ArgumentType(ArgumentTypeEnum.FLOAT), 0, **additional)
        self.title = title
        self.date = date
        self.min_date = min_date
        self.max_date = max_date

    def to_dict_widget(self):
        date_dict = super().to_dict_widget()

        if self.title is not None:
            if isinstance(self.title, str):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            if isinstance(self.title, Node):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: {
                        AttributeNames.REF.value: f"{self.title.node_id}:{self.title.active_output}"
                    }
                })

        if self.date is not None:
            if isinstance(self.date, float) or isinstance(self.date, int):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DATE.value: self.date
                })
            if isinstance(self.date, Node):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DATE.value: {
                        AttributeNames.REF.value: f"{self.date.node_id}:{self.date.active_output}"
                    }
                })

        if self.min_date is not None:
            if isinstance(self.min_date, float) or isinstance(self.min_date, int):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN_DATE.value: self.min_date
                })
            if isinstance(self.min_date, Node):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MIN_DATE.value: {
                        AttributeNames.REF.value: f"{self.min_date.node_id}:{self.min_date.active_output}"
                    }
                })

        if self.max_date is not None:
            if isinstance(self.max_date, float) or isinstance(self.max_date, int):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX_DATE.value: self.max_date
                })
            if isinstance(self.max_date, Node):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.MAX_DATE.value: {
                        AttributeNames.REF.value: f"{self.max_date.node_id}:{self.max_date.active_output}"
                    }
                })

        return date_dict


class Slider(WidgetNode):
    def __init__(self,
                 min_value,
                 max_value,
                 step,
                 default_value: TypeVar('N', int, float) = None,
                 value_type: type = float,
                 in_range: bool = False,
                 name: str = None,
                 title: str = None,
                 formatter: str = "number",
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         Number._argument_type(default_value, value_type),
                         default_value,
                         **additional)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.title = title
        self.in_range = in_range
        self.formatter = formatter

    def to_dict_widget(self):
        slider_dict = super().to_dict_widget()
        slider_dict[AttributeNames.PROPERTIES.value].update(self._argument_value_to_dict())
        slider_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.MIN.value: self.min_value,
            AttributeNames.MAX.value: self.max_value,
            AttributeNames.STEP.value: self.step,
            AttributeNames.TITLE.value: self.title,
            AttributeNames.RANGE.value: self.in_range,
            AttributeNames.FORMAT.value: self.formatter
        })
        return slider_dict

    @staticmethod
    def _argument_type(default_value: TypeVar('N', int, float) = None,
                       default_type: type = None) -> ArgumentType:
        if not default_type:
            if not default_value:
                argument_type = ArgumentTypeEnum.DOUBLE
            else:
                if isinstance(default_value, float):
                    argument_type = ArgumentTypeEnum.DOUBLE
                elif isinstance(default_value, int):
                    argument_type = ArgumentTypeEnum.INT
                else:
                    raise TypeNotSupported("only supports int/float types")
        else:
            if default_type is float:
                argument_type = ArgumentTypeEnum.DOUBLE
            elif default_type is int:
                argument_type = ArgumentTypeEnum.INT
            else:
                raise TypeNotSupported("only supports int/float types")
        return ArgumentType(argument_type)

    def _argument_value_to_dict(self) -> dict:
        value_dict = self.value.to_dict()
        keys = list(value_dict.keys())
        del keys[keys.index(ArgumentValue.TYPE_KEY)]
        key = keys[0]
        value = value_dict[key]
        del value_dict[key]
        value_dict[ArgumentValue.VALUE_KEY] = value
        return value_dict

    @staticmethod
    def _argument_type(default_value: TypeVar('N', int, float) = None,
                       default_type: type = None) -> ArgumentType:
        if not default_type:
            if not default_value:
                argument_type = ArgumentTypeEnum.DOUBLE
            else:
                if isinstance(default_value, float):
                    argument_type = ArgumentTypeEnum.DOUBLE
                elif isinstance(default_value, int):
                    argument_type = ArgumentTypeEnum.INT
                else:
                    raise TypeNotSupported("only supports int/float types")
        else:
            if default_type is float:
                argument_type = ArgumentTypeEnum.DOUBLE
            elif default_type is int:
                argument_type = ArgumentTypeEnum.INT
            else:
                raise TypeNotSupported("only supports int/float types")
        return ArgumentType(argument_type)

    def _argument_value_to_dict(self) -> dict:
        value_dict = self.value.to_dict()
        keys = list(value_dict.keys())
        del keys[keys.index(ArgumentValue.TYPE_KEY)]
        key = keys[0]
        value = value_dict[key]
        del value_dict[key]
        value_dict[ArgumentValue.VALUE_KEY] = value
        return value_dict


class Button(Widget, EventProducer):
    def __init__(self,
                 widget_name: str = None,
                 text_button: str = "",
                 **additional):
        Widget.__init__(self, self.__class__.__name__, widget_name, **additional)
        EventProducer.__init__(self)
        self.text = text_button

    def on_click(self, algorithm: DSLAlgoReturnType):
        return self._link_event("click", self.parent_data_app, algorithm)

    def to_dict_widget(self):
        button_dict = super().to_dict_widget()
        button_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.TEXT.value: self.text,
            AttributeNames.EVENTS.value: [event.to_dict() for event in self.events]
        })
        return button_dict


class Timer(Widget, EventProducer):
    def __init__(self,
                 title: str, every: int, start_delay: int = None, times: int = None, hidden: bool = False,
                 **additional):
        Widget.__init__(self, self.__class__.__name__, "Timer", **additional)
        EventProducer.__init__(self)
        self.title = title
        self.every = every
        self.start_delay = start_delay
        self.times = times
        self.hidden = hidden

    def run(self, algorithm: DSLAlgoReturnType):
        return self._link_event("timer", self.parent_data_app, algorithm)

    def to_dict_widget(self):
        timer_dict = super().to_dict_widget()

        if self.start_delay is not None:
            timer_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.START_DELAY.value: self.start_delay
            })

        if self.times is not None:
            timer_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TIMES.value: self.times
            })

        timer_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.TITLE.value: self.title,
            AttributeNames.EVERY.value: self.every,
            AttributeNames.HIDDEN.value: self.hidden,
            AttributeNames.EVENTS.value: [event.to_dict() for event in self.events]
        })
        return timer_dict


class SequenceSelector(WidgetNode):
    def __init__(self,
                 collection: Collection = None,
                 sequences: List[Sequence] = None,
                 default_sequence: Sequence = None,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         ArgumentType(ArgumentTypeEnum.SEQUENCE),
                         default_sequence,
                         **additional)
        self.collection = collection
        self.sequences = sequences
        self.title = title
        self.default_sequence = default_sequence

    def to_dict_widget(self):
        sequence_selector_dict = super().to_dict_widget()
        if self.collection is not None:
            sequence_selector_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.COLLECTION_ID.value: self.collection.collection_id}
            )
        if self.sequences is not None:
            sequences = [seq.sequence_id for seq in self.sequences]
            sequence_selector_dict[AttributeNames.PROPERTIES.value].update({
                f"{AttributeNames.SEQUENCE_ID.value}s": sequences
            })
        if self.title is not None:
            sequence_selector_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: self.title}
            )
        if self.default_sequence:
            sequence_selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DEFAULT.value: self.default_sequence.sequence_id
            })
        return sequence_selector_dict


class LineChart(Widget):
    def __init__(self,
                 title: str = None,
                 sequence: TypeVar('T', Sequence, SequenceSelector, Node) = None,
                 x_axis: TypeVar('T', NDArray, Node) = None,
                 y_axis: TypeVar('T', NDArray, Node) = None,
                 views: TypeVar('T', List[View], Node) = None,
                 temporal_context: TemporalContext = None,
                 filtering_context: FilteringContext = None,
                 **additional):
        self.title = title
        self.sequence = sequence
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.views = views
        self.temporal_context = temporal_context
        self.filtering_context = filtering_context
        self._plots = list()

        if self.sequence and (self.y_axis or self.x_axis):
            raise Exception("sequence and axis properties are incompatible")

        if self.temporal_context and (self.y_axis or self.x_axis):
            raise Exception("temporal contexts cannot be used with axis properties")

        if self.filtering_context and (self.y_axis or self.x_axis):
            raise Exception("filtering contexts cannot be used with axis properties")

        widget_type = "LineChart"
        if self.sequence:
            widget_type = f"{self.__class__.__name__}:{AttributeNames.SEQUENCE.value.capitalize()}"
        if self.y_axis:
            widget_type = f"{self.__class__.__name__}:{AttributeNames.NDARRAY.value}"
        super().__init__(widget_type, "LineChart", **additional)
        temporal_context_id = None
        if self.temporal_context:
            temporal_context_id = self.temporal_context.context_id
            self.temporal_context.widgets.append(self.widget_id)
        filtering_context_id = None
        if self.filtering_context:
            filtering_context_id = filtering_context.context_id
            filtering_context.output_widgets.append(self.widget_id)
        self.temporal_context = temporal_context_id
        self.filtering_context = filtering_context_id

    def plot(self, y_axis: Union[NDArray, Node], x_axis: Union[NDArray, Node] = None, label: Union[str, Node] = None):
        plot_dict = dict()
        if isinstance(y_axis, NDArray):
            plot_dict.update({
                AttributeNames.Y_AXIS.value: y_axis.nd_array_id
            })
        if isinstance(y_axis, Node):
            plot_dict.update({
                AttributeNames.Y_AXIS.value: {
                    AttributeNames.REF.value: f"{y_axis.node_id}:{y_axis.active_output}"
                }
            })

        if x_axis is not None:
            if isinstance(x_axis, NDArray):
                plot_dict.update({
                    AttributeNames.X_AXIS.value: x_axis.nd_array_id
                })
            if isinstance(x_axis, Node):
                plot_dict.update({
                    AttributeNames.X_AXIS.value: {
                        AttributeNames.REF.value: f"{x_axis.node_id}:{x_axis.active_output}"
                    }
                })

        if label is not None:
            if isinstance(label, str):
                plot_dict.update({
                    AttributeNames.LABEL.value: label
                })
            if isinstance(label, Node):
                plot_dict.update({
                    AttributeNames.LABEL.value: {
                        AttributeNames.REF.value: f"{label.node_id}:{label.active_output}"
                    }
                })

        self._plots.append(plot_dict)

    def to_dict_widget(self):
        line_chart_dict = super().to_dict_widget()
        if self.title is not None:
            if isinstance(self.title, str):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            if isinstance(self.title, Node):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: {
                        AttributeNames.REF.value: f"{self.title.node_id}:{self.title.active_output}"
                    }
                })
        if self.sequence:
            if isinstance(self.sequence, SequenceSelector):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.SEQUENCE_ID.value: {
                        AttributeNames.WIDGET_REF.value: self.sequence.widget_id
                    },
                })
            elif isinstance(self.sequence, Node):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.SEQUENCE_ID.value: {
                        AttributeNames.REF.value: f"{self.sequence.node_id}:{self.sequence.active_output}"
                    },
                })
            else:
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.SEQUENCE_ID.value: self.sequence.sequence_id,
                })
        if self.x_axis:
            if isinstance(self.x_axis, Node):
                x_axis_value = {
                    AttributeNames.REF.value: f"{self.x_axis.node_id}:{self.x_axis.active_output}"
                }
            if isinstance(self.x_axis, NDArray):
                x_axis_value = self.x_axis.nd_array_id

            if x_axis_value:
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.X_AXIS.value: x_axis_value
                })
        if self.y_axis:
            if isinstance(self.y_axis, Node):
                y_axis_value = {
                    AttributeNames.REF.value: f"{self.y_axis.node_id}:{self.y_axis.active_output}"
                }
            if isinstance(self.y_axis, NDArray):
                y_axis_value = self.y_axis.nd_array_id

            if y_axis_value:
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.Y_AXIS.value: y_axis_value
                })
        if self.views:
            if isinstance(self.views, Node):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: {
                        AttributeNames.REF.value: f"{self.views.node_id}:{self.views.active_output}"
                    }
                })
            if isinstance(self.views, List) and all(isinstance(view, View) for view in self.views):
                view_list = [view.to_dict() for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })

        if len(self._plots) > 0:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLOTS.value: self._plots
            })
        return line_chart_dict


class MetadataField(Widget):
    def __init__(self,
                 field_name: str,
                 field_type: MetadataType,
                 collection: Collection,
                 name: str = None,
                 **additional):
        super().__init__(widget_type=self.__class__.__name__,
                         widget_name=name,
                         **additional)
        self.field_type = field_type
        self.collection = collection
        self.field_name = field_name

    def to_dict_widget(self):
        metadata_field_dict = super().to_dict_widget()
        metadata_field_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.COLLECTION_ID.value: self.collection.collection_id,
            AttributeNames.NAME.value: self.field_name,
            AttributeNames.TYPE.value: self.frontend_type,
            AttributeNames.COLLECTION_ID.value: self.collection.collection_id
        })
        return metadata_field_dict

    @property
    def frontend_type(self):
        value = self.field_type.value
        return value[0] + value[1:].lower()


class MetadataFilter(Widget):
    def __init__(self,
                 metadata_elements: List[MetadataField],
                 name: str = None,
                 title: str = None,
                 filtering_context: List[FilteringContext] = None,
                 **additional):
        super().__init__(widget_type=self.__class__.__name__,
                         widget_name=name,
                         **additional)
        metadata_fields = []
        for metadata in metadata_elements:
            metadata_fields.append([metadata.field_name, metadata.frontend_type])
        self.metadata_fields = metadata_fields
        self.title = title
        filtering_context_id = []
        if filtering_context:
            for filtering in filtering_context:
                filtering_context_id.append(filtering.context_id)
                filtering.input_filters.append(self.widget_id)
        self.filtering_context = filtering_context_id

    def to_dict_widget(self):
        metadata_filter_dict = super().to_dict_widget()
        metadata_filter_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.METADATA_FIELDS.value: self.metadata_fields,
            AttributeNames.TITLE.value: self.title,
        })
        return metadata_filter_dict


class MultiSequenceSelector(WidgetNode):
    def __init__(self,
                 collection: Collection = None,
                 sequences: List[Sequence] = None,
                 default_sequence: List[Sequence] = None,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         ArgumentType(ArgumentTypeEnum.LIST, ArgumentTypeEnum.SEQUENCE),
                         default_sequence if default_sequence else list(),
                         **additional)
        self.collection = collection
        self.sequences = sequences
        self.title = title
        self.default_sequence = default_sequence if default_sequence is not None else []

    def to_dict_widget(self):
        multi_sequence_selector_dict = super().to_dict_widget()
        if self.collection is not None:
            multi_sequence_selector_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.COLLECTION_ID.value: f"{self.collection.collection_id}"}
            )
        if self.sequences is not None:
            sequences = [seq.sequence_id for seq in self.sequences]
            multi_sequence_selector_dict[AttributeNames.PROPERTIES.value].update({
                f"{AttributeNames.SEQUENCE_ID.value}s": sequences
            })
        if self.title is not None:
            multi_sequence_selector_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )
        if self.default_sequence:
            multi_sequence_selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DEFAULT.value: [sequence.sequence_id for sequence in self.default_sequence]
            })
        return multi_sequence_selector_dict


class Selector(WidgetNode):

    def __init__(self, options: List, title: str = None, index_by: str = None, label_by: str = None,
                 value_by: str = None,
                 value: TypeVar('N', int, float, str, any) = None,
                 **additional):
        argument_type, default_value = Selector._argument_type(options, value_by)
        super().__init__(self.__class__.__name__, "Selector", argument_type, default_value, **additional)
        self.title = title
        self.options = options
        self.index_by = index_by
        self.label_by = label_by
        self.value_by = value_by
        self.value = value
        self.argument_type = argument_type

        if isinstance(self.options, list) and all((isinstance(x, dict)) for x in self.options):
            if self.index_by is None:
                raise Exception("You must indicate the index_by property")
            if self.label_by is None:
                raise Exception("You must indicate the label_by property")
            if self.value_by is None:
                raise Exception("You must indicate the value_by property")

    def to_dict_widget(self):
        selector_dict = super().to_dict_widget()

        selector_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.TYPE.value: self.argument_type.types[0].__dict__["_value_"],
            AttributeNames.OPTIONS.value: self.options,
        })

        if self.title is not None:
            selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TITLE.value: self.title,
            })

        if self.index_by is not None:
            selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.INDEX_BY.value: self.index_by,
            })

        if self.label_by is not None:
            selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.LABEL_BY.value: self.label_by,
            })

        if self.value_by is not None:
            selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VALUE_BY.value: self.value_by,
            })

        if self.value is not None:
            selector_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VALUE.value: self.value,
            })

        return selector_dict

    @staticmethod
    def _argument_type(options: List, value_by: str) -> ArgumentType:
        if all(isinstance(x, str) for x in options):
            argument_type = ArgumentTypeEnum.STRING
            default_value = ""
        if all(isinstance(x, int) for x in options):
            argument_type = ArgumentTypeEnum.INT
            default_value = 0
        if all(isinstance(x, float) for x in options):
            argument_type = ArgumentTypeEnum.FLOAT
            default_value = 0
        if all(isinstance(x, dict) for x in options):
            return Selector._argument_type(options[0][value_by], value_by)
        return ArgumentType(argument_type), default_value


class Label(Widget):

    def __init__(self, text: TypeVar('T', str, int, float, Node), **additional):
        super().__init__(self.__class__.__name__, "Label", **additional)
        self.text = text

    def to_dict_widget(self):
        label_dict = super().to_dict_widget()
        text_value = None

        if isinstance(self.text, Node):
            text_value = {
                AttributeNames.REF.value: f"{self.text.node_id}:{self.text.active_output}"
            }
        if isinstance(self.text, str):
            text_value = self.text

        label_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.TEXT.value: text_value,
        })
        return label_dict


class Markdown(Label):

    def __init__(self, text: TypeVar('T', str, int, float, Node), **additional):
        super().__init__(text, **additional)


class BarChart(Widget):
    def __init__(self,
                 data: NDArray,
                 categories: NDArray = None,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__, name, **additional)
        if categories:
            self.categories = categories
        self.data = data
        self.title = title

    def to_dict_widget(self):
        bar_chart_dict = super().to_dict_widget()
        if hasattr(self, "categories"):
            categories_value = None
            if isinstance(self.categories, Node):
                categories_value = {
                    AttributeNames.REF.value: f"{self.categories.node_id}:{self.categories.active_output}"
                }
            if isinstance(self.categories, NDArray):
                categories_value = self.categories.nd_array_id

            bar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.CATEGORIES.value: categories_value
            })
        if hasattr(self, "data"):
            data_value = None
            if isinstance(self.data, Node):
                data_value = {
                    AttributeNames.REF.value: f"{self.data.node_id}:{self.data.active_output}"
                }
            if isinstance(self.data, NDArray):
                data_value = self.data.nd_array_id

            bar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: data_value
            })
        if self.title is not None:
            bar_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )
        return bar_chart_dict


class Histogram(Widget):
    def __init__(self, x: Union[List[int], List[float], NDArray, Node],
                 bins: Union[int, float, Node] = None,
                 cumulative: Union[bool, Node] = False, **additional):
        super().__init__(self.__class__.__name__, "Histogram", **additional)
        self._x = x
        self._bins = bins
        self._cumulative = cumulative

    def to_dict_widget(self):
        histogram_dict = super().to_dict_widget()

        if isinstance(self._x, List) and all([isinstance(item, int) or isinstance(item, float) for item in self._x]):
            histogram_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.X.value: self._x
            })
        if isinstance(self._x, NDArray):
            histogram_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.X.value: self._x.nd_array_id
            })
        if isinstance(self._x, Node):
            histogram_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.X.value: {
                    AttributeNames.REF.value: f"{self._x.node_id}:{self._x.active_output}"
                }
            })
        if self._bins is not None:
            if isinstance(self._bins, int) or isinstance(self._bins, float):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.BINS.value: self._bins
                })
            if isinstance(self._bins, List) and all(
                    [isinstance(item, int) or isinstance(item, float) for item in self._bins]):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.BINS.value: self._bins
                })
            if isinstance(self._bins, NDArray):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.BINS.value: self._bins.nd_array_id
                })
            if isinstance(self._bins, Node):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.BINS.value: {
                        AttributeNames.REF.value: f"{self._bins.node_id}:{self._bins.active_output}"
                    }
                })
            if isinstance(self._cumulative, bool):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.CUMULATIVE.value: self._cumulative
                })
            if isinstance(self._cumulative, Node):
                histogram_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.CUMULATIVE.value: {
                        AttributeNames.REF.value: f"{self._cumulative.node_id}:{self._cumulative.active_output}"
                    }
                })

        return histogram_dict


class ScatterPlot(Widget):
    def __init__(self,
                 x_axis: NDArray,
                 y_axis: NDArray,
                 size: NDArray = None,
                 color: NDArray = None,
                 categories: NDArray = None,
                 name: str = None,
                 title: str = None,
                 trend_line: bool = False,
                 **additional):
        super().__init__(self.__class__.__name__, name, **additional)
        if size:
            self.size = size
        if color:
            self.color = color
        if categories:
            self.categories = categories
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.title = title
        self.trend_line = trend_line

    def to_dict_widget(self):
        scatter_plot_dict = super().to_dict_widget()
        if hasattr(self, "size"):
            size_value = None
            if isinstance(self.size, Node):
                size_value = {
                    AttributeNames.REF.value: f"{self.size.node_id}:{self.size.active_output}"
                }
            if isinstance(self.size, NDArray):
                size_value = self.size.nd_array_id

            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.SIZE.value: size_value
            })
        if hasattr(self, "color"):
            color_value = None
            if isinstance(self.color, Node):
                color_value = {
                    AttributeNames.REF.value: f"{self.color.node_id}:{self.color.active_output}"
                }
            if isinstance(self.color, NDArray):
                color_value = self.color.nd_array_id

            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.COLOR.value: color_value
            })
        if self.title is not None:
            scatter_plot_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )

        if hasattr(self, "categories"):
            categories_value = None
            if isinstance(self.categories, Node):
                categories_value = {
                    AttributeNames.REF.value: f"{self.categories.node_id}:{self.categories.active_output}"
                }
            if isinstance(self.categories, NDArray):
                categories_value = self.categories.nd_array_id

            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.CATEGORIES.value: categories_value
            })

        if self.title is not None:
            if isinstance(self.title, str):
                scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            if isinstance(self.title, Node):
                scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: {
                        AttributeNames.REF.value: f"{self.title.node_id}:{self.title.active_output}"
                    }
                })

        if hasattr(self, "x_axis"):
            x_axis_value = None
            if isinstance(self.x_axis, Node):
                x_axis_value = {
                    AttributeNames.REF.value: f"{self.x_axis.node_id}:{self.x_axis.active_output}"
                }
            if isinstance(self.x_axis, NDArray):
                x_axis_value = self.x_axis.nd_array_id

            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.X_AXIS.value: x_axis_value
            })

        if hasattr(self, "y_axis"):
            y_axis_value = None
            if isinstance(self.y_axis, Node):
                y_axis_value = {
                    AttributeNames.REF.value: f"{self.y_axis.node_id}:{self.y_axis.active_output}"
                }
            if isinstance(self.y_axis, NDArray):
                y_axis_value = self.y_axis.nd_array_id

            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.Y_AXIS.value: y_axis_value
            })

        if hasattr(self, "trend_line"):
            scatter_plot_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TREND_LINE.value: self.trend_line
            })
        return scatter_plot_dict


class PieChart(Widget):
    def __init__(self,
                 data: NDArray,
                 categories: NDArray = None,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__, name, **additional)
        if categories:
            self.categories = categories
        self.data = data
        self.title = title

    def to_dict_widget(self):
        pie_chart_dict = super().to_dict_widget()
        if hasattr(self, "categories"):
            categories_value = None
            if isinstance(self.categories, Node):
                categories_value = {
                    AttributeNames.REF.value: f"{self.categories.node_id}:{self.categories.active_output}"
                }
            if isinstance(self.categories, NDArray):
                categories_value = self.categories.nd_array_id

            pie_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.CATEGORIES.value: categories_value
            })
        if hasattr(self, "data"):
            data_value = None
            if isinstance(self.data, Node):
                data_value = {
                    AttributeNames.REF.value: f"{self.data.node_id}:{self.data.active_output}"
                }
            if isinstance(self.data, NDArray):
                data_value = self.data.nd_array_id

            pie_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: data_value
            })

        if self.title is not None:
            pie_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )
        return pie_chart_dict


class PolarArea(WidgetNode):
    def __init__(self,
                 categories: NDArray,
                 data: NDArray,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         ArgumentType(ArgumentTypeEnum.ND_ARRAY),
                         data,
                         **additional)
        self.categories = categories
        self.data = data
        self.title = title

    def to_dict_widget(self):
        polar_chart_dict = super().to_dict_widget()
        if self.categories is not None:
            polar_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.CATEGORIES.value: f"{self.categories.nd_array_id}"}
            )
        if self.data:
            polar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: self.data.nd_array_id
            })
        if self.title is not None:
            polar_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )
        return polar_chart_dict


class RadarArea(WidgetNode):
    def __init__(self,
                 categories: NDArray,
                 data: NDArray,
                 groups: NDArray,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(self.__class__.__name__,
                         name,
                         ArgumentType(ArgumentTypeEnum.ND_ARRAY),
                         data,
                         **additional)
        self.categories = categories
        self.data = data
        self.groups = groups
        self.title = title

    def to_dict_widget(self):
        radar_chart_dict = super().to_dict_widget()
        if self.categories is not None:
            radar_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.CATEGORIES.value: f"{self.categories.nd_array_id}"}
            )
        if self.data:
            radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: self.data.nd_array_id
            })
        if self.groups:
            radar_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.GROUPS.value: self.groups.nd_array_id
            })
        if self.title is not None:
            radar_chart_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.TITLE.value: f"{self.title}"}
            )
        return radar_chart_dict


class DonutChart(PieChart):
    def __init__(self,
                 data: NDArray,
                 categories: NDArray = None,
                 name: str = None,
                 title: str = None,
                 **additional):
        super().__init__(data,
                         categories,
                         name,
                         title,
                         **additional)

        self.widget_type = self.__class__.__name__


class Image(Widget):
    def __init__(self,
                 fp: Union[str, bytes, Path, Figure, Node],
                 **additional):
        super().__init__(self.__class__.__name__, "Image", **additional)
        self._fp = fp
        self._additional = additional

    def to_dict_widget(self):
        image_dict = super().to_dict_widget()
        if isinstance(self._fp, str):
            # Reading image from local PATH
            if file_exists(self._fp):
                file = open(self._fp, 'rb')
                buffer = file.read()
                image_data = base64.b64encode(buffer).decode('utf-8')

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.DATA.value: f"{image_data}"}
                )
            else:
                raise FileNotFoundError(f"The file {self._fp} does not exist")
        elif isinstance(self._fp, Path):
            if self._fp.exists():
                file = open(self._fp, 'rb')
                buffer = file.read()
                image_data = base64.b64encode(buffer).decode('utf-8')

                image_dict[AttributeNames.PROPERTIES.value].update(
                    {AttributeNames.DATA.value: f"{image_data}"}
                )
            else:
                raise FileNotFoundError(f"The file {self._fp} does not exist")
        elif isinstance(self._fp, bytes):
            image_data = base64.b64encode(self._fp).decode("utf-8")

            image_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.DATA.value: f"{image_data}"}
            )
        elif isinstance(self._fp, Figure):
            bio = BytesIO()
            # TODO: pass information from self._additional to savefig function
            self._fp.savefig(bio, format="png", bbox_inches='tight')
            image_data = base64.b64encode(bio.getvalue()).decode("utf-8")

            image_dict[AttributeNames.PROPERTIES.value].update(
                {AttributeNames.DATA.value: f"{image_data}"}
            )
        elif isinstance(self._fp, Node):
            image_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.DATA.value: {
                    AttributeNames.REF.value: f"{self._fp.node_id}:{self._fp.active_output}"
                }
            })

        return image_dict
