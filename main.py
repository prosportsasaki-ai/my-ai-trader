import yfinance as yf
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime

# ==========================================
# 【最終確定】APIキー直接入力 & 最新モデルフルパス設定
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'

# 監視対象
TICKER = "AAPL" 

def send_slack_notification(message):
    payload = {"text": message}
    try:
        requests.post(MY_SLACK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"Slack送信エラー: {e}")

def run_omni_wealth_ai():
    print(f"--- {TICKER} 分析開始 ---")
    
    # 1. データ取得
    try:
        data = yf.download(TICKER, period="2y", progress=False)
        current_price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return
    
    # 2. AI設定（名前の前に models/ をつけるのが現在の正解です）
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"Appleの現在価格 ${current_price:.2f} を踏まえ、50年後も成長し続けているかを分析して。「買い」か「見送り」を文頭に入れて150文字で判定して。"
    
    # 3. AIに聞く
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
    except Exception as e:
        print(f"AI分析エラー: {e}")
        # 万が一モデル名でまだエラーが出る場合の予備
        try:
            print("予備のモデル名で再試行中...")
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            ai_response = response.text
        except:
            return

    # 4. 必ず通知を送る
    msg = f"🚀 *AIトレーダー稼働中*\n*銘柄:* {TICKER}\n*価格:* ${current_price:.2f}\n\n*AI分析:*\n{ai_response}"
    send_slack_notification(msg)
    print("✅ Slackに送信しました！")

if __name__ == "__main__":
    run_omni_wealth_ai()
