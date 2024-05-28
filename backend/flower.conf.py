import os

enable_utc = False
natural_time = False
port = 5555
username = os.environ.get('FLOWER_USERNAME', 'admin')
password = os.environ.get('FLOWER_PASSWORD', 'admin')
basic_auth = [f'{username}:{password}']
url_prefix = 'flower'
