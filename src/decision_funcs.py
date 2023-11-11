from src.artifact_logic.artifact import Artifact, SubStat
import numpy as np
from optim_func import place_holder_optim

def sim_damage(optim_func, N=10**4):
    # Try randomly sampling plume artifacts and check damage dist
    damage_numbers = np.zeros((N,))
    for i in range(N):
        # Random sample artifact
        artifact = Artifact("plume", level=0)
        artifact.gen_artifact()
        artifact.level_artifact(20)
        # Calculate damage
        damage_numbers[i] = optim_func(artifact)
    return damage_numbers

def top_damage(optim_func, current_damage, N=10**4):
    # Try randomly sampling plume artifacts and check damage dist
    damage_numbers = sim_damage(optim_func, N=N)

    # Plot histogram of damage
    import matplotlib.pyplot as plt
    plt.hist(damage_numbers, bins=100, density=True)
    # Add current damage as vertical line
    plt.axvline(x=current_damage, color="red")

    # Set title to what quantile the current damage is
    quantile = np.sum(damage_numbers < current_damage) / N
    plt.title("Current artifact is top " + str(np.round(100 - quantile * 100)) + "%")
    plt.xlabel("Damage")
    plt.ylabel("Probability density")
    plt.show()

    # Get average damage upgrade
    greddy_damage_numbers = damage_numbers.copy()
    greddy_damage_numbers[greddy_damage_numbers < current_damage] = current_damage
    print("Average damage upgrade: " + str(np.mean(greddy_damage_numbers) - current_damage))

    return damage_numbers

def upgrade_path(damage_numbers, current_damage, N_length=100, N_sim=100):
    """ This function computes a bootstrapped estimate of damage upgrade path.
    It samples from the damage_numbers with replacement.

    Input:
        damage_numbers (np.array): array of damage numbers (N)
        current_damage (float): current damage
        N_length (int): number of upgrades to simulate
        N_sim (int): number of simulations to run
    """
    history = np.zeros((N_sim, N_length))
    for i in range(N_sim):
        # Randomly sample an entire upgrade path
        upgrade_path = np.random.choice(damage_numbers, size=(N_length,), replace=True)
        # Upgrade path is cumulative max
        path = np.maximum.accumulate(upgrade_path)
        path[path < current_damage] = current_damage
        history[i] = path

    # Plot average, 5 and 95% quantiale of upgrade path
    import matplotlib.pyplot as plt
    plt.plot(np.mean(history, axis=0), color="blue", label="Average")
    plt.plot(np.quantile(history, 0.05, axis=0), color="blue", linestyle="--", label="5 and 95% quantile")
    plt.plot(np.quantile(history, 0.95, axis=0), color="blue", linestyle="--")
    plt.axhline(y=current_damage, color="orange", label="Current damage")
    plt.axhline(y=damage_numbers.max(), color="green", label="Maximum damage")
    plt.xlabel("Number of artifacts")
    plt.ylabel("Damage")
    # Add legends, with the same tag for quantile lines
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Create current artifact
    test_art = Artifact("plume", level=20)
    test_art.substats[0] = SubStat("crit_damage", "plume", value=5.4)
    test_art.substats[1] = SubStat("crit_chance", "plume", value=7.4)
    test_art.substats[2] = SubStat("em", "plume", value=58)
    test_art.substats[3] = SubStat("def_per", "plume", value=13.1)
    current_damage = place_holder_optim(test_art)
    print("Current damage: " + str(current_damage))

    damage_numbers = sim_damage(place_holder_optim, N=10**5)
    upgrade_path(damage_numbers, current_damage, N_length=100, N_sim=10**4)