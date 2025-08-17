"""
Flask Application for NeuroTwin DBS Simulator
Main API server for educational DBS simulation
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import traceback
import os

# Import our models
from models.brain_tissue import BrainTissue
from models.field_solver import ElectricFieldSolver
from models.electrode import DBSElectrode
from models.neuron_models import NeuronPopulationManager
from optimization.disease_models import DiseaseModelManager
from optimization.parameter_optimizer import DBSExplorer

# Create Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Global variables for models (initialized once for efficiency)
brain_tissue = None
dbs_electrode = None
dbs_explorer = None
disease_manager = None

def initialize_models():
    """Initialize the computational models."""
    global brain_tissue, dbs_electrode, dbs_explorer, disease_manager
    
    print("Initializing NeuroTwin models...")
    
    # Initialize brain tissue model
    brain_tissue = BrainTissue(grid_size=(30, 30, 30))  # Smaller for demo
    print("* Brain tissue model initialized")
    
    # Initialize DBS electrode at center of tissue
    center_position = tuple(np.array(brain_tissue.physical_size) / 2)
    dbs_electrode = DBSElectrode(position=center_position, electrode_type="quadripolar")
    dbs_electrode.set_stimulation_configuration('monopolar', [0], [2.0])
    print("* DBS electrode model initialized")
    
    # Initialize DBS explorer
    dbs_explorer = DBSExplorer(brain_tissue, dbs_electrode)
    print("* DBS parameter explorer initialized")
    
    # Initialize disease manager
    disease_manager = DiseaseModelManager()
    print("* Disease model manager initialized")
    
    print("NeuroTwin initialization complete!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'NeuroTwin API is running',
        'models_initialized': brain_tissue is not None
    })

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    """
    Run DBS simulation with given parameters.
    
    Expected JSON payload:
    {
        "frequency": 130,
        "amplitude": 2.0,
        "contact": 0,
        "condition": "parkinson",
        "pulse_width": 90
    }
    """
    try:
        # Get parameters from request
        params = request.json
        if not params:
            return jsonify({'error': 'No parameters provided'}), 400
        
        # Extract parameters with defaults
        frequency = float(params.get('frequency', 130.0))
        amplitude = float(params.get('amplitude', 2.0))
        contact = int(params.get('contact', 0))
        condition = params.get('condition', 'healthy')
        pulse_width = float(params.get('pulse_width', 90.0))
        
        # Validate parameters
        if not (1 <= frequency <= 250):
            return jsonify({'error': 'Frequency must be between 1-250 Hz'}), 400
        if not (0.1 <= amplitude <= 10.0):
            return jsonify({'error': 'Amplitude must be between 0.1-10.0 mA'}), 400
        if not (0 <= contact < len(dbs_electrode.contacts)):
            return jsonify({'error': f'Contact must be between 0-{len(dbs_electrode.contacts)-1}'}), 400
        
        # Configure electrode
        dbs_electrode.set_stimulation_configuration('monopolar', [contact], [amplitude])
        
        # Run simulation using DBS explorer
        simulation_params = {
            'frequency': frequency,
            'amplitude': amplitude,
            'contact': contact,
            'condition': condition,
            'pulse_width': pulse_width
        }
        
        effects = dbs_explorer.calculate_effects(simulation_params)
        
        # Get additional visualization data
        electrode_positions = [dbs_electrode.contacts[contact].position]
        potential = dbs_explorer.field_solver.solve_potential(electrode_positions, [amplitude])
        field_data = dbs_explorer.field_solver.get_visualization_data(potential)
        tissue_data = brain_tissue.get_visualization_data()
        electrode_data = dbs_electrode.get_electrode_geometry()
        
        # Generate pathological pattern for visualization
        time_array = np.arange(0, 1000.0, 1.0)  # 1s simulation with 1ms resolution
        disease_manager.set_condition(condition)
        pathological_pattern = disease_manager.generate_pathological_pattern(time_array)
        
        return jsonify({
            'success': True,
            'parameters': simulation_params,
            'effects': effects,
            'field_data': {
                'potential': field_data['potential'],
                'field_magnitude': field_data['field_magnitude'],
                'coordinates': {
                    'x': field_data['x_coords'],
                    'y': field_data['y_coords'],
                    'z': field_data['z_coords']
                }
            },
            'tissue_data': tissue_data,
            'electrode_data': electrode_data,
            'neural_activity': {
                'pathological_pattern': pathological_pattern,
                'time_array': time_array[::10].tolist()  # Downsample for transfer
            }
        })
        
    except Exception as e:
        print(f"Simulation error: {e}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Simulation failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/explore', methods=['POST'])
def explore_parameters():
    """
    Explore parameter space for educational insights.
    
    Expected JSON payload:
    {
        "condition": "parkinson",
        "parameter_ranges": {
            "frequency": [1, 250],
            "amplitude": [0.1, 10.0]
        },
        "exploration_type": "comprehensive"
    }
    """
    try:
        params = request.json
        condition = params.get('condition', 'parkinson')
        parameter_ranges = params.get('parameter_ranges', None)
        exploration_type = params.get('exploration_type', 'comprehensive')
        
        # Run parameter space exploration
        exploration_results = dbs_explorer.explore_parameter_space(
            condition=condition,
            parameter_ranges=parameter_ranges
        )
        
        return jsonify({
            'success': True,
            'condition': condition,
            'exploration_results': exploration_results,
            'insights': exploration_results.get('educational_insights', [])
        })
        
    except Exception as e:
        print(f"Exploration error: {e}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Parameter exploration failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_parameters():
    """
    Optimize DBS parameters for given condition and objective.
    
    Expected JSON payload:
    {
        "condition": "parkinson",
        "optimization_target": "therapeutic_window",
        "method": "differential_evolution"
    }
    """
    try:
        params = request.json
        condition = params.get('condition', 'parkinson')
        optimization_target = params.get('optimization_target', 'therapeutic_window')
        method = params.get('method', 'differential_evolution')
        
        # Run optimization
        optimization_results = dbs_explorer.optimize_parameters(
            condition=condition,
            optimization_target=optimization_target,
            method=method
        )
        
        return jsonify({
            'success': True,
            'condition': condition,
            'optimization_target': optimization_target,
            'results': optimization_results
        })
        
    except Exception as e:
        print(f"Optimization error: {e}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Parameter optimization failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/conditions', methods=['GET'])
def get_conditions():
    """Get available neurological conditions."""
    try:
        condition_info = disease_manager.get_condition_info()
        
        return jsonify({
            'success': True,
            'conditions': condition_info
        })
        
    except Exception as e:
        print(f"Conditions error: {e}")
        return jsonify({
            'error': f'Failed to get conditions: {str(e)}',
            'success': False
        }), 500

@app.route('/api/electrode-configs', methods=['GET'])
def get_electrode_configurations():
    """Get available electrode configurations."""
    try:
        # Get current electrode geometry
        electrode_data = dbs_electrode.get_electrode_geometry()
        
        # Define available configurations
        configurations = {
            'monopolar': {
                'description': 'Single active contact with case as ground',
                'pros': 'Simple, good for initial programming',
                'cons': 'Less selective, may cause side effects'
            },
            'bipolar': {
                'description': 'Two adjacent contacts with opposite polarity',
                'pros': 'More selective stimulation',
                'cons': 'Higher amplitude may be needed'
            },
            'multipolar': {
                'description': 'Multiple contacts with different current ratios',
                'pros': 'Highly customizable field shaping',
                'cons': 'Complex programming, higher power consumption'
            }
        }
        
        return jsonify({
            'success': True,
            'current_electrode': electrode_data,
            'available_configurations': configurations,
            'contact_count': len(dbs_electrode.contacts)
        })
        
    except Exception as e:
        print(f"Electrode config error: {e}")
        return jsonify({
            'error': f'Failed to get electrode configurations: {str(e)}',
            'success': False
        }), 500

@app.route('/api/educational-content', methods=['GET'])
def get_educational_content():
    """Get educational content about DBS mechanisms."""
    try:
        content = {
            'dbs_basics': {
                'title': 'Deep Brain Stimulation Basics',
                'content': [
                    'DBS uses electrical impulses to modulate abnormal brain activity',
                    'High-frequency stimulation (>100 Hz) typically blocks pathological signals',
                    'The exact mechanism involves complex interactions with neurons and circuits',
                    'Parameter selection is crucial for balancing efficacy and side effects'
                ]
            },
            'frequency_effects': {
                'title': 'Frequency Parameter Effects',
                'content': [
                    'Low frequency (1-50 Hz): May cause muscle contractions, worsen symptoms',
                    'Medium frequency (50-100 Hz): Partial therapeutic effects',
                    'High frequency (100-180 Hz): Optimal therapeutic range for most conditions',
                    'Very high frequency (>180 Hz): Risk of speech/cognitive side effects'
                ]
            },
            'amplitude_effects': {
                'title': 'Amplitude Parameter Effects',
                'content': [
                    'Low amplitude: Minimal side effects but limited therapeutic benefit',
                    'Medium amplitude: Good balance of efficacy and side effects',
                    'High amplitude: Strong therapeutic effect but increased side effect risk',
                    'Amplitude determines the volume of tissue activated (VTA)'
                ]
            },
            'conditions': {
                'title': 'Neurological Conditions',
                'parkinson': [
                    'Characterized by beta oscillations (13-30 Hz) in motor circuits',
                    'DBS disrupts pathological synchronization',
                    'Typical parameters: 130-180 Hz, 1-4 mA'
                ],
                'dystonia': [
                    'Irregular muscle contractions and abnormal postures',
                    'Lower frequencies often effective (60-120 Hz)',
                    'May require bilateral stimulation'
                ],
                'tremor': [
                    'Rhythmic oscillatory movements (4-12 Hz)',
                    'DBS blocks tremor circuits in VIM nucleus',
                    'Responds well to moderate frequencies'
                ]
            }
        }
        
        return jsonify({
            'success': True,
            'educational_content': content
        })
        
    except Exception as e:
        print(f"Educational content error: {e}")
        return jsonify({
            'error': f'Failed to get educational content: {str(e)}',
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        # Initialize models on startup
        initialize_models()
        
        # Run Flask app
        print("Starting NeuroTwin API server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"Failed to start NeuroTwin API: {e}")
        print(traceback.format_exc())
