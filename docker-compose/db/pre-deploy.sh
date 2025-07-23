# Pgadmin requires special owner when mounted on host
mkdir -p /zpool/docker/db/pgadmin
chown -R 5050:5050 /zpool/docker/db/pgadmin

# Clickhouse requires SSL
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout docker/clickhouse/cert/server.key \
  -out docker/clickhouse/cert/server.crt \
  -days 99999 \
  -subj "/CN=clickhouse-server" 
