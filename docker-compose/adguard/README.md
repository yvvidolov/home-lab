# Debian DNS
> Most systems already bind :53 so we must disable systemd-resolv to deploy another DNS

1. Disable the service (might come back on system update):  
sudo systemctl stop systemd-resolved  
sudo systemctl disable systemd-resolved  
sudo systemctl mask systemd-resolved  
sudo rm /etc/resolv.conf  
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf  
  
2. Disable the listener:  
Or set DNSStubListener=no in /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved 


# Test
sudo apt install dnsutils  
nslookup example.com  
dig example.com  
