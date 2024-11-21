# Slurp'it

## Getting started

This repository is for hosting the documentation and configuration files for the Slurp'it images.
Our changelog can be found here: https://slurpit.io/knowledge-base/changelog/

To learn how to install Slurp'it and all the possible options, please read the **installation manual**.
When you are looking for an **OVA** visit: https://slurpit.io/knowledge-base/ova-installation-guide/

## Quick start

Rename docker-compose.override-EXAMPLE.yml to docker-compose.override.yml

Change in the file docker-compose.override.yml:

1. Three times your Timezone for the slurpit-warehouse, slurpit-scraper, slurpit-scanner & slurpit-portal containers:
   - `TZ: Europe/Amsterdam`

2. The url to visit the web gui:
   - `PORTAL_BASE_URL: http://localhost`

The Portal URL to access the web GUI is currently set to http://localhost. If you prefer to use HTTPS, update the URL to https://your_domain_name or https://your_server_ip and ensure you have the correct SSL certificates placed in the `certs` folder. 

_Incase you changed the default ports for the portal, add it after the PORTAL_BASE_URL. E.g. http://localhost:81_

### Windows

To start the containers run `up.bat`
To stop the containers run `down.bat`

### macOS or Linux

To start the containers run `up.sh`
To stop the containers run `down.sh`

## Default login

Username:
`admin@admin.com`

Password:
`12345678`

## Backups

Since the system is based on containers, the application's data and configuration are stored within volume folders.
This makes it very easy to backup and restore the application.

### Create backup

Copy the folders `certs` and `db` to safe location where you store your backups.
You can do this while the platform is running, but it's better to turn off the application.

> Example

```cp -a /opt/slurpit/db /opt/backup/db -R```

*-a means keep the original permissions, this is required for the DB folder.*

*-R means copy every file in the folder*

### Restore backup

1. Turn off the software by running down.bat or down.sh
2. Replace the backup folders `certs` and `db`.
3. Turn on the software again up.bat or up.sh

## Update the containers

### Online environment

When you start Slurp'it by using up.sh or up.bat the containers will be automatically updated.
So incase you want to update the application you just have to restart it using the scripts.

### Offline environment

1. Stop the application
2. Download the latest images like specified in the Installation Manual.
3. Start the application

## SSL Certificate

### Adding a certificate

To add a certificate:

1. Place the following files in the `certs` folder:
   - `private.key`
   - `certificate.crt`
2. Change the `PORTAL_BASE_URL`, `WAREHOUSE_CALLBACK_SCANNER_URL`, `WAREHOUSE_CALLBACK_SCRAPER_URL` variable to `https` in the `docker-compose.yml` file.

### Replace a certificate

To replace a certificate:

1. Run the `down.sh` or `down.bat` script.
2. Replace the files in the `certs` folder.
3. Run the `up.sh` or `up.bat` script.

### Create a self-signed certificate

If you don't have a certificate yet, follow these steps to create one:

1. Generate a private key:
   ```openssl genrsa -out private.key 2048```
2. Generate a certificate signing request (CSR):
    ```openssl req -new -key private.key -out certificate.csr```
3. Generate a self-signed certificate:
    ```openssl x509 -req -in certificate.csr -signkey private.key -out certificate.crt```