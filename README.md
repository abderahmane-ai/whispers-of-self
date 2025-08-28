# 🌊 Whispers of Self

> **Emergent Cooperation and Collapse under Scarce Resources**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Mesa](https://img.shields.io/badge/Mesa-ABM%20Framework-green.svg)](https://mesa.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Platform-orange.svg)](https://github.com/your-username/whispers-of-self)

<div align="center">

![Whispers of Self Banner](https://via.placeholder.com/800x200/1a1a2e/ffffff?text=Whispers+of+Self)

*A cutting-edge agent-based modeling platform exploring the dynamics of cooperation, competition, and collapse in resource-constrained environments.*

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [🔬 Research](#-research) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Whispers of Self** is a sophisticated agent-based modeling (ABM) research platform that investigates how individual strategies, resource scarcity, and adaptive learning shape population-level outcomes in simulated environments. Our platform explores emergent cooperation, collapse dynamics, and oscillatory patterns under various constraints.

### 🌟 What Makes It Special

- **🧠 Multi-Strategy Agents**: Altruists, Pragmatists, and Egoists with distinct behavioral patterns
- **⚡ Adaptive Learning**: Rule-based, cultural, evolutionary, and reinforcement learning modes
- **🌍 Real-World Applications**: Fisheries management, urban commons, bandwidth allocation
- **📈 Comprehensive Analytics**: Extinction probability, inequality metrics, sustainability analysis

---

## ✨ Features

### 🎮 Core Simulation Engine
- **Agent-Based Model**: Sophisticated population simulation with distinct personality types
- **Resource Dynamics**: Regenerating main pools + intermittent high-value resources
- **Environmental Shocks**: Stochastic events testing system resilience
- **Network Topologies**: Flexible pairing mechanisms for resource negotiation

### 🧬 Adaptation Mechanisms
- **Rule-Based**: Baseline deterministic strategies
- **Cultural Learning**: Social transmission of successful behaviors
- **Evolutionary Selection**: Natural selection pressure on strategies
- **Reinforcement Learning**: PPO/DQN for adaptive agent behavior

### 📊 Analysis & Visualization
- **Parameter Sweeps**: Systematic exploration of parameter spaces
- **Real-time Metrics**: Population dynamics, resource levels, cooperation rates
- **Static Plots**: Matplotlib/Seaborn for publication-ready figures
- **Interactive Dashboards**: Streamlit/Dash for exploratory analysis *(planned)*

### 🔬 Research Tools
- **Reproducibility**: YAML configurations, seed-based determinism
- **Docker Support**: Containerized environments for consistent results
- **Comprehensive Logging**: Detailed CSV outputs for post-analysis
- **Unit Testing**: Robust test suite for validation

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10 or higher
- **pip** (Python package manager)
- **Git** (for version control)
- **Docker** *(optional, for containerized runs)*

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/whispers-of-self.git
cd whispers-of-self

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest tests/
```

### 🎯 Your First Simulation

```bash
# Run a single simulation
python simulator/model.py --config configs/default.yaml --seed 42

# Execute parameter sweeps
python experiments/run_batch.py --config configs/default.yaml --sweeps configs/sweep.yaml

# Generate visualizations
python analysis/plots.py --log logs/run_seed42.csv
```

---

## �� Project Structure

```
whispers-of-self/
├── 🎛️  configs/                 # Configuration files
│   └── default.yaml            # Default simulation parameters
├── 🎮  simulator/              # Core ABM components
│   ├── model.py               # Main simulation model
│   ├── environment.py         # Resource pool management
│   ├── allocator.py           # Proportional resource allocation
│   └── big_resource.py        # Big resource negotiation
├── 🤖  agents/                # Agent definitions
│   ├── base.py                # Abstract base agent
│   └── rule_based.py          # Altruist, Pragmatist, Egoist agents
├── 🔗  pairing/               # Pairing mechanisms
│   ├── base.py                # Abstract pairing interface
│   └── random_pairing.py      # Random pairing for big resource
├── 📊  analysis/              # Metrics and visualization
│   ├── metrics.py             # Metric calculations
│   └── plots.py               # Static plots
├── 🧪  tests/                 # Unit tests
│   ├── test_allocator.py      # Allocation tests
│   ├── test_agents.py         # Agent behavior tests
│   └── test_big_resource.py   # Negotiation tests
├── 📋  requirements.txt       # Python dependencies
├── 🐳  Dockerfile             # Docker configuration
└── 📖  README.md              # This file
```

---

## 🔬 Research Applications

### 🎯 Key Research Questions

- **Cooperation Emergence**: How do cooperative strategies evolve under resource scarcity?
- **System Resilience**: What factors determine collapse vs. sustainability?
- **Inequality Dynamics**: How does resource distribution affect population stability?
- **Adaptation Speed**: Which learning mechanisms promote optimal outcomes?

### 🌍 Real-World Analogues

| Domain | Resource | Agents | Application |
|--------|----------|--------|-------------|
| **Fisheries** | Fish stocks | Fishing vessels | Sustainable harvesting |
| **Urban Commons** | Public spaces | Residents | Community management |
| **Bandwidth** | Network capacity | Users | Fair allocation |
| **Climate** | Carbon budget | Nations | Global cooperation |

---

## ⚙️ Configuration

### Basic Parameters

```yaml
# Resource Dynamics
R0: 100        # Initial main resource stock
g: 20          # Daily regeneration rate
s: 5           # Survival threshold
b: 10          # Reproduction threshold

# Population
N0: 3          # Initial population size
x_E: 0.33      # Egoist proportion

# Big Resource
Q_B: 50        # Big resource amount
N_th: 10       # Trigger threshold

# Cooperation
alpha: 0.05    # Cooperation bonus
beta: 0.10     # Defection penalty

# Environment
p_shock: 0.05  # Shock probability
mu: 0.05       # Mutation probability
```

### Parameter Sweeps

```yaml
# Example sweep configuration
x_E: [0, 0.25, 0.5, 0.75, 1.0]  # Egoist share
g: [10, 20, 40]                  # Regeneration rates
seeds: 50                        # Seeds per setting
```

---

## 📊 Example Output

### CLI Log Format

```
DAY,SEED,DAY_NUM,N,R,DMD,EXT,PHI,NA,NP,NE,BIRTHS,DEATHS,AGREES,SHOCK
run42,seed42,12,87,41.3,95.6,41.3,0.432,30,33,24,7,4,1,0
```

### Key Metrics

- **N**: Population size
- **R**: Resource level
- **DMD**: Demand
- **EXT**: Extinction probability
- **PHI**: Cooperation rate
- **NA/NP/NE**: Agent type counts

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_agents.py

# Run with coverage
pytest --cov=simulator tests/
```

---

## 🗺️ Development Roadmap

| Phase | Timeline | Focus |
|-------|----------|-------|
| **Phase 1** | Weeks 1-2 | Baseline ABM, rule-based agents, CLI logging |
| **Phase 2** | Weeks 3-4 | Environmental shocks, mutation, reputation systems |
| **Phase 3** | Weeks 5-6 | Cultural learning, evolutionary selection |
| **Phase 4** | Weeks 7-8 | Reinforcement learning (PPO/DQN) |
| **Phase 5** | Weeks 9-10 | Experiment consolidation, sensitivity analysis |

---

## 🤝 Contributing

We welcome contributions from researchers, developers, and enthusiasts!

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a pull request with detailed description

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting

---

## 📚 Documentation

- **[API Reference](docs/api.md)** - Detailed API documentation
- **[Tutorials](docs/tutorials.md)** - Step-by-step guides
- **[Research Papers](docs/papers.md)** - Academic publications
- **[Examples](docs/examples.md)** - Code examples and use cases

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Mesa Framework** for the ABM foundation
- **Computational Social Science** community for inspiration
- **Open Source Contributors** for their valuable input

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/your-username/whispers-of-self/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/whispers-of-self/discussions)
- **Email**: your-email@example.com
- **Twitter**: [@whispers_of_self](https://twitter.com/whispers_of_self)

---

<div align="center">

**Built with ❤️ using [Mesa](https://mesa.readthedocs.io/) and inspired by computational social science research**

[![GitHub stars](https://img.shields.io/github/stars/your-username/whispers-of-self?style=social)](https://github.com/your-username/whispers-of-self)
[![GitHub forks](https://img.shields.io/github/forks/your-username/whispers-of-self?style=social)](https://github.com/your-username/whispers-of-self)

</div>