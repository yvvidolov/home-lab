[Official Docs](https://docs.goauthentik.io/docs/installation/docker-compose)

First install: `http://192.168.2.2:88/if/flow/initial-setup/`

## LDAP setup
https://www.youtube.com/watch?v=RtPKMMKRT_E
> NOTE: ldap provider needs search group added, the search group should contain the bind user!

## Services working with SSO

- [x] NextCloud
- [x] Gitea
- [ ] Gitlab - should be possible
- [ ] MailServer - should be possible
- [ ] RoundCube - should be possible
- [ ] Dolibarr - (can't authenticate with LDAP, only reads users)
