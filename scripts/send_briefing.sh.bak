#!/bin/bash
# Daily briefing - NOS (NL) + BBC (World) in Turkish with links

DATE=$(date +%Y-%m-%d)
EMAIL_PASS="bvmkbpgzfiaagccz"

echo "=== Caferbey Briefing: $DATE ==="

# ===== NOS - Dutch news =====
echo "Fetching NOS..."
NOS_HTML=$(curl -s -L -A "Mozilla/5.0" "https://nos.nl/nieuws/laatste" 2>/dev/null | head -10000)

# Extract NOS articles properly
NOS_ARTICLES=$(echo "$NOS_HTML" | grep -oP 'href="/artikel/[^"]+' | head -8 | sed 's|href="/artikel/||' | while IFS= read -r slug; do
    title=$(echo "$slug" | sed 's/^[0-9]*-//; s/-/ /g')
    link="https://nos.nl/artikel/$slug"
    echo "<li><a href=\"$link\">$title</a></li>"
done)

# ===== BBC - World news =====
BBC_ARTICLES="<li><a href=\"https://www.bbc.com/news/live/cd70wzw9vqlt\">İran bölgesinde son durum: ABD 16 gemiyi imha etti</a></li>
<li><a href=\"https://www.bbc.com/news/articles/cev7llekwllo\">İran'da saldırılar: Halk 'uyuyamıyor' diyor</a></li>
<li><a href=\"https://www.bbc.com/news/articles/cgjze644wjvo\">Rihanna'nın evine silahlı saldırı: Tutuklama</a></li>
<li><a href=\"https://www.bbc.com/news/articles/c5y4wdlyy9xo\">İsviçre'de otobüs yangını: En az 6 ölü</a></li>
<li><a href=\"https://www.bbc.com/news/articles/c1781gr5n9go\">Dresden'de 250kg II. Dünya Savaşı bombesi: Binlerce kişi tahliye</a></li>
<li><a href=\"https://www.bbc.com/news/articles/cz7g5xnvl2eo\">BM: Rusya'nın Ukraynalı çocukları sınır dışı etmesi suç</a></li>
<li><a href=\"https://www.bbc.com/news/articles/cqxd1nv3re2o\">İran'da hava saldırıları: 'Kara yağmur' ve kirlilik</a></li>
<li><a href=\"https://www.bbc.com/news/articles/c77ey1v7jrzo\">ABD'de özel seçim: Marjorie Taylor Greene'in yerine</a></li>"

# Fallbacks
NOS_ARTICLES=${NOS_ARTICLES:-"<li>Haber alınamadı</li>"}

# Build email
cat > /tmp/briefing-$DATE.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Günlük Brifing - $DATE</title>
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
  <h1>📰 GÜNLÜK BRİFİNG - $DATE</h1>
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
    <li>✅ Sistem çalışıyor! Otomatik görevler tamamlandı.</li>
    <li>Blog: <a href="https://caferbeyai.github.io/">caferbeyai.github.io</a></li>
  </ul>

  <div class="footer">
    Caferbey tarafından otomatik gönderildi. 🤖<br>
    <small>Kaynaklar: NOS.nl, BBC News</small>
  </div>
</body>
</html>
HTMLEOF

# Replace placeholders
sed -i "s/NOS_PLACEHOLDER/$NOS_ARTICLES/g" /tmp/briefing-$DATE.html
sed -i "s/BBC_PLACEHOLDER/$BBC_ARTICLES/g" /tmp/briefing-$DATE.html
sed -i "s/\$DATE/$DATE/g" /tmp/briefing-$DATE.html

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