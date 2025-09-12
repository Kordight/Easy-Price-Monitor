#!/bin/bash

# -----------------------------
# Backup MySQL Database Script
# -----------------------------

# Paths
CONFIG_JSON="/home/sebastian/easy-price-monitor/mysql_config.json"
BACKUP_DIR="/home/sebastian/easy-price-monitor/backups"

JQ_BIN="/usr/bin/jq"
MYSQLDUMP_BIN="/usr/bin/mysqldump"

# Check if config exists
if [ ! -f "$CONFIG_JSON" ]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Config file $CONFIG_JSON not found!"
    exit 1
fi

# Read configuration from JSON
DB_HOST=$($JQ_BIN -r '.connection.host' "$CONFIG_JSON")
DB_USER=$($JQ_BIN -r '.connection.user' "$CONFIG_JSON")
DB_PASSWORD=$($JQ_BIN -r '.connection.password' "$CONFIG_JSON")
DB_NAME=$($JQ_BIN -r '.connection.database' "$CONFIG_JSON")
DB_PORT=$($JQ_BIN -r '.connection.port' "$CONFIG_JSON")

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Backup filename with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$TIMESTAMP.sql"

# Perform the backup without tablespaces to avoid PROCESS privilege error
$MYSQLDUMP_BIN -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" --no-tablespaces "$DB_NAME" > "$BACKUP_FILE" 2

# Check result
if [ $? -eq 0 ]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Backup successful: $BACKUP_FILE"
else
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Backup FAILED!"
    exit 1
fi
