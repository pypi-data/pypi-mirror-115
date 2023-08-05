## Introduction
Scaleway Dedibox (online.net) DNS Authenticator plugin for Certbot

## Get API Key
Your API Key is accessible from [this link](https://console.online.net/en/api/access)

## Configuration
Generate a credential.ini with very limited access. The file should contain only one line
```
certbot_dns_online:dns_online_token = <api-secret-key>
```

## Get Certificats
Launch the following command:
```
certbot certonly \
  --authenticator certbot-dns-online:dns-online \
  --dns-online-credentials ~/credential.ini \
  -d example.com
```
