import os
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QAction, QToolBar, 
                             QTabWidget, QStatusBar, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon, QKeySequence, QPalette, QColor
from PyQt5.QtNetwork import QNetworkProxy

from .navigation import Navigation
from .tabs import Tabs
from .local_pages import LocalPages


class Browser(QMainWindow, Navigation, Tabs, LocalPages):
    def __init__(self, static_path):
        super().__init__()
        self.static_path = static_path
        self.setWindowTitle("Miku Browser Pro 🎶")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.set_dark_theme()

        # Initialize UI components
        self.init_ui()

    def set_dark_theme(self):
        """Set dark theme for the application"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.BrightText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)

    def init_ui(self):
        """Initialize user interface"""
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search query...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setClearButtonEnabled(True)

        # Navigation toolbar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.navbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.navbar)

        # Initialize components
        self.init_navigation()
        self.init_local_pages()
        self.init_menu()

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # Add first tab
        self.add_new_tab(self.get_local_url("browser.html"), "Home")

    def init_menu(self):
        """Initialize menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut(QKeySequence.AddTab)
        new_tab_action.triggered.connect(self.add_blank_tab)
        file_menu.addAction(new_tab_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Exit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        zoom_in = QAction("Zoom In", self)
        zoom_in.setShortcut(QKeySequence.ZoomIn)
        zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("Zoom Out", self)
        zoom_out.setShortcut(QKeySequence.ZoomOut)
        zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out)
        
        reset_zoom = QAction("Reset Zoom", self)
        reset_zoom.setShortcut("Ctrl+0")
        reset_zoom.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom)

    def get_local_url(self, filename):
        """Get local file URL"""
        file_path = os.path.join(self.static_path, filename)
        if os.path.exists(file_path):
            return QUrl.fromLocalFile(file_path)
        else:
            QMessageBox.warning(self, "File Not Found", 
                              f"Local file {filename} not found at {file_path}")
            return QUrl("about:blank")

    def zoom_in(self):
        """Zoom in current tab"""
        current = self.tabs.currentWidget()
        if current:
            current.setZoomFactor(current.zoomFactor() + 0.1)

    def zoom_out(self):
        """Zoom out current tab"""
        current = self.tabs.currentWidget()
        if current:
            current.setZoomFactor(max(0.1, current.zoomFactor() - 0.1))

    def reset_zoom(self):
        """Reset zoom to 100%"""
        current = self.tabs.currentWidget()
        if current:
            current.setZoomFactor(1.0)
