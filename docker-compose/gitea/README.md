After installation:
- Open `192.168.2.2:${PORT_HTTP}`
- Site Title: `gitea: vidolov.net`
- Server Domain: `gitea.vidolov.net`
- Gitea base URL: `https://gitea.vidolov.net/`
- EMail Settings (optional):
- Server and Third party settings:
  - Enable OpenID Sign-in: `False`
  - Disable Self-Registration: `True`
  - Require Sign-in to View Pages: ?
- Administrator Account Settings:
  - Username: `gitea` # `admin` is reserved
  - Email address: `gitea@vidolov.net`
  - Password: `my_secret_password`

After login:
- Open: Settings -> Site Administration
- Identity & Access -> Authentication Sources
- Actions -> Runners

From OMV SSH:
- `nano /zpool/docker/gitea/gitea/gitea/conf/app.ini`
- `[server]`
  - `SSH_DOMAIN = vidolov.net`
  - `SSH_PORT = 8022`
  - `MINIMUM_KEY_SIZE_CHECK = false`
  - `ROOT_URL = https://gitea.vidolov.net/`
- `[openid]`
  - `ENABLE_OPENID_SIGNIN = false`
  - `ENABLE_OPENID_SIGNUP = false`
- `[service]`
  - `ALLOW_ONLY_EXTERNAL_REGISTRATION = false`

From Internet Router:
- Add WAN port forward: `omv_gitea_ssh`: `8022` -> `192.168.2.2:8022`

LDAP:
- Admin settings -> Identity & Access -> Authentication Sources -> Add
- Authentication name: `ldap`
- Security protocol: `Unencrypted`
- Host: `192.168.2.2`
- Port: `389`
- Bind DN: `cn=ldapservice,ou=users,DC=ldap,DC=goauthentik,DC=io`
- Bind Password: `[ldapservice user password]`
- User search base: `DC=ldap,DC=goauthentik,DC=io`
- User Filter: `(&(objectClass=posixAccount)(sAMAccountName=%s))`
- User attribute: `sAMAccountName`
- First name attribute: `name`
- Email attribute: `mail`

OpenID:
- Admin settings -> Identity & Access -> Authentication Sources -> Add
- Authentication Type: `OAuth2`
- Authentication Name: `Authentik`
- OAuth2 Provider: `OpenID Connect`
- Client ID (Key): `[copy from authentic provider]`
- Client Secret: `[copy from authentic provider]`
- Icon URL: `https://authentik.vidolov.net/static/dist/assets/icons/icon.svg`
- OpenID Connect Auto Discovery URL: `https://authentik.vidolov.net/application/o/gitea/.well-known/openid-configuration`