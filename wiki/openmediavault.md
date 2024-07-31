# OpenMediaVault

This is the operating system of our server, it is enough to make a network attached storage (NAS) without any other dependencies. 

## Installation

> [Official installation guide](https://docs.openmediavault.org/en/stable/installation/index.html)  
> [Official download link](https://www.openmediavault.org/download.html)  

### Prepare bootable media

- Download omv iso file: `wget https://sourceforge.net/projects/openmediavault/files/iso/7.0-32/openmediavault_7.0-32-amd64.iso`
- Download usb multiboot flash tool: `wget https://sourceforge.net/projects/ventoy/files/v1.0.99/ventoy-1.0.99-linux.tar.gz/download -O ventoy.zip && tar -xzf ventoy.zip`
- Use ventoy to prepare a USB drive: `./ventoy-1.0.99/VentoyGUI.x86_64` or `./ventoy-1.0.99/VentoyWeb.sh`
- Copy `openmediavault_7.0-32-amd64.iso` to newly mounted ventoy driver
- Unmount usb drive safely, as copy process is asynchronous

### Install on target device

- attach the usb storage to your server
  - when powering up press F12 to enter boot menu
  - when powering up press F10 or Delete, to enter BIOS and change the boot order
- install OMV7 on the emmc or SSD storage (NOT the HDDs meant for RAID)
- setup SSH root password during installation
> NOTE: the OS will use the whole physical disk, you can later repartition by shrinking the OS volume.

## Setup

### First Login

- find server IP by using your router: Network Map -> List Clients
> NOTE: we will use IP 192.168.2.2 as an example to access OMV
- access OMV through a browser at: `local.nas` or `http://192.168.2.2:80`
- first login credentials, User: `admin` Password: `openmediavault`
- change Admin Password: User Settings -> Change Password
> NOTE: if you forget your password login with SSH and run `omv-firstaid`
- install all updates: System -> Update Management -> Updates -> Install Updates
- install omv-extras from ssh shell or System -> Plugins -> wetty:
  - `ssh root@192.168.2.2` 
  - `wget -O - https://github.com/OpenMediaVault-Plugin- Developers/packages/raw/master/install | bash`
- change OMV web interface port: System -> Workbench -> port -> `82`
- from now on access your NAS OMV server by: `http://nas.local:82` `http://192.168.2.2:82`

### Setup HDD Spindown (optional)

> NOTE: this might be useful if you have a single client with very low usage.
> HDDs are meant for continuous use and spinning them up and down will effect their lifespan. This will also introduce latency to the system.

Storage -> Disks -> Edit:  
- Advanced power management < 127 (this enables spin down)
- Spindown time: 60min

### Setup ZFS (RAID)

> NOTE: this is an advanced filesystem supporting compression, encryption and redundancy. It is heavily optimized by utilizing various caches. 

> All you need to know (advanced): [ZFS Bible](https://jro.io/truenas/openzfs/#arc)

- install ZFS plugin: System -> Plugins -> openmediavault-zfs -> install

#### Setup zfs using the GUI:
- Storage -> zfs -> pools
  - Add -> Add pool:
    - Name: zpool
    - Pool type: mirror (hdd == 2), raidz1 (hdd > 2), raidz2 (hdd > 4)
    - Devices: select all physical disks you want in the pool
    - Mount point: /zpool/
    - Device alias: By ID
    - Compression: Only if you have the extra CPU power
    - Save
  - Click zpool -> Add -> Add filesystem:
    - Prefix: choose zpool
    - Name: docker
    - Mountpoint: /zpool/docker
    - Add
  - Click zpool -> Add -> Add filesystem:
    - Prefix: choose zpool
    - Name: users
    - Mountpoint: /zpool/users
    - Add

#### Setup zfs using the CLI:
- connect to ssh server: `ssh root@{IP}`
- find disk ids: `ls -la /dev/disk/bi-ud/`
- make pool: 
  - `zpool create -f zpool mirror /dev/disk/by-id/ata-### /dev/disk/by-id/ata-###`
  - or
  - `zpool create -f zpool raidz1 /dev/disk/by-id/ata-### /dev/disk/by-id/ata-### /dev/disk/by-id/ata-###`
- make fs: `zfs create zpool/docker`
- make fs: `zfs create zpool/users`
- check status: `zpool list -v; zfs list`

##### Fix ACL permissions for ZFS pool
`optional`
https://dannyda.com/2022/05/02/how-to-fix-openmediavault-zfs-pool-acl-privileges-error-failed-to-execute-command-export-operation-not-supported/
> NOTE: this might be needed for advanced control of windows shares

### Setup Smart and Scrub
- Storage -> SMART -> Settings -> Enabled -> True
- Storage -> SMART -> Scheduled Tasks:
  - Add for each HDD:
    - Short Self-Test 00 * * * # every day at 0AM
    - Long Self-Test 01 * * 6 # every Saturday

> This will ensure an HDD will not fail without notice. You will receive emails from the system if something is wrong (if SMTP is properly set)

- Make sure ZFS Scrub CRON is enabled (you might need to modify this file):
  - from SSH: `cat /etc/cron.d/zfsutils-linux`

```
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# TRIM the second Sunday of every month.
24 0 8-14 * * root if [ $(date +\%w) -eq 0 ] && [ -x /usr/lib/zfs-linux/trim ]; then /usr/lib/zfs-linux/trim; fi

# Scrub the first and third Sunday of every month.
24 0 1-7 * * root if [ $(date +\%w) -eq 0 ] && [ -x /usr/lib/zfs-linux/scrub ]; then /usr/lib/zfs-linux/scrub; fi
24 0 15-21 * * root if [ $(date +\%w) -eq 0 ] && [ -x /usr/lib/zfs-linux/scrub ]; then /usr/lib/zfs-linux/scrub; fi
```

> NOTE: SCRUB every two weeks, this will ensure data integrity and redundancy. TRIM once a month, this maintains unused storage, optimizes writes and reduces wear.

### Setup Docker
- System -> omv-extras -> enable 'Docker repo'
- Storage -> Shared Folders -> Create: zpool/docker docker_compose_data/
- Storage -> Shared Folders -> Create: zpool/docker docker_compose_shared/
- Services -> Compose -> Settings:
  - Compose Files -> shared folder: docker_compose_shared
  - Data -> shared folder: docker_compose_data
  - Docker -> Docker storage: /zpool/docker/docker_storage

### Portainer
- Services -> Compose -> Files -> Add -> Add from example -> name: portainer - portainer
- Services -> Compose -> Files -> portainer -> edit -> image: portainer/portainer-ce:sts
- Services -> Compose -> Files -> portainer -> up
- Browse `192.168.2.2:9000`
- Change Admin Password: `my_secret_pass`
- Settings -> Environments -> local -> Public IP: `192.168.2.2`
- Settings -> App Tempplates -> URL: 
  - `https://raw.githubusercontent.com/yvvidolov/home-lab/main/portainer-templates/templates.json`
  - or
  - `https://raw.githubusercontent.com/Lissy93/portainer-templates/main/templates.json`

> NOTE: You can manage docker entirely through the OMV interface, but portainer will make deployment and management easier. You can also split access to the OS and container management.

### VPN Wireguard
- Services -> Wireguard -> Tunnels -> Create:
  - Enable: `check`
  - Tunnel number: `1`
  - Name: `omv_vpn`
  - Network adapter: `enp2s0`
  - Endpoint: `vidolov.net`
  - Port: `54320`
  - Advanced -> Configure iptables: `check`
- Services -> Wireguard -> Clients -> Create:
  - Enable: `check`
  - Client number: `1`
  - Tunnel number: `1 - omv_vpn`
  - Name: `Android/Laptop/etc`
- Services -> Wireguard -> Clients -> Generate QR code or Client Config
  - scan the QR code on the client device
  - generate client config file and copy the contents

- Forward wireguard UDP port on your WAN Router: `UDP :54320 to 192.168.2.2:54320`
