def furina_optim(artifact, equpied_artifacts):
    """ This function is a placefolder function, that takes an artifact as input, and outputs number to optimise out.
    This could for example be the damage of a specific skill """

    equpied_artifacts = equpied_artifacts.copy()
    base_EM = 0
    base_damage = 1 + 0.12
    base_attack = 1014
    base_flat_attack = 0
    base_attack_per = 1.0 + 0.331
    base_damage_increase = 1.0 + 0.209 + 0.28
    base_hp = 15307
    base_hp_per = 0.25
    base_crit_rate = 0.402
    base_crit_damage = 0.5
    art_hp_flat = 0

    if artifact is None:
        pass
    elif artifact.slot == "flower":
        equpied_artifacts["flower"] = artifact
    elif artifact.slot == "plume":
        equpied_artifacts["plume"] = artifact
    elif artifact.slot == "sands":
        equpied_artifacts["sands"] = artifact
    elif artifact.slot == "goblet":
        equpied_artifacts["goblet"] = artifact
    elif artifact.slot == "circlet":
        equpied_artifacts["circlet"] = artifact

    for art in equpied_artifacts.values():
        # Get values from artifact
        stat_dict = art.get_full_stats()
        # Add values to base values
        base_EM += stat_dict["em"]
        base_damage += stat_dict["electro_per"] / 100.
        base_flat_attack += stat_dict["att_flat"]
        base_attack_per += stat_dict["att_per"] / 100.
        base_crit_rate += stat_dict["crit_chance"] / 100.
        base_crit_damage += stat_dict["crit_damage"] / 100.
        art_hp_flat += stat_dict["hp_flat"]
        base_hp_per += stat_dict["hp_per"] / 100.

    # Add set damage
    base_damage_increase += 0.7

    # Calculate damage
    total_damage = base_damage_increase
    total_crit_rate = base_crit_rate
    total_crit_damage = base_crit_damage
    total_hp = base_hp * (1 + base_hp_per + 350 * 0.004) + art_hp_flat

    # Damage for ability
    total_hydro_res = 0.1 - 0.4
    enemy_def_multi = 0.5 * (1 - total_hydro_res / 2)
    damage = 0.149 * total_hp * 1.4 * (1 + total_damage) * (1.0 + total_crit_rate * total_crit_damage) * enemy_def_multi

    return damage
