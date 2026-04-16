import yfinance as yf
import google.generativeai as genai
import requests
import json
import os
from datetime import datetime

# ==========================================
# 設定（あなたのキーをそのまま使います）
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'

# 監視対象：エヌビディア (NVDA) に変更しました！
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
    
    # 2. AI設定
    genai.configure(api_key=MY_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 🌟 AIへの「熱い分析」命令
    prompt = f"""
    あなたは世界情勢、地政学、金融テクノロジーに精通した「伝説の投資コンサルタント」です。
    
    【依頼内容】
    現在価格 ${current_price:.2f} の {TICKER} (NVIDIA) について、あなたの持つ最新知識を総動員して分析してください。
    
    【分析の視点】
    1. 現在の世界情勢（AI革命、データセンター需要、半導体輸出規制、競合他社の動きなど）から見て、この銘柄は今「激熱」なのか。
    2. 短期的なバブル懸念か、それとも100年に一度のパラダイムシフトの主役か。
    
    結論を「激熱」「買い」「見送り」のいずれかで文頭に明記し、200文字程度でプロフェッショナルかつ情熱的に解説してください。
    """
    
    # 3. AIに分析を実行させる
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
    except Exception as e:
        print(f"AI分析エラー: {e}")
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(prompt)
            ai_response = response.text
        except:
            return

    # 4. Slackへレポートを送信
    msg = (
        f"🌍 *【AI世界情勢分析レポート：注目銘柄】*\n"
        f"*対象銘柄:* {TICKER} (NVIDIA)\n"
        f"*市場価格:* ${current_price:.2f}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{ai_response}"
    )
    send_slack_notification(msg)
    print(f"✅ {TICKER} の分析レポートをSlackに送信しました！")

if __name__ == "__main__":
    run_omni_wealth_ai()
