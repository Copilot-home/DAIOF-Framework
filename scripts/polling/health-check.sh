#!/bin/bash
echo "APO Health — $(date '+%Y-%m-%d %H:%M:%S')"
[ -n "$NOTION_API_KEY" ] && curl -sf -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/users/me" > /dev/null && echo "Notion: OK" || echo "Notion: FAIL"
gh api user -q .login > /dev/null 2>&1 && echo "GitHub: OK" || echo "GitHub: FAIL"
docker info > /dev/null 2>&1 && echo "Docker: OK ($(docker ps -q | wc -l | tr -d ' ') containers)" || echo "Docker: FAIL"
