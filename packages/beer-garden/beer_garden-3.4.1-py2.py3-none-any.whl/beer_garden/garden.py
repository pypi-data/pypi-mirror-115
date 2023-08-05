# -*- coding: utf-8 -*-
"""Garden Service

The garden service is responsible for:

* Generating local `Garden` record
* Getting `Garden` objects from the database
* Updating `Garden` objects in the database
* Responding to `Garden` sync requests and forwarding request to children
* Handling `Garden` events
"""
import logging
from datetime import datetime
from typing import List

from brewtils.errors import PluginError
from brewtils.models import Events, Garden, Operation, System, Event

import beer_garden.config as config
import beer_garden.db.api as db
from beer_garden.events import publish_event, publish
from beer_garden.namespace import get_namespaces
from beer_garden.systems import get_systems, remove_system

logger = logging.getLogger(__name__)


def get_garden(garden_name: str) -> Garden:
    """Retrieve an individual Garden

    Args:
        garden_name: The name of Garden

    Returns:
        The Garden

    """
    if garden_name == config.get("garden.name"):
        return local_garden()

    return db.query_unique(Garden, name=garden_name)


def get_gardens(include_local: bool = True) -> List[Garden]:
    """Retrieve list of all Gardens

    Args:
        include_local: Also include the local garden

    Returns:
        All known gardens

    """
    gardens = db.query(Garden)

    if include_local:
        gardens += [local_garden()]

    return gardens


def local_garden(all_systems: bool = False) -> Garden:
    """Get the local garden definition

    Args:
        all_systems: If False, only include "local" systems in the garden systems list

    Returns:
        The local Garden

    """
    filter_params = {}
    if not all_systems:
        filter_params["local"] = True

    return Garden(
        name=config.get("garden.name"),
        connection_type="LOCAL",
        status="RUNNING",
        systems=get_systems(filter_params=filter_params),
        namespaces=get_namespaces(),
    )


@publish_event(Events.GARDEN_SYNC)
def publish_garden(status: str = "RUNNING") -> Garden:
    """Get the local garden, publishing a GARDEN_SYNC event

    Args:
        status: The garden status

    Returns:
        The local garden, all systems
    """
    garden = local_garden(all_systems=True)
    garden.connection_type = None
    garden.status = status

    return garden


def update_garden_config(garden: Garden) -> Garden:
    """Update Garden configuration parameters

    Args:
        garden: The Garden to Update

    Returns:
        The Garden updated

    """
    db_garden = db.query_unique(Garden, id=garden.id)
    db_garden.connection_params = garden.connection_params
    db_garden.connection_type = garden.connection_type
    db_garden.status = "INITIALIZING"

    return update_garden(db_garden)


def update_garden_status(garden_name: str, new_status: str) -> Garden:
    """Update an Garden status.

    Will also update the status_info heartbeat.

    Args:
        garden_name: The Garden Name
        new_status: The new status

    Returns:
        The updated Garden
    """
    garden = db.query_unique(Garden, name=garden_name)
    garden.status = new_status
    garden.status_info["heartbeat"] = datetime.utcnow()

    return update_garden(garden)


@publish_event(Events.GARDEN_REMOVED)
def remove_garden(garden_name: str) -> None:
    """Remove a garden

    Args:
        garden_name: The Garden name

    Returns:
        None

    """
    garden = db.query_unique(Garden, name=garden_name)

    for system in garden.systems:
        remove_system(system.id)

    db.delete(garden)
    return garden


@publish_event(Events.GARDEN_CREATED)
def create_garden(garden: Garden) -> Garden:
    """Create a new Garden

    Args:
        garden: The Garden to create

    Returns:
        The created Garden

    """
    garden.status_info["heartbeat"] = datetime.utcnow()

    return db.create(garden)


def garden_add_system(system: System, garden_name: str) -> Garden:
    """Add a System to a Garden

    Args:
        system: The system to add
        garden_name: The Garden Name to add it to

    Returns:
        The updated Garden

    """
    garden = get_garden(garden_name)

    if garden is None:
        raise PluginError(
            f"Garden '{garden_name}' does not exist, unable to map '{str(system)}"
        )

    if system.namespace not in garden.namespaces:
        garden.namespaces.append(system.namespace)

    if str(system) not in garden.systems:
        garden.systems.append(str(system))

    return update_garden(garden)


@publish_event(Events.GARDEN_UPDATED)
def update_garden(garden: Garden) -> Garden:
    """Update a Garden

    Args:
        garden: The Garden to update

    Returns:
        The updated Garden
    """
    return db.update(garden)


def garden_sync(sync_target: str = None):
    """Do a garden sync

    If we're here it means the Operation.target_garden_name was *this* garden. So the
    sync_target is either *this garden* or None.

    If the former then call the method to publish the current garden.

    If the latter then we need to send sync operations to *all* known downstream
    gardens.

    Args:
        sync_target:

    Returns:

    """
    # If a Garden Name is provided, determine where to route the request
    if sync_target:
        logger.debug("Processing garden sync, about to publish")

        publish_garden()

    else:
        from beer_garden.router import route

        # Iterate over all gardens and forward the sync requests
        for garden in get_gardens(include_local=False):
            logger.debug(f"About to create sync operation for garden {garden.name}")

            route(
                Operation(
                    operation_type="GARDEN_SYNC",
                    target_garden_name=garden.name,
                    kwargs={"sync_target": garden.name},
                )
            )


def handle_event(event):
    """Handle garden-related events

    For GARDEN events we only care about events originating from downstream. We also
    only care about immediate children, not grandchildren.

    Whenever a garden event is detected we should update that garden's database
    representation.

    This method should NOT update the routing module. Let its handler worry about that!
    """
    if event.garden != config.get("garden.name"):

        if event.name in (
            Events.GARDEN_STARTED.name,
            Events.GARDEN_UPDATED.name,
            Events.GARDEN_STOPPED.name,
            Events.GARDEN_SYNC.name,
        ):
            # Only do stuff for direct children
            if event.payload.name == event.garden:
                existing_garden = get_garden(event.payload.name)

                for system in event.payload.systems:
                    system.local = False

                if existing_garden is None:
                    event.payload.connection_type = None
                    event.payload.connection_params = {}

                    garden = create_garden(event.payload)
                else:
                    for attr in ("status", "status_info", "namespaces", "systems"):
                        setattr(existing_garden, attr, getattr(event.payload, attr))

                    garden = update_garden(existing_garden)

                # Publish update events for UI to dynamically load changes for Systems
                for system in garden.systems:
                    publish(
                        Event(
                            name=Events.SYSTEM_UPDATED.name,
                            payload_type="System",
                            payload=system,
                        )
                    )

    elif event.name == Events.GARDEN_UNREACHABLE.name:
        target_garden = get_garden(event.payload.target_garden_name)

        if target_garden.status not in [
            "UNREACHABLE",
            "STOPPED",
            "BLOCKED",
            "ERROR",
        ]:
            update_garden_status(event.payload.target_garden_name, "UNREACHABLE")
    elif event.name == Events.GARDEN_ERROR.name:
        target_garden = get_garden(event.payload.target_garden_name)

        if target_garden.status not in [
            "UNREACHABLE",
            "STOPPED",
            "BLOCKED",
            "ERROR",
        ]:
            update_garden_status(event.payload.target_garden_name, "ERROR")
    elif event.name == Events.GARDEN_NOT_CONFIGURED.name:
        target_garden = get_garden(event.payload.target_garden_name)

        if target_garden.status == "NOT_CONFIGURED":
            update_garden_status(event.payload.target_garden_name, "NOT_CONFIGURED")
