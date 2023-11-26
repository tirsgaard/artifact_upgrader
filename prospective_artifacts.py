import numpy as np

from src.artifact_logic.artifact import Artifact
from src.artifact_progression import plot_damage_over_time
from src.call_gcsim import GCSimConfig
from src.formulas.Furina import calculate_mademoiselle_crabaletta_dmg
from src.formulas.default import prepare_artifacts, convert_to_GCSim
from src.io.load_from_GO import get_art_from_JSON
from tqdm import tqdm
import matplotlib.pyplot as plt

if __name__ == "__main__":
    np.random.seed(1)
    # Load artifacts from JSON
    #path = r"C:\Users\rasmu\Downloads\Inventory_KameraV1.3.9\GenshinData\genshinData_GOOD_2023_11_12_14_48.json"
    path = r"C:\Users\rasmu\Downloads\gcsim\genshinData_GOOD_2023_11_25_21_37.json"
    char = "Ganyu"
    worn_artifacts = get_art_from_JSON(path, char)
    equipped_artifacts = {}
    for art in worn_artifacts:
        equipped_artifacts[art.slot] = art

    print("Original damage:")
    gcsim_path = r"C:\Users\rasmu\Downloads\gcsim\gcsim.exe"
    gcsim_input_path = r"C:\Users\rasmu\Downloads\gcsim\config_peter.txt"
    gcsim_output_path = r"C:\Users\rasmu\Downloads\gcsim\config_temp.txt"
    config = GCSimConfig(gcsim_path, gcsim_input_path, gcsim_output_path)
    config.modify_iterations(10)
    optim_func = lambda x: config.evaluate_stats("ganyu", convert_to_GCSim(prepare_artifacts(x, equipped_artifacts)))
    current_damage = optim_func(None)
    print(current_damage)

    all_artifacts = ["flower", "plume", "sands", "goblet", "circlet"]
    N = 10 ** 3

    artifact_benefits = np.zeros((len(all_artifacts), N))
    for j, artifact_type in tqdm(enumerate(all_artifacts), total=len(all_artifacts)):
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

    artifact_benefits_per = 100*artifact_benefits / current_damage
    plot_damage_over_time(artifact_benefits_per, all_artifacts, N_steps=100)




