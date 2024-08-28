For first login:
- find password: `sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password`
- or use initial_root_password set in installation .env
- login using: `root:[PASS]`

Do not forget to disable User registration from admin panel