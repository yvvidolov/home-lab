This list is sorted by importance, you should complete each point in order.  
There are minimum requirements for particular functionality and optional components.  


## Hardware

`paid/one-time` 

- [ ] [Server](hardware.md#device) - mini-itx pc, x86 single board computer, odroid
- [ ] [Storage](hardware.md#storage) - storage hdd/emmc/ssd

## Software

`free` `minimum/NAS`

- [x] [OpenMediaVault](openmediavault.md) - OS/NAS/Docker
- [x] [ZFS/Raid](openmediavault.md#setup-zfs-raid) - Filesystem integrating redundancy
- [x] [VPN](openmediavault.md#vpn-wireguard) - Access to your local network and shares

`free` `minimum/cloud`

- [x] [Portainer](openmediavault.md#setup-docker) - Used to deploy most server services

`free` `optional`

- [ ] [Benchmark](benchmark.md) - Benchmark and compare the used hardware (cpu/memory/hdd)

## External Services 

`paid/subscription` `optional/business`

- [ ] [DNS](dns.md) - Domain name, SSL certificate
  - [ ] [WebSite](website.md) - Some providers have simple hosting
- [ ] [Email](email.md) - email is monopoly, there is no alternative

`free` `optional/personal`

- [ ] [DNS](https://freedns.afraid.org/domain/registry/) - free DNS subdomains

## Self-Hosted Services

`free` `minimum/cloud`

- [ ] [ReverseProxy](reverseproxy.md) - subdomain -> service resolution
- [ ] [NextCloud](nextcloud.md) - Alternative to Google Suite (drive, mail, chat, meet, etc ...)

`free` `optional`

- [ ] [GitLab](gitlab.md) - Source control, issue tracker, wiki, CI/CD

