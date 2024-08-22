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

From Internet Router:
- Add WAN port forward: `omv_gitea_ssh`: `8022` -> `192.168.2.2:8022`
