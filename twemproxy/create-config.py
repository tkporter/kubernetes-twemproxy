#!/usr/bin/env python

import argparse
import os
import requests
import types
import urlparse

DEFAULT_CRT_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
DEFAULT_TOKEN_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/token'
DEFAULT_TEMPLATE_PATH = '/twemproxy.template'
DEFAULT_REDIS_PORT = 6379
DEFAULT_LABEL_SELECTOR = {
    'name': 'redis-node'
}

def create_config(args):
    pod_ips = all_pod_ips()
    with open(DEFAULT_TEMPLATE_PATH, 'r') as template:
        config = template.read().rstrip() + '\n'
        config += server_config(pod_ips)
    return config

def server_config(pod_ips):
    servers = ''
    for ip in pod_ips:
        servers += '    - {}:{}:1\n'.format(ip, DEFAULT_REDIS_PORT)
    return servers

def all_pod_ips():
    all_pods = all_kubernetes_pods()
    ip_list = []
    for pod in all_pods:
        ip = get_nested(pod, 'status.podIP')
        if ip:
            ip_list.append(ip)

    return ip_list

def all_kubernetes_pods():
    all_pods = api_get_redis_pods()
    return all_pods.get('items')

def api_get_redis_pods():
    api_base_url = api_service_url()
    pod_api_url = urlparse.urljoin(api_base_url, 'namespaces/default/pods')
    api_auth_header = api_authorization_header()
    label_selector = api_label_selector(DEFAULT_LABEL_SELECTOR)
    pod_api_response = requests.get(pod_api_url, headers=api_auth_header, params=label_selector, verify=DEFAULT_CRT_PATH)
    return pod_api_response.json()

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

def api_service_url():
    base_url = 'https://kubernetes:{}/api/v1/'.format(os.environ['KUBERNETES_PORT_443_TCP_PORT'])
    return base_url

def api_authorization_header():
    token = open(DEFAULT_TOKEN_PATH).read()
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
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--kubernetes-service',
    #                     default=_default_kubernetes_service_url(),
    #                     help='Kubernetes service to poll')
    # parser.add_argument('--api-version',
    #                     default='v1beta3',
    #                     help='Kubernetes API version')
    # parser.add_argument('--name-label',
    #                     default='redis-node',
    #                     help='Service name label to poll for')
    # parser.add_argument('--config-template',
    #                     default=(os.environ.get('TEMPLATE') or
    #                              '/twemproxy.template'),
    #                     help='twemproxy config template')
    # parser.add_argument('--debug',
    #                     action='store_true',
    #                     default=False,
    #                     help='Display debug messages')
    # args = parser.parse_args()
    # if args.debug:
    #   logging.getLogger('root').setLevel(logging.DEBUG)
    return None
    # return args


if __name__ == '__main__':
    main(process_args())
