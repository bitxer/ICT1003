#!/bin/bash

APP_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd ${APP_DIR}
echo "[+] Working in: $(pwd)"

while getopts f:k: OPTION; do
    case "${OPTION}" in
        f)
        export CAMERA_FOLDER=$(pwd)/"${OPTARG}"
        CAMERA_FOLDER_SET="yes"
        ;;
        k)
        export ROOM_KEY="${OPTARG}"
        ROOM_KEY_SET="yes"
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

# Run program
echo "[*] Starting Controller..."
cd app/
python3 controller.py
