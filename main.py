import yfinance as yf
import requests
import json

# 設定
MY_API_KEY = 'AQ.Ab8RN6JUWBGW6ozrFNjYXN9jWgHqzgS2scGHlOc8TELU451KIg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    # 1. 株価取得
    data = yf.download(TICKER, period="2y", progress=False)
    price = data['Close'].iloc[-1].item()

    # 2. AIに直接リクエスト（ライブラリを使わない「直通」方式）
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MY_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{
                "text": f"NVIDIAの株価が${price:.2f}です。世界情勢から見て激熱か分析して。結論を文頭に200文字で。"
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        # AIの返答を取り出す
        ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
        
        # 3. Slack送信
        msg = f"🌍 *【AI深層分析レポート】*\n*銘柄:* {TICKER}\n*価格:* ${price:.2f}\n\n{ai_text}"
        requests.post(MY_SLACK_URL, json={"text": msg})
        print("✅ 成功しました！Slackを確認してください。")
        
    except Exception as e:
        print(f"❌ エラー発生: {res_json if 'res_json' in locals() else e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
