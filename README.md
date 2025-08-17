# NeuroTwin - Interactive Deep Brain Stimulation Simulator

<div align="center">

🧠 **Advanced Educational Tool for Understanding DBS Mechanisms** ⚡

![NeuroTwin](https://img.shields.io/badge/NeuroTwin-Educational%20DBS%20Simulator-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/React-18.2%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)
![License](https://img.shields.io/badge/License-Educational%20Use-orange)

</div>

## 🌟 Overview

NeuroTwin is a comprehensive, interactive educational simulator that demonstrates Deep Brain Stimulation (DBS) principles through computational neuroscience. Users can explore how different stimulation parameters affect brain tissue and neural activity in a simplified but scientifically-grounded virtual brain model.

**🎯 Purpose**: Educational research tool for understanding DBS mechanisms  
**⚠️ Important**: Not intended for clinical use - educational simulation only

## ✨ Key Features

### 🧠 Advanced Brain Modeling
- **3D Tissue Simulation**: Realistic brain tissue with gray matter, white matter, and CSF
- **Electrical Properties**: Accurate conductivity distributions and heterogeneity
- **Biophysical Accuracy**: Based on established neuroscience principles

### ⚡ Electric Field Simulation
- **Poisson Equation Solver**: Finite difference method for electric field propagation
- **Field Visualization**: Real-time 3D visualization of stimulation spread
- **Tissue Interaction**: Models how electric fields interact with different tissues

### 🔬 Neuron Response Modeling
- **Hodgkin-Huxley Models**: Detailed single neuron dynamics
- **Population Simulations**: Large-scale neural network responses
- **Activity Patterns**: Realistic firing rate and synchronization modeling

### 🩺 Disease Simulations
- **Parkinson's Disease**: Beta oscillations and bradykinesia patterns
- **Dystonia**: Irregular muscle activation modeling
- **Essential Tremor**: Rhythmic oscillatory activity
- **Healthy Baseline**: Normal brain activity for comparison

### 🎛️ Interactive Parameter Control
- **Real-time Adjustment**: Frequency, amplitude, contact selection
- **Preset Configurations**: Clinical standard parameter sets
- **Advanced Settings**: Pulse width, stimulation modes

### 📊 Comprehensive Analysis
- **Therapeutic Metrics**: Symptom improvement, side effect scoring
- **Field Analysis**: Volume of tissue activated, penetration depth
- **Efficiency Metrics**: Power consumption, selectivity scoring
- **Educational Insights**: Personalized recommendations and explanations

### 🔍 Parameter Exploration
- **Systematic Exploration**: Automated parameter space mapping
- **Optimization Algorithms**: Automatic parameter tuning
- **Visualization Tools**: 2D parameter maps and effect relationships

### 🎓 Educational Features
- **Interactive Tutorial**: Step-by-step guided learning
- **Real-time Feedback**: Immediate parameter effect visualization
- **Scientific Explanations**: In-depth mechanism descriptions
- **Comparative Analysis**: Side-by-side parameter comparison

## 🏗️ Technical Architecture

### Backend (Python Flask)
```
backend/
├── app.py                          # Main Flask application
├── models/
│   ├── brain_tissue.py            # 3D tissue conductivity modeling
│   ├── field_solver.py            # Electric field Poisson solver
│   ├── electrode.py               # DBS electrode geometry
│   └── neuron_models.py           # HH & integrate-fire models
├── optimization/
│   ├── disease_models.py          # Pathological pattern simulation
│   └── parameter_optimizer.py     # Parameter space exploration
└── requirements.txt               # Python dependencies
```

### Frontend (React.js)
```
frontend/
├── src/
│   ├── components/
│   │   ├── BrainVisualization.jsx    # 3D Plotly visualization
│   │   ├── ParameterControls.jsx     # Interactive parameter UI
│   │   ├── ResultsDisplay.jsx        # Metrics and analysis
│   │   ├── ExplorationPanel.jsx      # Parameter exploration
│   │   └── TutorialMode.jsx          # Educational tutorial
│   ├── utils/
│   │   └── apiClient.js              # Backend communication
│   └── App.jsx                       # Main application
└── package.json                      # Node.js dependencies
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control

### Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd neurotwin
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
*Backend will start on http://localhost:5000*

3. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```
*Frontend will start on http://localhost:3000*

4. **Open NeuroTwin**
Navigate to `http://localhost:3000` in your web browser

## 📖 Detailed Setup Instructions

### Backend Configuration

#### Python Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv neurotwin-env

# Activate virtual environment
# Windows:
neurotwin-env\Scripts\activate
# macOS/Linux:
source neurotwin-env/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

#### Key Dependencies
- **Flask 2.3.2**: Web framework for API endpoints
- **NumPy 1.24.3**: Numerical computations and arrays
- **SciPy 1.10.1**: Scientific computing and optimization
- **Matplotlib 3.7.1**: Plotting and visualization
- **Flask-CORS**: Cross-origin resource sharing

#### Environment Variables (Optional)
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Frontend Configuration

#### Node.js Setup
```bash
cd frontend
npm install
```

#### Key Dependencies
- **React 18.2.0**: UI framework
- **Plotly.js**: 3D visualization library
- **Axios**: HTTP client for API communication
- **React Scripts**: Build tooling

#### Development Mode
```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
```

## 🎮 Usage Guide

### Getting Started
1. **Launch Tutorial**: Click "📚 Tutorial Mode" for guided introduction
2. **Select Condition**: Choose brain condition (Healthy, Parkinson's, etc.)
3. **Adjust Parameters**: Use sliders to modify frequency, amplitude, contacts
4. **Run Simulation**: Click "🧠 Run Simulation" to see results
5. **Analyze Results**: Review metrics in the Results panel

### Parameter Guidelines

#### Frequency (Hz)
- **1-50 Hz**: ❌ May worsen symptoms, cause muscle effects
- **50-100 Hz**: ⚠️ Partial therapeutic effects
- **100-180 Hz**: ✅ Optimal therapeutic range
- **180+ Hz**: ⚠️ Risk of speech/cognitive side effects

#### Amplitude (mA)
- **0.1-1.5 mA**: Minimal effects, good for testing
- **1.5-4.0 mA**: Therapeutic range for most patients
- **4.0-10.0 mA**: High intensity, increased side effect risk

#### Contact Selection
- **Contact 0**: Deepest, targets deep brain structures
- **Contact 1-2**: Mid-level targeting
- **Contact 3**: Shallowest, closer to cortex

### Advanced Features

#### Parameter Exploration
1. Navigate to the Exploration Panel (left side)
2. Select exploration mode (Comprehensive, Frequency Sweep, etc.)
3. Click "🗺️ Explore Parameters"
4. Review optimal regions and insights

#### Automatic Optimization
1. Choose optimization target (Therapeutic Window, Efficiency, etc.)
2. Click "⚡ Optimize Parameters"
3. Review optimal parameters and sensitivity analysis

#### 3D Visualization Controls
- **View Mode**: Switch between field, tissue, or combined views
- **Field Threshold**: Adjust sensitivity of field visualization
- **Electrode Display**: Toggle electrode contact visibility
- **Interactive Rotation**: Click and drag to rotate 3D view

## 📊 Understanding Results

### Therapeutic Metrics
- **Symptom Improvement (%)**: Primary therapeutic outcome measure
- **Side Effect Score**: Risk assessment (0-1, lower is better)
- **Therapeutic Window**: Benefit-to-side-effect ratio

### Field Metrics
- **VTA Volume (mm³)**: Volume of Tissue Activated
- **Max Field Strength (V/m)**: Peak electric field intensity
- **Penetration Depth (mm)**: How deep stimulation reaches

### Neural Metrics
- **Firing Rate Change (Hz)**: Modification of neural activity
- **Synchrony Index**: Population coordination measure
- **Population Coherence**: Network-level synchronization

### Efficiency Metrics
- **Power Consumption (mW)**: Battery life estimation
- **Selectivity Score**: Spatial targeting precision
- **Efficiency Ratio**: Benefit per unit power

## 🔬 Scientific Background

### Computational Models

#### Brain Tissue Model
- **Finite Element Method**: 3D grid-based tissue representation
- **Conductivity Values**: Literature-based tissue properties
  - Gray Matter: 0.33 S/m
  - White Matter: 0.14 S/m
  - CSF: 1.79 S/m
- **Heterogeneity**: ±10% random variations for realism

#### Electric Field Solver
- **Poisson Equation**: ∇·(σ∇V) = I
- **Finite Difference**: Second-order accurate discretization
- **Sparse Linear Algebra**: Efficient scipy.sparse.linalg solver
- **Boundary Conditions**: Neumann/Dirichlet options

#### Neuron Models
- **Hodgkin-Huxley**: Detailed membrane dynamics
  - Sodium, potassium, and leak currents
  - Voltage-gated channel kinetics
  - Realistic action potential generation
- **Leaky Integrate-and-Fire**: Population-level efficiency
  - Membrane time constants
  - Spike threshold mechanisms
  - Population statistics

#### Disease Models
- **Parkinson's Disease**: 
  - Beta oscillations (13-30 Hz)
  - Reduced baseline activity (40% reduction)
  - Tremor components (4-6 Hz)
- **Dystonia**: 
  - Irregular bursting patterns
  - Low-frequency oscillations (3-12 Hz)
  - Muscle cocontraction modeling
- **Essential Tremor**: 
  - Rhythmic oscillations (6-12 Hz)
  - Harmonic components
  - Frequency variability

### Validation & Limitations

#### Model Validation
- Based on established neuroscience literature
- Parameter ranges from clinical studies
- Simplified but scientifically grounded

#### Known Limitations
- Simplified brain geometry (not patient-specific)
- Reduced complexity for educational purposes
- No individual variability modeling
- Limited to educational scenarios

## 🎓 Educational Applications

### Learning Objectives
1. **DBS Mechanism Understanding**: How electrical stimulation modulates neural activity
2. **Parameter Relationships**: Effects of frequency, amplitude, and spatial targeting
3. **Clinical Decision Making**: Balancing therapeutic benefit with side effects
4. **Optimization Principles**: Systematic parameter exploration strategies

### Recommended Exercises

#### Exercise 1: Parameter Effects
1. Start with standard parameters (130 Hz, 2 mA, Contact 1)
2. Vary frequency: 50 Hz → 130 Hz → 180 Hz
3. Observe changes in therapeutic metrics
4. **Learning Goal**: Understand frequency-response relationships

#### Exercise 2: Condition Comparison
1. Run identical parameters on different conditions
2. Compare healthy vs. Parkinson's vs. tremor
3. Note differences in optimal parameters
4. **Learning Goal**: Condition-specific parameter requirements

#### Exercise 3: Optimization Strategy
1. Use parameter exploration to map effect landscape
2. Identify optimal regions
3. Compare manual vs. automatic optimization
4. **Learning Goal**: Systematic optimization approaches

#### Exercise 4: Trade-off Analysis
1. Find parameters with high therapeutic benefit
2. Find parameters with low side effects
3. Use therapeutic window to balance both
4. **Learning Goal**: Clinical decision-making process

### Assessment Questions
1. Why is high-frequency stimulation (>100 Hz) typically more effective?
2. How does amplitude affect the volume of tissue activated?
3. What factors determine optimal contact selection?
4. How do different neurological conditions respond to DBS?

## 🛠️ Development & Customization

### Adding New Disease Models
1. Create new class in `disease_models.py`
2. Implement `generate_pathological_activity()` method
3. Add to `DiseaseModelManager.available_conditions`
4. Update frontend condition selector

### Modifying Brain Geometry
1. Adjust `grid_size` in `BrainTissue.__init__()`
2. Modify `_generate_tissue_structure()` for new anatomical regions
3. Update visualization coordinates in frontend

### Custom Optimization Objectives
1. Add new objective function in `parameter_optimizer.py`
2. Implement calculation logic in `calculate_effects()`
3. Update frontend optimization target selector

### Advanced Visualizations
1. Add new trace types in `BrainVisualization.jsx`
2. Implement custom Plotly configurations
3. Create new visualization modes

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Follow coding standards and add tests
4. Submit pull request with detailed description

### Code Standards
- **Python**: PEP 8 style guide, type hints preferred
- **JavaScript**: ESLint configuration, functional components
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Unit tests for computational functions

### Issue Reporting
- Use GitHub Issues for bug reports and feature requests
- Include system information and reproduction steps
- Tag issues appropriately (bug, enhancement, documentation)

## 📄 License & Citation

### License
This project is released under an Educational Use License. See LICENSE file for details.

### Citation
If you use NeuroTwin in educational or research contexts, please cite:
```
NeuroTwin: Interactive Deep Brain Stimulation Simulator
[Year] - Educational computational neuroscience tool
Repository: [URL]
```

### Acknowledgments
- Computational models based on established neuroscience literature
- DBS parameter ranges from clinical research studies
- Educational framework inspired by neuroscience pedagogy best practices

## 🆘 Troubleshooting

### Common Issues

#### Backend Connection Errors
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Restart backend
cd backend
python app.py
```

#### Frontend Build Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

#### Visualization Not Loading
1. Ensure Plotly.js is properly installed
2. Check browser console for JavaScript errors
3. Verify simulation data format in API response

#### Slow Simulation Performance
1. Reduce brain tissue grid size in `brain_tissue.py`
2. Decrease simulation time in parameters
3. Use smaller neuron population sizes

### Performance Optimization

#### Backend Optimization
- Use smaller grid sizes for real-time interaction
- Implement result caching for repeated simulations
- Consider parallel processing for parameter exploration

#### Frontend Optimization
- Implement data downsampling for large datasets
- Use React.memo for expensive components
- Optimize Plotly rendering with reduced data points

### Getting Help
1. Check this README for common solutions
2. Review GitHub Issues for similar problems
3. Create new issue with detailed error information
4. Include system specs and reproduction steps

## 🔮 Future Enhancements

### Planned Features
- **Patient-Specific Modeling**: Custom brain geometries
- **Advanced Electrode Models**: Directional leads, new geometries
- **Network Analysis**: Connectivity-based stimulation effects
- **Machine Learning**: Automated parameter prediction
- **Clinical Data Integration**: Real-world outcome validation

### Research Opportunities
- **Closed-Loop DBS**: Adaptive stimulation algorithms
- **Multi-Target Stimulation**: Simultaneous multiple region targeting
- **Biomarker Integration**: EEG/LFP signal incorporation
- **Computational Efficiency**: GPU acceleration, cloud computing
- **Educational Assessment**: Learning outcome measurement tools

---

<div align="center">

**🧠 NeuroTwin - Advancing DBS Education Through Interactive Simulation ⚡**

*Computational Neuroscience • Educational Technology • Interactive Learning*

</div>
