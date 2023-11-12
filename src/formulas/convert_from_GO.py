import re






def calculate_mademoiselle_crabaletta_dmg(artifact_bonuses: dict[str, float]) -> float:
    art_hp_bonus = artifact_bonuses["hp_per"] / 100
    art_hp = artifact_bonuses["hp_flat"]
    art_crit_dmg = artifact_bonuses["crit_damage"] / 100
    art_crit_rate = artifact_bonuses["crit_chance"] / 100
    art_elem_mastery = artifact_bonuses["em"]

    # Constants given in the formula
    char_hp = 15307
    furina_hp = 25
    furina_common_dmg_bonus = 100
    furina_ele_skill_crit_rate_bonus = 16
    char_elem_mastery = 115.20
    weapon_elem_mastery = 165.38
    char_crit_rate = 19.2
    default_crit_rate = 5
    default_crit_dmg = 50
    char_level = 90
    enemy_level = 90
    base_enemy_hydro_dmg_res = 10
    kazuha_enemy_hydro_dmg_res = -40

    # Derived calculations
    total_hp = char_hp * (1 + 400 * 0.0035 + art_hp_bonus / 100 + furina_hp / 100) + art_hp
    team_hp = furina_hp
    total_common_dmg_bonus = furina_common_dmg_bonus
    total_ele_skill_dmg_bonus = min(0.7 * total_hp * 0.001, 28.0) + 70  # 20% + 25% + 25%
    total_hydro_dmg_bonus = 0.04 * (char_elem_mastery + weapon_elem_mastery + art_elem_mastery)
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + furina_ele_skill_crit_rate_bonus + art_crit_rate, 100), 0)
    total_crit_dmg = default_crit_dmg + art_crit_dmg
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_enemy_hydro_dmg_res = base_enemy_hydro_dmg_res + kazuha_enemy_hydro_dmg_res

    # Final damage calculation
    damage = total_hp * (1 + total_common_dmg_bonus / 100) * (1 + total_ele_skill_dmg_bonus / 100) * \
             (1 + total_hydro_dmg_bonus / 100) * (1 + total_crit_rate / 100 * total_crit_dmg / 100) * \
             enemy_def_multiplier * (1 - total_enemy_hydro_dmg_res / 200)

    return damage

# Inputs for the function, replace with user inputs when using
art_hp_bonus = 113.6  # in percentage
art_hp = 6034.8
art_crit_dmg = 136.0  # in percentage
art_crit_rate = 22.6  # in percentage
art_elem_mastery = 256.44

# Calculate the damage
damage = calculate_damage(art_hp_bonus, art_hp, art_crit_dmg, art_crit_rate, art_elem_mastery)




if __name__ == "__main__":
    input_example = """
    Mademoiselle Crabaletta DMG 53208 = 14.9% * Total HP 63989 * Salon Members Mult. 140% * ( 100% + Total DMG Bonus 219.5% ) * ( 100% + Total Crit Rate 62.8% * Total Crit DMG 186.0% ) * Enemy DEF Multiplier 50% * ( 100% - Total Enemy Hydro DMG RES -30.0% / 2 )
    Total HP 63989 = Char. HP 15307 * ( 100% + 400 * 0.35% + Art. HP 113.6% + Team HP 25% ) + Art. HP 6034.8
    """
    calculation_function = create_calculation_function(input_example)
    print(calculation_function)