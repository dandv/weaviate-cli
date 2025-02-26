import sys
import click
from weaviate_cli.managers.backup_manager import BackupManager
from weaviate_cli.utils import get_client_from_context
from weaviate_cli.managers.collection_manager import CollectionManager

# Restore Group
@click.group()
def restore() -> None:
    """Restore backups in Weaviate."""
    pass

@restore.command("backup")
@click.option(
    "--backend",
    default="s3",
    type=click.Choice(["s3", "gcs", "filesystem"]),
    help="The backend used for storing the backups (default: s3).",
)
@click.option(
    "--backup_id",
    default="test-backup",
    help="Identifier used for the backup (default: test-backup).",
)
@click.option(
    "--wait", is_flag=True, help="Wait for the backup to complete before returning."
)
@click.option(
    "--include",
    default=None,
    help="Collection to include in backup (default: None).",
)
@click.option(
    "--exclude",
    default=None,
    help="Collection to exclude in backup (default: None).",
)
@click.pass_context
def restore_backup_cli(ctx, backend, include, exclude, backup_id, wait):
    """Restore a backup in Weaviate."""

    try:
        client = get_client_from_context(ctx)
        backup_manager = BackupManager(client)
        backup_manager.restore_backup(
            backend=backend,
            backup_id=backup_id,
            include=include,
            exclude=exclude,
            wait=wait,
        )
    except Exception as e:
        print(f"Error: {e}")
        client.close()
        sys.exit(1)  # Return a non-zero exit code on failure

    client.close()