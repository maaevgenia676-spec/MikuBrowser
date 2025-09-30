import sys
import os
import subprocess
import atexit
import requests
import time
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMessageBox
from browser.browser_window import Browser

class ProxyManager:
    def __init__(self):
        self.proxy_process = None
        self.proxy_url = "http://127.0.0.1:5000"
    
    def is_proxy_running(self):
        """Проверяет, запущен ли proxy сервер"""
        try:
            response = requests.get(f"{self.proxy_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_proxy(self):
        """Запускает proxy сервер как subprocess"""
        if self.is_proxy_running():
            print("✓ Proxy server is already running")
            return True
            
        try:
            if getattr(sys, 'frozen', False):
                # В собранном приложении
                proxy_path = Path(sys.executable).parent / "proxy.exe"
                if proxy_path.exists():
                    self.proxy_process = subprocess.Popen([str(proxy_path)])
                    print("✓ Started proxy from executable")
                else:
                    print("✗ Proxy executable not found")
                    return False
            else:
                # В режиме разработки
                proxy_path = Path(__file__).parent / "proxy.py"
                if proxy_path.exists():
                    self.proxy_process = subprocess.Popen(
                        [sys.executable, str(proxy_path)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    print("✓ Started proxy from Python script")
                else:
                    print("✗ Proxy script not found")
                    return False
            
            # Ждем запуска proxy
            for i in range(10):
                time.sleep(0.5)
                if self.is_proxy_running():
                    print("✓ Proxy server started successfully")
                    return True
                print(f"Waiting for proxy... {i+1}/10")
            
            print("✗ Proxy server failed to start")
            return False
            
        except Exception as e:
            print(f"✗ Error starting proxy: {e}")
            return False
    
    def stop_proxy(self):
        """Останавливает proxy сервер"""
        if self.proxy_process:
            try:
                self.proxy_process.terminate()
                self.proxy_process.wait(timeout=5)
                print("✓ Proxy server stopped")
            except subprocess.TimeoutExpired:
                self.proxy_process.kill()
                print("✓ Proxy server force stopped")
            except Exception as e:
                print(f"✗ Error stopping proxy: {e}")

def main():
    # Создаем менеджер proxy
    proxy_manager = ProxyManager()
    
    # Пытаемся запустить proxy
    if not proxy_manager.start_proxy():
        # Если не удалось запустить proxy, спросим пользователя
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Proxy Server")
        msg.setText("Не удалось запустить proxy сервер")
        msg.setInformativeText("Хотите продолжить без поиска и AI функций?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.No:
            sys.exit(1)
    
    # Регистрируем остановку proxy при выходе
    atexit.register(proxy_manager.stop_proxy)
    
    # Создаем приложение Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Miku Browser Pro 🎶")
    app.setApplicationVersion("2.0.0")
    
    # Определяем путь к статическим файлам
    def get_resource_path(relative_path: str) -> str:
        """Работает и в dev, и в exe"""
        if getattr(sys, 'frozen', False):
            # для exe
            return str(Path(sys._MEIPASS) / relative_path)
        else:
            # для разработки
            return str(Path(__file__).parent / relative_path)

    # В main()
    static_path = get_resource_path("static")

    
    # Создаем и показываем главное окно
    window = Browser(str(static_path))
    window.show()
    
    # Запускаем цикл событий
    exit_code = app.exec_()
    
    # Останавливаем proxy перед выходом
    proxy_manager.stop_proxy()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()