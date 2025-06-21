from django.conf import settings
from zabbix_utils import ZabbixAPI

class ApiZabbix:
    """
    Class to interact with the Zabbix API.
    """
    def __init__(self):
        """
        Initialize the Zabbix API client with the configured URL and token.
        """
        self.zabbix = ZabbixAPI(
            url=settings.ZABBIX_URL,
            token=settings.ZABBIX_TOKEN
        )

    def get_connection(self):
        """
        Get the Zabbix API client instance.
        
        Returns:
            ZabbixAPI: The Zabbix API client instance.
        """
        return self.zabbix
    
    def get_host_groups(self):
        """
        Fetch all host groups from Zabbix.
        Returns:
            list: A list of host groups.
        """
        host_groups = self.zabbix.hostgroup.get({
            'output': ['groupid', 'name'],
            'sortfield': 'name',
            'sortorder': 'ASC'
        })
        return host_groups
    
    def get_host_group(self, groupid):
        """
        Fetch a specific host group by its ID from Zabbix.
        
        Args:
            groupid (str): The ID of the host group to fetch.
        
        Returns:
            dict: The host group details.
        """
        host_group = self.zabbix.hostgroup.get({
            'output': ['groupid', 'name'],
            'groupids': groupid
        })
        return host_group[0] if host_group else None

    def get_hosts(self, groupid):
        """
        Fetch all hosts in a specific host group from Zabbix.
        """
        hosts = self.zabbix.host.get({
            'output': ['hostid', 'name'],
            'groupids': groupid,
            'sortfield': 'name',
            'sortorder': 'ASC'
        })
        return hosts
    
    def get_info_hosts(self, groupid):
        """
        Fetch detailed information about specific hosts by their IDs from Zabbix.
        
        Args:
            groupid (str): The ID of the host group to fetch information for.

        Returns:
            list: A list of host details.
        """
        hosts = self.zabbix.host.get({
            'output': ['hostid', 'name', 'status'],
            'groupids': groupid,
            'selectInterfaces': ['ip', 'dns', 'type'],
            'sortfield': 'name',
            'sortorder': 'ASC'
        })
        return hosts