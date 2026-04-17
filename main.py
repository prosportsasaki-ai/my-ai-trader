import yfinance as yf
import requests
import json

# 🚀 あなたが提供してくれた最新のURLに差し替えました
MY_SLACK_URL = 'https://hooks.slack.com/services/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'
# あなたのAPIキー（1000015200.png で動作確認済みのもの）
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 分析＆Slack送信開始 ---")
    
    # 1. 最新株価の取得
    try:
        data = yf.download(TICKER, period="1d", progress=False)
        price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"株価取得エラー: {e}")
        return

    # 2. Gemini AIによる分析 (動作確認済みの gemini-3-flash-preview を使用)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={MY_API_KEY}"
    prompt = f"NVDAの現在の株価は${price:.2f}です。プロの投資家として、この状況を短く情熱的に分析して日本語で教えてください。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        ai_res = requests.post(url, json=payload).json()
        # AIの回答を抽出
        analysis = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        # 3. Slackへの通知実行
        slack_payload = {
            "text": f"📢 *NVDA 株式分析レポート*\n現在の価格: *${price:.2f}*\n\n{analysis}"
        }
        
        response = requests.post(MY_SLACK_URL, json=slack_payload)
        
        if response.status_code == 200:
            print("✅ 成功！Slackにメッセージを送信しました！")
        else:
            print(f"❌ Slack送信失敗。エラーコード: {response.status_code}")
            print(f"返答内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 実行中にエラーが発生しました: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
