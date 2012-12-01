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
LOG=$INSTALL_DIR/install.log
echo -n "" > $LOG


# install software requirements
echo -e "\nInstall required software? (y/n)"
read YN
if [ "$YN" == "y" ]; then
    echo -e "\nInstalling required packages with 'apt' and 'pip'"
    apt-get install -q -y openssh-server python2.7 python-pip sqlite3 &>> $LOG
    pip install -r requirements.txt &>> $LOG
fi

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

