from artifact import Artifact, SubStat
import numpy as np

from constants import sub_stat_rolls, sub_stat_chances
from upgrade_comb_const import upgrade_sets
# Use pycharm inline timer


def new_optim(artifact):
    """ This function is a placefolder function, that takes a artifact as input, and outputs number to optimise out.
    This could for example be the damage of a specific skill """

    base_EM = 81.59 + 80
    base_damage = 1 + 0.12 + 0.466
    base_attack = 889.50
    base_flat_attack = 19.45
    base_attack_per = 1.0 + 0.302 + 0.18 + 0.822
    base_crit_rate = 0.144 + 0.05 + 0.167
    base_crit_damage = 0.5 + 0.746

    # Get values from artifact
    stat_dict = artifact.get_full_stats()
    # Add values to base values
    base_EM += stat_dict["em"]
    base_damage += stat_dict["electro_per"] / 100.
    base_flat_attack += stat_dict["att_flat"]
    base_attack_per += stat_dict["att_per"]  / 100.
    base_crit_rate += stat_dict["crit_chance"]  / 100.
    base_crit_damage += stat_dict["crit_damage"]  / 100.

    # Calculate damage
    total_attack = base_attack*base_attack_per + base_flat_attack
    total_damage = base_damage
    total_crit_rate = base_crit_rate
    total_crit_damage = base_crit_damage


    # Damage for ability
    enemy_def_multi = 0.5*(1-0.1)
    damage = 1.517 * total_attack * (total_damage + (base_EM*0.0015))*(1 + total_crit_rate*total_crit_damage)*enemy_def_multi

    return damage

def place_holder_optim(artifact):
    """ This function is a placefolder function, that takes a artifact as input, and outputs number to optimise out.
    This could for example be the damage of a specific skill """

    base_EM = 81.59 + 80
    base_damage = 1 + 0.12 + 0.466
    base_attack = 889.50
    base_flat_attack = 19.45
    base_attack_per = 1.0 + 0.302 + 0.18 + 0.822
    base_crit_rate = 0.144 + 0.05 + 0.167
    base_crit_damage = 0.5 + 0.746

    # Get values from artifact
    stat_dict = artifact.get_full_stats()
    # Add values to base values
    base_EM += stat_dict["em"]
    base_damage += stat_dict["electro_per"] / 100.
    base_flat_attack += stat_dict["att_flat"]
    base_attack_per += stat_dict["att_per"]  / 100.
    base_crit_rate += stat_dict["crit_chance"]  / 100.
    base_crit_damage += stat_dict["crit_damage"]  / 100.

    # Calculate damage
    total_attack = base_attack*base_attack_per + base_flat_attack
    total_damage = base_damage
    total_crit_rate = base_crit_rate
    total_crit_damage = base_crit_damage


    # Damage for ability
    enemy_def_multi = 0.5*(1-0.1)
    damage = 1.517 * total_attack * (total_damage + (base_EM*0.0015))*(1 + total_crit_rate*total_crit_damage)*enemy_def_multi

    return damage

def average_benefit(artifact, optim_func):
    """ This function (exactly) computes the average benefit of upgrading an artifact.
    It does so by going through all possible upgrades, and computing the benefit of each upgrade.
    """
    # Get current damage
    current_damage = optim_func(artifact)

    # Get all possible upgrades
    upgrade_candidates, p_vals = artifact.get_upgrade_candidates()

    # Compute benefit of each upgrade
    benefit = 0
    for upgrade in upgrade_candidates:
        # Get damage of upgrade
        upgrade_damage = optim_func(upgrade)
        # Add benefit
        benefit += p_vals*max((upgrade_damage - current_damage, 0))

    # Divide by number of upgrades
    benefit /= len(upgrade_candidates)

    return benefit


def benefit_rolls(artifact, upgrade_list, opt_function, current_opt):
    """ This function calculates the benefit of different rolls of upgrades for the substats of an artifact.
    The sub-stats to be upgraded are specified in the upgrade_list."""

    # Convert the tuple indecating how many times each substat is upgraded to a list when each substat is upgraded
    # I.e. The format (2, 0, 1, 1) to the new [0, 0, 2, 3] format
    upgrades = []
    for i in range(len(upgrade_list)):
        if upgrade_list[i] > 0:
            upgrades.extend([i] * upgrade_list[i])

    # Construct array to store all combinations of upgrades
    roll_array = np.zeros((4,) * sum(upgrade_list))

    # Before iterating over all possible rolls, we can check if the best possible roll is even a upgrade
    # If not, we can return 0
    # Upgrade substats
    new_artifact = artifact.__copy__()
    for i, upgrade in enumerate(upgrades):
        # Get value of new roll
        try:
            value = max(sub_stat_rolls[new_artifact.substats[upgrade].type])
        except:
            test = 2
        new_artifact.substats[upgrade].upgrade(value=value)

    # calculate benefit
    if opt_function(new_artifact) <= current_opt:
        return 0, roll_array

    for index, element in np.ndenumerate(roll_array):
        # Upgrade substats
        new_artifact = artifact.__copy__()
        for i, upgrade in enumerate(upgrades):
            # Get value of new roll
            value = sub_stat_rolls[new_artifact.substats[upgrade].type][index[i]]
            new_artifact.substats[upgrade].upgrade(value=value)
        # calculate benefit
        benefit = opt_function(new_artifact) - current_opt
        benefit = max(benefit, 0)

        roll_array[index] = benefit

    # Weight with probability
    roll_benefit = roll_array.mean()  # We can take the average, as all combinations are equally likely

    opt_function(new_artifact)
    opt_function(new_artifact)
    return roll_benefit, roll_array


def average_upgrade_benefit(artifact, optim_func, current_obj):
    """ This function calculates the average benefit of upgrading an artifact."""
    # Get number of potential upgrades
    n_upgrades = artifact.n_upgrades_left()
    avg_improv = 0
    sum_prob = 0

    # Handle any missing substats
    # Check for any None substat
    types = list(substat.type for substat in artifact.substats)
    # Check if more than one type is None
    if types.count(None) > 1:
        raise ValueError("More than one substat is missing. This is currently not supported")

    benefits = []
    probs = []
    # Check if last sub-type is None (missing)
    if None in types:
        sub_prob = sub_stat_chances[artifact.slot].copy()
        # Block existing substats
        black_list = [substat.type for substat in artifact.substats]
        black_list.append(artifact.main_stat.type)
        # Remove black listed items
        for item in black_list:
            if item in sub_prob.keys():
                sub_prob.pop(item)
        # Re-normalize probabilities
        sub_prob = {key: value / sum(sub_prob.values()) for key, value in sub_prob.items()}

        for substat in sub_prob.keys():
            # add substat and weight with posibility
            sub_stat_benefit = 0
            for stat_value in sub_stat_rolls[substat]:
                new_artifact = artifact.__copy__()
                new_artifact.substats[-1] = SubStat(substat, artifact.slot, value=stat_value, upgrade_number=0)
                # Update level of artifact
                levels_to_breakpoint = 4 - new_artifact.level % 4
                new_artifact.main_stat.level += levels_to_breakpoint
                new_artifact.level += levels_to_breakpoint

                # Calulate average improvement and weight it with sample probability
                stat_avg_improv, stat_benefits, stat_probs = average_upgrade_benefit(new_artifact, optim_func, current_obj)
                substat_value_prob = sub_prob[substat]*0.25
                avg_improv += substat_value_prob*stat_avg_improv
                sub_stat_benefit += 0.25*avg_improv
                benefits.append(stat_benefits)
                probs.append(substat_value_prob*stat_probs)
                sum_prob += substat_value_prob
    else:
        # Compute all combinations of upgrades
        for i, (upgrade_set, set_prob) in enumerate(upgrade_sets[n_upgrades].items()):
            # Create copy of artifact
            new_artifact = artifact.__copy__()
            # Upgrade mainstat before all value combinations
            new_artifact.main_stat.level = 20
            new_artifact.level = 20

            # Compute average improvement
            benefit, all_benefits = benefit_rolls(new_artifact, upgrade_set, optim_func, current_obj)
            all_benefits = all_benefits.flatten()
            benefits.append(all_benefits)
            probs.append(set_prob/len(all_benefits) + np.zeros(all_benefits.shape))
            sum_prob += set_prob
            avg_improv += set_prob*benefit

        if len(upgrade_sets[n_upgrades]) == 0:
            # No upgrades possible
            return 0, np.zeros((4, 4, 4, 4)), np.zeros((4, 4, 4, 4))

    assert(np.isclose(sum_prob, 1.))
    benefits = np.concatenate(benefits)
    probs = np.concatenate(probs)
    return avg_improv, benefits, probs


if __name__ == "__main__":
    """
    from decision_funcs import top_damage
    # Create current artifact
    test_art = Artifact("plume", level=20)
    
    test_art.substats[0] = SubStat("em", "plume", value=51)
    test_art.substats[1] = SubStat("att_per", "plume", value=4.7)
    test_art.substats[2] = SubStat("def_per", "plume", value=19.7)
    test_art.substats[3] = SubStat("crit_damage", "plume", value=7.8)
    "
    test_art.substats[0] = SubStat("crit_damage", "plume", value=20.2)
    test_art.substats[1] = SubStat("crit_chance", "plume", value=5.4)
    test_art.substats[2] = SubStat("att_per", "plume", value=5.3)
    test_art.substats[3] = SubStat("er", "plume", value=16.8)
    current_damage = place_holder_optim(test_art)
    print("Current damage: " + str(current_damage))

    damage_numbers = top_damage(place_holder_optim, current_damage)
    """
    
    test = Artifact("sands")
    test.gen_artifact()

    test = Artifact("goblet")
    test_plume = Artifact("plume", level=20)
    test_plume.substats[0] = SubStat("hp_per", "plume", value=3.89)
    test_plume.substats[1] = SubStat("hp_flat", "plume", value=7.4)
    test_plume.substats[2] = SubStat("em", "plume", value=48)
    test_plume.substats[3] = SubStat("crit_damage", "plume", value=0)
    test = Artifact("flower")
    test = Artifact("circlet")
    print(test_plume)
    current_damage = new_optim(test_plume)

    # Create current artifact
    test_art = Artifact("plume", level=0)
    test_art.substats[0] = SubStat("em", "plume", value=24)
    test_art.substats[1] = SubStat("hp_flat", "plume", value=6.99)
    test_art.substats[2] = SubStat("hp_per", "plume", value=3.50)
    #test_art.substats[3] = SubStat("crit_damage", "plume", value=6.99)

    benefit, benefits, set_prob = average_upgrade_benefit(test_art, new_optim, current_damage)
    print("avg benefit exact: " + str(benefit))
    # Make histogram of benefits and their probabilities
    import matplotlib.pyplot as plt

    plt.hist(benefits, weights=set_prob, bins=30)
    plt.xlabel("Damage increase")
    plt.ylabel("Probability")
    plt.title("Distribution of damage increase")
    plt.show()

    """
    N = 10**5
    # validate code with randomly upgrading artifact
    benefits = np.zeros(N)
    for i in range(N):
        new_art = test_art.__copy__()
        for j in range(new_art.n_upgrades_left()):
            new_art.upgrade_substats()
        new_art.main_stat.level = 20
        new_art.level = 20
        new_damage = place_holder_optim(new_art)
        benefits[i] = max(new_damage - current_damage, 0)

    print("avg benefit random: " + str(np.mean(benefits)))
    #plt.hist(benefits, bins=30)
    #plt.show()
    """


    # Also plot the 1-cdf
    sort_idx = np.argsort(benefits)
    plt.plot(benefits[sort_idx], 1-np.cumsum(set_prob[sort_idx]))
    plt.xlabel("Damage increase")
    plt.ylabel("Probability")
    plt.title("Distribution of damage increase")
    plt.show()
