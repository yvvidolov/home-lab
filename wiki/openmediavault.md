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

### First Login (web)

- find server IP by using your router: Network Map -> List Clients
> NOTE: we will use IP 192.168.2.2 as an example to access OMV
- access OMV through a browser at: `local.nas` or `http://192.168.2.2:80`
- first login credentials, User: `admin` Password: `openmediavault`
- change Admin Password: User Settings -> Change Password
> NOTE: if you forget your password login with SSH and run `omv-firstaid`
- install all updates: System -> Update Management -> Updates -> Install Updates
- install omv-extras from ssh shell or System -> Plugins -> wetty:
  - `ssh root@192.168.2.2` 
  - `wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash`
- change OMV web interface port: System -> Workbench -> port -> `82`
- from now on access your NAS OMV server by: `http://nas.local:82` `http://192.168.2.2:82`

### Additional linux tools (ssh)

Installation is pretty bare-bones, install some administration packages:
- apt install net-tools # ifconfig
- apt install lm-sensors # sensors-detect, sensors
- apt install tree # filesystem visualization
  
### Setup Partitions (ssh)(optional)
To modify partitions, the root file system needs to be unmounted. In order to do this, we can boot another OS from a USB drive or using omv-kernel:

- System -> Plugins -> openmediavault-kernel
- System -> Kernel:
> Using GUI # connect monitor and keyboard/mouse to server
  - GParted Live -> Install
  - GParted Live -> Reboot Once
  - Attach monitor, System -> Reboot
  - Boot GParted: GParted Live (Safe graphic settings, vga=normal)
> Using CLI # headless (network)
  - Clonezilla -> Install CloneZilla
  - Clonezilla -> Reboot to Clonezilla once

#### Resize OS partition (optional)
> By default OMV uses the whole disk, the os partition can be shrunk to avoid wasting space. Default installation uses around 3gb. Using docker storage images/volumes for a medium size homelab might expand this to 16gb. To future proof use 64/128gb.

##### GParted

- Press `enter` (don't touch keymap), `enter` (language), `enter` (boot)
- Select your physical device on top left
- Check partitions for OMV OS (usually the biggest one)(ext4)
- Right click -> Resize -> New Size (64000MiB)
- Apply All Operations

##### CLI (risky)

On connected network machine (headless):
- `ssh-keygen -f "~.ssh/known_hosts" -R "192.168.2.2"`
- `ssh user@192.168.2.2 # pass live`

Find disk and partition information:
- `lsblk` # find physical disks and partitions
- `sudo fdisk /dev/nvme0n1 -l` # list partitions of OMV OS disk
- `sudo e2fsck -f -y -v -C 0 /dev/nvme0n1p2` # check partition for errors
- `sudo resize2fs -P /dev/nvme0n1p2` # check used space in sectors

Shrink the OS partition:
- `resize2fs -p 'dev' 128G` # shrink filesystem
- TODO: is this command correct? : `parted /dev/sdb resizepart 2 10G` # shrink partition
- TODO: is this necessary? : `resize2fs /dev/sdb2` # extend to full size


### Setup backup (web/cli)
- System -> Plugins -> openmediavault-backup

#### Second fallback OS (cli)
- Install second instance of OMV on eMMC (if first is on SSD)
- Storage -> File Systems -> Mount Existing -> /dev/mmcblk0p2
- Storage -> Shared Folders -> Create -> /dev/mmcblk0p2
- `ssh root@192.168.2.2`
- `rsync -ah --delete --info=progress2 --exclude=/srv --exclude=/mnt --exclude=/home --exclude=/root --exclude=/zpool --exclude=/tmp --exclude=/export --exclude=/lost+found --exclude=/media --exclude=/proc --exclude=/sys / /srv/dev-disk-by-uuid-####` # change last argument to second OMV installation!

##### Restore
- Change bad OS disk
- Install OMV on new OS disk
- Boot to second fallback OS (from emmc)(fully functional copy)
- rsync files back to new instalation

#### Backup Image (web)
- Storage -> ZFS -> Pools -> Add filesystem -> name: backup_omv
- Storage -> Shared Folders -> Create -> /zpool/backup_omv
- System -> Backup -> Settings:
  - shared folder: backup_omv
  - method: fsarchiver
  - extra options: `--exclude=/srv --exclude=/mnt --exclude=/home --exclude=/root --exclude=/zpool --exclude=/tmp --exclude=/export --exclude=/lost+found --exclude=/media --exclude=/proc --exclude=/sys`
- Run backup or setup CRON

##### Restore
[tutorial](https://forum.openmediavault.org/index.php?thread/43774-how-to-restore-omv-system-backup-made-with-openmediavault-backup-plugin/)

### Setup UPS (web)(todo)
- System -> Plugins -> openmediavault-nut
- Services -> UPS:

### Setup notifications (web)(e-mail)(todo)
- System -> Notification -> Settings:
  - Enabled: check

- System -> Notification -> Events:
  - SMART
  - UPS
  - ZFS ZED
  - ?

### Setup HDD Spindown (web)(optional)

> NOTE: this might be useful if you have a single client with very low usage.
> HDDs are meant for continuous use and spinning them up and down will effect their lifespan. This will also introduce latency to the system.

Storage -> Disks -> Edit:  
- Advanced power management < 127 (this enables spin down)
- Spindown time: 60min

### Setup ZFS (web)(RAID)

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

#### Add L2ARC cache (ssh)
We can speed up slow HDD access to files/metadata by using a faster SSD for ZFS caching.

##### Setup un-partitioned space on any disk
- `fdisk -l` # identify partition positions (start/end sectors)
- `fdisk /dev/nvme0n1` # replace nvme with your disk device
  - `F` # print un-partitioned space {start}/{end} sectors
  - `n` # choose number, enter for default
    - `enter` # choose default number
    - `enter` # verify first sector is {start}
    - `enter` # verify last sector is {end}
  - `w` # apply changes
  - `q` # quit
- `fdisk -l /dev/nvme0n1` # verify new partition
- note new partition device: `/dev/nvme0n1p4`

##### Setup L2ARC
- `zpool add zpool cache /dev/nvme0n1p4` # the partition to use
- `zpool status` # verify it is being used
- `arcstat -a` # check stats
- `arcsummary` # check stats

### Setup Smart and Scrub (web)
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

### Setup Shares

#### /zpool/docker - docker
You can mount the docker folder over the network, so it's easier to work with service configurations. Note that this is dangerous and should be used for development only. You can use the folder from any user, read/write will be treated as if it was done by root:root on the server (squash).
- Storage -> Shared Folders -> Create: docker, zpool/docker, /
- Services -> NFS -> Shares -> Create: docker, 192.168.2.0/24, Read/Write
  - Extra Options: `rw,sync,no_subtree_check,all_squash,anonuid=0,anongid=0,crossmnt`

> Client: `sudo mount 192.168.2.2:/docker ./docker`

#### /zpool/users - nextcloud



### Setup Docker

#### Vanilla (web)(cli/portainer)
- System -> omv-extras -> enable 'Docker repo'
- System -> plugins -> openmediavault-compose
- Services -> Compose -> Settings:
  - Docker Storage: /ssd/docker_storage (/var/lib/docker)
  - Reinstall Docker

##### Portainer installation (ssh)
- `cd /zpool/docker/; mkdir -p portainer; cd portainer`
- `wget https://raw.githubusercontent.com/yvvidolov/home-lab/main/docker-compose/portainer/docker-compose.yml`
- `docker compose up -d`

#### With OMV management (web)
- System -> omv-extras -> enable 'Docker repo'
- Storage -> Shared Folders -> Create: zpool/docker docker_compose_data/
- Storage -> Shared Folders -> Create: zpool/docker docker_compose_shared/
- Services -> Compose -> Settings:
  - Compose Files -> shared folder: docker_compose_shared
  - Data -> shared folder: docker_compose_data
  - Docker -> Docker storage: /zpool/docker/docker_storage

##### Portainer installation (optional)
- Services -> Compose -> Files -> Add -> Add from example -> name: portainer - portainer
- Services -> Compose -> Files -> portainer -> edit -> image: portainer/portainer-ce:sts
- Services -> Compose -> Files -> portainer -> up

### Portainer Setup (web)
- Browse `192.168.2.2:9000`
- Change Admin Password: `my_secret_pass`
- Settings -> Environments -> local -> Public IP: `192.168.2.2`
- Settings -> App Tempplates -> URL: 
  - `https://raw.githubusercontent.com/yvvidolov/home-lab/main/portainer-templates/templates.json`
  - or
  - `https://raw.githubusercontent.com/Lissy93/portainer-templates/main/templates.json`

> NOTE: You can manage docker entirely through the OMV interface, but portainer will make deployment and management easier. You can also split access to the OS and container management.

### VPN Wireguard (web)
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
