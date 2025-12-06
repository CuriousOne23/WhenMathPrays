"""
Qt main window wrapper for interactive scenario editor.

Embeds matplotlib figures in PySide6 framework with native
toolbars, menus, and status bar.
"""

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QToolBar, 
    QStatusBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeySequence, QUndoStack
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class EditorMainWindow(QMainWindow):
    """
    Main window for interactive scenario editor.
    
    Embeds matplotlib figures in Qt framework with native
    toolbars, menus, and status bar.
    
    Signals:
        save_requested: Emitted when user requests save (passes modifiers dict)
    """
    
    save_requested = Signal(dict)  # {'csv': bool, 'png': bool}
    
    def __init__(self, csv_file: Path):
        super().__init__()
        self.csv_file = csv_file
        self.setWindowTitle(f'Interactive Scenario Editor - {csv_file.name}')
        self.setGeometry(100, 100, 1400, 800)
        
        # Create matplotlib figure (same size as Phase 1)
        self.fig = Figure(figsize=(14, 8))
        
        # Embed in Qt canvas
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.setCentralWidget(self.canvas)
        
        # Undo stack (for Phase 2.4 - create before toolbar)
        self.undo_stack = QUndoStack(self)
        
        # Add toolbar
        self._setup_toolbar()
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        
        # Save callback (will be set by interactive_editor.py)
        self.save_callback = None
        self.cleanup_callback = None
    
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
        
        # Save PNG action
        save_png_action = QAction('Save PNG', self)
        save_png_action.setShortcut('Shift+Ctrl+S')
        save_png_action.setStatusTip('Save plots to PNG (Shift+Ctrl+S)')
        save_png_action.triggered.connect(lambda: self._on_save(csv=False, png=True))
        toolbar.addAction(save_png_action)
        
        # Save Both action
        save_both_action = QAction('Save Both', self)
        save_both_action.setStatusTip('Save both CSV and PNG')
        save_both_action.triggered.connect(lambda: self._on_save(csv=True, png=True))
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
        
        # Undo/Redo (Phase 2.4 - placeholder for now)
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
        self._save_png_action = save_png_action
        self._save_both_action = save_both_action
        self._undo_action = undo_action
        self._redo_action = redo_action
    
    def _on_save(self, csv=True, png=False):
        """
        Handle save request.
        
        Args:
            csv: Whether to save CSV
            png: Whether to save PNG
        """
        if self.save_callback:
            self.save_callback({'csv': csv, 'png': png})
        else:
            self.show_message('Save callback not configured', 'warning')
    
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
            self.status_bar.showMessage(f'Error: {message}', 0)
    
    def update_window_title(self, csv_file: Path):
        """Update window title with new file name."""
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
        """Handle window close event to properly exit the application."""
        # Call cleanup callback if set
        if self.cleanup_callback:
            self.cleanup_callback()
        
        # Accept the close event and quit the application
        event.accept()
        self.close()
        # Force application exit
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
    
    def showEvent(self, event):
        """Handle window show event (including restore from minimize)."""
        super().showEvent(event)
        # Refresh canvas to prevent event handling issues after minimize/restore
        if hasattr(self, 'canvas'):
            self.canvas.draw_idle()
    
    def changeEvent(self, event):
        """Handle window state changes (minimize, restore, etc)."""
        super().changeEvent(event)
        # If window is being restored from minimized state
        if event.type() == event.Type.WindowStateChange:
            if not self.isMinimized() and hasattr(self, 'canvas'):
                # Refresh canvas after restore
                self.canvas.draw_idle()
