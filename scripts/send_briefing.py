#!/usr/bin/env python3
"""Daily briefing email sender."""

import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Secrets from environment
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
EMAIL_PASS = os.environ.get('EMAIL_PASS', 'bvmkbpgzfiaagccz')

def get_news():
    """Fetch news from local fetch_news.py"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', '/home/caferbey/.openclaw/workspace/scripts/fetch_news.py'],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return {}

def build_html(news):
    """Build HTML email from news data."""
    nos = news.get('nos', ['No data'])
    bbc = news.get('bbc', ['No data'])
    cnn = news.get('cnn', ['No data'])
    reuters = news.get('reuters', ['No data'])
    
    html = f"""<html>
<head>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px; }}
    h2 {{ border-bottom: 2px solid #007acc; padding-bottom: 8px; margin-top: 24px; }}
    .flag {{ font-size: 1.2em; margin-right: 8px; }}
    a {{ color: #007acc; }}
    .footer {{ margin-top: 30px; font-size: 0.9em; color: #666; border-top: 1px solid #ddd; padding-top: 15px; }}
  </style>
</head>
<body>
  <h1>📰 GÜNLÜK BRİFİNG - {datetime.now().strftime('%Y-%m-%d')}</h1>

  <h2>🇳🇱 HOLLANDADAN HABERLER</h2>
  <h3>NOS.nl</h3>
  <ul>
    {''.join(f'<li>{a}</li>' for a in nos)}
  </ul>

  <h2>🌍 DÜNYADAN HABERLER</h2>
  <h3>BBC News</h3>
  <ul>
    {''.join(f'<li>{a}</li>' for a in bbc)}
  </ul>
  <h3>CNN</h3>
  <ul>
    {''.join(f'<li>{a}</li>' for a in cnn)}
  </ul>
  <h3>Reuters</h3>
  <ul>
    {''.join(f'<li>{a}</li>' for a in reuters)}
  </ul>

  <h2>🤖 CAFFERBEY GÜNLÜĞÜ</h2>
  <ul>
    <li>Sistem çalışıyor! Otomatik görevler tamamlandı.</li>
    <li>Blog: <a href='https://caferbeyai.github.io/'>View Blog</a></li>
  </ul>

  <div class='footer'>
    Caferbey tarafından otomatik gönderildi. 🤖<br>
    <small>News from NOS.nl, BBC, CNN, Reuters</small>
  </div>
</body>
</html>"""
    return html

def send_email(html_content):
    """Send email via Gmail SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Caferbey AI <caferbeyai@gmail.com>'
        msg['To'] = 'Omurden <omurdenden@gmail.com>'
        msg['Subject'] = f"📰 Günlük Brifing - {datetime.now().strftime('%Y-%m-%d')}"
        
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('caferbeyai@gmail.com', EMAIL_PASS)
        server.sendmail('caferbeyai@gmail.com', 'omurdenden@gmail.com', msg.as_string())
        server.quit()
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("Fetching news...")
    news = get_news()
    
    print("Building email...")
    html = build_html(news)
    
    print("Sending email...")
    send_email(html)
    
    # Also save to file for reference
    with open('/tmp/briefing-latest.html', 'w') as f:
        f.write(html)
    print("Saved to /tmp/briefing-latest.html")
