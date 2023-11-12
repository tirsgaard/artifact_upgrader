import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from src.artifact_logic.constants import ARTIFACT_DROP_RATE_DOMAIN, ARTIFACT_DROP_SLOT_RATE
from scipy.special import logsumexp


def max_dist_quantile(data: np.ndarray, levels: tuple[float], N_steps: int = 1000):
    # sort the data:
    data_sorted = np.sort(data, axis=1)
    N = data.shape[1]
    cdf = 1. * np.arange(N) / (N - 1)
    inverted_cdf = np.log(1. - cdf)
    pdf = np.log(1. / (N - 1))

    current_dist = pdf

    quantile_array = np.zeros((N_steps, data.shape[0], len(levels)))
    for step in range(N_steps):
        current_dist = inverted_cdf + current_dist
        current_dist = current_dist - logsumexp(current_dist)
        cum_dist = np.cumsum(np.exp(current_dist))
        indexes = (cum_dist[:, None] > levels).sum(axis=0) - 1
        quantile_array[step, :, :] = np.clip(data_sorted[:, indexes], a_min=0, a_max=float("Inf"))
    return quantile_array


def plot_damage_over_time(artifact_benefits, all_artifacts, N_steps=100):
    # Plot the quantiles (0.05, 0.5, 0.95) of the max distribution for each of the artifacts
    max_dist_timeline = max_dist_quantile(artifact_benefits, (0.05, 0.5, 0.95), N_steps=N_steps)
    x = np.arange(1, 1+N_steps)*ARTIFACT_DROP_SLOT_RATE  # 5 artifact slots, 2 sets of artifacts
    colors = ["red", "blue", "green", "orange", "purple"]
    for j, artifact_type in tqdm(enumerate(all_artifacts)):
        plt.plot(x, max_dist_timeline[:, j, 0], linestyle="dashed", color=colors[j])
        plt.plot(x, max_dist_timeline[:, j, 1], label=artifact_type, color=colors[j])
        plt.plot(x, max_dist_timeline[:, j, 2], linestyle="dashed", color=colors[j])
    plt.xlabel("Number of domain runs")
    plt.xscale("log")
    plt.ylabel("Increase in damage")
    plt.legend()
    plt.show()
