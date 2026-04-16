import yfinance as yf
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime

# --- GitHubの「隠し金庫」から鍵を読み込む設定 ---
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

# 監視対象
TICKER = "AAPL" 

def send_slack_notification(message):
    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def run_omni_wealth_ai():
    print(f"[{TICKER}] 分析開始...")
    data = yf.download(TICKER, period="2y", progress=False)
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    
    current_price = data['Close'].iloc[-1].item()
    sma200 = data['SMA200'].iloc[-1].item()
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"株価 ${current_price:.2f} と将来性を踏まえ、50年スパンでの「買い」か「見送り」かを文頭に含めて150文字で判定して。"
    ai_response = model.generate_content(prompt).text

    is_technical_ok = current_price > sma200
    is_ai_ok = "買い" in ai_response[:10] 

    if is_technical_ok and is_ai_ok:
        msg = f"🚀 *【AI投資通知】*\n*銘柄:* {TICKER}\n*判定:* 買い推奨\n\n*AI分析:*\n{ai_response}"
        send_slack_notification(msg)

run_omni_wealth_ai()
