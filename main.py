import yfinance as yf
import requests
import json
from datetime import datetime

# ==========================================
# 設定（新しいAPIキーを適用済み）
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6LJeB4ZjawC0bvrZemQMqmSIaNcMm8PyX1a9BnuJAD8Rg'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 世界情勢・直通分析開始 ---")
    
    # 1. 株価データの取得
    try:
        data = yf.download(TICKER, period="2y", progress=False)
        current_price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return

    # 2. AIへ直接リクエスト（最新モデル gemini-1.5-flash を直叩き）
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MY_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
    あなたは世界情勢、金融に精通した「伝説の投資コンサルタント」です。
    現在価格 ${current_price:.2f} の {TICKER} (NVIDIA) について分析してください。
    【視点】AI革命、データセンター需要から見て今「激熱」か。
    結論を「激熱」「買い」「見送り」のいずれかで文頭に書き、200文字程度で情熱的に解説して。
    """
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    # 3. AIに実行させる
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        # AIの返答を取り出す
        if 'candidates' in res_json:
            ai_response = res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"AIエラー応答: {res_json}")
            return

        # 4. Slackへ送信
        msg = (
            f"🌍 *【AI世界情勢分析：NVDA】*\n"
            f"*市場価格:* ${current_price:.2f}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{ai_response}"
        )
        requests.post(MY_SLACK_URL, json={"text": msg})
        print("✅ ついに成功！Slackに通知を飛ばしました！")

    except Exception as e:
        print(f"実行エラー: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
