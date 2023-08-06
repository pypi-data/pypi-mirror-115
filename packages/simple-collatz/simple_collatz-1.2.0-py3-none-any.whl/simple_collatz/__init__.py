"""
Collatz Conjecture.

A simple Plot of the Collatz Conjecture

Copyright Manas Mengle 2021
"""
import json
import os
from datetime import datetime

from appdirs import user_data_dir
from matplotlib import pyplot as plt

from .math_utils import mean, median, mode

appname = "simple-collatz"
appauthor = "appcreatorguy"


def collatz(max_seed=10465, start_seed=1):
    """Run Collatz Conjecture."""
    with plt.ion():
        start = start_seed
        fig, ax = plt.subplots()
        fail_fig, fail_ax = plt.subplots()
        fig.suptitle("Collatz Conjecture Sequences")
        fail_fig.suptitle("Collatz Conjecture Stopping Time")
        fail_bottom = [1]
        fail_fig.supxlabel("Seed")
        fail_top = [0]
        fail_fig.supylabel("Stopping Time (iterations)")
        bottom = []
        fig.supxlabel("Iterations")
        top = []
        fig.supylabel("Value")
        bottom.append(1)
        top.append(start)
        ax.plot(bottom, top)
        inLoop = True
        while inLoop:
            try:
                if (top[-1] % 2) == 0:  # Even
                    top.append(top[-1] / 2)
                    bottom.append(bottom[-1] + 1)
                else:  # Odd
                    top.append(top[-1] * 3 + 1)
                    bottom.append(bottom[-1] + 1)
                ax.plot(bottom, top)
                if top[-1] == 4:  # Loop failed
                    fail_bottom.append(fail_bottom[-1] + 1)
                    fail_top.append(bottom[-1])
                    print(top[0], "reached 1 after", bottom[-1], "iterations")
                    bottom.clear()
                    top.clear()
                    start += 1
                    if start == max_seed:
                        inLoop = False
                        fail_ax.scatter(fail_bottom, fail_top)
                        return fail_top
                    bottom.append(1)
                    top.append(start)
            except KeyboardInterrupt:
                fail_bottom.append(fail_bottom[-1] + 1)
                fail_top.append(bottom[-1])
                fail_ax.scatter(fail_bottom, fail_top)
                print(top[0], "reached 1 after", bottom[-1], "iterations")
                bottom.clear()
                top.clear()
                start += 1
                inLoop = False
                return fail_top


def main():
    fail_top = collatz()
    filename = os.path.join(
        user_data_dir(appname, appauthor),
        "simple_collatz_history",
        (datetime.now().strftime("%d.%m.%Y_%H.%M.%S") + ".txt"),
    )
    os.makedirs(
        os.path.dirname(filename), exist_ok=True
    )  # Create intermediate directories if necessary
    with open(filename, "w") as f:
        data = {
            "averages": {
                "mode": mode(fail_top),
                "mean": mean(fail_top),
                "median": median(fail_top),
            },
            "iterations": fail_top,
        }
        json.dump(data, f, indent=4, sort_keys=True)
    print("mode:", mode(fail_top))
    print("median:", median(fail_top))
    print("mean:", mean(fail_top))
    input("Press enter to quit.")


if __name__ == "__main__":
    main()
