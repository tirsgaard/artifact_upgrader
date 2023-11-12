def calculate_ganyu_damage(artifact_bonuses: dict[str, float]) -> float:
    # Extract artifact bonuses
    art_atk_bonus = artifact_bonuses["att_per"] / 100
    art_atk_flat = artifact_bonuses["att_flat"]
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_cryo_dmg_bonus = artifact_bonuses["cryo_per"] / 100

    # Constants given in the formula
    char_atk = 334.85
    weapon_atk = 608.07
    default_crit_rate = 5 / 100
    default_crit_dmg = 50 / 100
    char_crit_dmg = 38.4 / 100
    weapon_crit_dmg = 66.2 / 100
    the_first_great_magic_atk_bonus = 32 / 100
    the_first_great_magic_charged_att_dmg_bonus = 16 / 100
    blizzard_strayer_cryo_dmg_bonus = 15 / 100
    rosaria_atk_bonus = 20 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_cryo_dmg_res = 10 / 100

    # Derived calculations
    base_atk = char_atk + weapon_atk
    total_atk = base_atk * (1 + the_first_great_magic_atk_bonus + art_atk_bonus + rosaria_atk_bonus) + art_atk_flat
    total_cryo_dmg_bonus = blizzard_strayer_cryo_dmg_bonus + art_cryo_dmg_bonus

    # Frostflake Arrow DMG
    frostflake_arrow_dmg_bonus = the_first_great_magic_charged_att_dmg_bonus
    frostflake_crit_rate = art_crit_rate
    frostflake_crit_dmg = char_crit_dmg + weapon_crit_dmg + default_crit_dmg + art_crit_dmg
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_enemy_cryo_dmg_res = base_enemy_cryo_dmg_res
    frostflake_arrow_dmg = 2.304 * total_atk * (1 + frostflake_arrow_dmg_bonus + total_cryo_dmg_bonus) * \
                           (1 + frostflake_crit_rate * frostflake_crit_dmg) * \
                           enemy_def_multiplier * (1 - total_enemy_cryo_dmg_res)

    # Frostflake Arrow Bloom DMG
    frostflake_bloom_crit_rate = max(min(15 / 100 + default_crit_rate + art_crit_rate, 1), 0)
    frostflake_bloom_dmg = 3.917 * total_atk * (1 + frostflake_arrow_dmg_bonus + total_cryo_dmg_bonus) * \
                           (1 + frostflake_bloom_crit_rate * frostflake_crit_dmg) * \
                           enemy_def_multiplier * (1 - total_enemy_cryo_dmg_res)

    # Skill DMG
    skill_dmg_bonus = total_cryo_dmg_bonus
    total_enemy_cryo_dmg_res_skill = -45 / 100 + base_enemy_cryo_dmg_res
    skill_dmg = 2.112 * total_atk * (1 + skill_dmg_bonus) * (1 + frostflake_crit_dmg) * \
                enemy_def_multiplier * (1 - total_enemy_cryo_dmg_res_skill / 2)

    # Ice Shard DMG
    ice_shard_dmg = 1.265 * total_atk * (1 + skill_dmg_bonus) * (1 + frostflake_crit_dmg) * \
                    enemy_def_multiplier * (1 - total_enemy_cryo_dmg_res_skill / 2)

    # Total Damage Calculation
    total_damage = frostflake_arrow_dmg + frostflake_bloom_dmg + skill_dmg + 10 * ice_shard_dmg + \
                   3 * frostflake_arrow_dmg + 3 * frostflake_bloom_dmg + skill_dmg

    return total_damage
