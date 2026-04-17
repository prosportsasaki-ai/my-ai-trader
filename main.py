import yfinance as yf
import requests
import json

# 設定（最新のキーを使います）
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 最終リベンジ分析開始 ---")
    
    # 1. 価格取得
    try:
        price = yf.download(TICKER, period="1d", progress=False)['Close'].iloc[-1].item()
    except:
        return

    # 2. AIへリクエスト（ブラウザで成功した「v1」エンドポイントを使用）
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={MY_API_KEY}"
    
    prompt = f"伝説の投資家として分析して。NVIDIAの株価が${price:.2f}です。今の世界情勢から見て激熱か、150文字で情熱的に解説して。結論は文頭に。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload)
        res_data = response.json()

        if 'candidates' in res_data:
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
            # 3. Slack送信
            msg = f"🚀 *【AI最新分析：NVDA】*\n*現在値:* ${price:.2f}\n\n{ai_text}"
            requests.post(MY_SLACK_URL, json={"text": msg})
            print("✅ 成功しました！Slackを確認してください！")
        else:
            print(f"❌ 応答エラー詳細: {res_data}")
    except Exception as e:
        print(f"❌ 通信エラー: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
