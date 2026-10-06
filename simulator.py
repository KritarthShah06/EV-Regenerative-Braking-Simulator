"""
EV Regenerative Braking Energy Recovery Simulator
Project 3

Runs the baseline five-event simulation and Experiments 1-5.
All output files are saved inside the same project folder as this script.
"""

import csv
from pathlib import Path

# Make plotting work without opening plot windows.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# FOLDERS
# ---------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DATA = PROJECT_DIR / "data"
OUTPUT_FIGURES = PROJECT_DIR / "figures"

OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------
def recovered_energy_kwh(mass_kg, initial_kmh, final_kmh, efficiency):
    """Calculate recovered braking energy in kWh."""
    initial_ms = initial_kmh / 3.6
    final_ms = final_kmh / 3.6
    braking_energy_j = 0.5 * mass_kg * (initial_ms**2 - final_ms**2)
    return efficiency * braking_energy_j / 3_600_000


def braking_distance_m(initial_kmh, final_kmh, deceleration):
    """Calculate braking distance in metres."""
    initial_ms = initial_kmh / 3.6
    final_ms = final_kmh / 3.6
    return (initial_ms**2 - final_ms**2) / (2 * deceleration)


def save_csv(filename, headers, rows):
    path = OUTPUT_DATA / filename
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def save_plot(filename):
    path = OUTPUT_FIGURES / filename
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------
# BASELINE MODEL
# ---------------------------------------------------------
MASS = 1800
BATTERY_CAPACITY = 60
EFFICIENCY = 0.80
STARTING_SOC = 40

BRAKING_EVENTS = [
    (80, 40, 6),
    (60, 20, 5),
    (70, 30, 6),
    (50, 0, 5),
    (90, 40, 7),
]


def run_baseline():
    soc = STARTING_SOC
    rows = []

    for number, (initial, final, deceleration) in enumerate(BRAKING_EVENTS, 1):
        energy = recovered_energy_kwh(
            MASS, initial, final, EFFICIENCY
        )
        distance = braking_distance_m(
            initial, final, deceleration
        )
        soc += energy / BATTERY_CAPACITY * 100

        rows.append([
            number,
            initial,
            final,
            deceleration,
            energy,
            distance,
            soc
        ])

    save_csv(
        "baseline_five_braking_events.csv",
        [
            "event",
            "initial_speed_kmh",
            "final_speed_kmh",
            "deceleration_m_s2",
            "recovered_energy_kwh",
            "braking_distance_m",
            "soc_percent"
        ],
        rows
    )

    events = [r[0] for r in rows]
    energy = [r[4] for r in rows]
    soc_values = [r[6] for r in rows]

    # Figure 6
    plt.figure(figsize=(7, 4.5))
    plt.bar(events, energy)
    plt.xlabel("Braking event")
    plt.ylabel("Recovered energy (kWh)")
    plt.title("Recovered Energy per Braking Event")
    plt.grid(axis="y")
    save_plot("figure_6_energy_per_event.png")

    # Figure 7
    plt.figure(figsize=(7, 4.5))
    plt.plot(events, soc_values, marker="o")
    plt.xlabel("Braking event")
    plt.ylabel("Battery SOC (%)")
    plt.title("Battery SOC During the Five Braking Events")
    plt.grid(True)
    save_plot("figure_7_soc.png")


# ---------------------------------------------------------
# EXPERIMENTS
# ---------------------------------------------------------
def run_experiments():

    # Experiment 1: Initial speed sensitivity
    speeds = [40, 50, 60, 70, 80, 90, 100]
    speed_rows = [
        [v, recovered_energy_kwh(1800, v, 0, 0.80)]
        for v in speeds
    ]

    save_csv(
        "experiment_1_speed.csv",
        ["initial_speed_kmh", "recovered_energy_kwh"],
        speed_rows
    )

    plt.figure(figsize=(7, 4.5))
    plt.plot(
        [r[0] for r in speed_rows],
        [r[1] for r in speed_rows],
        marker="o"
    )
    plt.xlabel("Initial speed (km/h)")
    plt.ylabel("Recovered energy (kWh)")
    plt.title("Experiment 1: Initial Speed vs Recovered Energy")
    plt.grid(True)
    save_plot("figure_1_speed_vs_energy.png")

    # Experiment 2: Vehicle mass sensitivity
    masses = [1000, 1200, 1500, 1800, 2100, 2400, 2700]
    mass_rows = [
        [m, recovered_energy_kwh(m, 80, 40, 0.80)]
        for m in masses
    ]

    save_csv(
        "experiment_2_mass.csv",
        ["mass_kg", "recovered_energy_kwh"],
        mass_rows
    )

    plt.figure(figsize=(7, 4.5))
    plt.scatter(
        [r[0] for r in mass_rows],
        [r[1] for r in mass_rows]
    )
    plt.xlabel("Vehicle mass (kg)")
    plt.ylabel("Recovered energy (kWh)")
    plt.title("Experiment 2: Vehicle Mass vs Recovered Energy")
    plt.grid(True)
    save_plot("figure_2_mass_vs_energy.png")

    # Experiment 3: Regenerative efficiency sensitivity
    efficiencies = [40, 50, 60, 70, 80, 90, 100]
    efficiency_rows = [
        [e, recovered_energy_kwh(1800, 80, 40, e / 100)]
        for e in efficiencies
    ]

    save_csv(
        "experiment_3_efficiency.csv",
        ["efficiency_percent", "recovered_energy_kwh"],
        efficiency_rows
    )

    plt.figure(figsize=(7, 4.5))
    plt.plot(
        [r[0] for r in efficiency_rows],
        [r[1] for r in efficiency_rows],
        marker="o"
    )
    plt.xlabel("Regenerative efficiency (%)")
    plt.ylabel("Recovered energy (kWh)")
    plt.title("Experiment 3: Efficiency vs Recovered Energy")
    plt.grid(True)
    save_plot("figure_3_efficiency_vs_energy.png")

    # Experiment 4: Battery capacity sensitivity
    baseline_total = sum(
        recovered_energy_kwh(
            MASS, initial, final, EFFICIENCY
        )
        for initial, final, _ in BRAKING_EVENTS
    )

    capacities = [40, 50, 60, 75, 100]
    capacity_rows = [
        [c, baseline_total / c * 100]
        for c in capacities
    ]

    save_csv(
        "experiment_4_battery_capacity.csv",
        [
            "battery_capacity_kwh",
            "soc_increase_percentage_points"
        ],
        capacity_rows
    )

    plt.figure(figsize=(7, 4.5))
    plt.plot(
        [r[0] for r in capacity_rows],
        [r[1] for r in capacity_rows],
        marker="o"
    )
    plt.xlabel("Battery capacity (kWh)")
    plt.ylabel("SOC increase (percentage points)")
    plt.title("Experiment 4: Battery Capacity vs SOC Increase")
    plt.grid(True)
    save_plot("figure_4_battery_capacity_vs_soc.png")

    # Experiment 5: Deceleration vs braking distance
    decelerations = [3, 4, 5, 6, 7, 8, 10]
    distance_rows = [
        [a, braking_distance_m(80, 0, a)]
        for a in decelerations
    ]

    save_csv(
        "experiment_5_deceleration_distance.csv",
        ["deceleration_m_s2", "braking_distance_m"],
        distance_rows
    )

    plt.figure(figsize=(7, 4.5))
    plt.plot(
        [r[0] for r in distance_rows],
        [r[1] for r in distance_rows],
        marker="o"
    )
    plt.xlabel("Deceleration (m/s²)")
    plt.ylabel("Braking distance (m)")
    plt.title("Experiment 5: Deceleration vs Braking Distance")
    plt.grid(True)
    save_plot("figure_5_deceleration_vs_distance.png")


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():
    print("Running Project 3 simulator...")
    run_baseline()
    run_experiments()
    print()
    print("Project 3 experiments completed successfully.")
    print(f"Data saved to: {OUTPUT_DATA}")
    print(f"Figures saved to: {OUTPUT_FIGURES}")


if __name__ == "__main__":
    main()
