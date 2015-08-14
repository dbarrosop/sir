#!/bin/sh
PMACCT_URL="http://sdn-internet-router-sir.readthedocs.org/en/latest/_static/eos_files.tar.gz"
TMP_FOLDER="/tmp"
PMACCT_FOLDER="/tmp/eos_files"

function help {
  echo "Usage: $0"
  echo "Optional arguments:"
  echo "	-h|--help            # This help."
  echo "	--vrf=VRF_NAME       # If you are using a management VRF specify the name here."
  echo "	--sir=SIR_PATH       # If you want to install SIR from a local file specify the path here. Otherwise the latest version will be downloaded from the Internet."
  echo "	--pmacct=PMACCT_PATH # If you want to install pmacct from a local file specify the path here. Otherwise the latest version will be downloaded from the Internet."
  echo "  -r|--restart-pmacct     # If set it will restart pmacct."
  echo "  -u|--upgrade-sir        # If set it will upgrade SIR and all its dependencies. If you are installing SIR from a file it will upgrade only its dependencies."
  exit 1
}

function install_pmacct {
  if [ $PMACCT == "default" ]; then
      echo "Downloading eos_file from $PMACCT_URL"
      $VRF_BIN wget -O $TMP_FOLDER/eos_files.tar.gz $PMACCT_URL
      tar xvzf $TMP_FOLDER/eos_files.tar.gz -C $TMP_FOLDER
  else
      echo "Using local eos_file: $PMACCT"
  fi
  echo ""


  echo "Installing pmacct"
  PMACCT_PID=$(ps fauxwww | grep sfacctd | grep -v grep | awk -F\  '{ print $2 }')
  if [ "$PMACCT_PID" ]; then
      if [ "$RESTART" ]; then
          echo "Stopping sfacctd: done"
          kill -9 $PMACCT_PID
      fi
  fi

  mkdir -p /mnt/drive/sir/output/bgp
  cp $PMACCT_FOLDER/pmacct/pmacct.conf /etc/
  cp $PMACCT_FOLDER/pmacct/pmacct /usr/bin/
  cp $PMACCT_FOLDER/pmacct/sfacctd /usr/sbin/
  cp $PMACCT_FOLDER/pmacct/libjansson.so.4 /usr/lib/
  cp -n $PMACCT_FOLDER/pmacct/pmacct.db /mnt/drive/sir/output/
  echo ""
}

function restart_pmacct {
  PMACCT_PID=$(ps fauxwww | grep sfacctd | grep -v grep | awk -F\  '{ print $2 }')
  if [ "$PMACCT_PID" ]; then
      echo "Starting sfacctd: sfacctd was already running"
  else
      echo "Starting sfacctd: done"
      immortalize --log=/var/log/pmacct.log --daemonize /usr/sbin/sfacctd -f /etc/pmacct.conf
  fi
  echo ""
}

function install_sir {
  if [ $SIR == "default" ]; then
      echo "Installing latest SIR from PIP"
      $VRF_BIN pip install $UPGRADE_KEYWORD SIR
  else
      echo "Installing SIR from local folder: $SIR"
      cd $SIR
      $VRF_BIN python setup.py install
  fi
  echo ""

  echo "Copying configuration files for SIR"
  cp $PMACCT_FOLDER/sir_uwsgi.ini /etc/uwsgi/
  cp $PMACCT_FOLDER/sir_nginx.conf /etc/nginx/external_conf/
  cp $PMACCT_FOLDER/sir_settings.py /mnt/drive/sir/settings.py
}

function restart_sir {
  SIR_PID=$(ps fauxwww | grep sir_uwsgi.ini | grep -v grep | awk -F\  '{ print $2 }')
  if [ "$SIR_PID" ]; then
      echo "Stopping SIR"
      kill -9 $SIR_PID
  fi
  echo "Starting SIR"
  SIR_SETTINGS='/mnt/drive/sir/settings.py' immortalize --daemonize --log=/var/log/sir.uwsgi.log /usr/bin/uwsgi --ini /etc/uwsgi/sir_uwsgi.ini
}

function restart_nginx {
  echo "Restarting nginx"
  $VRF_BIN service nginx restart
}

VRF="default"
SIR="default"
PMACCT="default"

for i in "$@"; do
  case $i in
    -h|--help)
    help
    ;;
    --vrf=*)
    VRF="${i#*=}"
    shift
    ;;
    --sir=*)
    SIR="${i#*=}"
    shift
    ;;
    --pmacct=*)
    PMACCT="${i#*=}"
    PMACCT_FOLDER="$PMACCT"
    shift
    ;;
    -r|--restart-pmacct)
    RESTART=1
    shift
    ;;
    -u|--upgrade-sir)
    UPGRADE_KEYWORD="-U"
    shift
    ;;
    *)
            # unknown option
    ;;
  esac
done

if [ $VRF == "default" ]; then
    VRF_BIN=""
else
    VRF_BIN="ip netns exec ns-$VRF"
fi

install_pmacct

restart_pmacct

install_sir

restart_sir

restart_nginx
