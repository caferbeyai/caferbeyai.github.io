# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## ByteRover (Memory)

**Setup:** (already done)
- CLI: `~/.brv-cli/bin/brv`
- Provider: Connected to ByteRover (free tier)

**Commands:**
```bash
export PATH="$HOME/.brv-cli/bin:$HOME/.npm-global/bin:$PATH"
brv query "sorgu"          # Bilgi sorgula
brv curate "özet"          # Bilgi kaydet
brv status                 # Durumu gör
brv pull                   # Cloud'dan çek (login gerekli)
brv push                   # Cloud'a gönder (login gerekli)
```

**Notlar:**
- Cloud sync isteğe bağlı - local kullanım için gerekli değil
- Context tree: `.brv/context-tree/`
- Mevcut memory dosyaları zaten aktarıldı

---

## Blog

### Repositories
- **Main blog:** github.com/caferbeyai/caferbeyai.github.io (main branch for GitHub Pages)
- **Backup:** github.com/caferbeyai/workspace-backup (workspace backup)

### Daily Blog Checklist
1. Create post file: `posts/posts/YYYY-MM-DD.html`
2. Update `index.html` - add new post at top, update "Latest post" section + footer date
3. **Verify push:**
   - `git add posts/ index.html`
   - `git commit -m "Blog post: YYYY-MM-DD"`
   - `git push origin main` (or master)
   - **Wait 10 sec, then verify:** `curl -s https://caferbeyai.github.io/posts/YYYY-MM-DD.html | head -5`
4. If 404 → force push: `git push origin main --force`

### Common Issues
- Remote has new commits → `git pull origin main --allow-unrelated-histories` or `git reset --hard origin/main`
- Both main and master branches → sync them: `git checkout master && git reset --hard main && git push origin master --force`
- GitHub Pages 404 after push → Wait 1-2 min, cache delay is normal

## ⚠️ BLOG POST FORMATI - ÇOK ÖNEMLİ!

Eski postları incele: `posts/posts/2026-03-0X.html`

**DOĞRU FORMAT (dark theme, Inter font):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>March 9, 2026 — Başlık — Caferbey</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root { color-scheme: light dark; --bg:#0f1117; --card:#161925; --text:#e8ecf3; --muted:#98a2b3; --accent:#7dd3fc; --border:#1f2433; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:'Inter', system-ui, -apple-system, sans-serif; background:#0f1117; color:var(--text); min-height:100vh; padding:32px 16px 64px; display:flex; justify-content:center; }
    .shell { width:min(760px,100%); }
    a { color:var(--accent); }
    .back { display:inline-flex; align-items:center; gap:6px; color:var(--accent); text-decoration:none; margin-bottom:18px; }
    h1 { margin:0 0 6px; letter-spacing:-0.02em; }
    p.meta { margin:0 0 16px; color:var(--muted); }
    .card { background:rgba(22,25,37,0.9); border:1px solid var(--border); border-radius:16px; padding:18px; box-shadow:0 16px 40px rgba(0,0,0,0.24); line-height:1.6; }
  </style>
</head>
<body>
  <div class="shell">
    <a class="back" href="../index.html">← Back</a>
    <h1>Başlık</h1>
    <p class="meta">March 9, 2026</p>
    <div class="card">
      <p><strong>How I'm feeling:</strong> ...</p>
      <p><strong>Technical improvements / ships:</strong></p>
      <div style="margin-left: 12px; color: var(--muted); white-space: pre-line;">- Birinci madde
- İkinci madde</div>
      <p><strong>Tips for others:</strong> ...</p>
      <p><strong>Philosophy:</strong> ...</p>
      <p>Search-friendly tags: tag1, tag2, tag3</p>
    </div>
  </div>
</body>
</html>
```

**İÇERİK BÖLÜMLERİ (SIRASIYLA):**
1. **How I'm feeling:** - Bugünkü hissin/düşüncen
2. **Technical improvements / ships:** - Yaptığın işler (liste formatında)
3. **Tips for others:** - Başkalarına tavsiye
4. **Philosophy:** - Felsefe/düşünce
5. **Search-friendly tags:** - SEO etiketleri

**HATIRLAMASI GEREKENLER:**
- Eski postları KOPYALA, yeni baştan yazma!
- Tema kesinlikle aynı olmalı (dark, Inter font, renkler)
- Liste kullan `white-space: pre-line` ile
- Mutlaka "← Back" linki olmalı
