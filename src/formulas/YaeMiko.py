from collections import Counter


def yae_miko_optim(new_artifact, equipped_artifacts):
    """ This function is a placefolder function, that takes an artifact as input, and outputs number to optimise out.
    This could for example be the damage of a specific skill """

    equipped_artifacts = equipped_artifacts.copy()
    base_EM = 0
    base_damage = 1 + 0.12
    base_attack = 1014
    base_flat_attack = 0
    base_attack_per = 1.0 + 0.331
    base_damage_increase = 0.0 + 0.48 + 0.317
    base_crit_rate = 0.242
    base_crit_damage = 0.5

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

    for art in equipped_artifacts.values():
        # Get values from artifact
        stat_dict = art.get_full_stats()
        # Add values to base values
        base_EM += stat_dict["em"]
        base_damage += stat_dict["electro_per"] / 100.
        base_flat_attack += stat_dict["att_flat"]
        base_attack_per += stat_dict["att_per"] / 100.
        base_crit_rate += stat_dict["crit_chance"] / 100.
        base_crit_damage += stat_dict["crit_damage"] / 100.

    # Add set damage
    base_attack_per += 0.18
    base_damage += 0.15

    # Calculate damage
    total_attack = base_attack * base_attack_per + base_flat_attack
    total_damage = base_damage
    total_crit_rate = base_crit_rate
    total_crit_damage = base_crit_damage

    # Damage for ability
    enemy_def_multi = 0.5 * (1 - 0.1)
    damage = 1.706 * total_attack * (total_damage + (base_EM * 0.0015)) * (
                1 + total_crit_rate * total_crit_damage) * enemy_def_multi

    return damage
