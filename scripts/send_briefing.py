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

NEWS_CONTENT = {
    "dunya": [
        {
            "baslik": "Houthis İsrail'e ikinci füze saldırısı başlattı, saldırılara devam sözü verdi",
            "ozet": "Yemen'in Husileri İsrail'e ikinci füze saldırısı düzenledi. Yemen hükümeti İran'ı ülkeyi savaşa 'sürüklemekle' suçluyor.",
            "link": "https://www.bbc.com/news/live/cje4x38q8xqt"
        },
        {
            "baslik": "Trump'ın içgüdüye dayalı savaş politikası işe yaramıyor",
            "ozet": "BBC analizine göre, İran'daki çatışmada Trump'ın gut-instinct yaklaşımı etkili olmuyor. Bir aydan fazla zaman geçmesine rağmen sonuç belirsiz.",
            "link": "https://www.bbc.com/news/articles/c5y969pnxgvo"
        },
        {
            "baslik": "ABD genelinde 'No Kings' protestoları Trump'a karşı düzenlendi",
            "ozet": "Minnesota'daki protestoda şarkıcı Bruce Springsteen sahne aldı. Trump yönetiminin politikalarına karşı büyüyen bir hareket.",
            "link": "https://www.bbc.com/news/articles/cq8wy7g1gd1o"
        },
        {
            "baslik": "22 göçmen Yunanistan açıklarında altı gün denizde kaldıktan sonra öldü",
            "ozet": "Hayatta kalanlar, ölen yolcuları denize atmek zorunda kaldıklarını söyledi. трагедия Akdeniz'deki göçmen krizini gözler önüne seriyor.",
            "link": "https://www.bbc.com/news/articles/cnv8z1lvn8ro"
        },
        {
            "baslik": "Mısır'da dükkan ve restoranlara enerji krizi nedeniyle erken kapanma emri",
            "ozet": "Orta Doğu çatışmasıyla bağlantılı olarak Mısır'da enerji krizi derinleşiyor. Yetkililer dükkan ve restoranların erken kapanmasını istedi.",
            "link": "https://www.bbc.com/news/articles/c0rxz7ggv8go"
        },
        {
            "baslik": "Bank of America, Epstein davası nedeniyle 72.5 milyon dolar ödeyecek",
            "ozet": "Bankanın Jeffrey Epstein'ın insan ticareti operasyonunu kolaylaştırdığı iddiasıyla açılan davayı kabul etmeden ödeme yapmayı kabul etti.",
            "link": "https://www.bbc.com/news/articles/cn2vj36yd12o"
        },
        {
            "baslik": "Londra'da aşırı sağcılığa karşı binlerce kişi yürüdü",
            "ozet": " 'Irkçılıkla değil cehaletle mücadele edin' ve 'Göçmenin yanında yaşamayı, Reform UK milletvekili yanında yaşamaktan daha çok tercih ederim' pankartları taşındı.",
            "link": "https://www.bbc.com/news/articles/cm2rn03ryz8o"
        }
    ],
    "hollanda": [
        {
            "baslik": "Yaz saati başladı — saatler bir saat ileri alındı",
            "ozet": "Hollanda bu hafta sonu yaz saatine geçti. İlkbahar ve yaz aylarında sabahları daha uzun süre karanlık, akşamları ise daha uzun süre aydınlık oluyor.",
            "link": "https://nos.nl/artikel/2608222"
        },
        {
            "baslik": "Zierikzee yakınlarında genç kadın kaza sonucu hayatını kaybetti",
            "ozet": "Zierikzee ile Nieuwerkerk arasında üç araç bilinmeyen nedenle çarpıştı. Kaza sonucu genç bir kadın hayatını kaybetti.",
            "link": "https://nos.nl/artikel/2608232"
        },
        {
            "baslik": "En az yedi megadatamerkez inşaatı siyasi muhalefete rağmen devam ediyor",
            "ozet": "Hem ulusal hem yerel siyaset büyük veri merkezlerine karşı çıkıyor, ancak yeni kurallar önümüzdeki yıllarda megadatamerkez sayısının en az ikiye katlanmasını engellemeyecek.",
            "link": "https://nos.nl/artikel/2608192"
        },
        {
            "baslik": "Paris'te Bank of America'ya bombalı saldırı engellendi, İran savaşıyla bağlantılı",
            "ozet": "17 yaşında bir genç gözaltına alındı. Yetkililer olayın devam eden İran savaşıyla bağlantılı olduğunu söylüyor.",
            "link": "https://nos.nl/artikel/2608196"
        },
        {
            "baslik": "Donör kuruluşları doğurganlık klinikleri hakkında ulusal soruşturma istiyor",
            "ozet": "Hatalar yapan klinikler hakkında daha fazla hikaye ortaya çıkıyor. Donör kuruluşları ulusal çapta bir soruşturma istiyor.",
            "link": "https://nos.nl/artikel/2608184"
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
    
    text = f"""GUNLUK BRIFING - {TODAY}

DUNYADAN HABERLER:
- Houthis İsrail'e ikinci füze saldırısı başlattı
- Trump'ın içgüdüye dayalı savaş politikası işe yaramıyor
- ABD genelinde 'No Kings' protestoları düzenlendi
- 22 göçmen Yunanistan açıklarında öldü
- Mısır'da enerji krizi nedeniyle dükkanlara erken kapanma emri
- Bank of America Epstein davası için 72.5 milyon dolar ödeyecek
- Londra'da binlerce kişi aşırı sağcılığa karşı yürüdü

HOLLANDADAN HABERLER:
- Yaz saati başladı, saatler ileri alındı
- Zierikzee yakınlarında genç kadın kaza sonucu öldü
- Megadatamerkez inşaatı siyasi muhalefete rağmen devam ediyor
- Paris'te bombalı saldırı engellendi
- Donör kuruluşları doğurganlık klinikleri soruşturması istiyor

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
