import requests

# あなたのSlack URL（これが正しいか今一度確認！）
MY_SLACK_URL = 'Https://hooks.slack.com/services/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'

def test_slack():
    print("--- Slack送信テスト開始 ---")
    payload = {"text": "🎉 テスト送信成功！ついに繋がりました！"}
    response = requests.post(MY_SLACK_URL, json=payload)
    
    if response.status_code == 200:
        print("✅ Slack側が『受け取ったよ！』と言っています。届いているはずです！")
    else:
        print(f"❌ Slack側で拒否されました。エラーコード: {response.status_code}")
        print(f"理由: {response.text}")

if __name__ == "__main__":
    test_slack()
