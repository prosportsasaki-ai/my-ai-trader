import yfinance as yf
import requests
import json

# 🌟 ここが運命の分かれ道です。URLが正しく貼られているか確認！
MY_SLACK_URL = 'https://hooks.slack.com/services/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'
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
TICKER = "NVDA"

def run_investor_ai():
    print(f"--- {TICKER} 分析＆Slack送信：最終テスト開始 ---")
    
    try:
        # 1. 株価取得
        data = yf.download(TICKER, period="1d", progress=False)
        price = data['Close'].iloc[-1].item()

        # 2. AI分析（1000015200.png で動作確認した最新モデルを使用）
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={MY_API_KEY}"
        prompt = f"NVDAの株価${price:.2f}について、情熱的な投資家として100文字で分析して。"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        ai_res = requests.post(url, json=payload).json()
        analysis = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        # 3. Slack送信（ここで新しいURLを使用）
        slack_payload = {"text": f"🚀 *NVDA分析完了*\n価格: ${price:.2f}\n\n{analysis}"}
        response = requests.post(MY_SLACK_URL, json=slack_payload)
        
        if response.status_code == 200:
            print("✅🎉【祝】ついに成功しました！Slackを確認してください！")
        else:
            print(f"❌ 送信失敗。エラーコード: {response.status_code}")
            print(f"理由: {response.text}")
            
    except Exception as e:
        print(f"❌ 実行エラー: {e}")

if __name__ == "__main__":
    run_investor_ai()
