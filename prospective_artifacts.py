import numpy as np

from src.artifact_logic.artifact import Artifact
from src.formulas.Furina import furina_optim
from src.io.load_from_GO import get_art_from_JSON
from tqdm import tqdm
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load artifacts from JSON
    path = r"C:\Users\rasmu\Downloads\Inventory_KameraV1.3.9\GenshinData\genshinData_GOOD_2023_11_11_14_51.json"
    worn_artifacts = get_art_from_JSON(path, location="Furina")
    equpied_artifacts = {}
    for art in worn_artifacts:
        equpied_artifacts[art.slot] = art

    print("Original damage:")
    optim_func = lambda x: furina_optim(x, equpied_artifacts)
    current_damage = optim_func(None)
    print(current_damage)

    all_artifacts = ["flower", "plume", "sands", "goblet", "circlet"]
    N = 10 ** 5

    artifact_benefits = np.zeros((len(all_artifacts), N))
    for j, artifact_type in tqdm(enumerate(all_artifacts)):
        for i in range(N):
            art = Artifact(artifact_type)
            art.gen_artifact()
            art.level_artifact(20)
            artifact_benefits[j, i] = optim_func(art)

    artifact_benefits = artifact_benefits - current_damage

    for j, artifact_type in tqdm(enumerate(all_artifacts)):
        plt.hist(artifact_benefits[j], bins=N // 100, density=True, cumulative=True, histtype='step', label=artifact_type)
    plt.xlabel("Increase in damage")
    plt.ylabel("CDF of artifacts")
    plt.xlim(0)
    plt.ylim(1 - (artifact_benefits > 0).mean(axis=1).max(), 1.01)
    plt.legend()
    plt.show()
