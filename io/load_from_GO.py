import json
from artifact_logic.artifact import Artifact, SubStat
from artifact_logic.constants import GO_conversion_dict

def convert_stats(stat):
    """ This function converts a stat from Genshin Optimizer to this projects format"""
    return GO_conversion_dict[stat]

def GO_to_artifact(artifact):
    """ This function converts an artifact from Genshin Optimizer to this projects format"""
    if artifact["rarity"] < 5:
        # We only want 5 star artifacts
        return None

    # Get artifact slot
    slot = artifact["slotKey"]
    # Get artifact level
    level = artifact["level"]
    # Get artifact main stat
    main_stat = convert_stats(artifact["mainStatKey"])
    # Get artifact substats
    substats = []
    un_converted_substats = artifact["substats"]
    for substat in un_converted_substats:
        type = convert_stats(substat["key"])
        value = substat["value"]
        substats.append(SubStat(type, slot, value=value))
    for i in range(4 - len(substats)):
        # Add empty substats
        substats.append(SubStat(None, slot, value=0))

    # Get artifact set
    set = artifact["setKey"]

    # Create artifact
    artifact = Artifact(slot, main_stat=main_stat, level=level, substats=substats, set=set)

    return artifact

def get_art_from_JSON(path, location=None):
    """ This function loads a JSON file containing artifact data from Genshin Optimizer,
    and returns a list of artifacts in this projects format"""
    # Load JSON file
    with open(path) as f:
        data = json.load(f)

    # The artifacts are loaded under the key "artifacts"
    artifacts = []
    for artifact in data["artifacts"]:
        if location is None:
            artifacts.append(GO_to_artifact(artifact))
        else:
            if artifact["location"] == location:
                # Only add artifacts equipped
                artifacts.append(GO_to_artifact(artifact))
    return artifacts

if __name__ == "__main__":
    path = r"C:\Users\rasmu\Downloads\Inventory_KameraV1.3.9\GenshinData\genshinData_GOOD_2023_07_28_01_55.json"
    artifacts = get_art_from_JSON(path, location="YaeMiko")
    for artifact in artifacts:
        print(artifact)