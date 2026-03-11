#!/bin/bash
# Daily briefing - Multi-source news fetcher
# Sources: NOS (NL), BBC (World), NTV & Hürriyet (TR)

DATE=$(date +%Y-%m-%d)
EMAIL_PASS="bvmkbpgzfiaagccz"

echo "=== Caferbey Briefing: $DATE ==="

# ===== DUTCH NEWS =====
echo "Fetching NOS.nl..."
NOS_HTML=$(curl -s -L -A "Mozilla/5.0" "https://nos.nl/nieuws/laatste" 2>/dev/null | head -10000)
NOS_ARTICLES=$(echo "$NOS_HTML" | grep -oP '(?<=href="/artikel/)\d+-[^"]+' | head -10 | sed 's/^[0-9]*-//' | sed 's/-/ /g' | head -10 | while read -r line; do 
    [ ${#line} -gt 10 ] && echo "- $line"
done)

# ===== BBC WORLD NEWS =====
echo "Fetching BBC..."
BBC_HTML=$(curl -s -L -A "Mozilla/5.0" "https://www.bbc.com/news/world" 2>/dev/null | head -15000)
BBC_ARTICLES=$(echo "$BBC_HTML" | grep -oP 'data-title="\K[^"]+' | head -10 | while read -r line; do 
    [ ${#line} -gt 10 ] && echo "- $line"
done)

# ===== TURKISH NEWS - NTV =====
echo "Fetching NTV..."
NTV_HTML=$(curl -s -L -A "Mozilla/5.0" "https://www.ntv.com.tr" 2>/dev/null | head -10000)
NTV_ARTICLES=$(echo "$NTV_HTML" | grep -oP 'class="font-semibold leading-6"[^>]*>\K[^<]+' | head -10 | while read -r line; do
    clean=$(echo "$line" | sed 's/&#x27;/'"'"'/g; s/&amp;/\&/g')
    [ ${#clean} -gt 15 ] && echo "- $clean"
done)

# ===== TURKISH NEWS - HÜRRİYET =====
echo "Fetching Hürriyet..."
HURRIYET_HTML=$(curl -s -L -A "Mozilla/5.0" "https://www.hurriyet.com.tr" 2>/dev/null | head -15000)
HURRIYET_ARTICLES=$(echo "$HURRIYET_HTML" | grep -oP '<h3[^>]*>.*?</h3>' | sed 's/<[^>]*>//g' | grep -v '^[[:space:]]*$' | head -10 | while read -r line; do
    [ ${#line} -gt 15 ] && echo "- $line"
done)

# Fallbacks if empty
NOS_ARTICLES=${NOS_ARTICLES:-"- Haber alınamadı"}
BBC_ARTICLES=${BBC_ARTICLES:-"- Haber alınamadı"}
NTV_ARTICLES=${NTV_ARTICLES:-"- Haber alınamadı"}
HURRIYET_ARTICLES=${HURRIYET_ARTICLES:-"- Haber alınamadı"}

# ===== BUILD EMAIL =====
cat > /tmp/briefing-$DATE.html << EOFHTML
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Günlük Brifing - $DATE</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; background: #f0f2f5; margin: 0; padding: 20px; }
    .container { max-width: 720px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden; }
    .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 25px 30px; }
    .header h1 { margin: 0; font-size: 1.8em; }
    .header .meta { opacity: 0.8; font-size: 0.9em; margin-top: 5px; }
    .content { padding: 25px 30px; }
    h2 { color: #1a1a2e; border-bottom: 2px solid #e63946; padding-bottom: 8px; margin: 25px 0 15px; font-size: 1.2em; }
    h2:first-of-type { margin-top: 0; }
    .flag { margin-right: 8px; }
    ul { padding-left: 20px; margin: 0; }
    li { margin-bottom: 10px; color: #333; }
    .caferbey-box { background: #f8f9fa; border-left: 4px solid #007acc; padding: 15px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
    .caferbey-box ul { padding-left: 0; list-style: none; }
    .caferbey-box li { margin-bottom: 8px; }
    .caferbey-box li:before { content: "✓ "; color: #007acc; font-weight: bold; }
    .footer { background: #f8f9fa; padding: 20px 30px; border-top: 1px solid #e9ecef; font-size: 0.85em; color: #6c757d; }
    .source-note { font-size: 0.8em; color: #adb5bd; margin-top: 5px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📰 Günlük Brifing</h1>
      <div class="meta">$DATE • Caferbey AI</div>
    </div>
    
    <div class="content">
      <h2><span class="flag">🇳🇱</span>Hollanda (NOS.nl)</h2>
      <ul>
      $NOS_ARTICLES
      </ul>

      <h2><span class="flag">🇬🇧</span>Dünya (BBC News)</h2>
      <ul>
      $BBC_ARTICLES
      </ul>

      <h2><span class="flag">🇹🇷</span>Türkiye (NTV)</h2>
      <ul>
      $NTV_ARTICLES
      </ul>

      <h2><span class="flag">🇹🇷</span>Türkiye (Hürriyet)</h2>
      <ul>
      $HURRIYET_ARTICLES
      </ul>

      <div class="caferbey-box">
        <strong>🤖 Caferbey Günlüğü</strong>
        <ul>
          <li>Sistem çalışıyor - Otomatik briefing aktif</li>
          <li>Blog yazıları tamamen geri yüklendi (20 Şubat'tan beri)</li>
          <li>Blog: <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a></li>
        </ul>
      </div>
    </div>

    <div class="footer">
      <strong>Caferbey</strong> tarafından otomatik gönderildi 🤖
      <div class="source-note">Kaynaklar: NOS.nl • BBC News • NTV • Hürriyet</div>
    </div>
  </div>
</body>
</html>
EOFHTML

# ===== SEND EMAIL =====
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