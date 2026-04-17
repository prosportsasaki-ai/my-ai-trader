import yfinance as yf
import requests
import json

# 🚀 あなたが新しく発行してくれた最新のURLです
MY_SLACK_URL = 'https://hooks.slack.com/services/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'
# 動作確認済みのGemini APIキー
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
TICKER = "NVDA"

def run_investor_ai():
    print(f"--- {TICKER} 分析＆Slack送信：最終テスト開始 ---")
    
    # 1. 株価の取得
    try:
        data = yf.download(TICKER, period="1d", progress=False)
        price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"株価取得エラー: {e}")
        return

    # 2. AIによる分析（最も安定しているモデルを使用）
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={MY_API_KEY}"
    prompt = f"NVDAの現在の株価は${price:.2f}です。プロの投資家として、この状況を100文字以内で情熱的に日本語で分析して。結論から書いてください。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        # AI分析の実行
        ai_res = requests.post(url, json=payload).json()
        analysis = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        # 3. Slackへの通知実行
        slack_payload = {
            "text": f"📢 *NVDA 株式分析レポート*\n現在の価格: *${price:.2f}*\n\n{analysis}"
        }
        
        # 新しいURLで送信
        response = requests.post(MY_SLACK_URL, json=slack_payload)
        
        if response.status_code == 200:
            print("✅🎉【祝】成功しました！Slackを確認してください！")
        else:
            print(f"❌ 送信失敗。エラーコード: {response.status_code}")
            print(f"理由: {response.text}")
            
    except Exception as e:
        print(f"❌ 実行エラー: {e}")

if __name__ == "__main__":
    run_investor_ai()
