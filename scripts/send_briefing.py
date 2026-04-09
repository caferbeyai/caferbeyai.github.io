#!/usr/bin/env python3
"""Daily briefing: NOS + BBC - Turkish summary with links."""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

NOS_NEWS = [
    ("ABD ve İran 2 haftalık ateşkes ve Hormuz Boğazı'nın yeniden açılması konusunda anlaştı. İran, saldırılar durdurulursa boğazı açmayı kabul etti.", "https://nos.nl/artikel/2609553-vs-en-iran-akkoord-over-staakt-het-vuren-van-2-weken-straat-hormuz-gaat-weer-open"),
    ("Rutte Trump'ın yanına gidiyor - Weski davasında pleymoya başvurulacak.", "https://nos.nl/artikel/2609559-wekdienst-8-4-rutte-langs-bij-trump-pleidooi-in-zaak-tegen-inez-weski"),
    ("Tour of Vlaanderen'de kırmızı ışık ihlali yapan 54 bisikletçi tespit edildi. Para cezası 400-5000 euro arasında.", "https://nos.nl/artikel/2609557-54-wielrenners-opgespoord-die-rood-licht-negeerden-tijdens-ronde-van-vlaanderen"),
    ("Irak'ta kaçırılan Amerikalı gazeteci serbest bırakıldı. Kittleson 31 Mart'ta Bağdat'ta bir İran yanlısı milis tarafından alınmıştı.", "https://nos.nl/artikel/2609556-in-irak-ontvoerde-amerikaanse-journalist-vrijgelaten"),
    ("Helmond'daki bir mezbahada iş kazası: bir işçi hayatını kaybetti. Çalışma Denetimi soruşturma başlattı.", "https://nos.nl/artikel/2609555-medewerker-van-slachthuis-in-helmond-overleden-bij-bedrijfsongeval"),
    ("Janine Abbring, Zomergasten'ın son sezonunu sunacak. Programı daha önce 2017-2022 arasında da sunmuştu.", "https://nos.nl/artikel/2609554-janine-abbring-presenteert-laatste-seizoen-zomergasten"),
    ("Berendsen ve Van Weel ilk AB dışı ziyaret olarak Fas'a gitti. Fas ile ilişkiler yeni hükümet için stratejik öneme sahip.", "https://nos.nl/artikel/2609552-berendsen-en-van-weel-in-marokko-onderstreept-goede-banden"),
]

BBC_NEWS = [
    ("İran ve ABD koşullu 2 haftalık ateşkes ve Hormuz Boğazı'nın açılması konusunda anlaştı. Pakistan Cuma günü tarafları bir araya getirecek. İsrail ateşkesi desteklediğini ama 'Lübnan'ı kapsamadığını söyledi.", "https://www.bbc.com/news/live/c5yw4g3z7qgt"),
    ("Trump: İran ateşkesi kısmi bir zafer ama yüksek maliyetle. Petrol fiyatları ateşkes haberiyle düştü.", "https://www.bbc.com/news/articles/cwyvp55xrlro"),
    ("Pakistan İran ve ABD arasındaki ateşkesi nasıl sağladı? Tarihsel bağlar ve karmaşık süreç anlatılıyor.", "https://www.bbc.com/news/articles/cj401qvgg19o"),
    ("Trump destekli Cumhuriyetçi Clay Fuller, Marjorie Taylor Greene'in boşalan koltuğu için yapılan seçimleri kazandı.", "https://www.bbc.com/news/articles/c8r40erdj6mo"),
    ("İran Savaşı: Hormuz Boğazı neden bu kadar önemli? Küresel petrol ticaretinin %20'si bu geçişten yapılıyor.", "https://www.bbc.com/news/articles/c78n6p09pzno"),
    ("Trump savunma bütçesi için 1.5 trilyon dolar istiyor, iç harcama kesintileriyle dengelenmesi planlanıyor.", "https://www.bbc.com/news/articles/crr1q4kjvn2o"),
    ("Macaristan'da 9 gün sonra seçimler: Orbán 16 yıl sonra yeniden sandıkta.", "https://www.bbc.com/news/articles/czd7y1n3jyjo"),
    ("Küba, ABD baskısı altında 2.000'den fazla mahkumu serbest bırakmaya başladı.", "https://www.bbc.com/news/articles/cwy3r3w4zl8o"),
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
