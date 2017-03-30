# These are the steps to setup loki on you own machine
### NOTE: Tested on **Ubuntu 16.04**, should work on **14.04** as well

## REQUIREMENTS:
1. Internet access
2. root privileges (to install apps and libs)

## Run the following commands from within the Loki/ folder
`sudo chmod +x install-libs.sh`

`sudo chmod +x setup-loki.sh`

`./install-libs.sh`

`source setup-libs.sh`

## Side effects:
1. Creates virtual env named "loki"
2. Creates user postgres and grants him permission to project db
**1 Creates db named loki and does all the required setup steps
3. Installs npm and setups bower to install bower components.
4. Installs all the required apps/libs

#### When done, find `manage.py` file and run `python manage.py runserver`
####  Should be up with all the jquery stuff

#### If something does not work, repeat the proccess as root
