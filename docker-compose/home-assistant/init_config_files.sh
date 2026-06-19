#!/bin/sh

OVERWRITE=true

if [ -f .env ]; then
  export $(echo $(grep -v '^#' .env | xargs))
else
  echo ".env file missing!"
  exit 1
fi

if [ -f .env-override ]; then
  export $(echo $(grep -v '^#' .env-override | xargs))
fi

echo "Initializing host directories at ${PATH_HOST}..."
mkdir -p "${PATH_HOST}/mosquitto/data" \
         "${PATH_HOST}/mosquitto/log" \
         "${PATH_HOST}/zigbee2mqtt/data" \
         "${PATH_HOST}/config"

# ========================
# === Mosquitto Config ===
# ========================
if [ ! -f "${PATH_HOST}/mosquitto/mosquitto.conf" ] || [ "$OVERWRITE" = true ]; then
  echo "Creating mosquitto.conf..."
  cat << EOF > "${PATH_HOST}/mosquitto/mosquitto.conf"
listener 1883
allow_anonymous true
EOF
fi

# ===========================
# === Zigbee2MQTT Config  ===
# ===========================
if [ ! -f "${PATH_HOST}/zigbee2mqtt/data/configuration.yaml" ] || [ "$OVERWRITE" = true ]; then
  echo "Creating Z2M configuration.yaml..."
  cat << EOF > "${PATH_HOST}/zigbee2mqtt/data/configuration.yaml"
homeassistant: true
mqtt:
  server: "mqtt://${SERVER_IP}:${PORT_MQTT}"
serial:
  port: "tcp://${RADIO_IP}:6638"
  adapter: ember
frontend:
  port: 8080
EOF
fi

# =============================
# === Home Assistant Config ===
# =============================
if [ ! -f "${PATH_HOST}/config/configuration.yaml" ] || [ "$OVERWRITE" = true ]; then
  echo "Creating HA configuration.yaml..."
  cat << EOF > "${PATH_HOST}/config/configuration.yaml"
default_config:

automation: !include automations.yaml

http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.16.0.0/12
    - ${SERVER_IP}
EOF
fi

echo "Initialization complete."
