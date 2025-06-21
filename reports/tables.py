import django_tables2 as tables
from utils.WebData import WebData
from django.utils.html import format_html

class MemberOfGroupTable(tables.Table):
    hostid = tables.Column(verbose_name="ID")
    name = tables.Column(verbose_name="Nombre")
    status = tables.Column(verbose_name="Estado")
    type = tables.Column(empty_values=(), verbose_name="Tipo")
    interface_ips = tables.Column(empty_values=(), verbose_name="Interfaces")

    def render_status(self, value):
        """Convert the status value to a human-readable format."""
        return "Activo" if value == "0" else "Inactivo"

    def render_interface_ips(self, record):
        """Render the IPs or DNS of the host's interfaces."""
        interfaces = record.get('interfaces', [])
        if not interfaces:
            return "-"
        # Mostrar IP o DNS de cada interfaz
        return ", ".join(
            iface.get('ip') or iface.get('dns') or "sin IP"
            for iface in interfaces
        )
    
    def render_type(self, record):
        """Render the type of the host based on its interfaces."""
        interfaces = record.get("interfaces", [])
        if not interfaces:
            return "-"
        return ", ".join(
            self.get_interface_type(iface['type']) for iface in interfaces
        )

    def get_interface_type(self, value):
        """Convert the interface type value to a human-readable format."""
        return "Agent" if value == "1" else "SNMP" if value == "2" else "IPMI" if value == "3" else "JMX"

    class Meta:
        sequence = ("name", "interface_ips", "type", "status")  # Sequence of columns to display
        empty_text = format_html(f'<p>{WebData.MSG_DATA}</p>')
        order_by = "name"
        exclude = ("hostid",)  # Exclude hostid from the table display
