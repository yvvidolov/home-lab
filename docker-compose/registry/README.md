# Common
docker tag myimage:latest localhost:5000/myimage:latest

docker push localhost:5000/myimage:latest
docker pull localhost:5000/myimage:latest

# List Images
curl http://localhost:5000/v2/_catalog

# basic authentication:
mkdir -p $PATH_DOCKER/registry/auth
docker run --rm --entrypoint htpasswd httpd:2 -Bbn username password > $PATH_DOCKER/registry/auth/htpasswd
 
# For testing with HTTP (insecure)
`/etc/docker/daemon.json`
"insecure-registries": ["localhost:5000", "your-registry-domain:5000"]

# To clean up unreferenced data
docker exec registry bin/registry garbage-collect /etc/docker/registry/config.yml
