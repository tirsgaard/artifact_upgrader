from collections import Counter


def calculate_sesshou_sakura_dmg_level_3(artifact_bonuses: dict[str, float]) -> float:
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
    electro_damage_bonus_skyward_atlas = 12 / 100
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
    total_enemy_electro_dmg_res = base_enemy_electro_dmg_res + kazuha_enemy_electro_dmg_res
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_crit_dmg = default_crit_dmg + art_crit_dmg
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + art_crit_rate, 1), 0)
    team_electro_dmg_bonus = (0.04/100)*(char_elem_mastery + weapon_elem_mastery + art_elem_mastery)
    total_electro_dmg_bonus = electro_damage_bonus_skyward_atlas + art_electro_dmg_bonus + team_electro_dmg_bonus
    total_elemental_mastery = art_elem_mastery
    ele_skill_dmg_bonus = total_elemental_mastery * (0.15/100)
    total_ele_skill_dmg_bonus = ele_skill_dmg_bonus + (20./100) + (25./100) + (25./100)
    team_common_dmg_bonus = furina_common_dmg_bonus
    total_common_dmg_bonus = team_common_dmg_bonus
    total_dmg_bonus = total_common_dmg_bonus + total_ele_skill_dmg_bonus + total_electro_dmg_bonus
    team_atk = sangonomiya_kokomi_atk_bonus
    base_atk = char_atk + weapon_atk
    total_atk = base_atk * (1 + 0.331 + art_atk_bonus + team_atk) + art_atk_flat

    # Final damage calculation
    damage = 1.706 * total_atk * (1 + total_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * \
             enemy_def_multiplier * (1 - total_enemy_electro_dmg_res / 2)

    return damage
