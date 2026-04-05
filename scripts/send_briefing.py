#!/usr/bin/env python3
"""Daily briefing: NOS + BBC - Turkish summary with links."""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

NOS_NEWS = [
    ("Megastar'lar konser için tek bir yerde toplanıyor: 'Hayranlar için çok az avantaj' - Harry Styles bu yıl Amsterdam'da on kez sahne alacak.", "https://nos.nl/artikel/2609009-megasterren-kiezen-voor-concerten-op-een-plek-weinig-voordelen-voor-fans"),
    ("Wekdienst 4/4: BM İran üzerinde oylama yapabilir • PSV sahaya çıkıyor.", "https://nos.nl/artikel/2609005-wekdienst-4-4-vn-stemt-mogelijk-over-iran-bijna-kampioen-psv-in-actie"),
    ("Isınan gaz fiyatlarıyla ısı pompaları yeniden ilgi görüyor.", "https://nos.nl/artikel/2609004-warmtepompen-weer-in-trek-door-gestegen-gasprijzen-mensen-wakker-geschud"),
    ("Papa Leo, Good Friday'de Haç taşıdı - on yıllardır ilk kez bir Papa.", "https://nos.nl/artikel/2609003-paus-leo-draagt-kruis-tijdens-goede-vrijdag-kruisweg-eerste-paus-in-tientallen-jaren"),
    ("Nijkerk'te İsrail merkezi yakınında patlama, 'hasar sınırlı kaldı'.", "https://nos.nl/artikel/2609000-explosie-bij-israelcentrum-in-nijkerk-schade-beperkt-gebleven"),
    ("İran hava savunması ABD savaş uçağını düşürdü, mürettebat aranıyor.", "https://nos.nl/artikel/2608991-bemanningslid-neergehaald-amerikaans-gevechtsvliegtuig-gered-zoekactie-nog-gaande"),
    ("Fransız savcılık, ırkçı yorumlar nedeniyle TV kanalı hakkında soruşturma başlattı.", "https://nos.nl/artikel/2608999-frans-om-begint-onderzoek-naar-tv-zender-om-mogelijk-racistische-opmerkingen"),
]

BBC_NEWS = [
    ("İran ve ABD, düşürülen savaş uçağındaki kayıp Amerikalı mürettebatı arıyor.", "https://www.bbc.com/news/live/cm29zmpdj3vt"),
    ("Macaristan'da 16 yıl sonra Orbán yeniden sandıkta - seçimler 9 gün sonra.", "https://www.bbc.com/news/articles/czd7y1n3jyjo"),
    ("Trump savunma için 1.5 trilyon dolar istiyor, iç harcama kesintileriyle birlikte.", "https://www.bbc.com/news/articles/crr1q4kjvn2o"),
    ("Küba, ABD baskısı altında 2.000'den fazla mahkumu serbest bırakmaya başladı.", "https://www.bbc.com/news/articles/cwy3r3w4zl8o"),
    ("ABD, Afrika kökenli sekiz kişiyi Uganda'ya sınır dışı etti.", "https://www.bbc.com/news/articles/c8ej43z8yw4o"),
    ("İtalya'nın ünlü Uffizi galerisi siber saldırı iddialarını kabul etti ama güvenlik ihlali reddetti.", "https://www.bbc.com/news/articles/cy51wzeq6g5o"),
    ("Pete Hegseth ABD Ordusu'nun en üst düzey generalini istifaya çağırdı.", "https://www.bbc.com/news/articles/cn8d63v058zo"),
    ("Burkina Faso'nun askeri lideri: 'Demokrasiyi unutun' dedi.", "https://www.bbc.com/news/articles/cly0zp1xgz3o"),
]

def build_email():
    date = datetime.now().strftime('%Y-%m-%d')
    
    nos_html = "".join([f'<li>{summary} <a href="{link}">[link]</a></li>' for summary, link in NOS_NEWS])
    bbc_html = "".join([f'<li>{summary} <a href="{link}">[link]</a></li>' for summary, link in BBC_NEWS])
    
    html = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px;">
  <h1 style="border-bottom: 3px solid #e63946; padding-bottom: 10px;">📰 GÜNLÜK BRİFİNG - {date}</h1>
  
  <h2 style="color: #007cc7;">🇳🇱 HOLLANDADAN HABERLER</h2>
  <ul style="padding-left: 20px;">
    {nos_html}
  </ul>
  
  <h2 style="color: #007cc7;">🌍 DÜNYADAN HABERLER</h2>
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
