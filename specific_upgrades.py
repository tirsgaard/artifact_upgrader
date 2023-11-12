import numpy as np
from joblib import Parallel, delayed

from src.artifact_logic.artifact import Artifact
from src.formulas.Furina import furina_optim
from src.formulas.Ganyu import calculate_ganyu_damage
from src.formulas.default import prepare_artifacts
from src.io.load_from_GO import get_art_from_JSON
from tqdm import tqdm
import matplotlib.pyplot as plt

from src.optim_func import average_upgrade_benefit

if __name__ == "__main__":

    # Load artifacts from JSON
    path = r"C:\Users\rasmu\Downloads\Inventory_KameraV1.3.9\GenshinData\genshinData_GOOD_2023_11_11_14_51.json"
    worn_artifacts = get_art_from_JSON(path, location="Furina")
    equipped_artifacts = {}
    for art in worn_artifacts:
        equipped_artifacts[art.slot] = art

    print("Original damage:")
    optim_func = lambda x: calculate_ganyu_damage(prepare_artifacts(x, equipped_artifacts))
    current_damage = optim_func(None)
    print(current_damage)

    # Get all artifacts
    all_artifacts = get_art_from_JSON(path, location=None)

    # Remove artifacts that are not from the set
    set_name = "GoldenTroupe"
    all_artifacts = [art for art in all_artifacts if art.set == set_name]

    benefit_list = Parallel(n_jobs=-1)(
        delayed(average_upgrade_benefit)(art, optim_func, current_damage) for art in tqdm(all_artifacts))
    benefit_list = [benefit for benefit, benefits, set_prob in benefit_list]

    # Sort artifacts by benefit
    benefit_list = np.array(benefit_list)
    sort_index = np.argsort(benefit_list)[::-1]
    all_artifacts = np.array(all_artifacts)
    all_artifacts = all_artifacts[sort_index]

    # Print top 10
    for i in range(10):
        print(all_artifacts[i])
        print(benefit_list[sort_index[i]])

    plt.hist(benefit_list[benefit_list>0], bins=30)
    plt.xlabel("Flat damage benefit")
    plt.ylabel("Number of artifacts")
    plt.show()


