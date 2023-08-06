import requests

from tew652brp.core.login import login
from tew652brp.core.utils import make_routes
from tew652brp.core.access.virtual import (
    set_virtual_server_info,
    get_servers_xml,
    xml_to_vserver_info_list,
    delete_virtual_server,
)


class Client:
    def __init__(self, base_url):
        self._base_url = base_url
        self._urls = make_routes(base_url)
        self._session = requests.Session()

    def login(self, username, password):
        return login(self._session, self._urls['login'], username, password)

    def get_virtual_server_list(self):
        xml = get_servers_xml(self._session, self._urls['get_set'], {
            'num_inst': '1',
            'oid_1': 'IGD_WANDevice_i_VirServRule_i_',
            'inst_1': '11000',
        })
        return xml_to_vserver_info_list(xml)

    def set_virtual_server_info(self, server_info):
        return set_virtual_server_info(self._session, self._urls['get_set'], server_info.to_dict())

    def delete_virtual_server(self, server_info):
        return delete_virtual_server(self._session, self._urls['get_set'], {
            'ccpSubEvent': 'CCP_SUB_VIRTUALSERVER',
            'nextPage': 'virtual_server.htm',
            'num_inst': '1',
            'oid_1': 'IGD_WANDevice_i_VirServRule_i_',
            'inst_1': server_info.instance,
        })
