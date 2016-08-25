#!/usr/bin/env bash
sudo add-apt-repository -y ppa:nginx/stable
sudo apt-get update
sudo apt-get install -y build-essential python-dev python-pip nginx nginx-extra uwsgi uwsgi-plugin-python
sudo pip install virtualenv
cd /vagrant
virtualenv .env --always-copy --no-site-packages
source .env/bin/activate
pip install -r requirements.txt
deactivate
touch /tmp/moflow.sock
sudo chown www-data:www-data /tmp/moflow.sock
sudo rm -rf /etc/nginx/sites-available/default
sudo cp /vagrant/nginx.conf /etc/nginx/sites-available/moflow
sudo ln -s /etc/nginx/sites-available/moflow  /etc/nginx/sites-enabled/moflow
sudo cp /vagrant/uwsgi.ini /etc/uwsgi/apps-available/moflow.ini
sudo ln -s /etc/uwsgi/apps-available/moflow.ini /etc/uwsgi/apps-enabled/moflow.ini
sudo service nginx restart
sudo service uwsgi restart