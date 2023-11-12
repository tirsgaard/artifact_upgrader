def calculate_new_custom_target_damage(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_atk_bonus = artifact_bonuses["att_per"] / 100
    art_atk_flat = artifact_bonuses["att_flat"]
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_elem_mastery = artifact_bonuses["em"]
    art_electro_dmg_bonus = artifact_bonuses["electro_per"] / 100

    # Constants given in the formula
    char_atk = 339.63
    weapon_atk = 674.33
    sangonomiya_kokomi_atk_bonus = 48 / 100
    furina_common_dmg_bonus = 100 / 100
    char_elem_mastery = 115.20
    weapon_elem_mastery = 165.38
    char_crit_rate = 19.2 / 100
    default_crit_rate = 5 / 100
    default_crit_dmg = 50 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_electro_dmg_res = 10 / 100
    kazuha_enemy_electro_dmg_res = -40 / 100

    # Derived calculations
    base_atk = char_atk + weapon_atk
    total_atk = base_atk * (1 + 0.331 + art_atk_bonus + sangonomiya_kokomi_atk_bonus) + art_atk_flat
    total_common_dmg_bonus = furina_common_dmg_bonus
    total_ele_skill_dmg_bonus = (0.059 * art_elem_mastery + 70) / 100  # 20% + 25% + 25%
    total_electro_dmg_bonus = 0.12 + art_electro_dmg_bonus + 0.04 * (
                char_elem_mastery + weapon_elem_mastery + art_elem_mastery)
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + art_crit_rate, 1), 0)
    total_crit_dmg = default_crit_dmg + art_crit_dmg
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_enemy_electro_dmg_res = base_enemy_electro_dmg_res + kazuha_enemy_electro_dmg_res

    # Damage calculations for each component
    sesshou_sakura_dmg = 1.706 * total_atk * (1 + total_common_dmg_bonus) * (1 + total_ele_skill_dmg_bonus) * \
                         (1 + total_electro_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * \
                         enemy_def_multiplier * (1 - total_enemy_electro_dmg_res / 2)

    skill_dmg = 4.68 * total_atk * (1 + total_common_dmg_bonus) * (1 + total_electro_dmg_bonus) * \
                (1 + total_crit_rate * total_crit_dmg) * enemy_def_multiplier * (1 - total_enemy_electro_dmg_res / 2)

    tenko_thunderbolt_dmg = 6.009 * total_atk * (1 + total_common_dmg_bonus) * (1 + total_electro_dmg_bonus) * \
                            (1 + total_crit_rate * total_crit_dmg) * enemy_def_multiplier * (
                                        1 - total_enemy_electro_dmg_res / 2)

    # Final calculation for New Custom Target
    new_custom_target_damage = 9 * sesshou_sakura_dmg + skill_dmg + 3 * tenko_thunderbolt_dmg

    return new_custom_target_damage
