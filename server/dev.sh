trap cleanup SIGINT SIGTERM SIGKILL

cleanup() {
    echo ""
    command -v deactivate >/dev/null 2>&1 && deactivate
    echo -e "\e[33m\e[1m[*]\e[0m Cleaning cache..."
    find ./web/ -type d -name __pycache__ -exec rm -r {} \+
    echo -e "\e[32m\e[1m[+]\e[0m Exiting..."
    exit
}

cd "$(dirname "$0")/"
SERVER_DIR=$(pwd)

echo -e "\e[32m\e[1m[+]\e[0m Working in: ${SERVER_DIR}"

while getopts tc: OPTION; do
    case "${OPTION}" in
        t)
        TESTING="yes"
        break
        ;;
        c)
        CLEAN_SET="yes"
        if [[ -d "./APPDATA/dev" ]]; then
            rm -rf ./APPDATA/dev/logs/* ./APPDATA/dev/uploads/*
        fi
        ;;
    esac
done

# Some default exports.
export REVERSEPROXY="no"
export SECURE="no"
if [[ -f "/etc/timezone" ]]; then
    export TZ=$(cat /etc/timezone)
else
    # Set default as Asia/Singapore.
    export TZ="Asia/Singapore"
fi

if [[ -z "${TESTING}" ]]; then
    # Run the development instance.
    if [[ -z "${CLEAN_SET}" ]]; then
        if [[ -d "./APPDATA/dev" ]]; then
            while true; do
                echo -en "\e[33m\e[1m[*]\e[0m "
                read -p "Remove old logs and uploads data? [Y/n] : " CLEAN_IN
                case "${CLEAN_IN}" in
                    [Yy])
                    # Remove old data.
                    rm -rf ./APPDATA/dev/logs/* ./APPDATA/dev/uploads/*
                    break
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
    fi

    mkdir -p ./APPDATA/dev/logs ./APPDATA/dev/uploads

    export LOG_FOLDER=${SERVER_DIR}/APPDATA/dev/logs
    export UPLOAD_FOLDER=${SERVER_DIR}/APPDATA/dev/uploads

    if [[ ! -d ./APPDATA/dev/venv ]]; then
        virtualenv -p python3 ./APPDATA/dev/venv
    fi

    # Activate Python virtual environment.
    . ./APPDATA/dev/venv/bin/activate
    pip install --no-cache-dir -r ./web/requirements.txt | grep -v "Requirement already satisfied"

    python3 ./web/debug.py

else
    # Run tests.
    echo -e "\e[32m\e[1m[+]\e[0m Running Tests."
    echo ""

    if [[ -d "./APPDATA/tests" ]]; then
        rm -rf ./APPDATA/tests/logs ./APPDATA/tests/uploads
    fi
    mkdir -p ./APPDATA/tests/logs ./APPDATA/tests/uploads

    export LOG_FOLDER=${SERVER_DIR}/APPDATA/tests/logs
    export UPLOAD_FOLDER=${SERVER_DIR}/APPDATA/tests/uploads

    if [[ ! -d ./APPDATA/tests/venv ]]; then
        virtualenv -p python3 ./APPDATA/tests/venv
    fi

    # Activate Python virtual environment.
    . ./APPDATA/tests/venv/bin/activate
    pip install --no-cache-dir -r ./web/requirements.txt | grep -v "Requirement already satisfied"

    nosetests -v -d -w tests

    # Delete cache.
    echo -e "\e[33m\e[1m[*]\e[0m Cleaning cache..."
fi

# Deactivate virtual environment.
deactivate
echo -e "\e[33m\e[1m[*]\e[0m Exiting..."
exit
