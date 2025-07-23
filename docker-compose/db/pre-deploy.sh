# Usage: ./pre-deploy.sh [pgadmin_host_path]

# Pgadmin requires special owner when mounted on host (do this manually, komodo hooks work inside a container)
if [ -n "$1" ]; then
  mkdir -p "$1"
  chown -R 5050:5050 "$1"
fi

# Clickhouse needs a keypair
mkdir -p docker/clickhouse/cert
[ -f docker/clickhouse/cert/server.key ] || openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout docker/clickhouse/cert/server.key \
  -out docker/clickhouse/cert/server.crt \
  -days 99999 \
  -subj "/CN=clickhouse-server"
