#!/usr/bin/env python

import argparse
import json
import logging
import os
import requests
import types
import urlparse

DEFAULT_CRT_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
DEFAULT_TOKEN_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/token'
DEFAULT_TEMPLATE_PATH = '/twemproxy.template'
DEFAULT_REDIS_PORT = 6379
DEFAULT_LABEL_SELECTOR = '{"name": "redis-node"}'

def create_config(args):
    pod_ips = all_pod_ips(args)
    if not pod_ips:
        return ''

    with open(DEFAULT_TEMPLATE_PATH, 'r') as template:
        config = template.read().rstrip() + '\n'
        config += server_config(pod_ips)
    return config

def server_config(pod_ips):
    servers = ''
    for ip in pod_ips:
        servers += '    - {}:{}:1\n'.format(ip, DEFAULT_REDIS_PORT)
    return servers

def all_pod_ips(args):
    all_pods = api_get_redis_pods(
        args.service_url,
        args.api_version,
        args.api_token_path,
        args.api_crt_path,
        args.label_selectors
    )
    if not all_pods or len(all_pods) == 0:
        return None

    ip_list = []
    for pod in all_pods:
        ip = get_nested(pod, 'status.podIP')
        if ip:
            ip_list.append(ip)

    return ip_list

def api_get_redis_pods(service_url, api_version, token_path, crt_path, label_selectors):
    pod_api_url = urlparse.urljoin(service_url + api_path(api_version), 'namespaces/default/pods')
    auth_header = api_authorization_header(token_path)
    label_selector = api_label_selector(label_selectors)
    pod_api_response = requests.get(pod_api_url, headers=auth_header, params=label_selector, verify=crt_path)
    api_json = pod_api_response.json()
    return api_json.get('items')

def api_label_selector(label_criteria):
    if not label_criteria or len(label_criteria) <= 0:
        return None

    criteria = []
    for label, value in label_criteria.iteritems():
        criteria.append('{}={}'.format(label, value))

    criteria_str = ','.join(criteria)
    return {
        'labelSelector': criteria_str
    }

def default_api_service_url():
    base_url = 'https://kubernetes:{}'.format(os.environ['KUBERNETES_PORT_443_TCP_PORT'])
    return base_url

def api_path(api_version):
    return '/api/{}/'.format(api_version)

def api_authorization_header(token_path):
    token = open(token_path).read()
    auth_value = 'Bearer {}'.format(token)
    return {
        'Authorization': auth_value
    }

def get_nested(source, dotted_property, default=None):
  pieces = dotted_property.split('.')
  while len(pieces):
    piece = pieces.pop(0)
    if isinstance(source, types.DictType):
      try:
        source = source[piece]
        continue
      except KeyError:
        pass
    elif isinstance(source, types.ListType):
      try:
        index = int(piece)
        source = source[index]
        continue
      except IndexError:
        pass
    return default
  return source

def main(args):
    print create_config(args)

def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service-url',
                        default=default_api_service_url(),
                        help='Kubernetes service to poll')
    parser.add_argument('--api-version',
                        default='v1',
                        help='Kubernetes API version')
    # Auto parses json into dictionary
    parser.add_argument('--label-selectors',
                        default=DEFAULT_LABEL_SELECTOR,
                        type=json.loads,
                        help='JSON label selectors to identify redis pods by')
    parser.add_argument('--config-template',
                        default=(os.environ.get('TEMPLATE') or DEFAULT_TEMPLATE_PATH),
                        help='Twemproxy config template')
    parser.add_argument('--redis-port',
                        default=DEFAULT_REDIS_PORT,
                        type=int,
                        help='Port of redis pods')
    parser.add_argument('--api-token-path',
                        default=DEFAULT_TOKEN_PATH,
                        help='Path to the Kubernetes API token')
    parser.add_argument('--api-crt-path',
                        default=DEFAULT_CRT_PATH,
                        help='Path to the Kubernetes API crt')
    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help='Display debug messages')
    args = parser.parse_args()
    if args.debug:
      logging.getLogger('root').setLevel(logging.DEBUG)

    return args


if __name__ == '__main__':
    main(process_args())
