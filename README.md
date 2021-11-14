# dyndns-linode

**dyndns-linode** is a lightweight dynamic DNS manager for Linode. It pushes IPv4 and IPv6 addresses to the Linode DNS manager for updating A/AAAA records automatically. It is written in Python and the Flask framework.

## Use case
* You use the name servers at Linode to manage the DNS records of your domains.
* You use the Linode services and you also have a local machine (eg. local, testing, UAT, ...) that:
    * is hosted on an internet connection with a dynamic IP address.
    * you want to be reachable through a (sub)domain
* You do not want to use an external Dynamic DNS provider.
* You do have a router that supports a DynDNS upload function and uses [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)
    * The DNS manager was originally written for supporting the DynDNS functionality of an AVM FRITZ!Box 7490 after reading [AsHeiduk's findings on Fritz!Box DynDNS](http://asheiduk.de/post/fritzbox-dyndns/)

## Installation

It is recommended (but not required) to use a virtual environment before installing the required libraries. [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) is a great option to get you started.


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install -r requirements.txt
```

## Configuration
### dyndns-linode 
Duplicate the example configuration file and name it **config.json**
```bash
cp example.config.json config.json
```

Fill in the required parameters:
```json
{
  "webhook":
  {
    "username": "router_username",
    "password": "router_password"
  },
  "linode": {
    "token": "linode_token",
    "domain": "example.com",
    "record": "local",
    "ttl": 300
  }
}

```
In the example above, the URL *local.example.com* would be updated to your dynamic IP address.
* **username**: username that the router sends to the webhook.
* **password**: password that the router sends to the webhook.
* **token**: The API token to update the domainname at the Linode DNS Manager. See the [Linode API documentation](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/#get-an-access-token) on how to retrieve this token. Be sure to give Domain permissions to the generated token.
* **domain**: The hostname domain on which you want the dynamic update to occur.
* **record**: The hostname of A record (and AAAA record if also using IPv6!) on which you want the dynamic update to occur.
* **ttl**: The Time To Live value in seconds. Note that this values follows the Linode guidelines. Valid values are 0, 300, 3600, 7200, 14400, 28800, 57600, 86400, 172800, 345600, 604800, 1209600, and 2419200

#### Deployment

You can choose to run the webhook that triggers the DNS manager on an existing webserver (for example through [mod_wsgi](https://modwsgi.readthedocs.io/en/master/) for Apache).

See the [Flask deployment guide](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/) to consider your options.

### Configuration on local router/deamon

Once the application is up and running you can point the Dynamic DNS update service of your router (or local deamon) to push any new IP addressess to the webhook in the following format (in this example we assume HTTPS is used): 
```bash
https://url/to/service?ipv4=12.34.56.78&ipv6=2001:0db8:85a3:0000:0000:8a2e:0370:7334
```
The webhook accepts 2 parameters:
* ipv4
* ipv6

**Important: note that the router or deamon needs to support [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) to authenticate to the webhook with the username and password that have been entered in the configuration file.**

The DNS manager will verify if the given IP addresses are valid and update the A/AAAA record at the Linode DNS Manager.

The response of the webhook call will report back if the service ran succesfully.
```json

{
  "msg": "Finished", 
  "result": {
    "ipv4": {
      "msg": {
        "created": "2021-11-14T09:37:27", 
        "id": 12345678, 
        "name": "local", 
        "port": 80, 
        "priority": 50, 
        "protocol": null, 
        "service": null, 
        "tag": null, 
        "target": "12.34.56.78", 
        "ttl_sec": 300, 
        "type": "A", 
        "updated": "2021-11-14T14:21:51", 
        "weight": 50
      }, 
      "success": true
    }, 
    "ipv6": {
      "msg": {
        "created": "2021-11-14T14:22:31", 
        "id": 12345678, 
        "name": "local", 
        "port": 0, 
        "priority": 0, 
        "protocol": null, 
        "service": null, 
        "tag": null, 
        "target": "2001:0db8:85a3:0000:0000:8a2e:0370:7334", 
        "ttl_sec": 300, 
        "type": "AAAA", 
        "updated": "2021-11-14T14:22:42", 
        "weight": 0
      }, 
      "success": true
    }
  }
}

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
