import yfinance as yf
import requests
import json

# キーとURLはそのまま
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    # 価格取得
    price = yf.download(TICKER, period="1d", progress=False)['Close'].iloc[-1].item()

    # 🌟 変更点：ブラウザで成功した「gemini-3-flash」を直接指定
    # エンドポイントも最新のプレビュー版（v1alpha）を試します
    url = f"https://generativelanguage.googleapis.com/v1alpha/models/gemini-3-flash:generateContent?key={MY_API_KEY}"
    
    prompt = f"伝説の投資家として分析して。NVIDIAの株価が${price:.2f}です。地政学的に今が激熱か150文字で。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload)
        res_data = response.json()

        if 'candidates' in res_data:
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text']
            requests.post(MY_SLACK_URL, json={"text": f"🚀 *【NVDA最新分析】*\n{ai_text}"})
            print("✅ 奇跡の成功！Slackを確認してください！")
        else:
            # 失敗した場合、今度は「どの名前なら使えるか」をリストアップする命令を追加
            print(f"❌ 404回避失敗。応答内容: {res_data}")
            
    except Exception as e:
        print(f"❌ 通信エラー: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
