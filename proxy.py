from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import os
import logging
import signal
import sys
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 🔑 API Keys
GOOGLE_API_KEY = "AIzaSyBfMx7kgyJU2wmIDBn4e1qFRVx2aaYeWUo"
GOOGLE_CX = "26f006107f7d34c06"

class SearchEngine:
    @staticmethod
    def duckduckgo_search(query):
        """Поиск через DuckDuckGo API"""
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=8)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"DuckDuckGo error: {e}")
            return None

    @staticmethod
    def google_search(query):
        """Поиск через Google Custom Search API"""
        try:
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
            response = requests.get(url, timeout=8)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Google Search error: {e}")
            return None

@app.route("/search")
def search():
    start_time = datetime.now()
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"error": "Пустой запрос"}), 400

    logger.info(f"Search query: {query}")

    # Сначала пробуем DuckDuckGo
    ddg_data = SearchEngine.duckduckgo_search(query)
    if ddg_data and (ddg_data.get("RelatedTopics") or ddg_data.get("AbstractText")):
        logger.info(f"DuckDuckGo results found for: {query}")
        return jsonify({
            "source": "ddg", 
            "data": ddg_data,
            "query_time": f"{(datetime.now() - start_time).total_seconds():.2f}s"
        })

    # Если DDG пустой → Google Custom Search
    google_data = SearchEngine.google_search(query)
    if google_data and "items" in google_data:
        logger.info(f"Google results found for: {query}")
        return jsonify({
            "source": "google", 
            "data": google_data,
            "query_time": f"{(datetime.now() - start_time).total_seconds():.2f}s"
        })

    # Если всё сломалось
    logger.warning(f"No results found for: {query}")
    return jsonify({
        "error": "Не удалось получить результаты поиска",
        "query_time": f"{(datetime.now() - start_time).total_seconds():.2f}s"
    }), 404

@app.route("/ai/chat", methods=["POST"])
def ai_chat():
    """AI Chat endpoint через наш прокси"""
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({"error": "Empty message"}), 400

        # Заглушка для AI - в реальности здесь будет интеграция с AI API
        responses = [
            "Привет! Я ваш AI помощник. Как я могу вам помочь?",
            "Интересный вопрос! К сожалению, сейчас я работаю в ограниченном режиме.",
            "Для полноценной работы AI ассистента настройте API ключ в интерфейсе браузера.",
            "Вы можете использовать различные AI сервисы через настройки браузера.",
        ]
        
        import random
        reply = random.choice(responses)
        
        return jsonify({
            "reply": reply,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    """Эндпоинт для проверки здоровья сервера"""
    return jsonify({
        "status": "healthy", 
        "service": "Miku Browser Proxy",
        "timestamp": datetime.now().isoformat()
    })

def signal_handler(signum, frame):
    """Обработчик сигналов для graceful shutdown"""
    logger.info("Received shutdown signal")
    sys.exit(0)

if __name__ == "__main__":
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("Starting Miku Browser Proxy Server on http://127.0.0.1:5000")
        app.run(host="127.0.0.1", port=5000, debug=False)
    except Exception as e:
        logger.error(f"Proxy server error: {e}")
        sys.exit(1)