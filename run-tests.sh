#!/bin/sh

source init-logging.sh run-tests

printf "\033[32mRunning \033[1mTesting \033[0;32menvironment\033[0m\n"

if ! docker -v >/dev/null 2>&1; then
  printf "\033[31mError: \033[1;36mDocker \033[0;31mis not installed or running\033[0m\n" >&2
  exit 1
fi

clean_up () {
  exec &> /dev/tty
  printf "\n\033[32mRemoving \033[1;36mDocker \033[0;32mcontainers\033[0m\n\n"
  docker compose --file docker-compose-tests.yml down -v --rmi all --remove-orphans
  trap "" EXIT
  exit 0
}
trap clean_up INT EXIT

if [ ! -z "$1" ]
  then export CLIENT_ID=$1
fi
if [ ! -z "$2" ]
  then export CLIENT_SECRET=$2
fi
printf "\033[32mCreating and starting \033[1;36mDocker \033[0;32mcontainers\033[0m\n"
printf "\033[33mTip: Use \033[1mCtrl + C\033[0;33m to cancel or close \033[1;36mDocker\033[0m\n\n"
docker compose --file docker-compose-tests.yml up --build