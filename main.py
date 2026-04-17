import requests
import json

# あなたの最新のキー
MY_API_KEY = 'AQ.Ab8RN6J8Nm--67IcH5cLD2YJiU7fxVRdjqLqbmYdctGU9uF_yQ'

def find_working_model():
    print("--- 調査開始：あなたのキーで使えるモデルを探します ---")
    
    # Googleに「私のキーで使えるモデルを全部教えて」と聞く
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={MY_API_KEY}"
    
    try:
        response = requests.get(url)
        res_data = response.json()
        
        if 'models' in res_data:
            print("✅ 使えるモデルが見つかりました！以下の名前のどれかを使います：")
            for m in res_data['models']:
                # 'models/gemini-...' という名前を表示
                name = m['name'].replace('models/', '')
                print(f"  - {name}")
            print("\nこのリストを教えてください。すぐに修正版を作ります！")
        else:
            print(f"❌ モデルリストの取得に失敗しました。応答: {res_data}")
            
    except Exception as e:
        print(f"❌ 接続エラー: {e}")

if __name__ == "__main__":
    find_working_model()
