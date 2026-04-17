import yfinance as yf
import requests
import json

# ==========================================
# 設定（New Projectで作成した最新キーを適用）
# ==========================================
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'
TICKER = "NVDA"

def run_omni_wealth_ai():
    print(f"--- {TICKER} 世界情勢・最終分析開始 ---")
    
    # 1. 株価データの取得
    try:
        data = yf.download(TICKER, period="2y", progress=False)
        current_price = data['Close'].iloc[-1].item()
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return

    # 2. AIへ直接リクエスト（最も安定した v1 エンドポイントを使用）
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={MY_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
    あなたは金融と地政学に精通した投資コンサルタントです。
    現在価格 ${current_price:.2f} の {TICKER} (NVIDIA) について、最新の世界情勢（AI需要、半導体規制など）を踏まえて分析してください。
    結論を「激熱」「買い」「見送り」のいずれかで文頭に書き、150文字〜200文字程度で情熱的に解説して。
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
        
        # AIの返答を抽出
        if 'candidates' in res_json:
            ai_response = res_json['candidates'][0]['content']['parts'][0]['text']
            
            # 4. Slackへ送信
            msg = (
                f"🌍 *【AI世界情勢分析：NVDA】*\n"
                f"*最新株価:* ${current_price:.2f}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"{ai_response}"
            )
            requests.post(MY_SLACK_URL, json={"text": msg})
            print("✅ ついに成功！Slackに通知を飛ばしました！")
        else:
            # エラー内容を詳細に表示
            print(f"❌ AIが応答を拒否しました。理由: {res_json}")

    except Exception as e:
        print(f"実行中に重大なエラーが発生しました: {e}")

if __name__ == "__main__":
    run_omni_wealth_ai()
