import ipaddress
import requests


# Validation of IP addresses
def validate_ip(version: int, address: str):
    try:
        ip_address = ipaddress.ip_address(address)
        if isinstance(ip_address, ipaddress.IPv4Address) and version == 4:
            return ip_address
        elif isinstance(ip_address, ipaddress.IPv6Address) and version == 6:
            return ip_address
    except ValueError:
        return False


# Update the record at Linode DNS Manager
def update_record(
        address: [ipaddress.IPv4Address, ipaddress.IPv6Address],
        token: str,
        domain: str,
        record: str,
        ttl: int
):
    api_url = "https://api.linode.com/v4/domains/"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    domain_id: str = ''
    record_id: str = ''

    # Define if we need to update an A or AAAA record
    if isinstance(address, ipaddress.IPv4Address):
        record_type = 'A'
    elif isinstance(address, ipaddress.IPv6Address):
        record_type = 'AAAA'
    else:
        return {'success': False,
                'msg': 'Did not receive a valid IP address.'}

    # Retrieve the list of domains
    print('Retrieve list of domains')
    try:
        domains = requests.get(api_url, headers=headers)
    except requests.exceptions.RequestException as e:
        return {'success': False,
                'msg': f'Linode API error: {str(e)}'}

    print(f'Search for domain {domain} and retrieve ID')

    # Search for the specific domain and retrieve the id
    for item in domains.json()['data']:
        if item['domain'] == domain:
            domain_id = item['id']

    # Exit if the domain was not found
    if not domain_id:
        return {'success': False, 'msg': 'Domain was not found in Linode DNS Manager.'}

    # Retrieve the list of records for the domain
    print(f'Retrieve list or records for domain {domain_id}')
    try:
        records = requests.get(f'{api_url}{domain_id}/records/', headers=headers)
    except requests.exceptions.RequestException as e:
        return {'success': False, 'msg': f'Linode API error: {str(e)}'}

    # Search for the specific record and retrieve the id
    print(f'Search for the specific record and retrieve the id in domain {domain_id}')
    for item in records.json()["data"]:
        if item['name'] == record and item['type'] == record_type:
            record_id = item['id']

    # Exit if the domain was not found
    if not record_id:
        return {
            'success': False,
            'msg': f'{record_type} record {record} on domain {domain} was not found in Linode DNS Manager.'
        }

    # Update the record
    print(f'update record: {address}')
    data = {
        "name": record,
        "target": address.exploded,
        "ttl_sec": ttl,
    }
    try:
        updated_record = requests.put(
            f'{api_url}{domain_id}/records/{record_id}',
            headers=headers,
            json=data
        )
    except requests.exceptions.RequestException as e:
        return {'success': False, 'msg': f'Linode API error: {str(e)}'}

    return {'success': True, 'msg': updated_record.json()}
