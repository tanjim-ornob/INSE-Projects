\# CSTR Cyber-Physical Attack Detection using MATLAB/Simulink



This project explores anomaly detection for a networked cyber-physical control system based on a Continuous-Stirred Tank Reactor (CSTR) model. The system uses a Kalman filter for state estimation and an LQI controller for reference tracking. Multiple attack scenarios are simulated to evaluate how a chi-squared anomaly detector performs under normal operation, false data injection, replay attacks, and active watermarking-based detection.



This project was completed as part of the \*\*INSE 6710: Fundamentals and Applications of Cyber-Physical Systems\*\* coursework.



\## Project Overview



The objective of this project is to study how cyber-physical systems respond to sensor and actuator attacks, and how anomaly detection techniques can be used to detect abnormal behavior.



The project is divided into four main parts:



\### Part 1 — Chi-Squared Anomaly Detector



A chi-squared anomaly detector is designed for the CSTR system under normal, no-attack conditions. The detector threshold is selected to target a 3% false alarm rate. The system is evaluated over 50 simulation trials.



\### Part 2 — False Data Injection Attack on Sensor Measurements



A false data injection attack is introduced into the measurement channel. The previously designed chi-squared detector is evaluated using detection rate, false alarm rate, F1 score, and tracking error.



\### Part 3 — Replay Attacks



Two replay attack scenarios are implemented against both the sensor measurements and control inputs. The detector is tested against both replay cases to compare how attack timing and attack structure affect detectability.



\### Part 4 — Active Watermarking-Based Detection



An active watermarking signal is injected into the control input to improve detection against stealthy replay attacks. The watermarking design is evaluated under the constraint that the tracking error should not increase by more than 15% compared to the no-watermark baseline.



\## Tools and Technologies



\- MATLAB

\- Simulink

\- State-space control modeling

\- Kalman filtering

\- LQI control

\- Chi-squared anomaly detection

\- False data injection attack simulation

\- Replay attack simulation

\- Active watermarking



\## Key Results



| Experiment | Detection Rate | False Alarm Rate | F1 Score | Tracking Error |

|---|---:|---:|---:|---:|

| Part 1: No Attack | N/A | 3.74% | N/A | 2.6997 |

| Part 2: Sensor FDI Attack | 100.00% | 17.95% | 78.96% | 4.1469 |

| Part 3: Replay Attack Equation 1.2 | 4.05% | 1.87% | 7.16% | 2.7000 |

| Part 3: Replay Attack Equation 1.3 | 69.17% | 1.75% | 77.11% | 22.1691 |

| Part 4: Active Watermarking | 50.93% | 4.48% | 57.49% | 3.6153 |



\## Main Observations



The chi-squared detector performed well under the false data injection attack in Part 2, achieving a 100% detection rate. However, the coordinated replay attack in Part 3 Equation 1.2 was much harder to detect, with a detection rate of only 4.05%. This shows the limitation of passive anomaly detection when an attacker can manipulate both sensor and actuator channels in a stealthy way.



The second replay attack case, Equation 1.3, was more detectable because it caused stronger residual divergence and a larger tracking error. Active watermarking improved the detectability of the stealthier replay attack while keeping the tracking error within the required performance constraint.



\## Repository Structure



```text

INSE-6710-CSTR-Attack-Detection/

│

├── README.md

├── .gitignore

│

├── docs/

│   └── CSTR-Attack-Detection-Report.pdf

│

├── results/

│   └── plots/

│       └── .gitkeep

│

└── src/

&#x20;   ├── part1/

&#x20;   │   ├── main.m

&#x20;   │   ├── Main\_Part1.m

&#x20;   │   └── NetworkedControlSystemBasic.slx

&#x20;   │

&#x20;   ├── part2/

&#x20;   │   ├── Main\_Part2.m

&#x20;   │   └── NetworkedControlSystemBasic\_Part2.slx

&#x20;   │

&#x20;   ├── part3/

&#x20;   │   ├── Main\_Part3.m

&#x20;   │   └── NetworkedControlSystemBasic\_Part3.slx

&#x20;   │

&#x20;   └── part4/

&#x20;       ├── Main\_Part4.m

&#x20;       └── NetworkedControlSystemBasic\_Part4.slx

```



\## Reproducibility and Running the Simulations



The simulations were originally developed and executed in MATLAB/Simulink as part of the course assignment. The repository includes the MATLAB scripts and Simulink model files required to reproduce the experiments.



To fully rerun the simulations, \*\*MATLAB with Simulink is required\*\*.



\### Option 1: Run with MATLAB/Simulink



1\. Open MATLAB.

2\. Navigate to the desired part folder inside `src/`.

3\. Run the corresponding MATLAB script.

4\. Open the associated Simulink model.

5\. Run the simulation and compare the generated outputs with the report.



Example for Part 1:



```matlab

cd src/part1

run main.m

run Main\_Part1.m

open\_system('NetworkedControlSystemBasic.slx')

```



Example for Part 2:



```matlab

cd src/part2

run Main\_Part2.m

open\_system('NetworkedControlSystemBasic\_Part2.slx')

```



Example for Part 3:



```matlab

cd src/part3

run Main\_Part3.m

open\_system('NetworkedControlSystemBasic\_Part3.slx')

```



Example for Part 4:



```matlab

cd src/part4

run Main\_Part4.m

open\_system('NetworkedControlSystemBasic\_Part4.slx')

```



\### Option 2: Review Without MATLAB



If MATLAB/Simulink is not available, the project can still be reviewed through:



\- The MATLAB source scripts in `src/`

\- The Simulink model files in `src/`

\- The final report in `docs/`, which includes the detector design, attack scenarios, result tables, plots, and analysis



The report serves as the archived record of the completed simulations and results.



\## Report



The full project report is available in:



```text

docs/CSTR-Attack-Detection-Report.pdf

```



The report includes:



\- CSTR system overview

\- Chi-squared detector design

\- Detector threshold and residual covariance

\- Attack implementation details

\- Simulation results over 50 trials

\- Output, control input, state-estimation, and detector plots

\- Comparison between replay attack scenarios

\- Active watermarking design and performance analysis



\## Notes on Generated Files



Generated MATLAB/Simulink cache and build files are intentionally excluded from this repository using `.gitignore`. These include files such as:



```text

slprj/

\*.slxc

\*.mexw64

\*.slx.r20\*

```



Only the source MATLAB scripts, Simulink models, report, and documentation are kept in the repository.



\## Academic Integrity Notice



This repository is shared for portfolio and educational demonstration purposes only. The project was completed as university coursework. Do not copy, submit, or reuse this work as your own academic submission.



\## Disclaimer



This project is based on a controlled academic simulation environment. The attack scenarios are implemented only for studying cyber-physical system security and anomaly detection in MATLAB/Simulink.



The project does not provide guidance for attacking real industrial systems. It is intended only for educational study of cyber-physical system resilience and detection techniques.

