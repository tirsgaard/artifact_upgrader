# Test with pytest
# Run with: pytest unit_tests.py
# Run with coverage: pytest --cov=unit_tests.py
import pytest
import numpy as np
from src.artifact_logic.artifact import Artifact

@pytest.fixture
def test_artifact():
    return Artifact("sands")

def test_no_duplicate_substats():
    # Check none of the substats are of the same type
    artifact_slots = ["sands", "goblet", "plume", "flower", "circlet"]
    for i in range(100):
        # Select random artifact slot
        slot = artifact_slots[np.random.randint(0, 5)]
        artifact = Artifact(slot)
        artifact.gen_artifact()
        substats = [substat.type for substat in artifact.substats]
        assert len(substats) == len(set(substats))

def test_no_substat_is_main_stat():
    # Check none of substats are of the same type as the main stat
    artifact_slots = ["sands", "goblet", "plume", "flower", "circlet"]
    for i in range(100):
        slot = artifact_slots[np.random.randint(0, 5)]
        artifact = Artifact(slot)
        artifact.gen_artifact()
        substats = [substat.type for substat in artifact.substats]
        assert artifact.main_stat.type not in substats

def test_substat_upgrade():
    # Check that substats are upgraded correctly
    artifact_slots = ["sands", "goblet", "plume", "flower", "circlet"]
    for i in range(100):
        slot = artifact_slots[np.random.randint(0, 5)]
        artifact = Artifact(slot)
        artifact.gen_artifact()
        # Check that all substats are at level 0
        for substat in artifact.substats:
            assert substat.upgrade_number == 0
        # Level artifact
        artifact.level_artifact(20)
        # Check that the number of times a substat has been upgraded sums to 4 or 5
        n_upgrades = sum([substat.upgrade_number for substat in artifact.substats])
        assert (n_upgrades == 4 or n_upgrades == 5)