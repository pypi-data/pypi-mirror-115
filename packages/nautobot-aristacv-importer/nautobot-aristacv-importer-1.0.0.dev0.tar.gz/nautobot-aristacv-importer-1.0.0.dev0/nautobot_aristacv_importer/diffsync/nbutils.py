"""Utility functions for Nautobot."""
from pynautobot import api


# pylint: disable=C0103,W0601
def connect_nb(nautobot_url, nautobot_token):
    """Connect to instance of Nautobot.

    Args:
        nautobot_url (str): Nautobot url.
        nautobot_token (str): Token used when connecting to Nautobot.
    """
    global _nautobot
    _nautobot = api(nautobot_url, nautobot_token)


def get_tags():
    """Get all tags from Nautobot."""
    return _nautobot.extras.tags.all()


def get_tagged_devices(tag_id):
    """Get devices containing a specific tag.

    Args:
        tag_id (str): Tag name.
    """
    return _nautobot.dcim.devices.filter(tag=tag_id)


def create_tag(name, slug):
    """Create new tag in Nautobot."""
    tag = _nautobot.extras.tags
    new_tag = tag.create(name=name, slug=slug)
    new_tag.save()


def get_devices():
    """Get list of devices from Nautobot."""
    return _nautobot.dcim.devices.all()


def get_device(name=None):
    """Get a specific device from Nautobot."""
    return _nautobot.dcim.devices.get(name=name)


def assign_tag(device, tag_slug):
    """Assign tag to device."""
    tag_object = _nautobot.extras.tags.get(slug=tag_slug)
    device.tags.append(tag_object)
    device.save()


def remove_tag(device, tag_slug):
    """Remove tag from device."""
    tag_object = _nautobot.extras.tags.get(slug=tag_slug)
    device.tags.remove(tag_object)
    device.save()
