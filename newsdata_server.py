import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

from flask import Flask

# =========================
# Flask App (keeps port open)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "News bot running"

# =========================
# CONFIG
# =========================


EMAIL_ADDRESS = "kurdishlearner2018@gmail.com"
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# =========================
# Fetch Latest News
# =========================
def get_latest_news():
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "country": "iq",
        "language": "en",
        "q": "Iraq OR Kurdistan"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return "No news found."

    articles = data["results"][:5]

    message = "Latest Iraq & Kurdistan News\n"
    message += "=" * 40 + "\n\n"

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No Title")
        description = article.get("description", "")
        content = article.get("content", "")

        message += f"{i}. {title}\n"
        message += "-" * 40 + "\n"

        if description:
            message += f"{description}\n\n"

        if content:
            message += f"{content}\n\n"

        message += "\n" + "=" * 40 + "\n\n"

    return message

# =========================
# Send Email
# =========================
def send_email():
    news_content = get_latest_news()

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "Iraq & Kurdistan News Update"

    msg.attach(MIMEText(news_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# =========================
# Schedule Every 2 Hours
# =========================
schedule.every(2).hours.do(send_email)

print("bot started...")

while True:
    schedule.run_pending()
    time.sleep(30)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
