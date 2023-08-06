"""DiffSync adapter for Nautobot."""
from diffsync import DiffSync  # pylint: disable=E0402
from pynautobot.core.query import RequestError
from nautobot_aristacv_importer.diffsync.nbutils import get_tags, get_tagged_devices  # pylint: disable=R0402
from nautobot_aristacv_importer.diffsync.models import UserTag  # pylint: disable=E0402


class Nautobot(DiffSync):
    """DiffSync adapter implementation for Nautobot user-defined tags."""

    tag = UserTag

    top_level = ["tag"]

    type = "Nautobot"

    def load(self):
        """Load device tag data from Nautobot and populate DiffSync models."""
        tags = get_tags()
        for cur_tag in tags:
            if ":" in cur_tag.name:
                label, value = cur_tag.name.split(":")
            else:
                label = cur_tag.name
                value = ""
            self.tag = UserTag(name=label, value=value)
            try:
                tagged_devices = get_tagged_devices(f"arista_{label}_{value}")
            except RequestError:
                # Tag does not have any assigned devices so continue through loop
                continue
            for dev in tagged_devices:
                self.tag.devices.append(dev.name)

            # Sort device list for diffsync
            self.tag.devices = sorted(self.tag.devices)
            self.add(self.tag)
