import yfinance as yf
import google.generativeai as genai
import requests
import json
from datetime import datetime

# ==========================================
# 設定（キーとURLは正しいのでそのまま）
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA" 

def send_slack_notification(message):
    payload = {"text": message}
    requests.post(MY_SLACK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def run_omni_wealth_ai():
    print(f"--- {TICKER} 分析開始 ---")
    
    # 1. データ取得
    data = yf.download(TICKER, period="2y", progress=False)
    current_price = data['Close'].iloc[-1].item()
    
    # 2. AI設定
    genai.configure(api_key=MY_API_KEY)
    
    prompt = f"NVDAの現在価格 ${current_price:.2f} を踏まえ、今の世界情勢（AI需要等）から見て『激熱』か分析して。結論を文頭に200文字で情熱的に。"

    # 3. AIに聞く（3つの名前を順番に試す「鉄壁」モード）
    ai_response = None
    # 試すモデル名のリスト
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    for name in model_names:
        try:
            print(f"モデル名 '{name}' で試行中...")
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            ai_response = response.text
            if ai_response:
                break # 成功したらループを抜ける
        except Exception as e:
            print(f"-> '{name}' はダメでした: {e}")
            continue

    # 4. 結果を送信
    if ai_response:
        msg = f"🌍 *【AI世界情勢分析：NVDA】*\n*価格:* ${current_price:.2f}\n\n{ai_response}"
        send_slack_notification(msg)
        print("✅ ついにSlackに送信しました！")
    else:
        print("❌ すべてのモデル名が拒絶されました。APIキーの有効化を待つ必要があります。")

if __name__ == "__main__":
    run_omni_wealth_ai()
