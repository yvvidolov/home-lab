1. Edit .env
2. Run init_config_files.sh # only once
3. docker compose up -d

# Add dashboards manually (z2m)
Settings -> Dashboards -> Add dashboard -> webpage:
- URL: http://${SERVER_IP}:${PORT_Z2M_UI}
- Title: Zigbee2MQTT
- Icon: mdi:zigbee
- URL: [automatic]

Settings -> Dashboards -> Add dashboard -> webpage:
- URL: http://${SERVER_IP}:${PORT_FILEEDITOR}
- Title: File Editor
- Icon: mdi:folder-text
- URL: [automatic]
