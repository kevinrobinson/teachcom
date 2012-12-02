#!/bin/bash
#
# This script will install dependencies for the teachercom app
#

# must be run as root
if [ `whoami` != "root" ]; then
  echo "This installation must be run as root."
  exit 1
fi

INSTALL_DIR=`pwd`
LOG=$INSTALL_DIR/log_install.log    # Silly name so I can type i + TAB to edit this
echo -n "" > $LOG


# install software requirements
echo -e "\nInstall required software? (y/n)"
read YN
if [ "$YN" == "y" ]; then
    echo -e "\nInstalling required packages with 'apt' and 'pip'"
    apt-get install -q -y openssh-server python2.7 python-pip sqlite3 &>> $LOG
    pip install -r requirements.txt &>> $LOG
fi

echo -e "\nSetup for production server (nginx, gunicorn, etc) (y/n)?"
read YN
if [ "$YN" == "y" ]; then
    apt-get install -q -y nginx &>> $LOG
    pip install gunicorn &>> $LOG

    # configure nginx
    NGINX_DEFAULT=/etc/nginx/sites-enabled/default
    if [ -e $NGINX_DEFAULT ]; then
        echo -e "\nFound a default config for nginx, saving it to $NGINX_DEFAULT.bak"
        cp $NGINX_DEFAULT{,.bak}
        rm $NGINX_DEFAULT
    fi

fi



CFG=/etc/nginx/sites-available/teachercom
GCFG=/etc/gunicorn.d/teachercom
    
configure_nginx() {
    if [ -z "$1" ]; then
        return 1
    fi

    if [ -e "$CFG" ]; then
        rm $CFG
    fi

    echo "upstream app_server {" > $CFG
    echo "    server unix:/tmp/gunicorn.sock fail_timeout=0;" >> $CFG
    echo "}" >> $CFG
    echo "server {" >> $CFG
    # echo "    listen 80 default;" >> $CFG
    echo "    server_name www.teachercom.org;" >> $CFG
    echo "    root $1/py/teachercom/;" >> $CFG
    echo "    location / {" >> $CFG
    echo "        try_files \$uri @proxy_to_app;" >> $CFG
    echo "    }" >> $CFG
    echo "    location @proxy_to_app {" >> $CFG
    echo "        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;" >> $CFG
    echo "        proxy_set_header Host \$http_host;" >> $CFG
    echo "        proxy_redirect off;" >> $CFG
    echo "        proxy_pass http://app_server;" >> $CFG
    echo "    }" >> $CFG
    echo "    location /static/ {" >> $CFG
    echo "        alias $1/py/teachercomapp/static/;" >> $CFG
    echo "    }" >> $CFG
    echo "}" >> $CFG

    return 0
}

configure_nginx $INSTALL_DIR

configure_gunicorn() {
    if [ -z "$1" ]; then
        return 1
    fi

    if [ -e "$GCFG" ]; then
        rm $GCFG
    fi

    echo "CONFIG = {" > $GCFG
    echo "    'mode': 'django'," >> $GCFG
    echo "    'environment': {" >> $GCFG
    echo "        'PYTHONPATH': '$1/py/teachercom'," >> $GCFG
    echo "        'DJANGO_SETTINGS_MODULE': 'settings'," >> $GCFG
    echo "    }," >> $GCFG
    echo "    'working_dir': '$1/py/teachercom'," >> $GCFG
    echo "    'user': 'www-data'," >> $GCFG
    echo "    'group': 'www-data'," >> $GCFG
    echo "    'args': (" >> $GCFG
    echo "        '--bind=unix:/tmp/gunicorn.sock'," >> $GCFG
    echo "        '--workers=4'," >> $GCFG
    echo "    )," >> $GCFG
    echo "}" >> $GCFG

    return 0
}

configure_gunicorn $INSTALL_DIR

pushd /etc/nginx/sites-enabled &> /dev/null
if [ -e ecep ]; then
    rm ecep
fi
ln -s $CFG
popd &> /dev/null

service gunicorn start
service nginx start






read_or_none() {
    read A
    if [ "x$A" == "x" ]; then
        A="None"
    else
        A="'$A'"
    fi
    echo "$A"
}

configure_django() {
    if [ -z "$1" ]; then
        return 1
    fi

    TWILIO_ENABLED="True"
    echo -e "\nEnter your Twilio credentials (you can leave these blank to use the test account)"

    echo -en "\nPlease enter your Twilio Account SID: "
    ACCOUNT_SID=$(read_or_none)

    echo -en "\nPlease enter your Twilio Account Auth Token: "
    ACCOUNT_AUTH=$(read_or_none)

    echo -en "\nPlease enter your Twilio SMS phone number in the form \"(ddd) ddd-dddd\": "
    PHONE=$(read_or_none)

    echo -en "\nPlease enter a username for the django admin: "
    read USERNAME

    echo -en "\nPlease enter an email address for the django admin: "
    read EMAIL

    LOCAL="$1/py/teachercom/teachercom/local_settings.py"

    echo "ADMINS = (" > $LOCAL
    echo "    ('$USERNAME', '$EMAIL')," >> $LOCAL
    echo ")" >> $LOCAL
    echo "" >> $LOCAL
    echo "TWILIO_ENABLED = $TWILIO_ENABLED" >> $LOCAL
    echo "TWILIO_ACCOUNT_SID = $ACCOUNT_SID" >> $LOCAL
    echo "TWILIO_AUTH_TOKEN = $ACCOUNT_AUTH" >> $LOCAL
    echo "TWILIO_PHONE = $PHONE" >> $LOCAL
    echo "" >> $LOCAL
    echo "MANAGERS = ADMINS" >> $LOCAL
    echo "" >> $LOCAL
    echo "MEDIA_ROOT = '$1/py/teachercom/teachercomapp/media/'" >> $LOCAL
    echo "" >> $LOCAL
    echo "STATIC_ROOT = '$1/py/teachercom/teachercomapp/static/'" >> $LOCAL
    echo "" >> $LOCAL
    echo "SECRET_KEY = '8pw%s3$@2&6lm1k&2!&!^c8w@4h0b#ae-7-$!04b24=1-b(554'" >> $LOCAL
    echo "" >> $LOCAL
    echo "TEMPLATE_DIRS = (" >> $LOCAL
    echo "    '$1/py/teachercom/templates/'" >> $LOCAL
    echo ")" >> $LOCAL
    echo "" >> $LOCAL
    echo "STAGING = False" >> $LOCAL

    return 0
}

configure_django $INSTALL_DIR

