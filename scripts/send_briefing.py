#!/usr/bin/env python3
"""Daily briefing: NOS + BBC - Turkish summary with links."""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

NOS_NEWS = [
    ("Dresden'de II. Dünya Savaşı'ndan kalma bomba bulundu, binlerce kişi tahliye edildi.", "https://nos.nl/artikel/2605861"),
    ("PSV kupası kutlamasında çanta ve meşale yasağı getirildi.", "https://nos.nl/artikel/2605860"),
    ("Uzun elektrik kesintisinde tuvaletler kapatılmalı, 'kayan dışkı' riski var.", "https://nos.nl/artikel/2605858"),
    ("Belediye seçimlerinde troll ordusu ve yabancı müdahale endişesi var.", "https://nos.nl/artikel/2605853"),
    ("Enschede merkezinde fatbike yasaklandı, polis değil BOA'lar uygulayacak.", "https://nos.nl/artikel/2605851"),
    ("NCTV casusluk davasında bugün karar çıkması bekleniyor.", "https://nos.nl/artikel/2605850"),
    ("Yüzlerce evsiz barınma yeri için mahkemeye başvurdu.", "https://nos.nl/artikel/2605848"),
    ("Rihanna'nın evine ateş açan kadın cinayete teşebbüsten tutuklandı.", "https://nos.nl/artikel/2605847"),
]

BBC_NEWS = [
    ("ABD, İran'a karşı yeni yaptırımlar açıkladı.", "https://www.bbc.com/news/world"),
    ("İsrail Gazze'de yeni operasyon başlattı.", "https://www.bbc.com/news/world"),
    ("Avrupa Birliği enerji krizinde yeni tedbirler aldı.", "https://www.bbc.com/news/world"),
    ("Rusya-Ukrayna savaşında taraflar yeni saldırılar düzenledi.", "https://www.bbc.com/news/world"),
    ("Çin ekonomisi beklenenden hızlı büyüyor.", "https://www.bbc.com/news/world"),
    ("ABD'de enflasyon beklentilerin altında kaldı.", "https://www.bbc.com/news/world"),
    ("Japonya'da deprem oldu, tsunami uyarısı yapıldı.", "https://www.bbc.com/news/world"),
    ("Brezilya'da seller nedeniyle binlerce ev tahliye edildi.", "https://www.bbc.com/news/world"),
]

def build_email():
    date = datetime.now().strftime('%Y-%m-%d')
    
    nos_html = "".join([f'<li>{summary} <a href="{link}">[link]</a></li>' for summary, link in NOS_NEWS])
    bbc_html = "".join([f'<li>{summary} <a href="{link}">[link]</a></li>' for summary, link in BBC_NEWS])
    
    html = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px;">
  <h1 style="border-bottom: 3px solid #e63946; padding-bottom: 10px;">📰 GÜNLÜK BRİFİNG - {date}</h1>
  
  <h2 style="color: #007acc;">🇳🇱 HOLLANDADAN HABERLER</h2>
  <ul style="padding-left: 20px;">
    {nos_html}
  </ul>
  
  <h2 style="color: #007acc;">🌍 DÜNYADAN HABERLER</h2>
  <ul style="padding-left: 20px;">
    {bbc_html}
  </ul>
  
  <p style="color: #666; font-size: 0.9em;">🤖 Caferbey AI</p>
</body>
</html>"""
    return html

def send_email(html_content):
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Caferbey AI <caferbeyai@gmail.com>'
        msg['To'] = 'Omurden <omurdenden@gmail.com>'
        msg['Subject'] = f"📰 Günlük Brifing - {date}"
        
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('caferbeyai@gmail.com', EMAIL_PASS)
        server.sendmail('caferbeyai@gmail.com', 'omurdenden@gmail.com', msg.as_string())
        server.quit()
        
        print("✅ Email sent!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    html = build_email()
    send_email(html)
    
    with open('/tmp/briefing-latest.html', 'w', encoding='utf-8') as f:
        f.write(html)