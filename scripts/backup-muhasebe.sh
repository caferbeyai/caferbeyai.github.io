#!/bin/bash
# 3CatsMuhasebe daily backup script
# Keeps last 3 days, deletes oldest

SOURCE_DIR="$HOME/Desktop/3CatsMuhasebe"
REPO_DIR="/tmp/3catsmuhasebe-backup-clone"
BACKUP_DATE=$(date +%Y-%m-%d)
BACKUP_FILE="${BACKUP_DATE}.tar.gz"

# Configure git
export GIT_AUTHOR_NAME="Caferbey"
export GIT_AUTHOR_EMAIL="caferbey@ai.local"
export GIT_COMMITTER_NAME="Caferbey"
export GIT_COMMITTER_EMAIL="caferbey@ai.local"

# Clone repo if not exists
if [ ! -d "$REPO_DIR" ]; then
    git clone https://caferbeyai:$GITHUB_TOKEN@github.com/caferbeyai/3catsmuhasebe-backup.git "$REPO_DIR"
    cd "$REPO_DIR"
    git config user.email "caferbey@ai.local"
    git config user.name "Caferbey"
    # Initialize main branch if empty
    if ! git branch -a | grep -q main; then
        echo "# 3CatsMuhasebe Backup" > README.md
        git add README.md
        git commit -m "Initial commit"
        git push -u origin main
    fi
fi

cd "$REPO_DIR"

# Create backup (exclude unnecessary files)
tar -czf "$BACKUP_FILE" \
    --exclude='*.tmp' \
    --exclude='.git' \
    -C "$SOURCE_DIR" .

# Add and commit
git add "$BACKUP_FILE"
git commit -m "Backup: $BACKUP_DATE" || echo "No changes to commit"

# Push
git push

# Keep only last 3 files - remove older backups
ls -1 *.tar.gz 2>/dev/null | sort -r | tail -n +4 | xargs -r rm

# Push deletions
git add -A
git commit -m "Cleanup: keep last 3 days" || echo "Nothing to cleanup"
git push

echo "Backup complete: $BACKUP_FILE"
