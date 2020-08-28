#!/usr/bin/env bash

scrapy runspider $SPIDER_PATH

if [[ -n "$AUTOCOMMIT" ]]; then
  echo "autocommit the result"
  git config --global user.name 'auto commit'
  git config --global user.email 'auto-commit@users.noreply.github.com'
  # git add fibertel
  git commit -am "Automated commit push"
  git push
else
  echo "no commit the result"
fi
