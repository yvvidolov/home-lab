- Run create_user.sh
  - ./create_user.sh <COUCHDB_URL> <ADMIN_NAME> <ADMIN_PASS> <USER_NAME> <USER_PASSWORD> script to create desired users
  - ./create_user.sh http://localhost:5984 admin_name admin_password user_name user_password
- Open http://host:port/_utils/#login to manage database
  - Config -> Cors -> Enable -> https://domain.com -> Add
- Reverse proxy setup
```
# Proxy headers for CouchDB
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

# Optional: CORS headers if needed
add_header 'Access-Control-Allow-Origin' '*' always;
add_header 'Access-Control-Allow-Methods' 'GET, PUT, POST, DELETE, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, Accept, Origin' always;
```
