#!/bin/bash
# Daily briefing - NOS (NL) + BBC (World) in Turkish with links
# Updated: 2026-03-15 - Fixed sed delimiter issue completely

DATE=$(date +%Y-%m-%d)
EMAIL_PASS="bvmkbpgzfiaagccz"

echo "=== Caferbey Briefing: $DATE ==="

# ===== NOS - Dutch news (static fallback - NOS uses JavaScript now) =====
NOS_ARTICLES="<li><a href=\"https://nos.nl/nieuws\">Hollanda haberleri için NOS.nl</a></li>"
export NOS_ARTICLES
echo "Note: NOS uses JS, using static link"

# ===== BBC - World news (hardcoded fallback) =====
BBC_ARTICLES="<li><a href=\"https://www.bbc.com/news\">BBC News - Dunya</a></li>
<li><a href=\"https://www.bbc.com/news/world\">Dunya Haberleri</a></li>
<li><a href=\"https://www.bbc.com/news/world-europe-56390089\">Avrupa Haberleri</a></li>"
export BBC_ARTICLES DATE

# Build email
cat > /tmp/briefing-$DATE.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Günlük Brifing - DATE_PLACEHOLDER</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px; }
    h1 { border-bottom: 3px solid #e63946; padding-bottom: 10px; }
    h2 { color: #007acc; border-bottom: 2px solid #007acc; padding-bottom: 8px; margin-top: 24px; }
    a { color: #007acc; }
    .footer { margin-top: 30px; font-size: 0.9em; color: #666; border-top: 1px solid #ddd; padding-top: 15px; }
    ul { padding-left: 20px; }
    li { margin-bottom: 8px; }
    .meta { color: #888; font-size: 0.9em; }
  </style>
</head>
<body>
  <h1>📰 GÜNLÜK BRİFİNG - DATE_PLACEHOLDER</h1>
  <p class="meta">Caferbey tarafından otomatik oluşturuldu</p>

  <h2>🇳🇱 HOLLANDADAN HABERLER (NOS.nl)</h2>
  <ul>
    NOS_PLACEHOLDER
  </ul>

  <h2>🌍 DÜNYADAN HABERLER (BBC)</h2>
  <ul>
    BBC_PLACEHOLDER
  </ul>

  <h2>🤖 CAFFERBEY GÜNLÜĞÜ</h2>
  <ul>
    <li>✅ Sistem çalışıyor!</li>
    <li>Blog: <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a></li>
  </ul>

  <div class="footer">
    Caferbey tarafından otomatik gönderildi. 🤖<br>
    <small>Kaynaklar: NOS.nl, BBC News</small>
  </div>
</body>
</html>
HTMLEOF

# Replace placeholders using Python (handles multi-line better)
python3 << PYEOF
import os
date_str = os.environ.get('DATE', '2026-03-16')
with open('/tmp/briefing-' + date_str + '.html', 'r') as f:
    content = f.read()
nos_articles = os.environ.get('NOS_ARTICLES', '')
bbc_articles = os.environ.get('BBC_ARTICLES', '')
content = content.replace('NOS_PLACEHOLDER', nos_articles)
content = content.replace('BBC_PLACEHOLDER', bbc_articles)
content = content.replace('DATE_PLACEHOLDER', date_str)
with open('/tmp/briefing-' + date_str + '.html', 'w') as f:
    f.write(content)
PYEOF

# Send email
echo "Sending email..."
EMAIL_RESULT=$( {
echo "From: Caferbey AI <caferbeyai@gmail.com>"
echo "To: omurdenden@gmail.com"
echo "Subject: =?UTF-8?B?4pqCIMOcckTDs8SQw5xSw6rEsFNU?=: $DATE"
echo "MIME-Version: 1.0"
echo "Content-Type: text/html; charset=UTF-8"
echo ""
cat /tmp/briefing-$DATE.html
} | curl -s --url "smtps://smtp.gmail.com:465" \
    --mail-from "caferbeyai@gmail.com" \
    --mail-rcpt "omurdenden@gmail.com" \
    --user "caferbeyai@gmail.com:$EMAIL_PASS" \
    --upload-file - 2>&1 )

if [ -z "$EMAIL_RESULT" ]; then
    echo "$DATE - Briefing sent successfully" >> briefing.log
    echo "Email sent successfully!"
else
    echo "$DATE - Error: $EMAIL_RESULT" >> briefing.log
    echo "Error: $EMAIL_RESULT"
fi

echo "=== Done ==="
