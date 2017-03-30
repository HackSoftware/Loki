apt-get update >> /dev/null

sudo apt-get --assume-yes install virtualenvwrapper
sudo apt-get --assume-yes install git

sudo apt-get --assume-yes install python3-dev python3-setuptools
# NOTE: Debian users might have a problem with libjpeg8-dev
sudo apt-get --assume-yes install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

sudo apt-get --assume-yes install libpq-dev

sudo apt-get --assume-yes install postgresql postgresql-contrib

sudo apt-get --assume-yes install npm
sudo apt-get --assume-yes install nodejs-legacy
