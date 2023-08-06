import xml.etree.ElementTree as ET

_nodes = {
    'name': 'vsRule_VirtualServerName_',
    'internal_ip': 'vsRule_InternalIPAddr_',
    'enabled': 'vsRule_Enable_',
    'protocol': 'vsRule_Protocol_',
    'public_port': 'vsRule_PublicPort_',
    'private_port': 'vsRule_PrivatePort_',
}


class VServerInfo:
    __slots__ = ('instance', 'name', 'internal_ip', 'enabled', 'protocol', 'public_port', 'private_port')

    def __init__(self, instance, name, internal_ip, enabled, protocol, public_port, private_port):
        self.instance = instance
        self.name = name
        self.internal_ip = internal_ip
        self.enabled = enabled
        self.protocol = protocol
        self.public_port = public_port
        self.private_port = private_port

    def to_dict(self):
        nodes = {k: f'{_nodes[k]}{self.instance}' for k in _nodes.keys()}

        return {
            nodes['name']: self.name,
            nodes['internal_ip']: self.internal_ip,
            nodes['enabled']: self.enabled,
            nodes['protocol']: self.protocol,
            nodes['public_port']: self.public_port,
            nodes['private_port']: self.private_port,
        }


def _find_all_virtual_servers(xml):
    return ET.fromstring(xml).findall('IGD_WANDevice_i_VirServRule_i_')


def _extract(xml):
    info = {key: xml.find(node).text for key, node in zip(_nodes.keys(), _nodes.values())}
    info['instance'] = xml.get('inst').replace(",", ".")
    return VServerInfo(**info)


def ccp_act(act, **params):
    def _ccp_act(func):
        def wrapper(session, url, data):
            data['ccp_act'] = act
            for param in params:
                data[param] = params[param]
            return func(session, url, data)
        return wrapper
    return _ccp_act


def xml_to_vserver_info_list(xml):
    servers = _find_all_virtual_servers(xml)
    return [_extract(server) for server in servers]


@ccp_act(act='get')
def get_servers_xml(session, url, data):
    return session.post(url, data=data).text


@ccp_act(act='set')
def set_virtual_server_info(session, url, data):
    return session.post(url, data=data)


@ccp_act(act='del')
def delete_virtual_server(session, url, data):
    return session.post(url, data=data)
