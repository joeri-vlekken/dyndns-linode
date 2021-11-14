from flask import Flask, make_response, request
from functions import *
import json
import sys

app = Flask(__name__)


@app.route('/')
def update_dns():
    with open(sys.path[0] + 'config.json') as config_file:
        config_data = json.load(config_file)

    if request.authorization:
        print(request.authorization)
    # Check for basic authentication headers
    if request.authorization and \
            request.authorization.username == config_data['webhook']['username'] \
            and request.authorization.password == config_data['webhook']['password']:

        # Retrieve the IPv4 and IPv6 address from the get request and validate
        ipv4 = validate_ip(4, request.args.get('ipv4'))
        ipv6 = validate_ip(6, request.args.get('ipv6'))

        # Throw error if neither IPv4 of IPv6 address was delivered
        if not ipv4 and not ipv6:
            make_response({'msg': 'Provide at least a valid IPv4 or IPv6 address'}, 400)

        # Update the IPv4 record at Linode if present
        if ipv4:
            ipv4 = update_record(
                ipv4,
                config_data['linode']['token'],
                config_data['linode']['domain'],
                config_data['linode']['record'],
                config_data['linode']['ttl']
            )

        # Update the IPv6 record at Linode if present
        if ipv6:
            ipv6 = update_record(
                ipv6,
                config_data['linode']['token'],
                config_data['linode']['domain'],
                config_data['linode']['record'],
                config_data['linode']['ttl']
            )

        # Confirmation response that the update ended successfully
        return make_response({'msg': 'Finished', 'result': {'ipv4': ipv4, 'ipv6': ipv6}}, 200)

    else:
        return make_response({'msg': 'Not authorized'}, 401, {'WWW-Authenticate': 'Basic realm="Login required'})


if __name__ == '__main__':
    app.run()
