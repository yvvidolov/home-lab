After installation:
- Open `192.168.2.2:${PORT_HTTP}`
- Site Title: `gitea: vidolov.net`
- Server Domain: `gitea.vidolov.net`
- SSH server port: `222`
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
