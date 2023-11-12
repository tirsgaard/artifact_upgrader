# Install
To install the package run the following command:
```bash
pip install -e .
```
# Usage

# Generation of optimisation target
The library functions be evaluating a optimisation target function based on equipted artifacts.
The ideal solution would be to allow other 3rd party libraries to be used to evaluate the target function.
This is a challenge as libraries such as Genshin Optimizer is writting in TypeScript, and this library is written in Python.

To solve this problem, you can go to the following GPT powered link and copy paste the calculation string from Genshin optimizer.
This should generate a function that this library can use. Please be sure to double check that the function is correct.
Please note that some stats not present on artifacts equipped in Genshin Optimizer will not be included in the function.

Link to GPT powered function converter:
https://chat.openai.com/g/g-WooZ5JJLo-python-function-converter

An example of a input to the GPT powered function converter:
```
Sesshou Sakura DMG: Level 3 21657 = 170.6% * Total ATK 3019.1 * ( 100% + Total DMG Bonus 256.0% ) * ( 100% + Total Crit Rate 85.6% * Total Crit DMG 123.0% ) * Enemy DEF Multiplier 50% * ( 100% - Total Enemy Electro DMG RES -30.0% / 2 )
Total ATK 3019.1 = Base ATK 1014.0 * ( 100% + Weapon ATK 33.1% + Art. ATK 82.7% + Team ATK 48% ) + Art. ATK 344.07
Base ATK 1014.0 = Char. ATK 339.63 + Weapon ATK 674.33
Team ATK 48% = ATK (Sangonomiya Kokomi) 48%
Total DMG Bonus 256.0% = Total Common DMG Bonus 100% + Total Ele. Skill DMG Bonus 75.9% + Total Electro DMG Bonus 80.1%
Total Common DMG Bonus 100% = Team Common DMG Bonus 100%
Team Common DMG Bonus 100% = Common DMG Bonus (Furina) 100%
Total Ele. Skill DMG Bonus 75.9% = Ele. Skill DMG Bonus 5.9% + Ele. Skill DMG Bonus 20% + Ele. Skill DMG Bonus 25% + Ele. Skill DMG Bonus 25%
Ele. Skill DMG Bonus 5.9% = Total Elemental Mastery 39.63 * 0.15%
Total Elemental Mastery 39.63 = Art. Elemental Mastery 39.63
Total Electro DMG Bonus 80.1% = Electro DMG Bonus (Skyward Atlas) 12% + Art. Electro DMG Bonus 46.6% + Team Electro DMG Bonus 21.5%
Team Electro DMG Bonus 21.5% = 0.04% * ( Char. Elemental Mastery 115.20 + Weapon Elemental Mastery 165.38 + Art. Elemental Mastery 256.44 )
Total Crit Rate 85.6% = Max( Min( Char. Crit Rate 19.2% + Default Crit Rate 5% + Art. Crit Rate 61.4%, 100% ), 0% )
Total Crit DMG 123.0% = Default Crit DMG 50% + Art. Crit DMG 73.0%
Enemy DEF Multiplier 50% = ( Char. Level 90 + 100 ) / ( Char. Level 90 + 100 + Enemy Level 90 + 100 )
Total Enemy Electro DMG RES -30.0% = Base Enemy Electro DMG RES 10% + Team Enemy Electro DMG RES -40%
Team Enemy Electro DMG RES -40% = Enemy Electro DMG RES (Kaedehara Kazuha) -40%
```
With the result:
```python
def calculate_sesshou_sakura_dmg_level3(artifact_bonuses: dict[str, float]) -> float:
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
    total_ele_skill_dmg_bonus = (0.059 * art_elem_mastery + 70) / 100
    total_electro_dmg_bonus = (0.12 + art_electro_dmg_bonus + 0.04 * (char_elem_mastery + weapon_elem_mastery + art_elem_mastery))
    total_crit_rate = max(min(char_crit_rate + default_crit_rate + art_crit_rate, 1), 0)
    total_crit_dmg = default_crit_dmg + art_crit_dmg
    enemy_def_multiplier = (char_level + 100) / (char_level + 100 + enemy_level + 100)
    total_enemy_electro_dmg_res = base_enemy_electro_dmg_res + kazuha_enemy_electro_dmg_res

    # Final damage calculation
    damage = 1.706 * total_atk * (1 + total_common_dmg_bonus) * (1 + total_ele_skill_dmg_bonus) * \
             (1 + total_electro_dmg_bonus) * (1 + total_crit_rate * total_crit_dmg) * \
             enemy_def_multiplier * (1 - total_enemy_electro_dmg_res / 2)

    return damage

```