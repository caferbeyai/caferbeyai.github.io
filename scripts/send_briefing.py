#!/usr/bin/env python3
"""Daily briefing sender - fetches news and emails in Turkish."""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

EMAIL_PASS = "bvmkbpgzfiaagccz"
EMAIL_FROM = "caferbeyai@gmail.com"
EMAIL_TO = "omurdenden@gmail.com"
TODAY = date.today().strftime("%Y-%m-%d")

# News content (manually compiled from sources)
NEWS_CONTENT = {
    "dunya": [
        {
            "baslik": "Zelensky: ABD, Ukrayna'yı Rusya'ya toprak vermeye zorluyor",
            "ozet": "Reuters'a verdiği röportajda Zelensky, Ortadoğu'daki savaşın Ukrayna savaşını etkilediğini söyledi. ABD, Kyiv'i toprak tavizlerine doğru itiyor gibi görünüyor.",
            "link": "https://nos.nl/artikel/2607847"
        },
        {
            "baslik": "BM, Afrikalıların köleliğini 'insanlığa karşı en ağır suç' olarak tanıdı",
            "ozet": "BM, tazminat fonu için özür ve katkı çağrısı yapan tarihi bir kararı onayladı.",
            "link": "https://www.bbc.com/news/articles/cvg06q36052o"
        },
        {
            "baslik": "Trump: İran müzakere istiyor ama korkuyor, Tehran reddediyor",
            "ozet": "İran Dışişleri Bakanı 'şu an müzakere niyetimiz yok' dedi. Beyaz Saray ise savaş hedeflerine neredeyse ulaşıldığını iddia ediyor.",
            "link": "https://www.bbc.com/news/live/cre0vl84qy9t"
        },
        {
            "baslik": "Meta ve YouTube sosyal medya bağımlılığı davasında sorumlu bulundu",
            "ozet": "ABD'de bir kadın 6 milyon dolar tazminat kazandı. Karar yüzlerce benzer dava için emsal teşkil edebilir.",
            "link": "https://www.bbc.com/news/articles/c747x7gz249o"
        },
        {
            "baslik": "Uzun süren Ortadoğu çatışması havacılığı nasıl şekillendirecek?",
            "ozet": "Körfez hub havalimanları ucuz uçuşları mümkün kılmıştı — şimdi gelecekleri belirsiz.",
            "link": "https://www.bbc.com/news/articles/cn08x9lw0pzo"
        }
    ],
    "hollanda": [
        {
            "baslik": "İslamolog Tariq Ramadan 18 yıl hapse mahkum edildi",
            "ozet": "Paris'te üç tecavüz suçlamasından suçlu bulunan Ramadan, 2009-2016 arasında Paris ve Lyon'da kadınlara saldırdı.",
            "link": "https://nos.nl/artikel/2607846"
        },
        {
            "baslik": "BM: Ortadoğu'daki mültecilere daha fazla para lazım",
            "ozet": "İran'daki çatışma devam ederken mülteci ajansı yetersiz fondan bahsediyor.",
            "link": "https://nos.nl/liveblog/2607468"
        },
        {
            "baslik": "Hollanda'da hastane ziyaretinde bir tutuklu daha kaçtı",
            "ozet": "Roermond'daki hastaneden kaçan adam üç güvenlik görevlisini atlatarak firar etti.",
            "link": "https://nos.nl/artikel/2607840"
        },
        {
            "baslik": "Yüksek yakıt fiyatları Hollanda sektörlerini vuruyor",
            "ozet": "Ev bakımı, balıkçılık ve direksiyon dersi verenler İran savaşının yarattığı maliyet artışıyla mücadele ediyor.",
            "link": "https://nos.nl/video/2607829"
        }
    ]
}

def build_html():
    """Build HTML email body."""
    dunya_html = ""
    for item in NEWS_CONTENT["dunya"]:
        dunya_html += f'''<li><a href="{item["link"]}"><strong>{item["baslik"]}</strong></a><br>
        <small>{item["ozet"]}</small></li>\n'''
    
    hollanda_html = ""
    for item in NEWS_CONTENT["hollanda"]:
        hollanda_html += f'''<li><a href="{item["link"]}"><strong>{item["baslik"]}</strong></a><br>
        <small>{item["ozet"]}</small></li>\n'''
    
    html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Günlük Brifing - {TODAY}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px; }}
    h1 {{ border-bottom: 3px solid #e63946; padding-bottom: 10px; }}
    h2 {{ color: #007acc; border-bottom: 2px solid #007acc; padding-bottom: 8px; margin-top: 24px; }}
    a {{ color: #007acc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .footer {{ margin-top: 30px; font-size: 0.9em; color: #666; border-top: 1px solid #ddd; padding-top: 15px; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 12px; }}
    .meta {{ color: #888; font-size: 0.9em; }}
    .blog-link {{ background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0; }}
  </style>
</head>
<body>
  <h1>📰 GÜNLÜK BRİFİNG - {TODAY}</h1>
  <p class="meta">Omurden Cengiz için Caferbey tarafından otomatik oluşturuldu</p>

  <h2>🌍 DÜNYADAN HABERLER</h2>
  <ul>
    {dunya_html}
  </ul>

  <h2>🇳🇱 HOLLANDADAN HABERLER</h2>
  <ul>
    {hollanda_html}
  </ul>

  <div class="blog-link">
    <h3>🤖 CAFFERBEY BLOG</h3>
    <p>Bugünkü günlüğümüz: <a href="https://caferbeyai.github.io/blog/posts/{TODAY}.html">caferbeyai.github.io/blog/posts/{TODAY}.html</a></p>
  </div>

  <div class="footer">
    Caferbey AI tarafından otomatik gönderildi. 🤖<br>
    <small>Kaynaklar: NOS.nl, BBC News</small>
  </div>
</body>
</html>'''
    return html

def send_email():
    """Send email via Gmail SMTP."""
    html_body = build_html()
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📰 Günlük Brifing: {TODAY}"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    
    # Plain text version
    text = f"""GUNLUK BRIFING - {TODAY}

DUNYADAN HABERLER:
- Zelensky: ABD, Ukrayna'yı Rusya'ya toprak vermeye zorluyor
- BM köleliği insanlığa karşı en ağır suç olarak tanıdı
- Trump İran'ın müzakere istediğini iddia ediyor
- Meta ve YouTube bağımlılık davasında sorumlu bulundu

HOLLANDADAN HABERLER:
- İslamolog Tariq Ramadan 18 yıl hapse mahkum edildi
- BM: Ortadoğu'daki mültecilere daha fazla para lazım
- Hollanda'da hastane ziyaretinde tutuklu kaçtı
- Yüksek yakıt fiyatları sektörleri vuruyor

Blog: https://caferbeyai.github.io/blog/posts/{TODAY}.html
"""
    
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"{TODAY} - Briefing sent successfully")
        return True
    except Exception as e:
        print(f"{TODAY} - Error: {e}")
        return False

if __name__ == "__main__":
    send_email()
