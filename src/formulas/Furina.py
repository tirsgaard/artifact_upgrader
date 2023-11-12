def calculate_mademoiselle_crabaletta_dmg(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_hp_percent = artifact_bonuses["hp_per"] / 100
    art_hp_flat = artifact_bonuses["hp_flat"]
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_elem_mastery = artifact_bonuses["em"]

    # Constants given in the formula
    char_hp = 15307
    furina_hp_bonus = 25 / 100
    furina_common_dmg_bonus = 100 / 100
    team_hydro_dmg_bonus = 21.5 / 100
    char_elem_mastery = 115.20
    weapon_elem_mastery = 165.38
    char_crit_rate = 19.2 / 100
    fleuve_cendre_crit_rate_bonus = 16 / 100
    default_crit_rate = 5 / 100
    default_crit_dmg = 50 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_hydro_res = 10 / 100
    kazuha_enemy_hydro_res = -40 / 100

    # Derived calculations
    total_hp = char_hp * (1 + 400 * 0.0035 + art_hp_percent + furina_hp_bonus) + art_hp_flat
    ele_skill_dmg_bonus_from_hp = min(0.007 * total_hp * 0.001, 28 / 100)
    total_ele_skill_dmg_bonus = ele_skill_dmg_bonus_from_hp + 20 / 100 + 25 / 100 + 25 / 100
    total_dmg_bonus = furina_common_dmg_bonus + total_ele_skill_dmg_bonus + team_hydro_dmg_bonus
    team_elem_mastery_bonus = 0.04 / 100 * (char_elem_mastery + weapon_elem_mastery + art_elem_mastery)
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + fleuve_cendre_crit_rate_bonus + art_crit_rate, 1), 0)
    total_crit_dmg = default_crit_dmg + art_crit_dmg
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_enemy_hydro_res = base_enemy_hydro_res + kazuha_enemy_hydro_res

    # Final damage calculation
    damage = 0.149 * total_hp * 1.4 * (1 + total_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * \
             enemy_def_multiplier * (1 - total_enemy_hydro_res / 2)

    return damage


def calculate_multi_object_target_damage(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_hp_per = artifact_bonuses["hp_per"] / 100
    art_hp_flat = artifact_bonuses["hp_flat"]
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_elem_mastery = artifact_bonuses["em"]

    # Constants given in the formula
    char_hp = 15307
    char_crit_rate = 19.2 / 100
    default_crit_rate = 5 / 100
    ele_skill_crit_rate_bonus = 16 / 100
    default_crit_dmg = 50 / 100
    char_level = 90
    enemy_level = 90
    base_enemy_hydro_dmg_res = 10 / 100
    kazuha_enemy_hydro_dmg_res = -40 / 100
    furina_common_dmg_bonus = 100 / 100
    furina_hp_bonus = 25 / 100
    salon_members_multiplier = 1.4
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)

    # Derived calculations
    total_hp = char_hp * (1 + 0.35 * 400 / 100 + art_hp_per + furina_hp_bonus) + art_hp_flat
    total_enemy_hydro_dmg_res = base_enemy_hydro_dmg_res + kazuha_enemy_hydro_dmg_res
    team_hydro_dmg_bonus = 0.04 / 100 * (115.20 + 165.38 + art_elem_mastery)
    total_hydro_dmg_bonus = team_hydro_dmg_bonus
    ele_skill_dmg_bonus = min(0.7 * total_hp * 0.001, 28 / 100)
    total_ele_skill_dmg_bonus = ele_skill_dmg_bonus + 20 / 100 + 25 / 100 + 25 / 100
    total_common_dmg_bonus = furina_common_dmg_bonus
    total_dmg_bonus = total_common_dmg_bonus + total_ele_skill_dmg_bonus + total_hydro_dmg_bonus
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + ele_skill_crit_rate_bonus + art_crit_rate, 1), 0)
    total_crit_dmg = default_crit_dmg + art_crit_dmg

    # Individual character damage calculations
    mademoiselle_crabaletta_dmg = 0.149 * total_hp * salon_members_multiplier * (1 + total_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * enemy_def_multiplier * (1 - total_enemy_hydro_dmg_res / 2)
    surintendante_chevalmarin_dmg = 0.058 * total_hp * salon_members_multiplier * (1 + total_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * enemy_def_multiplier * (1 - total_enemy_hydro_dmg_res / 2)
    gentilhomme_usher_dmg = 0.107 * total_hp * salon_members_multiplier * (1 + total_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * enemy_def_multiplier * (1 - total_enemy_hydro_dmg_res / 2)

    # Total damage calculation
    total_damage = mademoiselle_crabaletta_dmg + 2 * surintendante_chevalmarin_dmg + gentilhomme_usher_dmg

    return total_damage

