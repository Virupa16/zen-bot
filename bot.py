import os
import requests

# خواندن اطلاعات از محیط امن سرور
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")


def generate_and_send_zen():
  print("در حال ارتباط با هوش مصنوعی برای دریافت متن ذن...")

  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"

  headers = {"Content-Type": "application/json"}
  data = {
      "contents": [{
          "parts": [{
              "text": (
                  "تو یک دستیار خردمند ذن هستی. یک پست کوتاه و زیبا برای کانال"
                  " تلگرام شامل موارد زیر بنویس:\n1. یک جمله قصار یا کوآن"
                  " کوتاه از اساتید بزرگ ذن\n2. یک تمثیل یا داستان بسیار کوتاه"
                  " (حداکثر ۴ خط) با لحنی آرام و عمیق\n3. هشتگ‌های مرتبط در"
                  " انتها\nلحن متن باید بسیار آرامش‌بخش، عمیق و بدون حشو باشد."
              )
          }]
      }]
  }

  response = requests.post(url, headers=headers, json=data, timeout=30)
  if response.status_code != 200:
    print("خطا از طرف هوش مصنوعی:", response.text)
    return

  result_json = response.json()
  post_text = (
      result_json.get("candidates", [{}])[0]
      .get("content", {})
      .get("parts", [{}])[0]
      .get("text", "")
  )

  # ارسال به تلگرام
  tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHANNEL_USERNAME, "text": post_text}

  tg_response = requests.post(tg_url, json=payload)
  if tg_response.status_code == 200:
    print("پست با موفقیت در کانال منتشر شد! 🌿")
  else:
    print("خطا در ارسال به تلگرام:", tg_response.text)


if __name__ == "__main__":
  generate_and_send_zen()