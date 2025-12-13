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
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeySequence, QUndoStack


class EditorMainWindow(QMainWindow):
    """
    Main window for interactive scenario editor.
    
    Embeds PyQtGraph panels in Qt framework with native
    toolbars, menus, and status bar.
    
    Signals:
        save_requested: Emitted when user requests save (passes modifiers dict)
        cleanup_requested: Emitted before window closes (for application cleanup)
    """
    
    # Phase 3.5: Replace callback attributes with Qt signals
    save_requested = Signal(dict)  # {'csv': bool, 'png': bool}
    cleanup_requested = Signal()
    
    def __init__(self, csv_file: Path):
        super().__init__()
        self.csv_file = csv_file
        self.setWindowTitle(f'Interactive Scenario Editor - {csv_file.name}')
        self.setGeometry(100, 100, 1400, 600)
        self.setMinimumHeight(400)  # Allow resizing down to 400px
        
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
        
        # Store references to prevent garbage collection
        self._toolbar = toolbar
        self._save_action = save_action
        self._undo_action = undo_action
        self._redo_action = redo_action
    
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
        # Phase 3.5: Emit signal instead of calling callback
        self.save_requested.emit({'csv': csv, 'png': png})
    
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
