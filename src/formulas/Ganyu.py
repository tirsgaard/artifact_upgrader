def calculate_total_damage(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_atk_bonus = artifact_bonuses["att_per"] / 100
    art_atk_flat = artifact_bonuses["att_flat"]
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_cryo_dmg_bonus = artifact_bonuses["cryo_per"] / 100

    # Constants given in the formula
    char_atk = 334.85
    weapon_atk = 608.07
    rosaria_atk_bonus = 20 / 100
    the_first_great_magic_bonus = 32 / 100
    default_crit_rate = 5 / 100
    default_crit_dmg = 50 / 100
    char_crit_dmg = 38.4 / 100
    weapon_crit_dmg = 66.2 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_cryo_dmg_res = 10 / 100

    # Derived calculations for Total ATK and Total DMG Bonus
    base_atk = char_atk + weapon_atk
    total_atk_1 = base_atk * (1 + the_first_great_magic_bonus + art_atk_bonus + rosaria_atk_bonus) + art_atk_flat
    total_atk_2 = base_atk * (1 + 0.88 + the_first_great_magic_bonus + art_atk_bonus + rosaria_atk_bonus) + art_atk_flat
    total_cryo_dmg_bonus = art_cryo_dmg_bonus + 0.15 + 0.52
    total_charged_att_dmg_bonus = 0.16
    total_dmg_bonus_1 = total_charged_att_dmg_bonus + total_cryo_dmg_bonus
    total_dmg_bonus_2 = total_cryo_dmg_bonus
    total_crit_dmg = default_crit_dmg + char_crit_dmg + weapon_crit_dmg + art_crit_dmg

    # Enemy DEF Multiplier
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)

    # Damage calculations for each component
    frostflake_arrow_dmg = 2.304 * total_atk_1 * (1 + total_dmg_bonus_1) * \
                           (1 + default_crit_rate * total_crit_dmg) * \
                           enemy_def_multiplier * (1 - base_enemy_cryo_dmg_res)

    frostflake_arrow_bloom_dmg = 3.917 * total_atk_1 * (1 + total_dmg_bonus_1) * \
                                 (1 + (default_crit_rate + 0.15) * total_crit_dmg) * \
                                 enemy_def_multiplier * (1 - base_enemy_cryo_dmg_res)

    skill_dmg = 2.112 * total_atk_2 * (1 + total_dmg_bonus_2) * \
                (1 + total_crit_dmg) * enemy_def_multiplier * (1 - base_enemy_cryo_dmg_res / 2)

    ice_shard_dmg = 1.265 * total_atk_2 * (1 + total_dmg_bonus_2) * \
                    (1 + total_crit_dmg) * enemy_def_multiplier * (1 - base_enemy_cryo_dmg_res / 2)

    # Total damage
    total_damage = frostflake_arrow_dmg + 3 * frostflake_arrow_bloom_dmg + skill_dmg + ice_shard_dmg

    return total_damage
