from collections import Counter
from typing import Optional

from src.artifact_logic.artifact import Artifact
from src.artifact_logic.constants import stat_GO_to_GCSim


def prepare_artifacts(new_artifact: Optional[Artifact], equipped_artifacts: dict[str, Artifact]) -> Counter[str, float]:
    equipped_artifacts = equipped_artifacts.copy()
    if new_artifact is None:
        pass
    elif new_artifact.slot == "flower":
        equipped_artifacts["flower"] = new_artifact
    elif new_artifact.slot == "plume":
        equipped_artifacts["plume"] = new_artifact
    elif new_artifact.slot == "sands":
        equipped_artifacts["sands"] = new_artifact
    elif new_artifact.slot == "goblet":
        equipped_artifacts["goblet"] = new_artifact
    elif new_artifact.slot == "circlet":
        equipped_artifacts["circlet"] = new_artifact

    artifacts = list(Counter(equipped_artifact.get_full_stats()) for equipped_artifact in equipped_artifacts.values())
    artifacts = sum(artifacts, Counter())
    return artifacts

def convert_to_GCSim(artifacts: Counter[str, float]) -> str:
    """ Converts a Counter of artifacts to a GCSim string.

    :param artifacts: Counter of artifacts.
    :return: GCSim string.
    """

    output = ""
    for stat in artifacts:
        gc_stat = stat_GO_to_GCSim[stat]
        stat_value = artifacts[stat]
        stat_value = stat_value/100 if "%" or "er" in gc_stat else stat_value
        output += f"{gc_stat}={stat_value} "

    return output