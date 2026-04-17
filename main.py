import yfinance as yf
import requests
import json

# 設定
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 世界情勢・確定分析開始 ---")
    
    # 1. 株価データの取得
    try:
        data = yf.download(TICKER, period="1d", progress=False)
        current_price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return

    # 2. あなたのリストで確認できた「gemini-3-flash-preview」を使用
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={MY_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
    あなたは世界情勢と金融を知り尽くした投資のプロです。
    現在価格 ${current_price:.2f} の {TICKER} (NVIDIA) について、
    最新の世界情勢（AI半導体需要など）を踏まえ、今後「激熱」かどうか分析してください。
    【ルール】
    1. 結論（激熱・買い・見送り）を文頭に書く。
    2. 150文字程度で、投資家を鼓舞するように情熱的に解説して。
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # 3. AI実行とSlack送信
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        if 'candidates' in res_json:
            ai_response = res_json['candidates'][0]['content']['parts'][0]['text']
            
            msg = (
                f"🌍 *【AI世界情勢分析：{TICKER}】*\n"
                f"*市場価格:* ${current_price:.2f}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{ai_response}"
            )
            requests.post(MY_SLACK_URL, json={"text": msg})
            print("🚀【祝】ついに成功！Slackを確認してください！")
        else:
            print(f"❌ AI応答エラー: {res_json}")

    except Exception as e:
        print(f"実行エラー: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
