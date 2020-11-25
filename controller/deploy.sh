#!/bin/bash

if [[ "${EUID}" -ne 0 ]]; then
    echo "[!] Please run this script with root privileges."
    exit 1
fi

APP_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd ${APP_DIR}
echo "[+] Working in: $(pwd)"

while getopts f:k:ri OPTION; do
    case "${OPTION}" in
        f)
        export CAMERA_FOLDER=$(pwd)/"${OPTARG}"
        CAMERA_FOLDER_SET="yes"
        ;;
        k)
        export ROOM_KEY="${OPTARG}"
        ROOM_KEY_SET="yes"
        ;;
        r)
        export RUN_ONLY_SET="yes"
        ;;
        i)
        export INSTALL_SET="yes"
        ;;
    esac
done

# Get system timezone
export TZ=$(cat /etc/timezone)
echo "[+] Detected Timezone: ${TZ}"

# Setup Camera directory
echo "[*] Setting up data directories..."
if [[ -z "${CAMERA_FOLDER_SET}" ]]; then
    read -p "Camera data directory [camera] : " CAMERA_FOLDER_IN
    if [[ ! -z "${CAMERA_FOLDER_IN}" ]]; then
        export CAMERA_FOLDER=$(pwd)/${CAMERA_FOLDER_IN}
    else
        export CAMERA_FOLDER=$(pwd)/camera
    fi
fi
mkdir -p ${CAMERA_FOLDER}
echo "[+] Camera Folder:" ${CAMERA_FOLDER}

# Setup Room APIKEY
if [[ -z "${ROOM_KEY_SET}" ]]; then
    read -p "Room API Key : " ROOM_KEY_IN
    export ROOM_KEY=${ROOM_KEY_IN}
fi

if [[ ! -z "${RUN_ONLY_SET}" ]]; then
    # Run program
    echo "[*] Starting Controller..."
    cd app/
    python3 controller.py
fi

if [[ ! -z "${INSTALL_SET}" ]]; then
    pip3 install -r requirements.txt
    cat << EOF > controller.service
[Unit]
Description=Controller Service
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=$(pwd)/app
PIDFile=$(pwd)/app/controller.pid
Environment=CAMERA_FOLDER=${CAMERA_FOLDER}
Environment=ROOM_KEY=${ROOM_KEY}
ExecStart=/usr/bin/python3 controller.py
ExecStop=/bin/kill -SIGINT \$MAINPID

[Install]
WantedBy=multi-user.target
EOF
    mv controller.service /lib/systemd/system/controller.service
    systemctl daemon-reload
    systemctl enable controller.service
    systemctl stop controller.service
    systemctl start controller.service
fi
