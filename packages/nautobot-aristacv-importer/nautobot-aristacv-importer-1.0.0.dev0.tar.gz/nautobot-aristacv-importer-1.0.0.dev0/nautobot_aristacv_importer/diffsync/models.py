"""Diffsync models for Nautobot <-> CloudVision sync."""
from typing import List
from diffsync import DiffSyncModel
import nautobot_aristacv_importer.diffsync.nbutils as nbutils  # pylint: disable=R0402


class UserTag(DiffSyncModel):
    """Tag model."""

    _modelname = "tag"
    _identifiers = ("name", "value")
    _attributes = ("devices",)

    name: str
    value: str
    devices: List = list()

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create a tag in Nautobot."""
        tag_name = f"{ids['name']}:{ids['value']}"
        tag_slug = f"arista_{ids['name']}_{ids['value']}"
        nbutils.create_tag(tag_name, tag_slug)
        for device in attrs["devices"]:
            nb_device = nbutils.get_device(device)
            if nb_device:
                nbutils.assign_tag(nb_device, tag_slug)
        return super().create(ids=ids, diffsync=diffsync, attrs=attrs)

    def update(self, attrs):
        """Update user tag in Nautobot."""
        remove = set(self.devices) - set(attrs["devices"])
        add = set(attrs["devices"]) - set(self.devices)
        tag_slug = f"arista_{self.name}_{self.value}"
        for device in remove:
            nb_device = nbutils.get_device(device)
            if nb_device is not None:
                nbutils.remove_tag(nb_device, tag_slug)
        for device in add:
            nb_device = nbutils.get_device(device)
            if nb_device is not None:
                nbutils.assign_tag(nb_device, tag_slug)
        return super().update(attrs)

    def delete(self):
        """Delete user tag applied to devices in CloudVision."""
        print(
            "No deletion of tags take place in thie CLI tool. Please use the SSoT Arista Cloudvision Plugin to sync tags."
        )
        return self
