
### mxrouting.net
We are going to use mxrouting as an smtp relay to avoid IP blacklisting and RTP dns check.  
Current blackfriday deal 30\$ for 3 year service (7200 mails per day).  
Lifetime account is 150\$.

- Account Manager -> Domain Setup -> Add New -> vidolov.net
- Account Manager -> SSL Certificates -> Disable SSL   
- E-mail Manager -> Disable DKIM
- E-mail Manager -> Create Accont -> relay@vidolov.net

### cloudflare DNS
Generate DKIM key
`setup config dkim keysize 2048 domain 'example.com,not-example.com'`

- `CNAME` | `autoconfig` | `mail.vidolov.net`
- `CNAME` | `autodiscover` | `mail.vidolov.net`
- `CNAME` | `mail` | `vidolov.net`
- `MX` | `vidolov.net` | `mail.vidolov.net`
- `TXT` | `_dmarc` | `v=DMARC1; p=quarantine; sp=none; fo=0; adkim=r; aspf=r; pct=100; rf=afrf; ri=86400; rua=mailto:dmarc.report@vidolov.net; ruf=mailto:dmarc.report@vidolov.net`
- `TXT` | `mail._domainkey` | `v=DKIM1; k=rsa; p=[generated_key]` # generated DKIM key
- `TXT` | `vidolov.net` | `v=spf1 include:mxroute.com -all`

### Public Ports
Following ports need to be port forwarded to the mail server: 
- `25` # SMTP
- `587` # ESMTP
- `143` # IMAP4
- `993` # IMAP4

## docker-mailserver
[Official Documentation](https://docker-mailserver.github.io/docker-mailserver/latest/introduction/)

- Share lets encrypt etc directory volume from nginx proxy manager
- `docker compose up` # start the container or use portainer template
- `docker exec -ti mailserver setup email add admin@vidolov.net [my_secret_password]` # execute through ssh on server

### docker-mailserver command cheat sheet
Add new user: `docker exec -ti mailserver setup email add admin@vidolov.net [my_secret_password]`  
Add user alias: `docker exec -ti mailserver setup alias add yavor@vidolov.net admin@vidolov.net`  
Set user quota: `docker exec -ti mailserver setup quota set admin@vidolov.net 10M`  
Show user verbose list: `docker exec -ti mailserver setup email list`  

## RoundCube
> NOTE: There seems to be a bug in docker sqlite assigned owners  
> Execute the following to fix: `chown -R root:root /zpool/docker/roundcube # ${PATH_ROUNDCUBE}`

## Testing email setup and deliverability
- https://www.mail-tester.com/  
- https://mxtoolbox.com/deliverability
- https://mxtoolbox.com/SuperTool.aspx?action=dmarc%3amail.vidolov.net&run=toolpage
