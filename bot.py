import os
import time
import requests

# خواندن اطلاعات از محیط امن گیت‌هاب
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")


def generate_and_send_zen():
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

  post_text = None

  # ۵ بار تلاش خودکار با تایم‌اوت ۶۰ ثانیه‌ای
  for attempt in range(1, 6):
    print(f"تلاش شماره {attempt} برای دریافت متن از هوش مصنوعی...")
    try:
      # افزایش تایم‌اوت به ۶۰ ثانیه برای جلوگیری از قطع ارتباط زودهنگام
      response = requests.post(url, headers=headers, json=data, timeout=60)

      if response.status_code == 200:
        result_json = response.json()
        post_text = (
            result_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
        if post_text:
          break
      else:
        print(f"خطا در تلاش {attempt}:", response.text)
    except requests.exceptions.Timeout:
      print(
          f"اخطار در تلاش {attempt}: پاسخ سرور بیش از حد طول کشید (Timeout)."
      )
    except Exception as e:
      print(f"خطای شبکه در تلاش {attempt}:", e)

    if attempt < 5:
      print("۱۰ ثانیه صبر می‌کنیم و دوباره تلاش می‌کنیم...")
      time.sleep(10)

  if not post_text:
    print("خطا: پس از ۵ تلاش متوالی، پاسخ مناسبی از هوش مصنوعی دریافت نشد.")
    return

  print("متن ذن با موفقیت تولید شد. در حال ارسال به کانال تلگرام...")

  # ارسال پیام به کانال تلگرام
  tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHANNEL_USERNAME, "text": post_text}

  tg_response = requests.post(tg_url, json=payload, timeout=30)
  if tg_response.status_code == 200:
    print("پست با موفقیت در کانال منتشر شد! 🌿")
  else:
    print("خطا در ارسال به تلگرام:", tg_response.text)


if __name__ == "__main__":
  generate_and_send_zen()
