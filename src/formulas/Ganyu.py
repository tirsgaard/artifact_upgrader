def calculate_freeze_ganyu_damage(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_atk_per = artifact_bonuses["att_per"] / 100
    art_atk_flat = artifact_bonuses["att_flat"]
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_cryo_dmg_bonus = artifact_bonuses["cryo_per"] / 100

    # Constants given in the formula
    char_atk = 334.85
    weapon_atk = 608.07
    team_atk_bonus_rosaria = 20 / 100
    first_great_magic_atk_bonus = 32 / 100
    char_crit_dmg = 38.4 / 100
    weapon_crit_dmg = 66.2 / 100
    default_crit_dmg = 50 / 100
    blizzard_strayer_cryo_bonus = 15 / 100
    charged_attack_bonus = 16 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_cryo_res = 10 / 100
    additional_cryo_res_reduction = 45 / 100

    # Derived calculations
    base_atk = char_atk + weapon_atk
    total_atk_first_scenario = base_atk * (1 + first_great_magic_atk_bonus + art_atk_per + team_atk_bonus_rosaria) + art_atk_flat
    total_atk_second_scenario = base_atk * (1 + 0.88 + first_great_magic_atk_bonus + art_atk_per + team_atk_bonus_rosaria) + art_atk_flat
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_cryo_dmg_bonus = blizzard_strayer_cryo_bonus + art_cryo_dmg_bonus
    total_crit_dmg = char_crit_dmg + weapon_crit_dmg + default_crit_dmg + art_crit_dmg

    # Calculating each component's damage
    frostflake_arrow_dmg = 2.304 * total_atk_first_scenario * (1 + charged_attack_bonus + total_cryo_dmg_bonus) * \
                           (1 + art_crit_rate * total_crit_dmg) * enemy_def_multiplier * \
                           (1 - base_enemy_cryo_res)
    frostflake_arrow_bloom_dmg = 3.917 * total_atk_first_scenario * (1 + charged_attack_bonus + total_cryo_dmg_bonus) * \
                                 (1 + min(0.15 + art_crit_rate, 1) * total_crit_dmg) * enemy_def_multiplier * \
                                 (1 - base_enemy_cryo_res)
    skill_dmg = 2.112 * total_atk_second_scenario * (1 + total_cryo_dmg_bonus + additional_cryo_res_reduction) * \
                (1 + total_crit_dmg) * enemy_def_multiplier * \
                (1 - (additional_cryo_res_reduction - base_enemy_cryo_res) / 2)
    ice_shard_dmg = 1.265 * total_atk_second_scenario * (1 + total_cryo_dmg_bonus + additional_cryo_res_reduction) * \
                    (1 + total_crit_dmg) * enemy_def_multiplier * \
                    (1 - (additional_cryo_res_reduction - base_enemy_cryo_res) / 2)
    frostflake_arrow_dmg_third_scenario = 2.304 * total_atk_second_scenario * (1 + charged_attack_bonus + 0.52 + total_cryo_dmg_bonus) * \
                                          (1 + total_crit_dmg) * enemy_def_multiplier * \
                                          (1 - (additional_cryo_res_reduction - base_enemy_cryo_res) / 2)
    frostflake_arrow_bloom_dmg_third_scenario = 3.917 * total_atk_second_scenario * (1 + charged_attack_bonus + 0.52 + total_cryo_dmg_bonus) * \
                                                (1 + total_crit_dmg) * enemy_def_multiplier * \
                                                (1 - (additional_cryo_res_reduction - base_enemy_cryo_res) / 2)
    skill_dmg_third_scenario = 2.112 * total_atk_second_scenario * (1 + total_cryo_dmg_bonus + 0.52) * \
                               (1 + total_crit_dmg) * enemy_def_multiplier * \
                               (1 - (additional_cryo_res_reduction - base_enemy_cryo_res) / 2)

    # Total damage
    total_damage = frostflake_arrow_dmg + frostflake_arrow_bloom_dmg + skill_dmg + \
                   10 * ice_shard_dmg + 3 * frostflake_arrow_dmg_third_scenario + \
                   3 * frostflake_arrow_bloom_dmg_third_scenario + skill_dmg_third_scenario

    return total_damage
