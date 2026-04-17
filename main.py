import yfinance as yf
import requests
import json

# URLはこれで合っています！
MY_SLACK_URL = 'https://hooks.slack.com/services/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'
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'
TICKER = "NVDA"

def run_investor_ai():
    print(f"--- {TICKER} Analysis & Slack Test ---")
    
    try:
        data = yf.download(TICKER, period="1d", progress=False)
        price = data['Close'].iloc[-1].item()

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={MY_API_KEY}"
        prompt = f"NVDAの株価${price:.2f}について、情熱的な投資家として100文字で日本語で分析して。"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        ai_res = requests.post(url, json=payload).json()
        analysis = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        slack_payload = {"text": f"🚀 *NVDA Analysis*\nPrice: ${price:.2f}\n\n{analysis}"}
        response = requests.post(MY_SLACK_URL, json=slack_payload)
        
        if response.status_code == 200:
            print("✅ Success! Check your Slack.")
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_investor_ai()
