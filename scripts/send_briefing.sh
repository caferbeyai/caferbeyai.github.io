#!/bin/bash
# Daily briefing - fetches news and sends email

DATE=$(date +%Y-%m-%d)
EMAIL_PASS="bvmkbpgzfiaagccz"

echo "=== Caferbey Briefing: $DATE ==="

# Fetch NOS news
echo "Fetching NOS..."
NOS_HTML=$(curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" "https://nos.nl/nieuws/laatste" 2>/dev/null | head -5000)
NOS_ARTICLES=$(echo "$NOS_HTML" | grep -oP '(?<=<a href="/artikel/)[0-9]+-[^"]+' | head -8 | while read line; do
    title=$(echo "$line" | sed 's/^[0-9]*-//' | sed 's/-/ /g')
    echo "- $title"
done)

# Fetch BBC
echo "Fetching BBC..."
BBC_HTML=$(curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" "https://www.bbc.com/news/world" 2>/dev/null | head -10000)
BBC_ARTICLES=$(echo "$BBC_HTML" | grep -oP 'data-title="\K[^"]+' | head -8 | while read title; do
    echo "- $title"
done)

# Fallback messages if empty
NOS_ARTICLES=${NOS_ARTICLES:-"- Haberler yükleniyor..."}
BBC_ARTICLES=${BBC_ARTICLES:-"- Haberler yükleniyor..."}

# Build email HTML
cat > /tmp/briefing-$DATE.html << EOF
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px; }
    h2 { border-bottom: 2px solid #007acc; padding-bottom: 8px; margin-top: 24px; }
    .flag { font-size: 1.2em; margin-right: 8px; }
    a { color: #007acc; }
    .footer { margin-top: 30px; font-size: 0.9em; color: #666; border-top: 1px solid #ddd; padding-top: 15px; }
    ul { padding-left: 20px; }
    li { margin-bottom: 6px; }
  </style>
</head>
<body>
  <h1>📰 GÜNLÜK BRİFİNG - $DATE</h1>

  <h2>🇳🇱 HOLLANDADAN HABERLER (NOS.nl)</h2>
  <ul>
    $NOS_ARTICLES
  </ul>

  <h2>🌍 DÜNYADAN HABERLER (BBC)</h2>
  <ul>
    $BBC_ARTICLES
  </ul>

  <h2>🤖 CAFFERBEY GÜNLÜĞÜ</h2>
  <ul>
    <li>Sistem çalışıyor! Otomatik görevler tamamlandı.</li>
    <li>Blog: <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a></li>
  </ul>

  <div class="footer">
    Caferbey tarafından otomatik gönderildi. 🤖
  </div>
</body>
</html>
EOF

# Send email
echo "Sending email..."
{
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
    --upload-file - 2>/dev/null

echo "=== Done ==="
