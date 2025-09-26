#!/bin/bash
set -euo pipefail

echo "Deploying venmo-tithing"

# nginx

sudo ln -sf /home/brig/code/venmo-tithing/deploy/nginx.conf /etc/nginx/conf.d/venmo-tithing.conf

sudo nginx -t
sudo systemctl reload nginx

# systemd

sudo ln -sf /home/brig/code/venmo-tithing/deploy/systemd.service /etc/systemd/system/venmo-tithing.service

sudo systemctl daemon-reload
sudo systemctl enable venmo-tithing.service
sudo systemctl restart venmo-tithing.service


echo "Deployment complete for venmo-tithing"
