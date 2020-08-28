#!/bin/sh -l

echo $SPIDER_PATH $AUTOCOMMIT

scrapy runspider $SPIDER_PATH

if [[ -z "$AUTOCOMMIT" ]]; then
  git config --global user.name 'auto commit'
  git config --global user.email 'auto-commit@users.noreply.github.com'
  # git add fibertel
  git commit -am "Automated commit push"
  git push
fi
