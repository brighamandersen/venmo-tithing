#!/bin/bash
set -euo pipefail

echo "Deploying venmo-tithing"

sudo ln -sf /home/brig/code/venmo-tithing/deploy/systemd/venmo-tithing.service /etc/systemd/system/venmo-tithing.service

sudo ln -sf /home/brig/code/venmo-tithing/deploy/nginx/venmo-tithing.conf /etc/nginx/conf.d/venmo-tithing.conf

sudo systemctl daemon-reload
sudo systemctl enable venmo-tithing.service
sudo systemctl restart venmo-tithing.service

sudo nginx -t
sudo systemctl reload nginx

echo "Deployment complete for venmo-tithing"
