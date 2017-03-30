mkvirtualenv -p /usr/bin/python3 loki

# git clone https://github.com/HackSoftware/Loki.git

cd Loki/

# Install base requirements after all required libs are installed
pip install -r requirements/base.txt

sudo -u postgres createuser root
sudo -u postgres createdb -O root loki

python manage.py makemigrations
python manage.py migrate

npm install -g bower

cd loki/static
bower install --allow-root bower.json
# Some libs fail the first time...javascript...
bower install --allow-root bower.json
