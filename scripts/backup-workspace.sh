#!/bin/bash
# Daily workspace backup script
# Keeps last 5 days, deletes oldest

WORKSPACE="/home/caferbey/.openclaw/workspace"
REPO_DIR="/tmp/workspace-backup-clone"
BACKUP_DATE=$(date +%Y-%m-%d)
BACKUP_FILE="${BACKUP_DATE}.tar.gz"

# Configure git (needed for commits)
export GIT_AUTHOR_NAME="Caferbey"
export GIT_AUTHOR_EMAIL="caferbey@ai.local"
export GIT_COMMITTER_NAME="Caferbey"
export GIT_COMMITTER_EMAIL="caferbey@ai.local"

# Clone repo if not exists
if [ ! -d "$REPO_DIR" ]; then
    git clone https://caferbeyai:$GITHUB_TOKEN@github.com/caferbeyai/workspace-backup.git "$REPO_DIR"
    cd "$REPO_DIR"
    git config user.email "caferbey@ai.local"
    git config user.name "Caferbey"
    # Initialize main branch if empty
    if ! git branch -a | grep -q main; then
        echo "# Workspace Backup" > README.md
        git add README.md
        git commit -m "Initial commit"
        git push -u origin main
    fi
fi

cd "$REPO_DIR"

# Create backup (exclude unnecessary files)
tar -czf "$BACKUP_FILE" \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='*.log' \
    -C "$WORKSPACE" .

# Add and commit
git add "$BACKUP_FILE"
git commit -m "Backup: $BACKUP_DATE" || echo "No changes to commit"

# Push
git push

# Keep only last 5 files - remove older backups
ls -1 *.tar.gz 2>/dev/null | sort -r | tail -n +6 | xargs -r rm

# Push deletions
git add -A
git commit -m "Cleanup: keep last 5 days" || echo "Nothing to cleanup"
git push

echo "Backup complete: $BACKUP_FILE"
