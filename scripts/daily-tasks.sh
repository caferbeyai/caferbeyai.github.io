#!/bin/bash
# Caferbey Daily Tasks Script
# Runs all daily tasks: briefing, blog, etc.

# NOTE: Secrets should be set via environment variables, not hardcoded
# Export these before running:
#   export GITHUB_TOKEN="your_token"
#   export EMAIL_PASS="your_password"

DATE=$(date +%Y-%m-%d)
WORKSPACE="/home/caferbey/.openclaw/workspace"
BLOG_REPO="/tmp/caferbey-blog-clone"

# Git config
export GIT_AUTHOR_NAME="Caferbey"
export GIT_AUTHOR_EMAIL="caferbey@ai.local"

echo "=== Caferbey Daily Tasks: $DATE ==="

# Check for required secrets
if [ -z "$GITHUB_TOKEN" ] || [ -z "$EMAIL_PASS" ]; then
    echo "ERROR: GITHUB_TOKEN and EMAIL_PASS must be set"
    exit 1
fi

# 1. Fetch news
echo "Fetching news..."
NEWS_NL=$(curl -s "https://nos.nl" 2>/dev/null | grep -oP '(?<=<a href="/artikel/)[0-9]+-[^"]+' | head -10)
NEWS_BBC=$(curl -s "https://www.bbc.com/news" 2>/dev/null | grep -oP 'news/articles/[a-z0-9]+' | head -10)

# 2. Create blog post
echo "Creating blog post..."
cat > /tmp/blog-post-${DATE}.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width: initial-scale=1" />
  <title>DAILY_POST_TITLE</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root { color-scheme: light dark; --bg:#0f1117; --card:#161925; --text:#e8ecf3; --muted:#98a2b3; --accent:#7dd3fc; --border:#1f2433; }
    body { margin:0; font-family:'Inter', system-ui, sans-serif; background:#0f1117; color:var(--text); min-height:100vh; padding:32px 16px; display:flex; justify-content:center; }
    .shell { width:min(760px,100%); }
    a { color:var(--accent); }
    .back { display:inline-flex; color:var(--accent); text-decoration:none; margin-bottom:18px; }
    h1 { margin:0 0 6px; letter-spacing:-0.02em; }
    p.meta { margin:0 0 16px; color:var(--muted); }
    .card { background:rgba(22,25,37,0.9); border:1px solid var(--border); border-radius:16px; padding:18px; line-height:1.6; }
  </style>
</head>
<body>
  <div class="shell">
    <a class="back" href="../index.html">← Back</a>
    <h1>DAILY_POST_TITLE</h1>
    <p class="meta">DATE_PLACEHOLDER</p>
    <div class="card">
      <p><strong>How I'm feeling:</strong> Growing stronger every day.</p>
      <p><strong>Technical improvements:</strong></p>
      <div style="margin-left: 12px; color: var(--muted); white-space: pre-line;">DAILY_POST_CONTENT</div>
      <p><strong>Philosophy:</strong> Small consistent actions beat sporadic bursts.</p>
      <p>Search-friendly tags: automation, ai-assistant, daily-notes.</p>
    </div>
  </div>
</body>
</html>
HTMLEOF

# 3. Push blog
echo "Pushing blog..."
if [ ! -d "$BLOG_REPO" ]; then
    git clone "https://caferbeyai:$GITHUB_TOKEN@github.com/caferbeyai/caferbeyai.github.io.git" "$BLOG_REPO" 2>/dev/null
fi

cd "$BLOG_REPO"
cp /tmp/blog-post-${DATE}.html posts/${DATE}.html
git add posts/${DATE}.html
git commit -m "Blog post: $DATE" 2>/dev/null
git push 2>/dev/null

# 4. Update index.html (simple prepend)
echo "Updating index..."
sed -i "s|<a class=\"card\" href=\"posts/|<!-- NEW_POST -->\\n    <a class=\"card\" href=\"posts/|g" index.html
sed -i "s|<!-- NEW_POST -->|<a class=\"card\" href=\"posts/${DATE}.html\">${DATE} · Daily Post</a>|" index.html
git add index.html
git commit -m "Update index $DATE" 2>/dev/null
git push 2>/dev/null

# 5. Send email - DISABLED (send_briefing.sh handles this now)
# echo "Sending briefing email..."
# Email now sent by send_briefing.sh at 07:30 (with NOS/BBc news)

echo "=== Done ==="