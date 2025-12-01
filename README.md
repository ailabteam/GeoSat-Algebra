# GeoSat-Algebra: Geometric and Conformal Algebra for Satellite Geometry and Pose Control

## 🚀 Overview

This repository establishes a robust, highly modular foundation for applying **Geometric Algebra (GA)** and its extension, **Conformal Geometric Algebra (CGA)**, to solve complex geometry and transformation problems in aerospace and satellite systems.

GA/CGA provides a mathematically unified framework where all geometric objects (points, lines, spheres) and transformations (rotation, translation) are represented consistently as **Multivectors**. This approach offers significant advantages over traditional methods (matrices, quaternions, Euler angles), notably eliminating singularities and streamlining complex geometric calculations crucial for autonomous satellite operations.

This project is structured as a series of executable Python scripts designed for demonstration and direct integration into larger simulation or optimization frameworks.

## 💡 Why GA/CGA for Satellites?

| Feature | Traditional Methods (Matrices/Quaternions) | Geometric Algebra (GA/CGA) |
| :--- | :--- | :--- |
| **Unified Representation** | Requires separate data structures for vectors, quaternions, points, lines, etc. | **All objects are Multivectors.** Geometry is intrinsic to the algebra. |
| **Rotation (GA)** | Requires Quaternions (complex multiplication) or 3x3 Matrices; prone to Gimbal Lock (Euler). | Uses **Rotors** (versors), which are singularity-free and easily invertible ($R^{-1} = \tilde{R}$). |
| **Translation (CGA)** | Requires Vector Addition (outside of the rotation structure). | Uses **Translators** (Motors), integrating translation and rotation into a single algebraic product. |
| **Geometric Operations** | Intersection/Distance requires complex projection formulas and case handling. | Uses **Meet ($\wedge$) and Join ($\vee$)** products for immediate geometric intersection testing. |

## 📐 Implementation Focus: G(3) and G(4,1)

### 1. Euclidean GA (G(3))

*   **Basis:** $e_1, e_2, e_3$ (3D space).
*   **Demo:** `src/demo_ga_3d_rotation.py` (Compares Rotor operation against traditional Matrix rotation).

### 2. Conformal GA (G(4,1))

*   **Basis:** $e_1, e_2, e_3, e_+, e_-$ (5D space).
*   **Null Basis:** $n_o$ (Origin) and $n_\infty$ (Infinity).
*   **Object Representation:** Points, lines, and spheres are created as multivectors in this space.

---

## 🛠️ Project Structure and Setup

The repository is designed to be executed directly via Python scripts, saving visualization output to the `5_Results_Analysis/` folder.

### Prerequisites

We recommend using a dedicated Conda environment to manage dependencies, especially the `clifford` library.

```bash
# Example setup command (See environment.yml for full dependencies)
conda create -n geo_sat_env python=3.12
conda activate geo_sat_env
pip install -r requirements.txt 

# Crucial step for module importing on servers
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Repository Contents

| Directory/File | Description | Status |
| :--- | :--- | :--- |
| `src/` | **Core Logic:** Contains all Python modules for algebra definitions and demos. | Complete |
| `src/ga_utilities.py` | **Algebraic Core:** Defines the G(3) and G(4,1) algebras, Null Basis vectors ($n_o, n_\infty$), and fundamental functions (`create_rotor`, `point_to_cga`, `create_translator`). | Complete |
| `src/satellite_geometry.py` | *(Reserved for future complex object definitions)* | Empty |
| `5_Results_Analysis/`| Output directory for all generated plots (`.png`). | Ready |
| `requirements.txt` | Python library dependencies (NumPy, Matplotlib, Clifford, etc.). | Complete |

## 🏃 Running the Demonstrations

Execute the scripts sequentially to observe the mathematical principles in action.

### Demo 1: 3D Attitude Rotation (G(3))

Demonstrates the use of the **Rotor** for rotation, comparing its output directly to a traditional rotation matrix.

```bash
python src/demo_ga_3d_rotation.py
# Output: 5_Results_Analysis/rotation_comparison_g3.png
```

### Demo 2: Conformal Translation (CGA)

Illustrates how **Points** and **Translators** are created in the 5D CGA space, showing a satellite position update via a single algebraic sandwich product.

```bash
python src/demo_cga_primitives.py
# Output: 5_Results_Analysis/cga_translation_demo.png
```

### Demo 3: Satellite Collision Avoidance (CGA Application)

A practical example where **Spheres** (representing satellites and their safe zones) are defined in CGA. The script uses the geometric concepts of Meet ($\wedge$) and vector projection to determine the proximity and intersection status of two satellites.

```bash
python src/application_collision_avoidance.py
# Output: 5_Results_Analysis/cga_collision_sphere.png
```

---

## 🔮 Future Research Paths (The Bridge to AI and Quantum)

This foundational work is specifically designed to be the geometry backbone for advanced topics, offering high potential for subsequent research papers:

### 1. Integration with AI/ML (High-Impact Paper)

*   **Problem:** Traditional state representations (Euler angles, 9-component matrices) often lead to complexity and instability in Deep Learning/Reinforcement Learning (DRL) models controlling satellite pose (ADCS).
*   **CGA Solution:** Multivectors (specifically Rotors/Motors) provide a **minimal, closed, and singularity-free** representation of rigid body motion.
*   **Research Direction:** Use CGA Rotors/Motors directly as input features for DRL agents to achieve robust and faster convergence in dynamic attitude control tasks (e.g., using a DRL agent to learn optimal ADCS commands based on the CGA representation of the required attitude change).

### 2. Quantum Computation Acceleration (Long-Term Vision)

*   **Problem:** Simulating large constellations (thousands of LEO satellites) requires immense computational power for $N^2$ collision/proximity checks, which rely heavily on geometric products.
*   **CGA Advantage:** The core algebraic operations of CGA (Geometric Product, Meet, Join) are mathematically precise and structurally simpler than their matrix equivalents.
*   **Research Direction:** Explore mapping the Geometric Product onto **Quantum Circuits** (using tools like Qiskit or Pennylane) or using **Quantum Annealers** to potentially achieve quadratic or exponential speedup in the complex collision/proximity calculation stage for massive constellation simulations.

---

*License: MIT*
