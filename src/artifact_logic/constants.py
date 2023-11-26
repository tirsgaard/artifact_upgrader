import numpy as np

main_level_stats = {
    'hp_flat': [717, 920, 1123, 1326, 1530, 1733, 1936, 2139, 2342, 2545, 2749, 2952, 3155, 3358, 3561, 3764, 3967,
                4171, 4374, 4577, 4780],
    'att_flat': [47, 60, 73, 86, 100, 113, 126, 139, 152, 166, 179, 192, 205, 219, 232, 245, 258, 272, 285, 298, 311],
    'hp_per': [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7, 40.7,
               42.7, 44.6, 46.6],
    'att_per': [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7,
                40.7, 42.7, 44.6, 46.6],
    'def_per': [8.7, 11.2, 13.7, 16.2, 18.6, 21.1, 23.6, 26.1, 28.6, 31.0, 33.5, 36.0, 38.5, 40.9, 43.4, 45.9, 48.4,
                50.8, 53.3, 55.8, 58.3],
    'phys_per': [8.7, 11.2, 13.7, 16.2, 18.6, 21.1, 23.6, 26.1, 28.6, 31.0, 33.5, 36.0, 38.5, 40.9, 43.4, 45.9, 48.4,
                 50.8, 53.3, 55.8, 58.3],
    'ele_per': [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7,
                40.7, 42.7, 44.6, 46.6],
    'em': [28.0, 35.9, 43.8, 51.8, 59.7, 67.6, 75.5, 83.5, 91.4, 99.3, 107.2, 115.2, 123.1, 131.0, 138.9, 146.9, 154.8,
           162.7, 170.6, 178.6, 186.5],
    'er': [7.8, 10.0, 12.2, 14.4, 16.6, 18.8, 21.0, 23.2, 25.4, 27.6, 29.8, 32.0, 34.2, 36.4, 38.6, 40.8, 43.0, 45.2,
           47.4, 49.6, 51.8],
    'crit_chance': [4.7, 6.0, 7.3, 8.6, 9.9, 11.3, 12.6, 13.9, 15.2, 16.6, 17.9, 19.2, 20.5, 21.8, 23.2, 24.5, 25.8,
                    27.1, 28.4, 29.8, 31.1],
    'crit_damage': [9.3, 12.0, 14.6, 17.3, 19.9, 22.5, 25.2, 27.8, 30.5, 33.1, 35.7, 38.4, 41.0, 43.7, 46.3, 49.0, 51.6,
                 54.2, 56.9, 59.6, 62.2],
    'healing': [5.4, 6.9, 8.4, 10.0, 11.5, 13.0, 14.5, 16.1, 17.6, 19.1, 20.6, 22.1, 23.7, 25.2, 26.7, 28.2, 29.8, 31.3,
                32.8, 34.3, 35.9]
}

main_level_stats["electro_per"] = main_level_stats["ele_per"]
main_level_stats["cryo_per"] = main_level_stats["ele_per"]
main_level_stats["hydro_per"] = main_level_stats["ele_per"]
main_level_stats["dendro_per"] = main_level_stats["ele_per"]
main_level_stats["pyro_per"] = main_level_stats["ele_per"]
main_level_stats["anemo_per"] = main_level_stats["ele_per"]
main_level_stats["geo_per"] = main_level_stats["ele_per"]

sub_stat_chances = {
    "flower": {"att_flat": 0.1579,
               "def_flat": 0.1579,
               "hp_per": 0.1053,
               "att_per": 0.1053,
               "def_per": 0.1053,
               "er": 0.1053,
               "em": 0.1053,
               "crit_chance": 0.0789,
               "crit_damage": 0.0789,
               },
    "plume": {"hp_flat": 0.1579,
              "def_flat": 0.1579,
              "hp_per": 0.1053,
              "att_per": 0.1053,
              "def_per": 0.1053,
              "er": 0.1053,
              "em": 0.1053,
              "crit_chance": 0.0789,
              "crit_damage": 0.0789,
              },
    "sands": {"hp_flat": 0.15,
              "att_flat": 0.15,
              "def_flat": 0.15,
              "hp_per": 0.10,
              "att_per": 0.10,
              "def_per": 0.10,
              "er": 0.10,
              "em": 0.10,
              "crit_chance": 0.075,
              "crit_damage": 0.075,
              },
    "goblet": {"hp_flat": 0.15,
               "att_flat": 0.15,
               "def_flat": 0.15,
               "hp_per": 0.10,
               "att_per": 0.10,
               "def_per": 0.10,
               "er": 0.10,
               "em": 0.10,
               "crit_chance": 0.075,
               "crit_damage": 0.075,
               },

    "circlet": {"hp_flat": 0.15,
                "att_flat": 0.15,
                "def_flat": 0.15,
                "hp_per": 0.10,
                "att_per": 0.10,
                "def_per": 0.10,
                "er": 0.10,
                "em": 0.10,
                "crit_chance": 0.075,
                "crit_damage": 0.075,
                },

}

# Must be monotonically increasing
sub_stat_rolls = {"hp_per": np.array([4.08, 4.66, 5.25, 5.83]),
                                    "hp_flat": np.array([209.13, 239.00, 268.88, 298.75]),
                                    "def_per": np.array([5.10, 5.83, 6.56, 7.29]),
                                    "def_flat": np.array([16.20, 18.52, 20.83, 23.15]),
                                    "att_per": np.array([4.08, 4.66, 5.25, 5.83]),
                                    "att_flat": np.array([13.62, 15.56, 17.51, 19.45]),
                                    "crit_chance": np.array([2.72, 3.11, 3.50, 3.89]),
                                    "crit_damage": np.array([5.44, 6.22, 6.99, 7.77]),
                                    "em": np.array([16.32, 18.65, 20.98, 23.31]),
                                    "er": np.array([4.53, 5.18, 5.83, 6.48]),
                                    None: None}

GO_conversion_dict = {
    # Elemental damage
    "electro_dmg_": "electro_per",
    "pyro_dmg_": "pyro_per",
    "hydro_dmg_": "hydro_per",
    "cryo_dmg_": "cryo_per",
    "geo_dmg_": "geo_per",
    "anemo_dmg_": "anemo_per",
    "dendro_dmg_": "dendro_per",
    "physical_dmg_": "phys_per",
    # Other main-stats
    "heal_": "healing",
    # typical sub-stats
    "hp_": "hp_per",
    "hp": "hp_flat",
    "def_": "def_per",
    "def": "def_flat",
    "atk_": "att_per",
    "atk": "att_flat",
    "eleMas": "em",
    "enerRech_": "er",
    "critRate_": "crit_chance",
    "critDMG_": "crit_damage",
    # special cases
    None: None
}

stat_GO_to_GCSim = {"hp_per": "hp%",
                   "hp_flat": "hp",
                   "att_per": "atk%",
                   "att_flat": "atk",
                   "def_per": "def%",
                   "def_flat": "def",
                   "er": "er",
                   "em": "em",
                   "crit_chance": "cr",
                   "crit_damage": "cd",
                   "healing": "heal",
                   "phys_dmg": "phys%",
                   "pyro_dmg": "pyro%",
                   "hydro_dmg": "hydro%",
                   "dendro_dmg": "dendro%",
                   "electro_dmg": "electro%",
                   "anemo_dmg": "anemo%",
                   "cryo_dmg": "cryo%",
                   "geo_dmg": "geo%",
                    "phys_per": "phys%",
                    "pyro_per": "pyro%",
                    "hydro_per": "hydro%",
                    "dendro_per": "dendro%",
                    "electro_per": "electro%",
                    "anemo_per": "anemo%",
                    "cryo_per": "cryo%",
                    "geo_per": "geo%"}


### Artifact drop rate, source is https://genshin-impact.fandom.com/wiki/Loot_System/Artifact_Drop_Distribution
SUBSTAT_COUNT_DISTRIBUTION_DOMAIN = [0, 0, 0, 0.8, 0.2]  # Index is number of substats, value is probability

ARTIFACT_DROP_RATE_DOMAIN = 1.07  # 1.07 is the average number of 5* artifacts dropped per run
ARTIFACT_DROP_SLOT_RATE = (2*5)/ARTIFACT_DROP_RATE_DOMAIN