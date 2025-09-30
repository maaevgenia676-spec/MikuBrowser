from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QUrl


class LocalPages:
    def init_local_pages(self):
        # Browser page
        self.browser_btn = QAction("🔍 Search", self)
        self.browser_btn.triggered.connect(self.open_local_browser)
        self.navbar.addAction(self.browser_btn)

        # Terminal page
        self.terminal_btn = QAction("💻 Terminal", self)
        self.terminal_btn.triggered.connect(self.open_local_terminal)
        self.navbar.addAction(self.terminal_btn)

        # AI Chat page
        self.ai_btn = QAction("🤖 AI Chat", self)
        self.ai_btn.triggered.connect(self.open_local_ai)
        self.navbar.addAction(self.ai_btn)

    def open_local_browser(self):
        url = self.get_local_url("browser.html")
        self.add_new_tab(url, "Search")

    def open_local_terminal(self):
        url = self.get_local_url("terminal.html")
        self.add_new_tab(url, "Terminal")

    def open_local_ai(self):
        url = self.get_local_url("ai.html")
        self.add_new_tab(url, "AI Chat")