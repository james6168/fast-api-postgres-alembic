#!/bin/bash

set -e

ACTION=$1
MESSAGE=$2

if [[ -z "$ACTION" ]]; then
  echo "Usage: ./manage_migrations.sh [make|upgrade|downgrade] [message_or_revision]"
  exit 1
fi

case "$ACTION" in

  make)
    if [[ -z "$MESSAGE" ]]; then
      echo "Specify message for migration: ./manage_migrations.sh make 'init user table'"
      exit 1
    fi
    echo "Creating migration: \"$MESSAGE\""
    docker compose exec -it app alembic revision --autogenerate -m "$MESSAGE"
    ;;

  upgrade)
    echo "Applying migrations (alembic upgrade head)"
    docker compose exec -it app alembic upgrade head
    ;;

  downgrade)
    if [[ -z "$MESSAGE" ]]; then
      echo "WARNING: Revision was not specified, so downgrade will be done by 1 revision back"
      docker compose exec -it app alembic downgrade -1
    else
      echo "Downgrade to revision: $MESSAGE"
      docker compose exec -it app alembic downgrade "$MESSAGE"
    fi
    ;;

  *)
    echo "Unknown action: $ACTION"
    echo "Available actions: make, upgrade, downgrade"
    exit 1
    ;;

esac