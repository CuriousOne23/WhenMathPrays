
from pyqtgraph import TextItem
from tools.editor.state_viewer import StateViewer

class TrajectoryLabelManager:
    """
    Manages trajectory label TextItems for a single plot/primitive.
    Allows creation, removal, show/hide, and state inspection of labels.
    """
    def __init__(self, plot):
        self.plot = plot
        self.labels = {}  # key: (event_idx, primitive) or other unique id, value: TextItem

    def add_label(self, key, text, x, y, color, border_pen, fill_brush):
        if key in self.labels:
            self.remove_label(key)
        label = TextItem(
            text=text,
            color=color,
            anchor=(0, 1),
            border=border_pen,
            fill=fill_brush
        )
        label.setPos(x, y)
        self.plot.addItem(label)
        self.labels[key] = label
        StateViewer.record(
            operation="add_label",
            entity=(key,),
            changes={"visible": (False, True), "text": (None, text)},
        )
        return label

    def remove_label(self, key):
        label = self.labels.pop(key, None)
        if label:
            self.plot.removeItem(label)
            StateViewer.record(
                operation="remove_label",
                entity=(key,),
                changes={"visible": (True, False), "text": (label.toPlainText(), None)},
            )

    def show_label(self, key):
        if key in self.labels:
            label = self.labels[key]
            before = label.isVisible()
            label.setVisible(True)
            StateViewer.record(
                operation="show_label",
                entity=(key,),
                changes={"visible": (before, True)},
            )

    def hide_label(self, key):
        if key in self.labels:
            label = self.labels[key]
            before = label.isVisible()
            label.setVisible(False)
            StateViewer.record(
                operation="hide_label",
                entity=(key,),
                changes={"visible": (before, False)},
            )

    def get_label(self, key):
        return self.labels.get(key)

    def all_labels(self):
        return self.labels.copy()

    def clear(self):
        for key, label in list(self.labels.items()):
            self.plot.removeItem(label)
            StateViewer.record(
                operation="clear_label",
                entity=(key,),
                changes={"visible": (label.isVisible(), False), "text": (label.toPlainText(), None)},
            )
        self.labels.clear()
