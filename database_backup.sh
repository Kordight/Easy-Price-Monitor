#!/bin/bash

CONFIG_JSON="/home/sebastian/easy-price-monitor/mysql_config.json"
BACKUP_DIR="/home/sebastian/easy-price-monitor/backups"
JQ_BIN="/usr/bin/jq"
MYSQLDUMP_BIN="/usr/bin/mysqldump"
LOG_FILE="/home/sebastian/easy-price-monitor/backup.log"

# Read config
DB_HOST=$($JQ_BIN -r '.connection.host' "$CONFIG_JSON")
DB_USER=$($JQ_BIN -r '.connection.user' "$CONFIG_JSON")
DB_PASSWORD=$($JQ_BIN -r '.connection.password' "$CONFIG_JSON")
DB_NAME=$($JQ_BIN -r '.connection.database' "$CONFIG_JSON")
DB_PORT=$($JQ_BIN -r '.connection.port' "$CONFIG_JSON")

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$TIMESTAMP.sql"

# Create temporary MySQL config file
TMP_CNF=$(mktemp)
chmod 600 "$TMP_CNF"
cat > "$TMP_CNF" <<EOL
[client]
user=$DB_USER
password=$DB_PASSWORD
host=$DB_HOST
port=$DB_PORT
EOL

# Run mysqldump using the temporary config file
$MYSQLDUMP_BIN --defaults-extra-file="$TMP_CNF" --no-tablespaces "$DB_NAME" > "$BACKUP_FILE" 2
RESULT=$?

rm -f "$TMP_CNF"

if [ $RESULT -eq 0 ]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Backup successful: $BACKUP_FILE"
else
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Backup FAILED!"
    exit 1
fi

# Function to read configuration from JSON file
read_config() {
    DB_HOST=$(jq -r '.host' "$CONFIG_JSON")
    DB_USER=$(jq -r '.user' "$CONFIG_JSON")
    DB_PASSWORD=$(jq -r '.password' "$CONFIG_JSON")
    DB_NAME=$(jq -r '.database' "$CONFIG_JSON")
}

# Function to create a backup
create_backup() {
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_DIR="backups"
    BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$TIMESTAMP.sql"
    mkdir -p "$BACKUP_DIR"
    mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Backup successful: $BACKUP_FILE"
    else
        echo "Backup failed!"
        exit 1
    fi
}

# Run functions
read_config
create_backup
