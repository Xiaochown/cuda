#!/usr/bin/env bash
exec /root/.9router/bin/cloudflared tunnel --url http://127.0.0.1:9400 --no-autoupdate --protocol http2
