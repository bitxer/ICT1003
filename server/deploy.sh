#!/bin/bash

APP_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd ${APP_DIR}
echo "[+] Working in: $(pwd)"

while getopts n:u:p:c OPTION; do
    case "${OPTION}" in
        n)
        export APP_NAME=${OPTARG}
        APP_NAME_SET="yes"
        ;;
        u)
        DOCKER_USER=${OPTARG}
        DOCKER_USER_SET="yes"
        ;;
        p)
        if [[ "${OPTARG}" == "0" ]]; then
            export APP_PORT=$(( 1 + RANDOM % (1 + 65534 + 1025) ))
            APP_PORT_SET="yes"
        elif ((${OPTARG} > 1024 && ${OPTARG} < 65535)); then
            export APP_PORT=${OPTARG}
            APP_PORT_SET="yes"
        fi
        ;;
        c)
        IGNORE_CLEAN_DIR="yes"
        ;;
    esac
done

# Get system timezone
export TZ=$(cat /etc/timezone)
echo "[+] Detected Timezone: ${TZ}"


if [[ -z "${APP_NAME_SET}" ]]; then
    read -p "Prefix for Docker container names [ICT1003] : " APP_NAME_IN
    if [[ ! -z "${APP_NAME_IN}" ]]; then
        export APP_NAME=${APP_NAME_IN}
    else
        export APP_NAME="ICT1003"
    fi
fi
echo "[+] Prefix: ${APP_NAME}"

if [[ -z "${APP_PORT_SET}" ]]; then
    while true; do
        echo "TCP Port for Web listener to listen on. Leave blank for random port."
        read -p "Choose a port above 1024 and below 65535 : " APP_PORT_IN
        if [[ -z "${APP_PORT_IN}" ]] || [[ "${APP_PORT_IN}" == "0" ]]; then
            export APP_PORT=$(( 1 + RANDOM % (1 + 65534 + 1025) ))
            break
        elif ((${APP_PORT_IN} > 1024 && ${APP_PORT_IN} < 65535)); then
            export APP_PORT=${APP_PORT_IN}
            break
        fi
        echo "[!] Invalid input detected."
    done
fi
echo "[+] Listening on host port: ${APP_PORT}/tcp"

if [[ -z "${DOCKER_USER_SET}" ]]; then
    DOCKER_USER=""

    read -p "Specify user used for Docker user namespace isolation (Leave blank if not enabled): " DOCKER_USER_IN
    if [[ ! -z "${DOCKER_USER_IN}" ]]; then
        DOCKER_USER=${DOCKER_USER_IN}
    fi
fi

if [[ -z "${IGNORE_CLEAN_DIR}" ]]; then
    echo "[*] Setting up data directories..."

    if [[ -d ./APPDATA/docker-${APP_NAME} ]]; then
        while true; do
            read -p "Old installation detected. Delete data? [Y/n] : " DELETE_OLD_IN
            case "${DELETE_OLD_IN}" in
                [Y])
                # Remove old data.
                sudo rm -rf ./APPDATA/docker-${APP_NAME}
                break
                ;;
                [y])
                echo "[!] Enter \"Y\" (Uppercase) for yes."
                ;;
                [Nn])
                break
                ;;
                *)
                echo "[!] Invalid input detected."
                ;;
            esac
        done
    fi

    mkdir -p ./APPDATA/docker-${APP_NAME}

    if [[ ! -z "${DOCKER_USER}" ]]; then
        echo "[+] Docker User: ${DOCKER_USER}"
        chown -R ${DOCKER_USER}:${DOCKER_USER} ./APPDATA/docker-${APP_NAME}/
    fi
fi

# Run docker-compose.
echo "[*] Starting containers..."
docker-compose --project-name "${APP_NAME}" up -d
docker image prune -af