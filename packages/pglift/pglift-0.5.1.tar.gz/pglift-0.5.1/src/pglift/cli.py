import json
import logging
from typing import IO, Any, Optional, Union

import click
import pydantic.json
from pydantic.utils import deep_update
from tabulate import tabulate
from typing_extensions import Literal

from . import _install, databases, exceptions
from . import instance as instance_mod
from . import pgbackrest, pm, roles
from .ctx import Context
from .models import helpers, interface
from .models.system import Instance
from .settings import SETTINGS
from .task import runner


def get_instance(ctx: Context, name: str, version: Optional[str]) -> Instance:
    try:
        return Instance.system_lookup(ctx, (name, version))
    except exceptions.InstanceNotFound as e:
        raise click.ClickException(e.show())
    except Exception as e:
        raise click.ClickException(str(e))


def instance_lookup(ctx: Context, instance_id: str) -> Instance:
    version = None
    try:
        version, name = instance_id.split("/", 1)
    except ValueError:
        name = instance_id
    return get_instance(ctx, name, version)


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
)
@click.pass_context
def cli(ctx: click.core.Context, log_level: Optional[str]) -> None:
    """Deploy production-ready instances of PostgreSQL"""
    if log_level is not None:
        logging.basicConfig(level=log_level)

    if not ctx.obj:
        ctx.obj = Context(plugin_manager=pm.PluginManager.get(), settings=SETTINGS)


@cli.command(
    "site-configure",
    hidden=True,
    help="Manage installation of extra data files for pglift.\n\nThis is an INTERNAL command.",
)
@click.argument(
    "action", type=click.Choice(["install", "uninstall"]), default="install"
)
@click.option("--settings", type=click.Path(exists=True), help="custom settings file")
@click.pass_obj
def site_configure(
    ctx: Context,
    action: Union[Literal["install"], Literal["uninstall"]],
    settings: Optional[str],
) -> None:
    if action == "install":
        env = f"SETTINGS=@{settings}" if settings else None
        _install.do(ctx, env=env)
    elif action == "uninstall":
        _install.undo(ctx)


@cli.group("instance")
def instance() -> None:
    """Manipulate instances"""


@instance.command("init")
@helpers.parameters_from_model(interface.Instance)
@click.pass_obj
def instance_init(ctx: Context, instance: interface.Instance) -> None:
    """Initialize a PostgreSQL instance"""
    if instance.spec(ctx).exists():
        raise click.ClickException("instance already exists")
    with runner(ctx):
        instance_mod.apply(ctx, instance)


@instance.command("apply")
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@click.pass_obj
def instance_apply(ctx: Context, file: IO[str]) -> None:
    """Apply manifest as a PostgreSQL instance"""
    with runner(ctx):
        instance_mod.apply(ctx, interface.Instance.parse_yaml(file))


@instance.command("alter")
@helpers.parameters_from_model(interface.Instance, False)
@click.pass_obj
def instance_alter(
    ctx: Context, name: str, version: Optional[str] = None, **changes: Any
) -> None:
    """Alter a PostgreSQL instance"""
    changes = helpers.unnest(interface.Instance, changes)
    try:
        values = instance_mod.describe(ctx, name, version).dict()
    except exceptions.InstanceNotFound as e:
        raise click.ClickException(e.show())
    values = deep_update(values, changes)
    altered = interface.Instance.parse_obj(values)
    with runner(ctx):
        instance_mod.apply(ctx, altered)


@instance.command("schema")
def instance_schema() -> None:
    """Print the JSON schema of PostgreSQL instance model"""
    print(interface.Instance.schema_json(indent=2))


name_argument = click.argument("name", type=click.STRING)
version_argument = click.argument("version", required=False, type=click.STRING)


@instance.command("describe")
@name_argument
@version_argument
@click.pass_obj
def instance_describe(ctx: Context, name: str, version: Optional[str]) -> None:
    """Describe a PostgreSQL instance"""
    try:
        described = instance_mod.describe(ctx, name, version)
    except exceptions.InstanceNotFound as e:
        raise click.ClickException(e.show())
    print(described.yaml(), end="")


@instance.command("list")
@click.option(
    "--version",
    type=click.Choice(list(SETTINGS.postgresql.versions)),
    help="Only list instances of specified version.",
)
@click.option("--json", "as_json", is_flag=True, help="Print as JSON")
@click.pass_obj
def instance_list(ctx: Context, version: Optional[str], as_json: bool) -> None:
    """List the available instances"""

    instances = instance_mod.list(ctx, version=version)
    if as_json:
        print(json.dumps(list(instances), default=pydantic.json.pydantic_encoder))
        return

    props = interface.InstanceListItem.__fields__
    content = [[getattr(item, p) for p in props] for item in instances]
    if content:
        headers = [p.capitalize() for p in props]
        print(tabulate(content, headers))


@instance.command("drop")
@name_argument
@version_argument
@click.pass_obj
def instance_drop(ctx: Context, name: str, version: Optional[str]) -> None:
    """Drop a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    with runner(ctx):
        instance_mod.drop(ctx, instance)


@instance.command("status")
@name_argument
@version_argument
@click.pass_context
def instance_status(ctx: click.core.Context, name: str, version: Optional[str]) -> None:
    """Check the status of a PostgreSQL instance.

    Output the status string value ('running', 'not running', 'unspecified
    datadir') and exit with respective status code (0, 3, 4).
    """
    instance = get_instance(ctx.obj, name, version)
    with runner(ctx.obj):
        status = instance_mod.status(ctx.obj, instance)
    click.echo(status.name.replace("_", " "))
    ctx.exit(status.value)


@instance.command("start")
@name_argument
@version_argument
@click.pass_obj
def instance_start(ctx: Context, name: str, version: Optional[str]) -> None:
    """Start a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    with runner(ctx):
        instance_mod.start(ctx, instance)


@instance.command("stop")
@name_argument
@version_argument
@click.pass_obj
def instance_stop(ctx: Context, name: str, version: Optional[str]) -> None:
    """Stop a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    with runner(ctx):
        instance_mod.stop(ctx, instance)


@instance.command("reload")
@name_argument
@version_argument
@click.pass_obj
def instance_reload(ctx: Context, name: str, version: Optional[str]) -> None:
    """Reload a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    with runner(ctx):
        instance_mod.reload(ctx, instance)


@instance.command("restart")
@name_argument
@version_argument
@click.pass_obj
def instance_restart(ctx: Context, name: str, version: Optional[str]) -> None:
    """Restart a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    with runner(ctx):
        instance_mod.restart(ctx, instance)


@instance.command("backup")
@name_argument
@version_argument
@click.option(
    "--type",
    type=click.Choice([t.name for t in pgbackrest.BackupType]),
    default=pgbackrest.BackupType.default().name,
    help="Backup type",
)
@click.option("--purge", is_flag=True, default=False, help="Purge old backups")
@click.pass_obj
def instance_backup(
    ctx: Context, name: str, version: Optional[str], type: str, purge: bool
) -> None:
    """Back up a PostgreSQL instance"""
    instance = get_instance(ctx, name, version)
    pgbackrest.backup(ctx, instance, type=pgbackrest.BackupType(type))
    if purge:
        pgbackrest.expire(ctx, instance)


instance_identifier = click.argument("instance", metavar="<version>/<instance>")


@cli.group("role")
def role() -> None:
    """Manipulate roles"""


@role.command("create")
@instance_identifier
@helpers.parameters_from_model(interface.Role)
@click.pass_obj
def role_create(ctx: Context, instance: str, role: interface.Role) -> None:
    """Create a role in a PostgreSQL instance"""
    i = instance_lookup(ctx, instance)
    with instance_mod.running(ctx, i):
        if roles.exists(ctx, i, role.name):
            raise click.ClickException("role already exists")
        with runner(ctx):
            roles.apply(ctx, i, role)


@role.command("alter")
@instance_identifier
@helpers.parameters_from_model(interface.Role, False)
@click.pass_obj
def role_alter(ctx: Context, instance: str, name: str, **changes: Any) -> None:
    """Alter a role in a PostgreSQL instance"""
    i = instance_lookup(ctx, instance)
    changes = helpers.unnest(interface.Role, changes)
    with instance_mod.running(ctx, i):
        try:
            values = roles.describe(ctx, i, name).dict()
        except exceptions.RoleNotFound as e:
            raise click.ClickException(e.show())
        values = deep_update(values, changes)
        altered = interface.Role.parse_obj(values)
        with runner(ctx):
            roles.apply(ctx, i, altered)


@role.command("schema")
def role_schema() -> None:
    """Print the JSON schema of role model"""
    print(interface.Role.schema_json(indent=2))


@role.command("apply")
@instance_identifier
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@click.pass_obj
def role_apply(ctx: Context, instance: str, file: IO[str]) -> None:
    """Apply manifest as a role"""
    i = instance_lookup(ctx, instance)
    with runner(ctx), instance_mod.running(ctx, i):
        roles.apply(ctx, i, interface.Role.parse_yaml(file))


@role.command("describe")
@instance_identifier
@click.argument("name")
@click.pass_obj
def role_describe(ctx: Context, instance: str, name: str) -> None:
    """Describe a role"""
    i = instance_lookup(ctx, instance)
    try:
        with instance_mod.running(ctx, i):
            described = roles.describe(ctx, i, name)
    except exceptions.RoleNotFound as e:
        raise click.ClickException(e.show())
    print(described.yaml(exclude={"state"}), end="")


@role.command("drop")
@instance_identifier
@click.argument("name")
@click.pass_obj
def role_drop(ctx: Context, instance: str, name: str) -> None:
    """Drop a role"""
    i = instance_lookup(ctx, instance)
    try:
        with instance_mod.running(ctx, i):
            roles.drop(ctx, i, name)
    except exceptions.RoleNotFound as e:
        raise click.ClickException(e.show())


@cli.group("database")
def database() -> None:
    """Manipulate databases"""


@database.command("create")
@instance_identifier
@helpers.parameters_from_model(interface.Database)
@click.pass_obj
def database_create(ctx: Context, instance: str, database: interface.Database) -> None:
    """Create a database in a PostgreSQL instance"""
    i = instance_lookup(ctx, instance)
    with instance_mod.running(ctx, i):
        if databases.exists(ctx, i, database.name):
            raise click.ClickException("database already exists")
        with runner(ctx):
            databases.apply(ctx, i, database)


@database.command("alter")
@instance_identifier
@helpers.parameters_from_model(interface.Database, False)
@click.pass_obj
def database_alter(ctx: Context, instance: str, name: str, **changes: Any) -> None:
    """Alter a database in a PostgreSQL instance"""
    i = instance_lookup(ctx, instance)
    changes = helpers.unnest(interface.Database, changes)
    with instance_mod.running(ctx, i):
        try:
            values = databases.describe(ctx, i, name).dict()
        except exceptions.DatabaseNotFound as e:
            raise click.ClickException(e.show())
        values = deep_update(values, changes)
        altered = interface.Database.parse_obj(values)
        with runner(ctx):
            databases.apply(ctx, i, altered)


@database.command("schema")
def database_schema() -> None:
    """Print the JSON schema of database model"""
    print(interface.Database.schema_json(indent=2))


@database.command("apply")
@instance_identifier
@click.option("-f", "--file", type=click.File("r"), metavar="MANIFEST", required=True)
@click.pass_obj
def database_apply(ctx: Context, instance: str, file: IO[str]) -> None:
    """Apply manifest as a database"""
    i = instance_lookup(ctx, instance)
    with runner(ctx), instance_mod.running(ctx, i):
        databases.apply(ctx, i, interface.Database.parse_yaml(file))


@database.command("describe")
@instance_identifier
@click.argument("name")
@click.pass_obj
def database_describe(ctx: Context, instance: str, name: str) -> None:
    """Describe a database"""
    i = instance_lookup(ctx, instance)
    try:
        with instance_mod.running(ctx, i):
            described = databases.describe(ctx, i, name)
    except exceptions.DatabaseNotFound as e:
        raise click.ClickException(e.show())
    print(described.yaml(exclude={"state"}), end="")


@database.command("drop")
@instance_identifier
@click.argument("name")
@click.pass_obj
def database_drop(ctx: Context, instance: str, name: str) -> None:
    """Drop a database"""
    i = instance_lookup(ctx, instance)
    try:
        with instance_mod.running(ctx, i):
            databases.drop(ctx, i, name)
    except exceptions.DatabaseNotFound as e:
        raise click.ClickException(e.show())
