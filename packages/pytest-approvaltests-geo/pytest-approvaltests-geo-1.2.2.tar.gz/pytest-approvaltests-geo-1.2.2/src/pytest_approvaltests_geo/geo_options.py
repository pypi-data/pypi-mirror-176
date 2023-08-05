from typing import Dict, Tuple, Callable, Optional

from approvaltests import Options, ScenarioNamer, Namer
from approvaltests.namer import NamerBase

from pytest_approvaltests_geo.float_utils import Tolerance
from pytest_approvaltests_geo.scrubbers import RecursiveScrubber


class GeoOptions(Options):
    _TAGS_SCRUBBER_FUNC = "tags_scrubber_func"
    _NAMER_WRAPPER_SCENARIO_BY_TAGS = "NamerWrapperScenarioByTags"
    _TOLERANCE = "tolerance"

    @classmethod
    def from_options(cls, options: Options) -> "GeoOptions":
        return GeoOptions(options.fields)

    def scrub_tags(self, data: Dict):
        if self.has_tags_scrubber():
            return self.fields[GeoOptions._TAGS_SCRUBBER_FUNC](data)
        return data

    def with_tags_scrubber(self, scrubber_func: RecursiveScrubber) -> "GeoOptions":
        return GeoOptions({**self.fields, **{GeoOptions._TAGS_SCRUBBER_FUNC: scrubber_func}})

    def has_tags_scrubber(self):
        return GeoOptions._TAGS_SCRUBBER_FUNC in self.fields

    def with_scenario_by_tags(self, tags_to_names: Callable[[Dict], Tuple[str, ...]]):
        return GeoOptions({**self.fields, **{GeoOptions._NAMER_WRAPPER_SCENARIO_BY_TAGS: tags_to_names}})

    def has_scenario_by_tags(self):
        return GeoOptions._NAMER_WRAPPER_SCENARIO_BY_TAGS in self.fields

    def wrap_namer_in_tags_scenario(self, namer: NamerBase, tags: Dict):
        if self.has_scenario_by_tags():
            return ScenarioNamer(namer, *self.fields[GeoOptions._NAMER_WRAPPER_SCENARIO_BY_TAGS](tags))

    @property
    def namer(self) -> Namer:
        return self.fields.get("namer")

    def with_tolerance(self, rel_tol: float = 1e-9, abs_tol: float = 0):
        return GeoOptions({**self.fields, **{GeoOptions._TOLERANCE: Tolerance(rel_tol, abs_tol)}})

    @property
    def tolerance(self) -> Optional[Tolerance]:
        return self.fields.get(GeoOptions._TOLERANCE)
