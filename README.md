<!-- ---------- Header ---------- -->
<div align="center">
  <h1>home-lab</h1>
<p>Setup your own cloud at home</p>

<!-- ---------- Badges ---------- -->
  <div align="center">
    <img alt="License" src="https://img.shields.io/github/license/yvvidolov/home-lab?color=c3e7ff&style=flat-square">
    <!--<img alt="Downloads" src="https://img.shields.io/github/downloads/yvvidolov/home-lab/total.svg?color=c3e7ff&style=flat-square">-->
    <img alt="Last commit" src="https://img.shields.io/github/last-commit/yvvidolov/home-lab?color=c3e7ff&style=flat-square">
    <img alt="Repo size" src="https://img.shields.io/github/repo-size/yvvidolov/home-lab?color=c3e7ff&style=flat-square">
    <img alt="Stars" src="https://img.shields.io/github/stars/yvvidolov/home-lab?color=c3e7ff&style=flat-square">
    <br>
</div>
</div>

<!-- ---------- Description ---------- -->
---

Setup the hardware, software and configuration for a Home Lab server. Your own personal and private cloud.
It can be used for personal needs or to setup the infrastructure for a (very) small IT company.

## Contents

- [wiki](wiki/README.md) - hardware and software tutorials
- [docker](docker) - custom published containers [hub.docker.com](https://hub.docker.com/repositories/yvvidolov)
- [docker-compose](docker-compose) - stacks for different services
- [portainer-templates](portainer-templates/README.md) - fast way to bring up needed services
  - [gen_all.py](portainer-templates) - generate portainer template Json from docker-compose.yml

## Services

- `openmediavault`: NAS server (nfs/cifs/web)
- `nextcloud`: Cloud (files/contacts/groups/sharing)
- `gitlab`: Source control, Issue tracker, Wiki
- `vaultwarden`: Password manager
- `owncast`: Video streaming
- `firefly-iii`: Personal finance
- `heimdall`: Home page
- `cloudflare-ddns`: Dynamic DNS
- `portainer`: Docker deployment

## License

This code is licensed under the [GNU General Public License](LICENSE.md) 
