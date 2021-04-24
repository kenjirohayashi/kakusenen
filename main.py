import automate
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 本番用トークンID
API_TOKEN = os.environ.get("KAKUSENEN_SLACK_API_TOKEN")
CHANNEL_ID = os.environ.get("KAKUSENEN_SLACK_CHANNEL_ID")

client = WebClient(token=API_TOKEN)

CHECK_URL = "https://my-site-105399-105686.square.site/s/appointments"


# 通知を送信する関数を定義
def send_slack_notification(message):
    try:
        # Slackへの通知を送信
        response = client.chat_postMessage(channel=CHANNEL_ID, text=message)
        # 通知が正常に送信されたかを確認
        if not response["ok"]:
            print("Slack通知の送信に失敗しました")
    except SlackApiError as e:
        print(f"Slack APIエラー: {e.response['error']}")


def handler(request):
    # seleniumに関するinstance生成を行う。
    driver = automate.Selenium()

    try:
        # Webページを開く
        driver.access(CHECK_URL)
        # ページ読み込みのために遅延させる。
        driver.stop(10)

        # ページのHTMLを取得
        div_element = driver.find_element(By.CSS_SELECTOR, 'div[class*="18-0-7NNp1l"]')
        h3_element = div_element.find_element(By.CSS_SELECTOR, 'h3')
        text = h3_element.text.strip()

        # 以前の結果をファイルから読み込む
        with open('previous_result.txt', 'r') as f:
            previous_result = f.read().strip()

        # 現在の結果と以前の結果を比較して通知を送信
        if text != previous_result:
            message = f"予約の受付が開始されました\n{url}"
            send_slack_notification(message)

        # 現在の結果をファイルに保存
        with open('previous_result.txt', 'w') as f:
            f.write(text)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        driver.quit()
