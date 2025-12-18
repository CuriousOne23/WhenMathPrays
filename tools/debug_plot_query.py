#!/usr/bin/env python3
"""
Debug script to query PyQtGraph plot contents without running the full GUI.
This adjunct program loads a scenario, creates the panels, updates them with data,
and inspects what's on the graphs for debugging purposes.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.editor.model import EditorModel
from tools.editor.controller import EditorController
from tools.editor.views.primitive_panel_pyqtgraph import PrimitivePanelPyQtGraph
from tools.editor.views.trajectory_panel_pyqtgraph import TrajectoryPanelPyQtGraph
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
import numpy as np

def query_plot_contents(panel, panel_name):
    """Query and print contents of a PyQtGraph panel."""
    print(f"\n=== {panel_name} Panel Query ===")

    # Check if graphics widget exists
    if not hasattr(panel, 'graphics_widget'):
        print("ERROR: No graphics_widget found")
        return

    gw = panel.graphics_widget
    print(f"GraphicsLayoutWidget type: {type(gw)}")
    print(f"GraphicsLayoutWidget visible: {gw.isVisible()}")

    # Get all items in the layout
    layout_items = gw.items()
    print(f"Total layout items: {len(layout_items)}")

    for i, item in enumerate(layout_items):
        print(f"  Item {i}: {type(item)} - {item}")
        if hasattr(item, 'listDataItems'):
            # It's a plot
            data_items = item.listDataItems()
            print(f"    Plot data items: {len(data_items)}")
            for j, data_item in enumerate(data_items):
                data = data_item.getData()
                if data is None:
                    print(f"      Data item {j}: No data")
                    continue
                x_data, y_data = data
                if x_data is None or y_data is None:
                    print(f"      Data item {j}: Invalid data")
                    continue
                print(f"      Data item {j}: {len(x_data)} points")
                if len(x_data) > 0:
                    print(f"        X range: {x_data[0]:.3f} to {x_data[-1]:.3f}")
                    print(f"        Y range: {y_data.min():.3f} to {y_data.max():.3f}")
                    print(f"        Sample points: x[:3]={x_data[:3]}, y[:3]={y_data[:3]}")
                else:
                    print("        No data points")
        elif hasattr(item, 'text'):
            # It's a label or text item
            try:
                text = item.text() if callable(item.text) else item.text
                print(f"    Text content: '{text}'")
            except:
                print(f"    Text item: {type(item)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python debug_plot_query.py <scenario_csv_path>")
        sys.exit(1)

    scenario_path = sys.argv[1]

    # Initialize Qt application (required for PyQtGraph)
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        # Load scenario
        print(f"Loading scenario: {scenario_path}")
        model = EditorModel()

        # Create panels first (needed for controller)
        print("Creating panels...")
        primitive_panel = PrimitivePanelPyQtGraph(None)  # Temporary None, will set controller later
        trajectory_panel = TrajectoryPanelPyQtGraph(None)

        controller = EditorController(model, primitive_panel, trajectory_panel)
        controller.load_scenario(scenario_path)
        print("Scenario loaded successfully")

        # Set controller on panels
        primitive_panel.controller = controller
        trajectory_panel.controller = controller

        # Get events for current perspective
        perspective = controller.perspective  # Should be 'M1' or 'M2'
        events = model.get_events(perspective)
        print(f"Retrieved {len(events)} events for perspective {perspective}")

        # Update panels with model data
        print("Updating panels with model data...")
        primitive_panel.update_from_model(events)
        # Trajectory panel may update through other means, skip for now

        # Query contents
        query_plot_contents(primitive_panel, "Primitive")
        query_plot_contents(trajectory_panel, "Trajectory")

        print("\n=== Query Complete ===")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()