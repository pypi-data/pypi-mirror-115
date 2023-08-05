import click
from .imessage.workflow_elt.oob_staged_tables.contact_names import refresh_contact_names
from .imessage.workflow_elt.workflow_elt import workflow_elt


@click.group(name='imessage')
def cli_imessage():
    """Doni iMessage-based CLI tools."""
    pass


cli_imessage.add_command(refresh_contact_names)
cli_imessage.add_command(workflow_elt)
