#!/usr/bin/env bash
set -euo pipefail
# Прави логически архив на PostgreSQL; cron трябва да се настрои отделно.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT/infra/postgres/docker-compose.yml"
: "${BACKUP_DIR:?Set BACKUP_DIR to a protected absolute path outside Git}"
[[ "$BACKUP_DIR" = /* ]] || { echo "BACKUP_DIR must be absolute" >&2; exit 1; }
command -v realpath >/dev/null || { echo "realpath is required" >&2; exit 1; }
command -v docker >/dev/null || { echo "Docker Compose is required" >&2; exit 1; }
[[ -f "$ROOT/.env" ]] || { echo "Missing ignored .env (see .env.example)" >&2; exit 1; }
umask 077
mkdir -p -m 700 "$BACKUP_DIR"
TARGET_DIR="$(realpath "$BACKUP_DIR")"
case "$TARGET_DIR/" in
  "$ROOT/"*) echo "Backups must not be written inside Git" >&2; exit 1 ;;
esac
BACKUP_FILE="$TARGET_DIR/bgdb-emds-pg-$(date -u +%Y%m%dT%H%M%SZ).dump"
trap 'rm -f "$BACKUP_FILE"' ERR
# pg_dump работи вътре в контейнера без токени в командния ред.
docker compose --env-file "$ROOT/.env" -f "$COMPOSE_FILE" exec -T postgres   sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc'   > "$BACKUP_FILE"
[[ -s "$BACKUP_FILE" ]] || { echo "Empty pg_dump archive" >&2; exit 1; }
trap - ERR
# Пази 14 календарни дни, само архивите с разпознаваемо име.
find "$TARGET_DIR" -maxdepth 1 -type f -name 'bgdb-emds-pg-*.dump' -mtime +13 -delete
echo "Backup created: $BACKUP_FILE"
