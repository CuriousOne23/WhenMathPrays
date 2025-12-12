"""
UI Builder for interactive editor.

Handles widget creation, layout setup, and signal connections.
Separates UI construction from application logic.
"""

from typing import Dict, Optional
from PySide6.QtWidgets import (
    QDockWidget, QLabel, QFrame, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

from tools.editor.views.primitive_panel_pyqtgraph import PrimitivePanelPyQtGraph
from tools.editor.views.trajectory_panel_pyqtgraph import TrajectoryPanelPyQtGraph
from tools.editor.widgets import (
    GammaSelf0Editor, InsertionOptionsWidget, PerspectiveSwitcher,
    NameEditor, NoteEditor
)


class UIBuilder:
    """
    Builds UI components for interactive editor.
    
    Responsibilities:
    - Create panels (primitive, trajectory)
    - Create editor widgets (gamma_self_0, insertions, perspective switcher, etc.)
    - Create dock widgets with proper configuration
    - Set up layout and sizing
    - Create gauges (readouts)
    
    Does NOT:
    - Connect signals (done by Application)
    - Access model/controller (just builds UI)
    - Handle events or business logic
    """
    
    def __init__(self, main_window):
        """
        Initialize UI builder.
        
        Args:
            main_window: EditorMainWindow instance
        """
        self.window = main_window
        
        # Panels
        self.primitive_panel: Optional[PrimitivePanelPyQtGraph] = None
        self.trajectory_panel: Optional[TrajectoryPanelPyQtGraph] = None
        
        # Docks
        self.primitive_dock: Optional[QDockWidget] = None
        self.trajectory_dock: Optional[QDockWidget] = None
        self.controls_dock: Optional[QDockWidget] = None
        
        # Editor widgets
        self.gamma_self0_editor: Optional[GammaSelf0Editor] = None
        self.insertion_options: Optional[InsertionOptionsWidget] = None
        self.perspective_switcher: Optional[PerspectiveSwitcher] = None
        self.name_editor: Optional[NameEditor] = None
        self.note_editor: Optional[NoteEditor] = None
        
        # Gauges
        self.primitive_gauge: Optional[QLabel] = None
        self.gamma_self_gauge: Optional[QLabel] = None
    
    def build_panels(self):
        """Create primitive and trajectory panels."""
        self.primitive_panel = PrimitivePanelPyQtGraph()
        self.trajectory_panel = TrajectoryPanelPyQtGraph()
        
        return {
            'primitive_panel': self.primitive_panel,
            'trajectory_panel': self.trajectory_panel
        }
    
    def build_dock_widgets(self):
        """Create and configure dock widgets for panels."""
        if self.primitive_panel is None or self.trajectory_panel is None:
            raise ValueError("Must call build_panels() first")
        
        # Primitive dock
        self.primitive_dock = QDockWidget("Primitives", self.window)
        self.primitive_dock.setWidget(self.primitive_panel)
        self.primitive_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable | 
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.LeftDockWidgetArea, self.primitive_dock)
        
        # Trajectory dock
        self.trajectory_dock = QDockWidget("Trajectory", self.window)
        self.trajectory_dock.setWidget(self.trajectory_panel)
        self.trajectory_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable | 
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.trajectory_dock)
    
    def build_editor_widgets(self, initial_gamma_self_0: complex, initial_perspective: str, initial_name: str):
        """
        Create editor control widgets.
        
        Args:
            initial_gamma_self_0: Initial gamma_self_0 value
            initial_perspective: Initial perspective ("M1" or "M2")
            initial_name: Initial scenario name
        """
        # Gamma_self_0 editor
        self.gamma_self0_editor = GammaSelf0Editor(initial_gamma_self_0)
        
        # Insertion options
        self.insertion_options = InsertionOptionsWidget()
        
        # Perspective switcher
        self.perspective_switcher = PerspectiveSwitcher()
        
        # Name editor
        self.name_editor = NameEditor(initial_name)
        
        # Note editor
        self.note_editor = NoteEditor()
        
        # Set initial perspective
        if initial_perspective == "M2":
            self.perspective_switcher.set_perspective("M2")
        
        return {
            'gamma_self0_editor': self.gamma_self0_editor,
            'insertion_options': self.insertion_options,
            'perspective_switcher': self.perspective_switcher,
            'name_editor': self.name_editor,
            'note_editor': self.note_editor
        }
    
    def build_gauges(self):
        """Create readout gauge widgets."""
        # Primitive gauge
        primitive_gauge_frame = QFrame()
        primitive_gauge_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        primitive_gauge_layout = QVBoxLayout()
        primitive_gauge_label = QLabel("Primitive Readout")
        primitive_gauge_label.setAlignment(Qt.AlignCenter)
        primitive_gauge_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        self.primitive_gauge = QLabel("--")
        self.primitive_gauge.setAlignment(Qt.AlignCenter)
        self.primitive_gauge.setStyleSheet(
            'background-color: lightyellow; '
            'border: 1px solid black; '
            'border-radius: 5px; '
            'padding: 10px; '
            'font-size: 12pt; '
            'font-weight: bold;'
        )
        self.primitive_gauge.setMinimumHeight(60)
        primitive_gauge_layout.addWidget(primitive_gauge_label)
        primitive_gauge_layout.addWidget(self.primitive_gauge)
        primitive_gauge_frame.setLayout(primitive_gauge_layout)
        
        # Gamma_self gauge
        gamma_gauge_frame = QFrame()
        gamma_gauge_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        gamma_gauge_layout = QVBoxLayout()
        gamma_gauge_label = QLabel("γ_self Readout")
        gamma_gauge_label.setAlignment(Qt.AlignCenter)
        gamma_gauge_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        self.gamma_self_gauge = QLabel("--")
        self.gamma_self_gauge.setAlignment(Qt.AlignCenter)
        self.gamma_self_gauge.setStyleSheet(
            'background-color: lightblue; '
            'border: 1px solid black; '
            'border-radius: 5px; '
            'padding: 10px; '
            'font-size: 11pt; '
            'font-weight: bold;'
        )
        self.gamma_self_gauge.setMinimumHeight(60)
        gamma_gauge_layout.addWidget(gamma_gauge_label)
        gamma_gauge_layout.addWidget(self.gamma_self_gauge)
        gamma_gauge_frame.setLayout(gamma_gauge_layout)
        
        return {
            'primitive_gauge': self.primitive_gauge,
            'gamma_gauge': self.gamma_self_gauge,
            'primitive_gauge_frame': primitive_gauge_frame,
            'gamma_gauge_frame': gamma_gauge_frame
        }
    
    def build_controls_dock(self):
        """Create controls dock widget with all editor widgets and gauges."""
        if (self.gamma_self0_editor is None or self.insertion_options is None or
            self.perspective_switcher is None or self.name_editor is None or
            self.note_editor is None):
            raise ValueError("Must call build_editor_widgets() first")
        
        # Build gauges
        gauges = self.build_gauges()
        primitive_gauge_frame = gauges['primitive_gauge_frame']
        gamma_gauge_frame = gauges['gamma_gauge_frame']
        
        # Combine widgets in a container
        dock_container = QWidget()
        dock_layout = QVBoxLayout()
        dock_layout.addWidget(self.perspective_switcher)
        dock_layout.addWidget(self.name_editor)
        dock_layout.addWidget(self.note_editor)
        dock_layout.addWidget(self.gamma_self0_editor)
        dock_layout.addWidget(primitive_gauge_frame)
        dock_layout.addWidget(gamma_gauge_frame)
        dock_layout.addWidget(self.insertion_options)
        dock_layout.addStretch()
        dock_container.setLayout(dock_layout)
        
        # Add controls as dock widget
        self.controls_dock = QDockWidget("Editor Controls", self.window)
        self.controls_dock.setWidget(dock_container)
        self.controls_dock.setFeatures(
            QDockWidget.DockWidgetMovable | 
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetClosable
        )
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.controls_dock)
    
    def configure_layout(self):
        """Configure dock layout and sizing."""
        if (self.primitive_dock is None or self.trajectory_dock is None or
            self.controls_dock is None):
            raise ValueError("Must create all docks first")
        
        # Split the right area horizontally: Trajectory on left, Controls on right
        # This creates the 3-column layout: [Primitives | Trajectory | Controls]
        self.window.splitDockWidget(self.trajectory_dock, self.controls_dock, Qt.Horizontal)
        
        # Setup View menu for dock widget visibility
        self.window._setup_view_menu({
            'Primitives': self.primitive_dock,
            'Trajectory': self.trajectory_dock,
            'Controls': self.controls_dock
        })
        
        # Configure initial layout widths
        # First set the main left/right split (Primitives vs rest)
        self.window.resizeDocks(
            [self.primitive_dock, self.trajectory_dock],
            [500, 1000],  # Primitives=500px, Right side (Trajectory+Controls)=1000px
            Qt.Horizontal
        )
        
        # Then set the Trajectory/Controls split within the right area
        self.window.resizeDocks(
            [self.trajectory_dock, self.controls_dock],
            [700, 300],  # Trajectory=700px, Controls=300px
            Qt.Horizontal
        )
    
    def get_dock_widgets(self) -> Dict[str, QDockWidget]:
        """Get dictionary of all dock widgets."""
        return {
            'Primitives': self.primitive_dock,
            'Trajectory': self.trajectory_dock,
            'Controls': self.controls_dock
        }
