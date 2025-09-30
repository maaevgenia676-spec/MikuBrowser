from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication
import os


class LinkHandlerPage(QWebEnginePage):
    def __init__(self, parent=None, url_update_callback=None):
        super().__init__(parent)
        self.url_update_callback = url_update_callback

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        """Override to handle navigation requests and update URL bar"""
        if self.url_update_callback and is_main_frame:
            self.url_update_callback(url.toString())
        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)


class Tabs:
    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or not qurl.isValid():
            qurl = self.get_local_url("browser.html")
            
        browser = QWebEngineView()
        
        # Create custom page with link handling
        page = LinkHandlerPage(browser, self.update_url_from_page)
        browser.setPage(page)
        browser.setUrl(qurl)
        
        # Add tab
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        
        # Connect signals
        browser.urlChanged.connect(lambda qurl, browser=browser: 
                                 self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=index, browser=browser: 
                                   self.tabs.setTabText(i, self.get_tab_title(browser)))
        
        # Update title when it changes
        browser.titleChanged.connect(lambda title, i=index: 
                                   self.tabs.setTabText(i, self.get_tab_title(browser)))
        
        # Context menu for links
        browser.page().linkHovered.connect(self.on_link_hovered)
        
        return browser

    def get_tab_title(self, browser):
        """Get appropriate title for tab"""
        title = browser.page().title()
        if not title or title == "Miku Browser Pro":
            url = browser.url().toString()
            if url.startswith('file://'):
                return "Home"
            elif 'youtube.com' in url:
                return "YouTube"
            elif 'google.com' in url:
                return "Google"
            else:
                # Extract domain name for title
                from urllib.parse import urlparse
                try:
                    domain = urlparse(url).netloc
                    if domain.startswith('www.'):
                        domain = domain[4:]
                    return domain[:20] if domain else "New Tab"
                except:
                    return "New Tab"
        return title[:20]

    def update_url_from_page(self, url):
        """Update URL bar when navigation occurs from page clicks"""
        # Don't update URL bar for local file navigation within the same domain
        if url and not url.startswith('file://') and not 'MikuBrowser' in url:
            self.url_bar.setText(url)
            self.url_bar.setCursorPosition(0)

    def on_link_hovered(self, url):
        """Show hovered link in status bar"""
        if url and not url.startswith('file://') and not 'MikuBrowser' in url:
            self.status.showMessage(f"Link: {url}")
        else:
            self.status.showMessage("Ready")

    def add_blank_tab(self):
        self.add_new_tab()

    def close_current_tab(self, index=None):
        if index is None:
            index = self.tabs.currentIndex()
            
        if self.tabs.count() <= 1:
            return
            
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
            
        self.tabs.removeTab(index)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
            
        current_url = q.toString()
        
        # Filter out local file paths and MikuBrowser references from URL bar
        if current_url.startswith('file://') or 'MikuBrowser' in current_url:
            # Show clean URL for external sites only
            self.url_bar.clear()
        else:
            self.url_bar.setText(current_url)
            self.url_bar.setCursorPosition(0)
        
        # Update status
        if hasattr(self, 'status'):
            if current_url.startswith('file://'):
                self.status.showMessage("Home")
            else:
                self.status.showMessage(f"Loaded: {current_url}")