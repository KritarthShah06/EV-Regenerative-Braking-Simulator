# EV Regenerative Braking Energy Recovery Simulator


Python-based physics simulation of regenerative braking in an electric vehicle. The project studies how vehicle speed, vehicle mass, regenerative efficiency, battery capacity and braking conditions affect calculated energy recovery.

The project is a simplified computational model. It is not a physical test of a production EV.

## Baseline model

- Vehicle mass: 1800 kg
- Battery capacity: 60 kWh
- Regenerative efficiency: 80%
- Starting SOC: 40%
- Five braking events

The baseline simulation gives approximately **0.3241 kWh** of total recovered energy and a final SOC of **40.5401%**.

## Main equations

Kinetic energy:

`E = 1/2 m v²`

Braking energy:

`E_braking = 1/2 m (v_i² - v_f²)`

Recovered energy:

`E_recovered = η E_braking`

Braking distance:

`d = (v_i² - v_f²) / (2a)`

SOC increase:

`ΔSOC = recovered energy / battery capacity × 100`

## Experiments

1. Initial speed vs recovered energy
2. Vehicle mass vs recovered energy
3. Regenerative efficiency vs recovered energy
4. Battery capacity vs SOC increase
5. Deceleration vs braking distance
6. Five-event baseline simulation, including cumulative SOC

## Repository structure

```text
EV_Regenerative_Braking_Project3/
├── README.md
├── paper.md
├── simulator.py
├── requirements.txt
├── data/
│   ├── baseline_five_braking_events.csv
│   ├── experiment_1_speed.csv
│   ├── experiment_2_mass.csv
│   ├── experiment_3_efficiency.csv
│   ├── experiment_4_battery_capacity.csv
│   └── experiment_5_deceleration_distance.csv
└── figures/
    ├── figure_1_speed_vs_energy.png
    ├── figure_2_mass_vs_energy.png
    ├── figure_3_efficiency_vs_energy.png
    ├── figure_4_battery_capacity_vs_soc.png
    ├── figure_5_deceleration_vs_distance.png
    ├── figure_6_energy_per_event.png
    └── figure_7_soc.png
```


## Limitations

The model does not fully represent motor/inverter efficiency, battery temperature, charging-power limits, SOC-dependent charging limits, tire traction, motor torque curves or battery degradation.

## Scope

The repository contains only the computational work and experiments used for this project. The results should be interpreted as outputs of the simplified model.

