#!/bin/bash

echo "install dependencies"
sudo dnf install nginx mariadb-devel -y
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.4.tar.gz
tar -xzvf 4.9.4.tar.gz
cd mod_wsgi-4.9.4
./configure --with-python=/path/to/your/python3
make
sudo make install
sudo rm -rvf mod_wsgi-4.9.4*
sudo rm -rvf 4.9.4.tar.gz*
echo 'installed dependencies'

# Set the path to your Django project directory
PROJECT_DIR="$1"
DEPLOY_PATH="$3"

# Set the name of your Nginx configuration file (without the .conf extension)
NGINX_CONF_FILE="$2"

# Activate your virtual environment (change 'venv' to your virtual environment name)
source "$PROJECT_DIR/venv/bin/activate"

# Configure mod_wsgi and Nginx
echo "LoadModule wsgi_module modules/mod_wsgi.so" | sudo tee -a /etc/nginx/conf.d/10-wsgi.conf

# Navigate to the Django project directory
cd "$PROJECT_DIR"

# Collect static files
python manage.py collectstatic --noinput
echo "Seed Initial production data..."
python manage.py runscript seed.seed_prod.py

# Run database migrations
python3 manage.py migrate

# Deactivate the virtual environment
deactivate

# Create or update the Nginx configuration file
sudo bash -c "echo 'server {
    listen 80;
    server_name $2;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $DEPLOY_PATH;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$DEPLOY_PATH/myproject.sock;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root $DEPLOY_PATH/templates/;
    }
}' > /etc/nginx/conf.d/${NGINX_CONF_FILE}.conf"

# Set permissions, excluding .git folders
sudo find "$DEPLOY_PATH" -type d -name '.git' -prune -o -exec chmod +rx {} +
sudo find "$DEPLOY_PATH" -type d -name '.git' -prune -o -exec chmod -R +rX {} +
sudo chown -R nginx:nginx "$DEPLOY_PATH"

# Enable Nginx and restart the Nginx service
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "Django application deployed successfully!"
