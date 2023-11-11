import numpy as np
from src.artifact_logic.constants import main_level_stats, sub_stat_chances, sub_stat_rolls
from line_profiler_pycharm import profile

class MainStat:
    """ Class for storing the main stat of an item"""

    def __init__(self, type, level):
        self.type = type
        self.level = level

    def get_value(self):
        return main_level_stats[self.type][self.level]

    def __copy__(self):
        return MainStat(self.type, self.level)


class SubStat:
    """ Class for storing one of the substats on an item"""
    @profile
    def __init__(self, type, slot, value=None, upgrade_number=0):
        self.legal_substat_list = ["hp_per", "hp_flat",
                                   "def_per", "def_flat",
                                   "att_per", "att_flat",
                                   "crit_chance", "crit_damage",
                                   "em", "er",
                                   None]

        self.possible_stat_rolls = sub_stat_rolls

        self.main_stat_rolls = {}

        assert (slot in ["flower", "plume", "sands", "goblet", "circlet"])
        self.type = type
        self.slot = slot
        self.check_legal_stat()
        self.upgrade_number = upgrade_number
        self.value = value
        self.combined_tier = 0
        if self.value is None:
            # Case where new value has to be determined
            self.value, self.combined_tier = self.random_roll()

    def check_legal_stat(self):
        assert self.type in self.legal_substat_list

    def possible_stat_vals(self):
        """ This function returns the possible values for the substat"""
        return self.possible_stat_rolls[self.type]

    def random_roll(self):
        """ This function rolls a random value for the substat. This is 100, 90, 80, 70% of the maximum value"""
        stat_vals = self.possible_stat_vals()
        if stat_vals is None:
            return None, None
        tier = np.random.randint(0, len(stat_vals))
        return stat_vals[tier], 0.6 + 0.1 * tier

    @profile
    def upgrade(self, value=None):
        """ Upgrades stat to next tier. If value is provided it is used instead of rolling a new value"""
        if value is None:
            value, new_tier = self.random_roll()

        else:
            """
            # Check if value is legal
            assert value in self.possible_stat_vals()
            """
            # Determine tier of value in array
            new_tier = value/self.possible_stat_vals()[-1]
        
        self.value += value
        self.combined_tier += new_tier
        self.upgrade_number += 1

    def __copy__(self):
        return SubStat(self.type, self.slot, value=self.value, upgrade_number=self.upgrade_number)


class Artifact:
    @profile
    def __init__(self, slot, main_stat=None, substat1=None, substat2=None, substat3=None, substat4=None, substats=None,
                 level=1, set=None, pre_gen=False):
        """ This class stores information related to a artifiact.
        The main stat is stored as a MainStat object and the substats are stored as SubStat objects.
        There can be a maximum of 4 substats.
        """
        self.level = level
        self.slot = slot
        self.set = set
        if not pre_gen:
            if main_stat == None:
                self.main_stat = self.gen_main(slot)
            else:
                self.main_stat = MainStat(main_stat, level)
            if substats == None:
                self.substats = [SubStat(substat1, self.slot),
                                 SubStat(substat2, self.slot),
                                 SubStat(substat3, self.slot),
                                 SubStat(substat4, self.slot)]
            else:
                self.substats = substats

    def gen_main(self, slot):
        self.slot_stats = {"sands": {"hp_per": 0.8 / 3,
                                     "att_per": 0.8 / 3,
                                     "def_per": 0.8 / 3,
                                     "er": 0.1,
                                     "em": 0.1},
                           "goblet": {"hp_per": 0.1925,
                                      "att_per": 0.1925,
                                      "def_per": 0.19,
                                      "pyro_per": 0.05,
                                      "electro_per": 0.05,
                                      "cryo_per": 0.05,
                                      "hydro_per": 0.05,
                                      "dendro_per": 0.05,
                                      "anemo_per": 0.05,
                                      "geo_per": 0.05,
                                      "phys_per": 0.05,
                                      "em": 0.025},
                           "plume": {"att_flat": 1},
                           "flower": {"hp_flat": 1},
                           "circlet": {"hp_per": 0.22,
                                       "att_per": 0.22,
                                       "def_per": 0.22,
                                       "crit_chance": 0.1,
                                       "crit_damage": 0.1,
                                       "healing": 0.1,
                                       "em": 0.04},
                           }
        stat_table = self.slot_stats[slot]
        # sample stat
        chances = np.array(list(stat_table.values()))
        values = np.array(list(stat_table.keys()))
        stat = np.random.choice(values, p=chances)
        return MainStat(stat, self.level)

    def gen_sub_stat(self, slot, black_list):
        """ Function for randomly sampling a sub stat.

        Input:
            slot (str): Type of slot of artifact
            black_list (list): List of strings containing types of stats that are already on artifact

        :return
            sub_stat (SubStat): Type of sub stat
        """
        sub_prob = sub_stat_chances[slot].copy()
        # Remove black listed items
        for item in black_list:
            if item in sub_prob.keys():
                sub_prob.pop(item)
        # Convert values to array and renormalize
        chances = np.array(list(sub_prob.values()))
        chances = chances / chances.sum()
        values = np.array(list(sub_prob.keys()))
        stat = np.random.choice(values, p=chances)
        return SubStat(stat, self.slot, upgrade_number=0)

    def upgrade_substats(self):
        """ This function selects a random not-None substat and upgrades it.
        If the artifact contains a None substat, that is filled instead
        """
        # Check for any None substat
        types = list(substat.type for substat in self.substats)
        if None in types:
            # Find the index of the None substat
            none_index = types.index(None)
            # Generate a new substat (with other substats as black list)
            new_substat = self.gen_sub_stat(self.slot, types)
            # Replace the None substat with the new substat
            self.substats[none_index] = new_substat

            # Check that all slots are filled (only 4 and 5-star artifacts are supported)
            assert (none_index < 4)
            return
        # Select a random substat to upgrade
        upgrade_index = np.random.randint(0, 4)
        # Upgrade the substat
        self.substats[upgrade_index].upgrade()

    def n_upgrades_left(self, end_level=20):
        # check number of break-points reached before
        break_points = self.level // 4
        # check number of break-points reached after
        break_points_after = end_level // 4
        n_break = break_points_after - break_points
        return n_break

    def level_artifact(self, level=20):
        """ Function for leveling an artifact to the level specified.
            Upgrading of substats at every 4 levels (4, 8, 12, 16, 20) is taken into account.
        """
        assert (level <= 20)
        n_break = self.n_upgrades_left(level)
        # Upgrade substats
        for i in range(n_break):
            self.upgrade_substats()
        # Upgrade main stat
        self.main_stat.level = level
        self.level = level

    def gen_artifact(self):
        self.main_stat = self.gen_main(self.slot)
        # Number of starting substats
        self.n_starting_substat = np.random.randint(3, 5)  # We assume 50-50 for 3 or 4 substats
        black_list = [self.main_stat.type]
        for i in range(self.n_starting_substat):
            self.substats[i] = self.gen_sub_stat(self.slot, black_list)
            black_list.append(self.substats[i].type)

    def __repr__(self):
        """ This function returns a string representation of the artifact """
        return self.__str__()

    def __str__(self):
        """ This function returns a string representation of the artifact """
        prefix_string = f"Slot: {self.slot}, Set: {self.set} \n " \
               f"Main Stat: {self.main_stat.type}  {self.main_stat.get_value()}\n " \
               f"Substats: {self.substats[0].type} {self.substats[0].value}, " \
               f"{self.substats[1].type} {self.substats[1].value}, " \
               f"{self.substats[2].type} {self.substats[2].value}, "
        if len(self.substats) == 4:
            prefix_string += f"{self.substats[3].type} {self.substats[3].value}\n"
        return prefix_string + f"Level: {self.level}"

    def get_full_stats(self):
        """ Function for getting stats given by artfiact.
        This includes filling all possible values. If a stat is not provided by the artifact, it's value will be 0.
        Input:
            None
        :return
            stats (dict): Dictionary containing all stats given by artifact
        """

        stats = {"hp_per": 0,
                 "att_per": 0,
                 "def_per": 0,
                 "hp_flat": 0,
                 "att_flat": 0,
                 "def_flat": 0,
                 "er": 0,
                 "em": 0,
                 "crit_chance": 0,
                 "crit_damage": 0,
                 "healing": 0,
                 "pyro_per": 0,
                 "electro_per": 0,
                 "cryo_per": 0,
                 "hydro_per": 0,
                 "dendro_per": 0,
                 "anemo_per": 0,
                 "geo_per": 0,
                 "phys_per": 0,
                 }
        # Add main stat
        stats[self.main_stat.type] += self.main_stat.get_value()
        # Add substats
        for substat in self.substats:
            if substat.type != None:
                stats[substat.type] += substat.value
        return stats

    @profile
    def __copy__(self):
        """ Function for copying an artifact """
        new_artifact = Artifact(self.slot, level=self.level, set=self.set, pre_gen=True)
        new_artifact.main_stat = self.main_stat.__copy__()
        new_artifact.substats = [substat.__copy__() for substat in self.substats]
        return new_artifact


if __name__ == "__main__":
    test = Artifact("sands")
    test.gen_artifact()
    print(test)
    test = Artifact("goblet")
    test = Artifact("plume")
    test = Artifact("flower")
    test = Artifact("circlet")
