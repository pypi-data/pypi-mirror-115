## Introduction
Scaleway Dedibox (online.net) DNS Authenticator plugin for Certbot

We use the library dns-lexicon like the official plugins. 
However, there is a small bug in the dns-lexicon online module.
This plugin supports only two-segment domain, such as example.com. 
Three segement domains such as service.gouv.fr are not supported

## Get API Key
Your API Key is accessible from [this link](https://console.online.net/en/api/access)

## Configuration
Generate a credential.ini with very limited access. The file should contain only one line
Windows
```
certbot_dns_online:dns_online_token = <api-secret-key>
```
Linux
```
dns_online_token = <api-secret-key>
```

## Get Certificats
Launch the following command:
```
certbot certonly \
  --authenticator dns-online \
  --dns-online-credentials ~/credential.ini \
  -d example.com
```
