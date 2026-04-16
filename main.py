import yfinance as yf
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime

# ==========================================
# 【修正版】直接書き込み（クォーテーションを正確に）
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'

# 監視対象
TICKER = "AAPL" 

def send_slack_notification(message):
    payload = {"text": message}
    requests.post(MY_SLACK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def run_omni_wealth_ai():
    print(f"[{TICKER}] 分析開始...")
    
    # データ取得
    data = yf.download(TICKER, period="2y", progress=False)
    current_price = data['Close'].iloc[-1].item()
    
    # AI設定（モデル名を -latest に修正）
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"Appleの現在価格 ${current_price:.2f} を踏まえ、50年後も成長し続けているかを分析して。「買い」か「見送り」を文頭に入れて150文字で判定して。"
    
    # AIに聞く
    response = model.generate_content(prompt)
    ai_response = response.text

    # 条件なしで必ずSlackに送る設定（まずは動作確認！）
    msg = f"🚀 *AIトレーダー稼働中*\n*銘柄:* {TICKER}\n*価格:* ${current_price:.2f}\n\n*AI分析:*\n{ai_response}"
    send_slack_notification(msg)
    print("Slackに送信しました！")

if __name__ == "__main__":
    run_omni_wealth_ai()
