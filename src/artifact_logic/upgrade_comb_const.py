from scipy.stats import multinomial
import numpy as np

def filter_comb(n_points, slots=4):
    """ This function generates all combinations of upgrades spread over slots, with n_points"""
    master_set = {}
    starting_point = (0, ) * slots
    return gen_comb(starting_point, master_set, n_points, slots=slots)

def gen_comb(cur_set, stored_set, n_points, slots=4):
    """ This function recursivelu extends the stored_set with all combinations of upgrades spread over slots from cur_set with n_points"""

    if n_points > 0:
        # Loop over all new combinations
        for slot in range(slots):
            allocation = (0, )*slot + (1, ) + (0,)*(slots-slot-1)
            new_comb = tuple([sum(x) for x in zip(cur_set, allocation)])
            # Continue recursion
            gen_comb(new_comb, stored_set, n_points-1, slots=slots)

    else:
        # Store the new set as they have reached the final upgrade state
        stored_set[cur_set] = multinomial.pmf(cur_set, n=sum(cur_set), p=np.ones((slots))/slots)

    return stored_set

upgrade_set_1 = filter_comb(1, slots=4)
upgrade_set_2 = filter_comb(2, slots=4)
upgrade_set_3 = filter_comb(3, slots=4)
upgrade_set_4 = filter_comb(4, slots=4)
upgrade_set_5 = filter_comb(5, slots=4)
upgrade_sets = [{}, upgrade_set_1, upgrade_set_2, upgrade_set_3, upgrade_set_4, upgrade_set_5]

if __name__ == "__main__":
    sets = filter_comb(5, slots=4)
    test = 2