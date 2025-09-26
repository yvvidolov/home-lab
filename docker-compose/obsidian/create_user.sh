#!/bin/bash
# set -e

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <COUCHDB_URL> <ADMIN_NAME> <ADMIN_PASS> <USER_NAME> <USER_PASSWORD>"
  echo "Example: $0 http://localhost:5984 admin_name admin_password user_name user_password"
  exit 1
fi

COUCHDB_URL="$1"
ADMIN_USER="$2"
ADMIN_PASS="$3"
USER_NAME="$4"
USER_PASS="$5"

CURL_CLI="-s -u $ADMIN_USER:$ADMIN_PASS"

declare -A USERS
USERS=( ["$USER_NAME"]="$USER_PASS" )

for USER in "${!USERS[@]}"; do
  PASS="${USERS[$USER]}"
  DB="vault_${USER}"

  # ======================= Initialize Database =======================
  echo "Trigger database initialization"
  STATUS=$(curl $CURL_CLI "$COUCHDB_URL/_all_dbs")
  echo "  Databases: $STATUS"

  if [[ "$STATUS" != *"_users"* ]]; then
    echo "  Create _users database"
    ST=$(curl $CURL_CLI -X PUT "$COUCHDB_URL/_users")
  fi

  if [[ "$STATUS" != *"_replicator"* ]]; then
    echo "  Create _replicator database"
    ST=$(curl $CURL_CLI -X PUT "$COUCHDB_URL/_replicator")
  fi

  if [[ "$STATUS" != *"_global_changes"* ]]; then
    echo "  Create _global_changes database"
    ST=$(curl $CURL_CLI -X PUT "$COUCHDB_URL/_global_changes")
  fi

  # ======================= Create User =======================
  echo -e "\nChecking if user '$USER' exists..."
  STATUS=$(curl $CURL_CLI -o /dev/null -w "%{http_code}" "$COUCHDB_URL/_users/org.couchdb.user:$USER")

  if [ "$STATUS" == "000" ]; then
    echo "[Error] Wrong server URL or PORT"
    break
  fi

  if [ "$STATUS" == "200" ]; then
    echo "  User '$USER' already exists. Skipping creation."
  elif [ "$STATUS" == "404" ]; then
    echo "  Creating user '$USER'..."
    curl $CURL_CLI -X PUT "$COUCHDB_URL/_users/org.couchdb.user:$USER" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "'"$USER"'",
        "password": "'"$PASS"'",
        "roles": [],
        "type": "user"
      }'
  else
    echo "[Error] Status: $STATUS"
    break
  fi

  # ======================= Create Database =======================
  echo -e "\nChecking if database '$DB' exists..."
  STATUS=$(curl $CURL_CLI -o /dev/null -w "%{http_code}" "$COUCHDB_URL/$DB")

  if [ "$STATUS" == "200" ]; then
    echo "  Database '$DB' already exists. Skipping creation."
  elif [ "$STATUS" == "404" ]; then
    echo "  Creating database '$DB'..."
    STATUS=$(curl $CURL_CLI -X PUT "$COUCHDB_URL/$DB")
  else
    echo "[Error] Status: $STATUS"
    break
  fi

  # ======================= Assign Permission =======================
  echo -e "\nAssigning permissions to '$USER' on '$DB'..."
  STATUS=$(curl $CURL_CLI -X PUT "$COUCHDB_URL/$DB/_security" \
    -H "Content-Type: application/json" \
    -d '{
      "admins": { "names": [], "roles": [] },
      "members": { "names": ["'"$USER"'"], "roles": [] }
    }')

  echo -e "\nFinished provisioning for '$USER'"
  echo "----------------------------------------"
done
