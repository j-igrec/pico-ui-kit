#!/usr/bin/env bash
# Usage: ./release.sh 0.0.2
# Run from the pico-ui-kit root after merging to main.

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version>  (e.g. 0.0.2)"
  exit 1
fi

BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
  echo "You must be on main to release. Currently on: $BRANCH"
  exit 1
fi

# Bump __init__.py
sed -i '' "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" __init__.py

# Remind to update CHANGELOG
echo ""
echo ">>> Add your release notes to CHANGELOG.md under [${VERSION}] - $(date +%Y-%m-%d), then press Enter to continue..."
read -r

# Commit, tag, push
git add __init__.py CHANGELOG.md
git commit -m "chore: release v${VERSION}"
git tag "v${VERSION}"
git push origin main
git push origin "v${VERSION}"

echo ""
echo "Released v${VERSION} and pushed tag to GitHub."
