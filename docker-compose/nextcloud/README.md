> NOTE: Beware of coturn port forward range: even 500 ports take 10gb ram!!

### NextCloud
Disable WebAuth: `occ config:system:set --type boolean --value false auth.webauthn.enabled`

### Theming
Install app `custom css` and modify Theming -> Custom CSS
```css
.guest-box {
	box-shadow: 0px 0px 10px black;
	background-color: rgba(200, 200, 200, 0.5);
}

.logo {
	visibility: hidden;
}

footer.guest-box {
	visibility: hidden;
}

.alternative-logins .button-vue:hover {
	background-color: rgb(59, 71, 81) !important;
  	color: white !important;
}

.alternative-logins .button-vue {
	background-color: rgb(59, 71, 81) !important;
  	color: rgb(255, 107, 50) !important;
}

```

### SingleSignOn

#### OpenID
- Admin -> Apps -> Social -> Social Login
- Admin -> Administration Settings -> Social Login
  - 

#### OpenID
- Admin -> Apps -> Social -> OpenID Connect user backend
- Admin -> Administration Settings -> OpenID Connect
  - Identifier: `Authentik`
  - Client ID: `[Copy from Authentic Provider]`
  - Client secret: `[Copy from Authentic Provider]`
  - Discovery endpoint: `https://authentik.vidolov.net/application/o/nextcloud/.well-known/openid-configuration`
  - Scope: `openid email profile`
  - User ID mapping: `preferred_username`
  - Use unique user id: `Uncheck`
  - Auto provision: ?

#### LDAP
- Admin -> Apps -> App Bundles -> LDAP user and group backend 
- Admin -> Administration Settings -> LDAP/AD integration
  - Server: `192.168.2.2` `389`
  - `cn=ldapservice,DC=ldap,DC=goauthentik,DC=io`
  - `[ldapservice user password from authentik]`
  - `DC=ldap,DC=goauthentik,DC=io`
  - Users -> LDAP Filter: `(&(|(objectclass=inetOrgPerson))(|(memberof=cn=nextcloud_users,ou=groups,dc=ldap,dc=goauthentik,dc=io)))`
  - Login Attributes -> LDAP Filter: `(&(&(|(objectclass=inetOrgPerson))(|(memberof=cn=nextcloud_users,ou=groups,dc=ldap,dc=goauthentik,dc=io)))(|(cn=%uid)(mail=%uid)))`
  - Expert -> Internal Username Attribute: `cn`
  - Expert -> UUID Attribute for Users: `uid` # extremely important! this fixes a bug!
  - [NOT NEEDED] Advanced -> Directory Settings -> User Display Name Field: `cn`

##### LDAP logout fix
When using LDAP, users will be logged out every 5 minutes with log message: 'Session token credentials are invalid'  
The fix can be found here: 'https://github.com/nextcloud/server/issues/11113'  
Edit `config.php`:
'auth.storeCryptedPassword' => false
