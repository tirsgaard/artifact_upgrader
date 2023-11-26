import subprocess
from copy import copy, deepcopy
from pathlib import Path
from time import time
import re
from dataclasses import dataclass
from typing import Optional, Counter
import random

from src.gcsim.constants import char_name_list


@dataclass
class GCSimChar:
    level: str
    weapon: str
    set: str
    stats: Optional[str]

    def __str__(self):
        return "".join([self.level, self.weapon, self.set, self.stats])


@dataclass
class Rotation:
    rotation: list[str]

    def __str__(self):
        return "".join(self.rotation)



@dataclass
class Settings:
    iterations: int
    swap_delay: int

    def __str__(self):
        return f"options iteration = {self.iterations} swap_delay = {self.swap_delay}; \n"


@dataclass
class Config:
    chars: dict[str, GCSimChar]
    options: Settings
    rotation: Rotation

    def __str__(self):
        return "\n".join([*[str(char) for char in self.chars.values()], str(self.options), str(self.rotation)])

    def modify_char_stats(self, new_config, char, stats):
        pass


def call_gcsim(gcsim_path, gcsim_input_path, n_iter_used, tol=0.01):
    """
    Calls the Genshin Calculator Simulator (GCSim) with the given input and output paths.

    :param gcsim_path: Path to the GCSim executable.
    :param gcsim_input_path: Path to the input file for GCSim.
    :param n_iter_used: Number of iterations used in the simulation.
    :param tol: Tolerance for the probability of the average dps to be ouside of two standard deviations (95% conf int).
    :return: the output of GCSim from stdout.
    """
    # Call GCSim

    output = subprocess.run([gcsim_path, "-c", gcsim_input_path], capture_output=True, text=True).stdout
    if len(output) == 0:
        raise ValueError("GCSim did not output anything. Check the config file.")
    """ Output is of the form
    'Average duration of 110.44 seconds (min: 110.03 max: 118.52 std: 1.56)\n
    Average 14874763.53 damage over 110.44 seconds, resulting in 134728 dps (min: 116451.62 max: 136058.76 std: 3106.82) \n
    Simulation completed 100 iterations\n\n'
    """
    # Get dps
    output_processed = output.split("\n")[1].split(" ")
    dps = float(output_processed[8])
    min_dps = float(output_processed[11])
    max_dps = float(output_processed[13])
    std_dps = float(output_processed[15].replace(")", ""))

    std_dps_iter = std_dps / (n_iter_used ** 0.5)
    if std_dps_iter > 2 * tol * dps:
        print(f"Warning: std_dps_iter = {std_dps_iter} > {tol} * {dps} = {tol * dps}")

    return dps



class GCSimConfig:
    def __init__(self, gcsim_path: str, gcsim_input_path: str, gcsim_output_path: str):
        self.gcsim_path = gcsim_path
        self.gcsim_input_path = gcsim_input_path
        self.gcsim_output_path = str(Path(gcsim_output_path).parent / ("temp_config_" + str(random.getrandbits(64)) + ".txt"))
        self.config = self.read_config()

    def read_config(self):
        with open(self.gcsim_input_path, "r") as f:
            lines = f.readlines()
        chars = self.get_chars(lines)
        options = self.get_options(lines)
        rotation = self.get_rotation(lines)
        return Config(chars, options, rotation)

    def get_chars(self, lines: list[str]) -> dict[str, GCSimChar]:
        """ Gets the characters from the config file.

        :param lines: List of lines from the config file.
        :return: Dictionary of characters.
        """
        chars = {}
        # Fill in characters
        for line in lines:
            line_start = line.split(" ")[0]
            if line_start in char_name_list:
                if chars.get(line_start) is None:
                    chars[line_start] = []
                chars[line_start].append(line)

        # Initialize chars
        for char in chars:
            stats = ""
            for line in chars[char]:
                if line.split(" ")[1] == "char":
                    level = line
                elif "weapon" in line.split(" ")[2]:
                    weapon = line
                elif "set" in line.split(" ")[2]:
                    set = line
                elif line.split(" ")[2] == "stats":
                    stats += line
            chars[char] = GCSimChar(level, weapon, set, stats)
        return chars


    def get_options(self, lines: list[str]) -> Settings:
        """ Gets the options from the config file.

        :param lines: List of lines from the config file.
        :return: Settings.
        """

        # Fill in options
        for i, line in enumerate(lines):
            line_start = line.split(" ")[0]
            if "options" in line_start:
                options = line

        # Initialize options
        swap_delay = int(re.findall("swap_delay[ ]*=[ ]*[0-9]+", options)[0].split("=")[1])
        iterations = int(re.findall("iteration[ ]*=[ ]*[0-9]+", options)[0].split("=")[1])
        return Settings(iterations, swap_delay)

    def get_rotation(self, lines: list[str]) -> Rotation:
        """ Gets the rotation from the config file.

        :param lines: List of lines from the config file.
        :return: Rotation.
        """

        # Fill in rotation
        line_start = -1
        for i, line in enumerate(lines):
            line_start = line.split(" ")[0]

            rot_start = line_start not in char_name_list
            rot_start &= "options" not in line_start
            rot_start &= "char" not in line_start
            rot_start &= "target" in line_start or "energy" in line_start or "active " in line_start or "for " in line_start
            if rot_start:
                line_start = i
                break
        if line_start == -1:
            raise ValueError("No rotation found in config file.")
        rotation = lines[line_start:]
        return Rotation(rotation)

    def modify_iterations(self, n_iter):
        """
        Modifies the config file for GCSim to use the correct number of iterations and seed.

        :param n_iter: Path to the GCSim executable.
        :return: None
        """
        # Modify config file
        self.config.options.iterations = n_iter

    @staticmethod
    def modify_char_stats(config, char, stats):
        """
        Modifies the config file for GCSim to use the correct character stats.

        :param char: Character name.
        :param stats: Dictionary of stats to modify.
        :return: None
        """
        # Modify config file
        stats_absolute = f"{char} add stats {stats};\n"
        config.chars[char].stats = stats_absolute
        return config

    def get_dps(self):
        return call_gcsim(self.gcsim_path, self.gcsim_output_path, self.config.options.iterations, tol=0.01)

    def generate_new_config(self, char, stats):
        new_config = deepcopy(self.config)
        new_config = self.modify_char_stats(new_config, char, stats)
        self.write_config(self.gcsim_output_path, new_config)
        return self.gcsim_output_path

    def evaluate_stats(self, char: str, stats: str):
        self.generate_new_config(char, stats)
        return self.get_dps()

    def write_config(self, output_path, config=None):
        config = self.config if config is None else config
        with open(output_path, "w") as f:
            f.write(str(config))


if __name__ == "__main__":
    # Call GCSim
    gcsim_path = r"C:\Users\rasmu\Downloads\gcsim\gcsim.exe"
    gcsim_input_path = r"C:\Users\rasmu\Downloads\gcsim\config.txt"
    gcsim_output_path = r"C:\Users\rasmu\Downloads\gcsim\config_temp.txt"
    n_iter = 1000

    config = GCSimConfig(gcsim_path, gcsim_input_path, gcsim_output_path)
    config.modify_iterations(n_iter)
    config.write_config(gcsim_output_path)
    output = call_gcsim(gcsim_path, gcsim_output_path, n_iter)
    print(output)
