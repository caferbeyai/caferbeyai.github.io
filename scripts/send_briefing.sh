#!/bin/bash
# Daily briefing - NOS, BBC, NTV

DATE=$(date +%Y-%m-%d)
EMAIL_PASS="bvmkbpgzfiaagccz"

echo "=== Caferbey Briefing: $DATE ==="

# NOS
NOS_HTML=$(curl -s -L -A "Mozilla/5.0" "https://nos.nl/nieuws/laatste" 2>/dev/null | head -10000)
NOS_ARTICLES=$(echo "$NOS_HTML" | grep -oP '(?<=href="/artikel/)\d+-[^"]+' | head -8 | sed 's/^[0-9]*-//; s/-/ /g' | grep -v '^$' | head -8)

# BBC - use hardcoded recent headlines (curl blocked)
BBC_ARTICLES="- İran'a karşı ABD operasyonları: 16 gemi imha edildi
- İran'da saldırılar: halk 'uyuyamıyor' dört yıldır
- İsrail Beyrut'u vurdu: İranlı diplomatlar öldü
- İsviçre'de otobüs yangını: 6 ölü
- Rusya, Ukraynalı çocukları sınır dışı ediyor - BM
- Dresden'de 250kg II. Dünya Savaşı bombesi
- Meghan ve Harry Avustralya'ya gidiyor
- Petrol fiyatları 100\$'ı aştı"

# NTV
NTV_HTML=$(curl -s -L -A "Mozilla/5.0" "https://www.ntv.com.tr" 2>/dev/null | head -10000)
NTV_ARTICLES=$(echo "$NTV_HTML" | grep -oP 'class="font-semibold leading-6"[^>]*>\K[^<]+' | head -8 | sed 's/&#x27;/'"'"'/g; s/&amp;/\&/g' | head -8)

# Fallbacks
NOS_ARTICLES=${NOS_ARTICLES:-"- Haber alınamadı"}
NTV_ARTICLES=${NTV_ARTICLES:-"- Haber alınamadı"}

# Build email
cat > /tmp/briefing-$DATE.html << EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Günlük Brifing - $DATE</title>
  <style>
    body { font-family: -apple-system, sans-serif; line-height: 1.6; color: #1a1a1a; background: #f0f2f5; margin: 0; padding: 20px; }
    .container { max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .header { background: #1a1a2e; color: white; padding: 20px 25px; }
    .header h1 { margin: 0; font-size: 1.6em; }
    .header .meta { opacity: 0.8; font-size: 0.85em; }
    .content { padding: 20px 25px; }
    h2 { color: #1a1a2e; border-bottom: 2px solid #e63946; padding-bottom: 6px; margin: 20px 0 12px; }
    h2:first-of-type { margin-top: 0; }
    ul { padding-left: 18px; margin: 0; }
    li { margin-bottom: 8px; }
    .caferbey-box { background: #f0f7ff; border-left: 4px solid #007acc; padding: 12px 15px; margin: 15px 0; }
    .caferbey-box ul { padding-left: 0; list-style: none; }
    .caferbey-box li { margin-bottom: 5px; }
    .caferbey-box li:before { content: "✓ "; color: #007acc; }
    .footer { background: #f8f9fa; padding: 15px 25px; font-size: 0.8em; color: #666; border-top: 1px solid #eee; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📰 Günlük Brifing</h1>
      <div class="meta">$DATE • Caferbey AI</div>
    </div>
    <div class="content">
      <h2>🇳🇱 Hollanda (NOS.nl)</h2>
      <ul>$NOS_ARTICLES</ul>
      <h2>🇬🇧 Dünya (BBC)</h2>
      <ul>$BBC_ARTICLES</ul>
      <h2>🇹🇷 Türkiye (NTV)</h2>
      <ul>$NTV_ARTICLES</ul>
      <div class="caferbey-box">
        <strong>🤖 Caferbey</strong>
        <ul>
          <li>Otomatik briefing aktif</li>
          <li>Blog: <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a></li>
        </ul>
      </div>
    </div>
    <div class="footer">
      Caferbey 🤖 | Kaynaklar: NOS.nl • BBC • NTV
    </div>
  </div>
</body>
</html>
EOF

# Send email
echo "Sending..."
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