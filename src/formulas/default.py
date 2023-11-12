from collections import Counter


def prepare_artifacts(new_artifact, equipped_artifacts):

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