#!/bin/bash

# Configuration
CONFIG_JSON="mysql_config.json"

# Check if config exists
if [ ! -f "$CONFIG_JSON" ]; then
    echo "Config file $CONFIG_JSON not found!"
    exit 1
fi

# Function to read configuration from JSON file
read_config() {
    DB_HOST=$(jq -r '.connection.host' "$CONFIG_JSON")
    DB_USER=$(jq -r '.connection.user' "$CONFIG_JSON")
    DB_PASSWORD=$(jq -r '.connection.password' "$CONFIG_JSON")
    DB_NAME=$(jq -r '.connection.database' "$CONFIG_JSON")
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
