#!/bin/bash

echo "install dependencies"
sudo dnf install httpd httpd-devel mariadb-devel -y
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.4.tar.gz
tar -xzvf 4.9.4.tar.gz
cd mod_wsgi-4.9.4
./configure --with-apxs=/usr/bin/apxs
make
sudo make install
sudo rm -rvf mod_wsgi-4.9.4*
sudo rm -rvf 4.9.4.tar.gz*
echo 'installed dependencies'

# Set the path to your Django project directory
PROJECT_DIR="$1"
DEPLOY_PATH="$3"

# Set the name of your Apache configuration file (without the .conf extension)
APACHE_CONF_FILE="$2"

# Activate your virtual environment (change 'venv' to your virtual environment name)
source "$PROJECT_DIR/venv/bin/activate"

# Configure mod_wsgi and Apache
echo "LoadModule wsgi_module modules/mod_wsgi.so" | sudo tee -a /etc/httpd/conf.modules.d/10-wsgi.conf

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

# Create or update the Apache configuration file
# Create or update the Apache configuration file
sudo bash -c "echo '<VirtualHost *:80>
    ServerName $2
    DocumentRoot $DEPLOY_PATH

    Alias /static $DEPLOY_PATH/static
    <Directory $DEPLOY_PATH/static>
        Require all granted
    </Directory>

    <Directory $DEPLOY_PATH>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIProcessGroup $2
    WSGIScriptAlias / $DEPLOY_PATH/wsgi.py

    ErrorLog /var/log/httpd/$2_error.log
    CustomLog /var/log/httpd/$2_access.log combined

</VirtualHost>' > /etc/httpd/conf.d/${APACHE_CONF_FILE}.conf"

# Set permissions, excluding .git folders
sudo find "$DEPLOY_PATH" -type d -name '.git' -prune -o -exec chmod +rx {} +
sudo find "$DEPLOY_PATH" -type d -name '.git' -prune -o -exec chmod -R +rX {} +
sudo chown -R apache:apache "$DEPLOY_PATH"

# Enable Apache modules and restart the Apache service
sudo systemctl stop httpd
# echo "Https configuration"
rm -fv "/etc/httpd/conf.d/$2-le-ssl.conf"
sudo certbot --apache --expand --non-interactive --domains $2
sudo sed -i "/WSGIProcessGroup/a WSGIDaemonProcess $2 python-home=$DEPLOY_PATH/venv python-path=$DEPLOY_PATH" "/etc/httpd/conf.d/$2-le-ssl.conf"
sudo systemctl restart httpd
echo "Django application deployed successfully!"
