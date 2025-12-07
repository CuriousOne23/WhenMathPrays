"""
Test to understand PyQtGraph coordinate system for click detection.
This will help us figure out the correct transformation for diagnostic markers.
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
import pyqtgraph as pg


class CoordinateTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtGraph Coordinate System Test")
        self.resize(800, 600)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Instructions
        info = QPushButton("Click anywhere on the plot. Check console for coordinates.")
        info.setEnabled(False)
        layout.addWidget(info)
        
        # Create a plot with known Y range
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        plot = self.plot_widget.getPlotItem()
        plot.setTitle("Click Test - Y range: -11 to 11")
        plot.setLabel('left', 'Y Value')
        plot.setLabel('bottom', 'X Value')
        plot.setYRange(-11, 11, padding=0)
        plot.setXRange(0, 60, padding=0)
        plot.showGrid(x=True, y=True, alpha=0.3)
        
        # Add reference markers at known positions
        # Top: y=10
        scatter_top = pg.ScatterPlotItem([30], [10], size=15, brush='r', symbol='o')
        plot.addItem(scatter_top)
        text_top = pg.TextItem("Y = +10", color='r', anchor=(0.5, 0))
        text_top.setPos(30, 10)
        plot.addItem(text_top)
        
        # Middle: y=0
        scatter_mid = pg.ScatterPlotItem([30], [0], size=15, brush='g', symbol='o')
        plot.addItem(scatter_mid)
        text_mid = pg.TextItem("Y = 0", color='g', anchor=(0.5, 0))
        text_mid.setPos(30, 0)
        plot.addItem(text_mid)
        
        # Bottom: y=-10
        scatter_bot = pg.ScatterPlotItem([30], [-10], size=15, brush='b', symbol='o')
        plot.addItem(scatter_bot)
        text_bot = pg.TextItem("Y = -10", color='b', anchor=(0.5, 0))
        text_bot.setPos(30, -10)
        plot.addItem(text_bot)
        
        # Add horizontal lines
        plot.addLine(y=10, pen=pg.mkPen('r', width=1, style=Qt.DashLine))
        plot.addLine(y=0, pen=pg.mkPen('g', width=1, style=Qt.DashLine))
        plot.addLine(y=-10, pen=pg.mkPen('b', width=1, style=Qt.DashLine))
        
        # Override mouse press to capture clicks
        self.plot_widget.mousePressEvent = self.on_mouse_press
        
        print("\n" + "="*70)
        print("COORDINATE SYSTEM TEST")
        print("="*70)
        print("Plot has Y range: -11 to 11")
        print("Red marker at Y = +10")
        print("Green marker at Y = 0")
        print("Blue marker at Y = -10")
        print("\nClick on or near these markers to test coordinate mapping.")
        print("="*70 + "\n")
    
    def on_mouse_press(self, event):
        """Handle mouse press and show coordinate information."""
        plot = self.plot_widget.getPlotItem()
        
        # Get scene position (pixel coordinates)
        scene_pos = event.position()
        
        # Check if click is within plot bounds
        if plot.sceneBoundingRect().contains(scene_pos):
            # Map to view coordinates (data coordinates)
            view_pos = plot.getViewBox().mapSceneToView(scene_pos)
            
            # Get current view range
            view_range = plot.viewRange()
            x_range = view_range[0]
            y_range = view_range[1]
            
            print("\n" + "-"*70)
            print(f"CLICK DETECTED:")
            print(f"  Scene pos (pixels):     ({scene_pos.x():.1f}, {scene_pos.y():.1f})")
            print(f"  View pos (data coords): ({view_pos.x():.2f}, {view_pos.y():.2f})")
            print(f"  Current Y range:        [{y_range[0]:.2f}, {y_range[1]:.2f}]")
            print(f"  Current X range:        [{x_range[0]:.2f}, {x_range[1]:.2f}]")
            
            # Determine what the user clicked near
            y_val = view_pos.y()
            if 8 < y_val < 12:
                expected = "+10 (RED marker)"
            elif -2 < y_val < 2:
                expected = "0 (GREEN marker)"
            elif -12 < y_val < -8:
                expected = "-10 (BLUE marker)"
            else:
                expected = f"{y_val:.2f}"
            
            print(f"  Expected near:          {expected}")
            print("-"*70)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoordinateTestWindow()
    window.show()
    sys.exit(app.exec())
