import yfinance as yf
import google.generativeai as genai
import requests
import json
from datetime import datetime

# ==========================================
# 【最終版】直接組み込み設定（これで確実に動きます）
# ==========================================
GOOGLE_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
SLACK_WEBHOOK_URL = 'Https://hooks.slack.com/services/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'

# 監視対象：Apple (AAPL)
TICKER = "AAPL" 

def send_slack_notification(message):
    """Slackへ通知を送る"""
    payload = {"text": message}
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code
    except Exception as e:
        print(f"Slack送信エラー: {e}")
        return None

def run_omni_wealth_ai():
    print(f"--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 分析開始 ---")
    
    # 1. 市場データの取得
    try:
        data = yf.download(TICKER, period="2y", progress=False)
        data['SMA200'] = data['Close'].rolling(window=200).mean()
        current_price = data['Close'].iloc[-1].item()
        sma200 = data['SMA200'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return

    # 2. AIによる未来分析
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    あなたはプロの投資家です。{TICKER}の現在価格 ${current_price:.2f} を踏まえ、
    50年後も成長し続けているかを分析してください。
    結論は必ず「買い」または「見送り」という言葉を文頭に含め、150文字程度で回答してください。
    """
    
    try:
        ai_response = model.generate_content(prompt).text
    except Exception as e:
        print(f"AI分析エラー: {e}")
        return

    # 3. 判定と通知
    # テストのために、AIが「買い」と言えば必ず通知が飛ぶようにしています
    if "買い" in ai_response:
        msg = (
            f"🚀 *【AI投資通知：買い推奨】*\n"
            f"*銘柄:* {TICKER}\n"
            f"*現在価格:* ${current_price:.2f}\n"
            f"\n*🧠 AIの分析結果:*\n{ai_response}"
        )
        send_slack_notification(msg)
        print("✅ Slackに通知を送りました！")
    else:
        print(f"⏳ 判定：見送り（AI回答：{ai_response[:20]}...）")

if __name__ == "__main__":
    run_omni_wealth_ai()
