"""
Main window for interactive scenario editor.

Phase 3.5 Architecture Refactoring:
    - Renamed from qt_window.py to main_window.py
    - Replaced callback attributes with Qt signals
    - Proper signal-based architecture (no middleman pattern)
    - save_callback → save_requested signal
    - cleanup_callback → cleanup_requested signal

Embeds PyQtGraph panels in PySide6 framework with native
toolbars, menus, and status bar.
"""

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QToolBar, 
    QStatusBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QAction, QKeySequence, QUndoStack


class EditorMainWindow(QMainWindow):
    """
    Main window for interactive scenario editor.
    
    Embeds PyQtGraph panels in Qt framework with native
    toolbars, menus, and status bar.
    
    Signals:
        save_requested: Emitted when user requests save (passes modifiers dict)
        cleanup_requested: Emitted before window closes (for application cleanup)
        print_dock_config_requested: Emitted when user presses Ctrl+D (for debugging dock layout)
    """
    
    # Phase 3.5: Replace callback attributes with Qt signals
    save_requested = Signal(dict)  # {'csv': bool, 'png': bool}
    save_both_requested = Signal()  # Save both M1 and M2 perspectives
    cleanup_requested = Signal()
    print_dock_config_requested = Signal()  # For Ctrl+D debug shortcut
    
    def __init__(self, csv_file: Path):
        super().__init__()
        self.csv_file = csv_file
        self.setWindowTitle(f'Interactive Scenario Editor - {csv_file.name}')
        
        # Initialize settings for state persistence
        self.settings = QSettings('WhenMathPrays', 'InteractiveEditor')
        
        # Restore saved geometry and state, or use defaults
        if self.settings.contains('geometry'):
            self.restoreGeometry(self.settings.value('geometry'))
        else:
            # Default: 90% of screen size, centered
            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen().availableGeometry()
            width = int(screen.width() * 0.9)
            height = int(screen.height() * 0.85)
            x = int((screen.width() - width) / 2)
            y = int((screen.height() - height) / 2)
            self.setGeometry(x, y, width, height)
        
        self.setMinimumSize(1000, 500)  # Minimum size for usability
        
        # Central widget will be set by application with PyQtGraph panels
        
        # Undo stack (created before toolbar for undo/redo actions)
        self.undo_stack = QUndoStack(self)
        
        # Add toolbar
        self._setup_toolbar()
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
    
    def _setup_toolbar(self):
        """Create toolbar with common actions."""
        toolbar = QToolBar('Main Toolbar')
        self.addToolBar(toolbar)
        
        # Save action
        save_action = QAction('Save CSV', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip('Save scenario to CSV (Ctrl+S)')
        save_action.triggered.connect(lambda: self._on_save(csv=True, png=False))
        toolbar.addAction(save_action)
        
        # Save Both Perspectives action
        save_both_action = QAction('Save Both M1 && M2', self)
        save_both_action.setShortcut(QKeySequence('Ctrl+Shift+S'))
        save_both_action.setStatusTip('Save both M1 and M2 perspectives to separate files (Ctrl+Shift+S)')
        save_both_action.triggered.connect(self._on_save_both)
        toolbar.addAction(save_both_action)
        
        toolbar.addSeparator()
        
        # Zoom actions
        zoom_in_action = QAction('Zoom In (+)', self)
        zoom_in_action.setStatusTip('Zoom in both panels (use + key for context-aware zoom)')
        toolbar.addAction(zoom_in_action)
        self.zoom_in_action = zoom_in_action
        
        zoom_out_action = QAction('Zoom Out (-)', self)
        zoom_out_action.setStatusTip('Zoom out both panels (use - key for context-aware zoom)')
        toolbar.addAction(zoom_out_action)
        self.zoom_out_action = zoom_out_action
        
        zoom_reset_action = QAction('Reset View (0)', self)
        zoom_reset_action.setStatusTip('Reset all views to original (press 0 key)')
        toolbar.addAction(zoom_reset_action)
        self.zoom_reset_action = zoom_reset_action
        
        toolbar.addSeparator()
        
        # Undo/Redo actions
        undo_action = self.undo_stack.createUndoAction(self, 'Undo')
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setStatusTip('Undo last action (Ctrl+Z)')
        toolbar.addAction(undo_action)
        
        redo_action = self.undo_stack.createRedoAction(self, 'Redo')
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setStatusTip('Redo last undone action (Ctrl+Y)')
        toolbar.addAction(redo_action)
        
        # Debug action for printing dock configuration (Ctrl+D)
        debug_dock_action = QAction('Print Dock Config', self)
        debug_dock_action.setShortcut(QKeySequence('Ctrl+D'))
        debug_dock_action.setStatusTip('Print dock configuration to terminal (Ctrl+D)')
        debug_dock_action.triggered.connect(self.print_dock_config_requested.emit)
        # Don't add to toolbar, just set up the shortcut
        self.addAction(debug_dock_action)
        
        # State Viewer Log export action (Ctrl+Shift+L)
        export_state_log_action = QAction('Export State Log', self)
        export_state_log_action.setShortcut(QKeySequence('Ctrl+Shift+L'))
        export_state_log_action.setStatusTip('Export state viewer log for debugging (Ctrl+Shift+L)')
        export_state_log_action.triggered.connect(self._on_export_state_log)
        # Don't add to toolbar, just set up the shortcut
        self.addAction(export_state_log_action)
        
        # Store references to prevent garbage collection
        self._toolbar = toolbar
        self._save_action = save_action
        self._save_both_action = save_both_action
        self._undo_action = undo_action
        self._redo_action = redo_action
        self._debug_dock_action = debug_dock_action
        self._export_state_log_action = export_state_log_action
    
    def switch_undo_stack(self, new_stack: QUndoStack):
        """
        Switch to a different undo stack and update UI actions.
        
        Args:
            new_stack: The new QUndoStack to use for undo/redo
        """
        if new_stack is None:
            return
        
        # Remove old actions from toolbar
        self._toolbar.removeAction(self._undo_action)
        self._toolbar.removeAction(self._redo_action)
        
        # Update undo stack reference
        self.undo_stack = new_stack
        
        # Create new actions connected to the new stack
        self._undo_action = self.undo_stack.createUndoAction(self, '&Undo')
        self._undo_action.setShortcut(QKeySequence.Undo)
        self._redo_action = self.undo_stack.createRedoAction(self, '&Redo')
        self._redo_action.setShortcut(QKeySequence.Redo)
        
        # Re-add actions to toolbar
        self._toolbar.insertAction(self._toolbar.actions()[0], self._undo_action)
        self._toolbar.insertAction(self._toolbar.actions()[1], self._redo_action)
        
        print(f"[UNDO] UI actions switched to new stack (size: {new_stack.count()})")
    
    def restore_dock_state(self):
        """
        Restore saved dock widget state after docks have been added.
        Should be called after all docks are created and added to window.
        """
        if self.settings.contains('windowState'):
            print("[STATE] Restoring saved window layout")
            self.restoreState(self.settings.value('windowState'))
        else:
            print("[STATE] No saved layout found, using defaults")
    
    def _setup_view_menu(self, dock_widgets: dict):
        """
        Create View menu with show/hide panel actions.
        
        Args:
            dock_widgets: Dict mapping panel names to QDockWidget instances
        """
        # Create View menu
        view_menu = self.menuBar().addMenu('&View')
        
        # Add toggle actions for each dock widget
        for name, dock in dock_widgets.items():
            toggle_action = dock.toggleViewAction()
            toggle_action.setText(f"Show {name}")
            view_menu.addAction(toggle_action)
    
    def _on_save(self, csv=True, png=False):
        """
        Handle save request.
        
        Args:
            csv: Whether to save CSV
            png: Whether to save PNG
        """
        # Phase 3.5: Use callback pattern (signals available but not connected yet)
        if hasattr(self, 'save_callback') and callable(self.save_callback):
            self.save_callback({'csv': csv, 'png': png})
        else:
            self.save_requested.emit({'csv': csv, 'png': png})
    
    def _on_save_both(self):
        """Handle save both perspectives request."""
        # Use callback pattern (signals available but not connected yet)
        if hasattr(self, 'save_both_callback') and callable(self.save_both_callback):
            self.save_both_callback()
        else:
            self.save_both_requested.emit()
    
    def _on_export_state_log(self):
        """Handle state viewer log export request (Ctrl+Shift+L)."""
        from datetime import datetime
        from tools.editor.state_viewer import StateViewer
        import os
        
        # Create logs directory if it doesn't exist
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'state_log_{timestamp}.txt'
        log_filepath = logs_dir / log_filename
        
        # Export state log using StateViewer
        StateViewer.export_to_file(str(log_filepath))
        
        # Update window title to show log mode
        original_title = self.windowTitle()
        self.setWindowTitle(f"{original_title} [STATE LOG EXPORTED]")
        
        # Show notification in status bar
        self.statusBar().showMessage(
            f"✓ State log exported: {log_filepath.absolute()}",
            5000  # Show for 5 seconds
        )
        
        # Also show message box for visibility
        QMessageBox.information(
            self,
            "State Log Exported",
            f"State viewer log exported to:\n\n{log_filepath.absolute()}\n\n"
            f"Share this file with AI assistant for debugging analysis."
        )
        
        # Reset window title after 5 seconds
        from PySide6.QtCore import QTimer
        QTimer.singleShot(5000, lambda: self.setWindowTitle(original_title))
    
    def show_message(self, message: str, level: str = 'info', timeout: int = 5000):
        """
        Show message in status bar or dialog.
        
        Args:
            message: Message text
            level: 'info', 'warning', or 'error'
            timeout: Milliseconds to show in status bar (0 = permanent)
        """
        if level == 'info':
            self.status_bar.showMessage(message, timeout)
        elif level == 'warning':
            QMessageBox.warning(self, 'Warning', message)
            self.status_bar.showMessage(f'Warning: {message}', timeout)
        elif level == 'error':
            QMessageBox.critical(self, 'Error', message)
            self.status_bar.showMessage(f'Error: {message}', timeout)
    
    def update_window_title(self, csv_file: Path):
        """
        Update window title with new filename.
        
        Args:
            csv_file: Path to current CSV file
        """
        self.csv_file = csv_file
        self.setWindowTitle(f'Interactive Scenario Editor - {csv_file.name}')
    
    def confirm_dialog(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog.
        
        Args:
            title: Dialog title
            message: Dialog message
            
        Returns:
            True if user clicked Yes, False otherwise
        """
        reply = QMessageBox.question(
            self, 
            title, 
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
    
    def closeEvent(self, event):
        """
        Handle window close event to properly exit the application.
        
        Phase 3.5: Emit cleanup_requested signal instead of calling callback.
        """
        # Save window geometry and state for next launch
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        self.settings.sync()  # Force immediate write to storage
        print("[STATE] Window layout saved")
        
        # Emit cleanup signal for application to handle
        self.cleanup_requested.emit()
        
        # Accept the close event and quit the application
        event.accept()
        self.close()
        
        # Force application exit
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
    
    def showEvent(self, event):
        """Handle window show event (including restore from minimize)."""
        super().showEvent(event)
        # PyQtGraph handles its own refresh automatically
    
    def changeEvent(self, event):
        """Handle window state changes (minimize, restore, etc)."""
        super().changeEvent(event)
        # PyQtGraph handles window state changes automatically
