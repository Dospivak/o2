#!/bin/bash

# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

# Create application directory if it doesn't exist
sudo mkdir -p /var/www/o2
sudo chown www-data:www-data /var/www/o2

# Install required system packages
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nginx

# Set up virtual environment
cd /var/www/o2
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt

# Copy and enable systemd service
sudo cp o2.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable o2
sudo systemctl restart o2

# Set up Nginx
sudo tee /etc/nginx/sites-available/o2 << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/o2 /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx 