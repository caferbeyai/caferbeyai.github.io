#!/usr/bin/env python3
"""Daily briefing: NOS + BBC - Turkish summary with links."""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

NOS_NEWS = [
    ("AZ taraftarları kubbe finali sonrası çılgına döndü. Taraftarlar beklemediği kadar farklı bir galibiyetle sevindi.", "https://nos.nl/video/2611153-az-supporters-uitzinnig-na-winst-bekerfinale"),
    ("İran muhalefeti de Iranlıları tehdit ediyor: Pahlavi'nin 'demokrat' adı altında da baskı var. muhalefet içinde bile ciddi sindirme harekatı sürüyor.", "https://nos.nl/artikel/2611106-iraniers-worden-van-alle-kanten-bedreigd-ook-uit-naam-van-democraat-pahlavi"),
    ("İran yeni görüşmelere katılmıyor • Trump: heyet Islamabad'a gidiyor. Ortadoğu'da sular durulmuyor.", "https://nos.nl/liveblog/2610235-iran-doet-niet-mee-aan-nieuwe-gesprekken-trump-delegatie-onderweg-naar-islamabad"),
    ("Bulgaristan seçimleri: Pro-Rus eski Cumhurbaşkanı Radev zafere koşuyor. Exit poll'e göre %39 oy alıyor.", "https://nos.nl/artikel/2611144-pro-russische-oud-president-radev-stevent-af-op-verkiezingszege-bulgarije"),
    ("Hollanda'da önümüzdeki günler güneşli ve kuru hava. İlkbahar sıcaklıkları artıyor.", "https://nos.nl/artikel/2611143-komende-dagen-veel-zon-en-vrijwel-droog-past-in-trend"),
    ("Groningen Eyaleti çiftçilere karşı suç duyurusunda bulundu. BBB'lı çoğunluk bu hafta bir çiftçinin mülküne el koyma lehinde oy kullandı.", "https://nos.nl/artikel/2611115-provincie-groningen-doet-aangifte-tegen-farmers-defence-force"),
    ("Louisiana'da aile içi kavgadan sonra 8 çocuk öldürüldü. Şüpheli polis tarafından kovalamaca sonrası öldürüldü.", "https://nos.nl/artikel/2611126-acht-kinderen-gedood-bij-schietpartij-in-louisiana-na-huiselijke-ruzie"),
    ("Avrupa Komisyonu yüksek enerji fiyatlarıyla mücadele için sabit evden çalışma günü istiyor.", "https://nos.nl/artikel/2611140-ec-voert-veel-zon-en-vrijwel-droog-op"),
]

BBC_NEWS = [
    ("ABD müzakerecileri Pakistan'a dönüyor — Trump İran'ın altyapısına tehditlerini yineledi. BBC'ye Beyaz Saray'dan bir yetkili ABD heyetinin JD Vance liderliğinde gideceğini söyledi.", "https://www.bbc.com/news/live/cly90l3ln30t"),
    ("Louisiana'da 8 çocuk öldürüldü: 1-14 yaş arası çocuklar, Shreveport'ta aile içi saldırıda hayatını kaybetti.", "https://www.bbc.com/news/articles/c0q9v1p2dd2o"),
    ("Zelensky Biden'ın Rus yaptırımları muafiyetini uzatmasını kınadı. ABD, İran ile savaş nedeniyle enerji krizini hafifletmek için muafiyeti savunuyor.", "https://www.bbc.com/news/articles/c248m3z49j1o"),
    ("Çin'de yarı maraton: İnsanlara karşı robotlar yarıştı. Pekin'de yarışan kazanan robot insan rakiplerini bıraktı.", "https://www.bbc.com/news/videos/cz0e54yrppno"),
    ("Ukrayna polis şefi istifa etti: subaylar ölümcül silahlı saldırıda kaçtıkları iddiasıyla soruşturuluyor.", "https://www.bbc.com/news/articles/c8ejn778j4do"),
    ("Avusturya'da HiPP bebek mamasasında zehirli madde: ailesi ölüm riski konusunda uyarıldı.", "https://www.bbc.com/news/articles/cvg07lq5ql4o"),
    ("Paris'te II. Dünya Savaşı bombasi imha edildi: 450 metre çaplı alandaki sakinler tahliye edildi.", "https://www.bbc.com/news/articles/cwy3r3w4zl8o"),
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
