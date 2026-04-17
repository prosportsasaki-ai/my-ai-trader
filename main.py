import yfinance as yf
import requests
import json

# 設定
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 互換モード分析開始 ---")
    
    # 1. 株価データの取得
    data = yf.download(TICKER, period="2y", progress=False)
    current_price = data['Close'].iloc[-1].item()

    # 2. AIへリクエスト
    # モデル名を「gemini-pro」という、最も安定した旧名称に変更しました
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={MY_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"NVIDIAの株価が${current_price:.2f}です。世界情勢から見て今後も熱いか、投資コンサルタントとして150文字で情熱的に分析して。結論は文頭に。"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        # 応答の解析
        if 'candidates' in res_json:
            ai_response = res_json['candidates'][0]['content']['parts'][0]['text']
            # Slack送信
            msg = f"🌍 *【AI分析レポート】*\n*銘柄:* {TICKER}\n*価格:* ${current_price:.2f}\n\n{ai_response}"
            requests.post(MY_SLACK_URL, json={"text": msg})
            print("✅ 成功しました！Slackを確認してください！")
        else:
            # ここでエラーが出たら、Google AI Studio側の設定に問題があります
            print(f"❌ モデルが応答しません: {res_json}")

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
