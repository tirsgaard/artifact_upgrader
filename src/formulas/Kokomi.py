def calculate_1_hit_dmg(artifact_bonuses: dict[str, float]) -> float:
    # Extracting artifact bonuses
    art_atk_per = artifact_bonuses["att_per"] / 100
    art_atk_flat = artifact_bonuses["att_flat"]
    art_hp_per = artifact_bonuses["hp_per"] / 100
    art_hp_flat = artifact_bonuses["hp_flat"]
    art_healing_bonus = artifact_bonuses["healing"] / 100
    art_hydro_dmg_bonus = artifact_bonuses["hydro_per"] / 100
    art_elem_mastery = artifact_bonuses["em"]

    # Constants given in the formula
    char_atk = 234.39
    weapon_atk = 401.29
    char_hp = 13471
    weapon_hp_bonus = (35.2 / 100)
    ocean_hued_clam_bonus = (15 / 100)
    sangonomiya_kokomi_hp_bonus = (25 / 100)
    furina_common_dmg_bonus = (100 / 100)
    char_hydro_dmg_bonus = (28.8 / 100)
    char_elem_mastery = 115.20
    weapon_elem_mastery = 165.38
    char_level = 90
    enemy_level = 90
    base_enemy_hydro_dmg_res = 10 / 100
    kazuha_enemy_hydro_dmg_res = -40 / 100

    # Other constants
    total_healing_bonus = 0.25 + 0.15 + art_healing_bonus

    # Derived calculations
    enemy_hydro_dmg_res = kazuha_enemy_hydro_dmg_res
    total_enemy_hydro_dmg_res = base_enemy_hydro_dmg_res + enemy_hydro_dmg_res
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    team_hydro_dmg_bonus = (0.04 / 100) * (char_elem_mastery + weapon_elem_mastery + art_elem_mastery)
    total_hydro_dmg_bonus = char_hydro_dmg_bonus + team_hydro_dmg_bonus + art_hydro_dmg_bonus
    team_common_dmg_bonus = furina_common_dmg_bonus
    total_common_dmg_bonus = team_common_dmg_bonus
    total_dmg_bonus = total_common_dmg_bonus + total_hydro_dmg_bonus
    team_hp = sangonomiya_kokomi_hp_bonus
    total_normal_att_damage_increase = ((8.2 / 100) + (15 / 100) * total_healing_bonus) * (char_hp * (1 + weapon_hp_bonus + art_hp_per + team_hp) + art_hp_flat)
    total_dmg_increase = total_normal_att_damage_increase
    base_atk = char_atk + weapon_atk
    total_atk = base_atk * (1 + art_atk_per) + art_atk_flat

    # Final damage calculation
    damage = (0.786 * total_atk + total_dmg_increase) * \
             (1 + total_dmg_bonus) * enemy_def_multiplier * \
             (1 - total_enemy_hydro_dmg_res / 2)

    return damage

