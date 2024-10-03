> NOTE: Beware of coturn port forward range: even 500 ports take 10gb ram!!

When using LDAP, users will be logged out every 5 minutes with log message: 'Session token credentials are invalid'  
The fix can be found here: 'https://github.com/nextcloud/server/issues/11113'  
Edit `config.php`:
'auth.storeCryptedPassword' => false
