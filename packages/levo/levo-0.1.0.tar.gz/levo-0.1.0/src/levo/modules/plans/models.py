import pathlib

import attr


@attr.s(slots=True)
class Plan:
    name: str = attr.ib()
    catalog: pathlib.Path = attr.ib()

    def iter_suite(self):
        return (self.catalog / self.name).iterdir()
