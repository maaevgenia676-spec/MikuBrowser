from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QUrl
import os
from urllib.parse import quote


class Navigation:
    def init_navigation(self):
        # Back button
        self.back_btn = QAction("← Back", self)
        self.back_btn.setShortcut(QKeySequence.Back)
        self.back_btn.triggered.connect(self.go_back)
        self.navbar.addAction(self.back_btn)

        # Forward button
        self.forward_btn = QAction("Forward →", self)
        self.forward_btn.setShortcut(QKeySequence.Forward)
        self.forward_btn.triggered.connect(self.go_forward)
        self.navbar.addAction(self.forward_btn)

        # Reload button
        self.reload_btn = QAction("⟳ Reload", self)
        self.reload_btn.setShortcut(QKeySequence.Refresh)
        self.reload_btn.triggered.connect(self.reload_page)
        self.navbar.addAction(self.reload_btn)

        # Home button
        self.home_btn = QAction("🏠 Home", self)
        self.home_btn.setShortcut("Ctrl+H")
        self.home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(self.home_btn)

        # URL bar
        self.navbar.addWidget(self.url_bar)

        # New tab button
        self.new_tab_btn = QAction("＋ New Tab", self)
        self.new_tab_btn.setShortcut(QKeySequence.AddTab)
        self.new_tab_btn.triggered.connect(self.add_blank_tab)
        self.navbar.addAction(self.new_tab_btn)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        
        # Clean URL - remove any MikuBrowser references
        url = url.replace('/MikuBrowser', '').replace('MikuBrowser/', '')
        
        # If it's a search query (contains spaces or no dots) or doesn't start with protocol
        if not url.startswith(('http://', 'https://', 'file://')):
            if '.' in url and ' ' not in url:
                # It's likely a domain, add https://
                url = f"https://{url}"
            else:
                # Treat as search query - use our search page instead of direct Google
                self.navigate_to_search(url)
                return
        
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl(url))

    def navigate_to_search(self, query):
        """Navigate to search results for the query"""
        # Use our local search interface instead of direct Google
        current_tab = self.tabs.currentWidget()
        if current_tab:
            # Set the search query in the local page (if it's our browser.html)
            current_tab.setUrl(self.get_local_url("browser.html"))
            # We'll need to execute JavaScript to set the search query
            # This will be handled in the browser.html page load

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.forward()

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.reload()

    def navigate_home(self):
        url = self.get_local_url("browser.html")
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(url)
