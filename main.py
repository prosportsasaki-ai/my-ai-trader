import yfinance as yf
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime

# ==========================================
# 【修正】モデル名から models/ を削除しました
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'

# 監視対象：エヌビディア (NVDA)
TICKER = "NVDA" 

def send_slack_notification(message):
    payload = {"text": message}
    try:
        requests.post(MY_SLACK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print(f"Slack送信エラー: {e}")

def run_omni_wealth_ai():
    print(f"--- {TICKER} 世界情勢・深層分析開始 ---")
    
    # 1. 株価データの取得
    try:
        data = yf.download(TICKER, period="2y", progress=False)
        current_price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return
    
    # 2. AI設定（モデル名を gemini-1.5-flash に固定）
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AIへの命令
    prompt = f"""
    あなたは世界情勢、地政学、金融テクノロジーに精通した「伝説の投資コンサルタント」です。
    現在価格 ${current_price:.2f} の {TICKER} (NVIDIA) について分析してください。
    
    【視点】AI革命、データセンター需要、半導体規制から見て今「激熱」か。
    結論を「激熱」「買い」「見送り」のいずれかで文頭に書き、200文字程度で情熱的に解説してください。
    """
    
    # 3. AIに分析を実行させる
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
    except Exception as e:
        # 万が一また404が出る場合の最終バックアップ
        print(f"1回目エラー: {e}")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        ai_response = response.text

    # 4. Slackへ送信
    msg = (
        f"🌍 *【AI世界情勢分析：NVDA】*\n"
        f"*市場価格:* ${current_price:.2f}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{ai_response}"
    )
    send_slack_notification(msg)
    print("✅ 分析完了！Slackを確認してください。")

if __name__ == "__main__":
    run_omni_wealth_ai()
