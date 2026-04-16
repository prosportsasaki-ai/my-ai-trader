import yfinance as yf
import google.generativeai as genai
import requests
import json
import os # ←これが必須！
from datetime import datetime

# --- ここが最重要：Secretsから鍵を読み込む設定 ---
GOOGLE_API_KEY = os.environ.get('AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg')
SLACK_WEBHOOK_URL = os.environ.get('https://hooks.slack.com/services/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')

# 監視対象
TICKER = "AAPL" 

def send_slack_notification(message):
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def run_omni_wealth_ai():
    # ...（以下は前のコードと同じ）...
    data = yf.download(TICKER, period="2y", progress=False)
    current_price = data['Close'].iloc[-1].item()
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"株価 ${current_price:.2f} を踏まえ、50年スパンでの「買い」か「見送り」かを文頭に含めて判定して。"
    ai_response = model.generate_content(prompt).text
    
    # AIが「買い」と言えば通知
    if "買い" in ai_response[:10]:
        msg = f"🚀 *AI投資通知*\n*銘柄:* {TICKER}\n*判定:* 買い\n\n*AI分析:*\n{ai_response}"
        send_slack_notification(msg)

run_omni_wealth_ai()
