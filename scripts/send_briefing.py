#!/usr/bin/env python3
"""Daily briefing: Fetches fresh news from NU.nl and BBC, sends email with Turkish translation."""

import os
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request
from deep_translator import GoogleTranslator

EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

# Initialize translator
nl_to_tr = GoogleTranslator(source='nl', target='tr')
en_to_tr = GoogleTranslator(source='en', target='tr')

def translate_to_turkish(text, lang='nl'):
    """Translate text to Turkish using deep-translator."""
    try:
        if lang == 'nl':
            return nl_to_tr.translate(text)
        else:
            return en_to_tr.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def fetch_nu_news():
    """Fetch latest news from NU.nl RSS feed."""
    try:
        url = "https://www.nu.nl/rss"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        news = []
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for item in items[:10]:
            title_match = re.search(r'<title>(.*?)</title>', item)
            link_match = re.search(r'<link>(.*?)</link>', item)
            if title_match and link_match:
                title = title_match.group(1).strip()
                title = re.sub(r'<!\[CDATA\[|\]\]>', '', title)
                link = link_match.group(1).strip()
                # Translate Dutch to Turkish
                summary = translate_to_turkish(title, 'nl')
                news.append((summary, link))
        
        return news
    except Exception as e:
        print(f"NU.nl fetch error: {e}")
        return []

def fetch_bbc_news():
    """Fetch latest news from BBC RSS feed."""
    try:
        url = "https://feeds.bbci.co.uk/news/rss.xml"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        news = []
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for item in items[:10]:
            title_match = re.search(r'<title>(.*?)</title>', item)
            link_match = re.search(r'<link>(.*?)</link>', item)
            if title_match and link_match:
                title = title_match.group(1).strip()
                title = re.sub(r'<!\[CDATA\[|\]\]>', '', title)
                link = link_match.group(1).strip()
                # Translate English to Turkish
                summary = translate_to_turkish(title, 'en')
                news.append((summary, link))
        
        return news
    except Exception as e:
        print(f"BBC fetch error: {e}")
        return []

def build_email(nu_news, bbc_news):
    """Build HTML email with news."""
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    nu_html = ""
    for summary, link in nu_news:
        nu_html += f'<li><a href="{link}" target="_blank">{summary}</a></li>\n'
    
    bbc_html = ""
    for summary, link in bbc_news:
        bbc_html += f'<li><a href="{link}" target="_blank">{summary}</a></li>\n'
    
    if not nu_news:
        nu_html = "<li>Sistem hatası - NU.nl haberleri alınamadı</li>\n"
    if not bbc_news:
        bbc_html = "<li>Sistem hatası - BBC haberleri alınamadı</li>\n"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 650px; margin: 0 auto; padding: 20px; }}
    h1 {{ border-bottom: 3px solid #e63946; padding-bottom: 10px; }}
    h2 {{ color: #007cc7; border-bottom: 2px solid #007cc7; padding-bottom: 8px; margin-top: 24px; }}
    a {{ color: #007cc7; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 10px; }}
    .footer {{ margin-top: 30px; font-size: 0.85em; color: #666; border-top: 1px solid #ddd; padding-top: 15px; }}
    .meta {{ color: #888; font-size: 0.9em; }}
    .blog-link {{ background: #f0f8ff; padding: 15px; border-radius: 8px; margin-top: 20px; }}
  </style>
</head>
<body>
  <h1>📰 GÜNLÜK BRİFİNG</h1>
  <p class="meta">{date}</p>
  
  <h2>🇳🇱 HOLLANDADAN HABERLER (NU.nl)</h2>
  <ul>
    {nu_html}
  </ul>
  
  <h2>🌍 DÜNYADAN HABERLER (BBC)</h2>
  <ul>
    {bbc_html}
  </ul>
  
  <div class="blog-link">
    <strong>📝 Blog:</strong> <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a>
  </div>
  
  <div class="footer">
    🤖 Caferbey AI tarafından otomatik oluşturuldu<br>
    <small>Kaynaklar: NU.nl, BBC News</small>
  </div>
</body>
</html>"""
    return html

def send_email(html_content):
    """Send email via Gmail SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Caferbey AI <caferbeyai@gmail.com>'
        msg['To'] = 'omurdenden@gmail.com'
        msg['Subject'] = f"📰 Günlük Brifing - {datetime.now().strftime('%Y-%m-%d')}"
        
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('caferbeyai@gmail.com', EMAIL_PASS)
            server.sendmail('caferbeyai@gmail.com', 'omurdenden@gmail.com', msg.as_string())
        
        print(f"✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def main():
    print("📰 Fetching NU.nl news...")
    nu_news = fetch_nu_news()
    print(f"   Found {len(nu_news)} NU.nl articles")
    
    print("🌍 Fetching BBC news...")
    bbc_news = fetch_bbc_news()
    print(f"   Found {len(bbc_news)} BBC articles")
    
    html = build_email(nu_news, bbc_news)
    
    # Save latest for debugging
    with open('/tmp/briefing-latest.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    success = send_email(html)
    
    # Also save log
    log_file = '/home/caferbey/.openclaw/workspace/briefing.log'
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - NU:{len(nu_news)} BBC:{len(bbc_news)} - {'OK' if success else 'FAIL'}\n")

if __name__ == "__main__":
    main()
