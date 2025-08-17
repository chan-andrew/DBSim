"""
Parameter Optimization for DBS Simulation
Educational exploration of DBS parameter effects and optimization
"""

import numpy as np
from scipy.optimize import differential_evolution, minimize
from typing import Dict, List, Tuple, Optional, Callable
from models.brain_tissue import BrainTissue
from models.field_solver import ElectricFieldSolver
from models.electrode import DBSElectrode
from models.neuron_models import NeuronPopulationManager
from optimization.disease_models import DiseaseModelManager


class DBSExplorer:
    """
    Educational tool for exploring DBS parameter effects and optimization.
    Demonstrates how different stimulation parameters affect neural activity.
    """
    
    def __init__(self, brain_model: BrainTissue, electrode: DBSElectrode):
        """
        Initialize DBS explorer.
        
        Args:
            brain_model: Brain tissue model
            electrode: DBS electrode model
        """
        self.brain_model = brain_model
        self.electrode = electrode
        self.field_solver = ElectricFieldSolver(brain_model)
        self.neuron_manager = NeuronPopulationManager()
        self.disease_manager = DiseaseModelManager()
        
        # Parameter bounds for optimization
        self.parameter_bounds = {
            'frequency': (1, 250),      # Hz
            'amplitude': (0.1, 10.0),   # mA
            'contact': (0, len(electrode.contacts) - 1),  # Contact index
            'pulse_width': (30, 450)    # μs
        }
        
        # Simulation settings
        self.simulation_time = 1000.0  # ms
        self.exploration_resolution = 20  # Points per parameter dimension
        
    def calculate_effects(self, parameters: Dict) -> Dict:
        """
        Calculate neural effects of given DBS parameters.
        
        Args:
            parameters: Dictionary with 'frequency', 'amplitude', 'contact', etc.
            
        Returns:
            Dictionary with calculated effects and metrics
        """
        # Extract parameters
        frequency = parameters.get('frequency', 130.0)
        amplitude = parameters.get('amplitude', 2.0)
        contact_idx = int(parameters.get('contact', 0))
        condition = parameters.get('condition', 'healthy')
        
        # Set disease condition
        self.disease_manager.set_condition(condition)
        
        # Configure electrode
        self.electrode.set_stimulation_configuration('monopolar', [contact_idx], [amplitude])
        
        # Solve electric field
        electrode_positions = [self.electrode.contacts[contact_idx].position]
        potential = self.field_solver.solve_potential(electrode_positions, [amplitude])
        field_data = self.field_solver.get_visualization_data(potential)
        
        # Generate pathological activity pattern
        time_array = np.arange(0, self.simulation_time, 0.1)
        pathological_pattern = self.disease_manager.generate_pathological_pattern(time_array)
        
        # Simulate neuron responses
        neural_response = self.neuron_manager.simulate_dbs_effects(
            field_data, frequency, amplitude, self.simulation_time
        )
        
        # Calculate DBS treatment effects
        baseline_activity = np.array(pathological_pattern['neural_activity'])
        dbs_response = self.disease_manager.simulate_dbs_response(
            baseline_activity, frequency, amplitude
        )
        
        # Calculate comprehensive metrics
        effects = self._calculate_comprehensive_metrics(
            field_data, neural_response, pathological_pattern, dbs_response, parameters
        )
        
        return effects
    
    def _calculate_comprehensive_metrics(self, field_data: Dict, neural_response: Dict,
                                       pathological_pattern: Dict, dbs_response: Dict,
                                       parameters: Dict) -> Dict:
        """Calculate comprehensive metrics for educational display."""
        
        # Field spread metrics
        field_magnitude = np.array(field_data['field_magnitude'])
        field_max = np.max(field_magnitude)
        field_mean = np.mean(field_magnitude[field_magnitude > field_max * 0.1])
        
        # Calculate volume of tissue activated (VTA)
        activation_threshold = 0.2  # V/m (typical neural activation threshold)
        vta_volume = np.sum(field_magnitude > activation_threshold) * np.prod(self.brain_model.voxel_size)
        
        # Neural activity metrics
        population_response = neural_response['population_response']
        baseline_firing_rate = np.mean(population_response['firing_rates'])
        synchrony_index = population_response['population_synchrony']
        
        # Treatment efficacy metrics
        symptom_improvement = dbs_response.get('improvement_percentage', 0)
        side_effect_score = dbs_response.get('side_effect_score', 0)
        
        # Energy efficiency metrics
        frequency = parameters.get('frequency', 130)
        amplitude = parameters.get('amplitude', 2.0)
        power_consumption = self._estimate_power_consumption(frequency, amplitude)
        
        # Selectivity metrics (target vs off-target stimulation)
        selectivity_score = self._calculate_selectivity_score(field_magnitude)
        
        return {
            'field_metrics': {
                'max_field_strength': float(field_max),
                'mean_field_strength': float(field_mean),
                'vta_volume_mm3': float(vta_volume),
                'field_penetration_depth': self._calculate_penetration_depth(field_magnitude)
            },
            'neural_metrics': {
                'firing_rate_change': float(baseline_firing_rate),
                'synchrony_index': float(synchrony_index),
                'population_coherence': self._calculate_population_coherence(population_response)
            },
            'therapeutic_metrics': {
                'symptom_improvement_percent': float(symptom_improvement),
                'side_effect_score': float(side_effect_score),
                'therapeutic_window': self._calculate_therapeutic_window(symptom_improvement, side_effect_score)
            },
            'efficiency_metrics': {
                'power_consumption_mw': float(power_consumption),
                'selectivity_score': float(selectivity_score),
                'efficiency_ratio': float(symptom_improvement / (power_consumption + 1e-6))
            },
            'parameter_effects': {
                'frequency_effect': self._analyze_frequency_effect(frequency),
                'amplitude_effect': self._analyze_amplitude_effect(amplitude),
                'spatial_effect': self._analyze_spatial_effect(field_magnitude)
            }
        }
    
    def explore_parameter_space(self, condition: str = 'parkinson',
                              parameter_ranges: Optional[Dict] = None) -> Dict:
        """
        Systematic exploration of parameter space for educational visualization.
        
        Args:
            condition: Neurological condition to simulate
            parameter_ranges: Optional custom parameter ranges
            
        Returns:
            Dictionary with parameter effect maps and insights
        """
        if parameter_ranges is None:
            parameter_ranges = self.parameter_bounds
        
        # Create parameter grids for exploration
        freq_range = np.linspace(parameter_ranges['frequency'][0], 
                               parameter_ranges['frequency'][1], 
                               self.exploration_resolution)
        amp_range = np.linspace(parameter_ranges['amplitude'][0],
                              parameter_ranges['amplitude'][1],
                              self.exploration_resolution)
        
        # Results storage
        exploration_results = {
            'frequency_sweep': [],
            'amplitude_sweep': [],
            'parameter_map': np.zeros((len(freq_range), len(amp_range))),
            'optimal_regions': [],
            'educational_insights': []
        }
        
        # Explore frequency effects (fixed amplitude)
        fixed_amplitude = 2.0
        for i, freq in enumerate(freq_range):
            params = {
                'frequency': freq,
                'amplitude': fixed_amplitude,
                'contact': 0,
                'condition': condition
            }
            effects = self.calculate_effects(params)
            
            exploration_results['frequency_sweep'].append({
                'frequency': freq,
                'symptom_improvement': effects['therapeutic_metrics']['symptom_improvement_percent'],
                'side_effects': effects['therapeutic_metrics']['side_effect_score'],
                'power_consumption': effects['efficiency_metrics']['power_consumption_mw'],
                'vta_volume': effects['field_metrics']['vta_volume_mm3']
            })
        
        # Explore amplitude effects (fixed frequency)
        fixed_frequency = 130.0
        for i, amp in enumerate(amp_range):
            params = {
                'frequency': fixed_frequency,
                'amplitude': amp,
                'contact': 0,
                'condition': condition
            }
            effects = self.calculate_effects(params)
            
            exploration_results['amplitude_sweep'].append({
                'amplitude': amp,
                'symptom_improvement': effects['therapeutic_metrics']['symptom_improvement_percent'],
                'side_effects': effects['therapeutic_metrics']['side_effect_score'],
                'power_consumption': effects['efficiency_metrics']['power_consumption_mw'],
                'vta_volume': effects['field_metrics']['vta_volume_mm3']
            })
        
        # Create 2D parameter map (frequency vs amplitude)
        for i, freq in enumerate(freq_range[::2]):  # Reduced resolution for 2D map
            for j, amp in enumerate(amp_range[::2]):
                params = {
                    'frequency': freq,
                    'amplitude': amp,
                    'contact': 0,
                    'condition': condition
                }
                effects = self.calculate_effects(params)
                
                # Use therapeutic window as the mapped value
                therapeutic_score = effects['therapeutic_metrics']['therapeutic_window']
                if i < exploration_results['parameter_map'].shape[0] and j < exploration_results['parameter_map'].shape[1]:
                    exploration_results['parameter_map'][i, j] = therapeutic_score
        
        # Identify optimal regions
        exploration_results['optimal_regions'] = self._identify_optimal_regions(
            exploration_results['parameter_map'], freq_range[::2], amp_range[::2]
        )
        
        # Generate educational insights
        exploration_results['educational_insights'] = self._generate_educational_insights(
            exploration_results, condition
        )
        
        return exploration_results
    
    def optimize_parameters(self, condition: str = 'parkinson',
                          optimization_target: str = 'therapeutic_window',
                          method: str = 'differential_evolution') -> Dict:
        """
        Optimize DBS parameters for given condition and target.
        
        Args:
            condition: Neurological condition
            optimization_target: Target metric to optimize
            method: Optimization method
            
        Returns:
            Optimization results with optimal parameters
        """
        def objective_function(params_array):
            """Objective function for optimization."""
            frequency, amplitude, contact_float = params_array
            contact = int(np.clip(contact_float, 0, len(self.electrode.contacts) - 1))
            
            parameters = {
                'frequency': frequency,
                'amplitude': amplitude,
                'contact': contact,
                'condition': condition
            }
            
            try:
                effects = self.calculate_effects(parameters)
                
                if optimization_target == 'therapeutic_window':
                    return -effects['therapeutic_metrics']['therapeutic_window']  # Minimize negative
                elif optimization_target == 'symptom_improvement':
                    return -effects['therapeutic_metrics']['symptom_improvement_percent']
                elif optimization_target == 'efficiency':
                    return -effects['efficiency_metrics']['efficiency_ratio']
                else:
                    return 0.0
                    
            except Exception as e:
                print(f"Optimization error: {e}")
                return 1000.0  # High penalty for failed evaluations
        
        # Define bounds for optimization
        bounds = [
            self.parameter_bounds['frequency'],
            self.parameter_bounds['amplitude'],
            (0, len(self.electrode.contacts) - 1)
        ]
        
        # Run optimization
        if method == 'differential_evolution':
            result = differential_evolution(
                objective_function,
                bounds,
                maxiter=50,  # Limited for educational purposes
                popsize=10,
                seed=42
            )
        else:
            # Use scipy minimize with initial guess
            x0 = [130.0, 2.0, 0.0]  # Standard DBS parameters
            result = minimize(objective_function, x0, bounds=bounds, method='L-BFGS-B')
        
        # Extract optimal parameters
        optimal_frequency, optimal_amplitude, optimal_contact_float = result.x
        optimal_contact = int(np.clip(optimal_contact_float, 0, len(self.electrode.contacts) - 1))
        
        # Calculate effects with optimal parameters
        optimal_parameters = {
            'frequency': optimal_frequency,
            'amplitude': optimal_amplitude,
            'contact': optimal_contact,
            'condition': condition
        }
        
        optimal_effects = self.calculate_effects(optimal_parameters)
        
        return {
            'optimal_parameters': optimal_parameters,
            'optimal_effects': optimal_effects,
            'optimization_result': {
                'success': result.success,
                'message': getattr(result, 'message', 'Optimization completed'),
                'iterations': getattr(result, 'nit', 0),
                'final_score': -result.fun
            },
            'parameter_sensitivity': self._analyze_parameter_sensitivity(optimal_parameters, condition)
        }
    
    def _calculate_penetration_depth(self, field_magnitude: np.ndarray) -> float:
        """Calculate field penetration depth into tissue."""
        # Simplified calculation of field penetration
        max_field = np.max(field_magnitude)
        threshold = max_field * 0.37  # 1/e threshold
        
        # Find penetration depth along electrode axis
        center_slice = field_magnitude[field_magnitude.shape[0]//2, :, field_magnitude.shape[2]//2]
        penetration_voxels = np.sum(center_slice > threshold)
        
        return float(penetration_voxels * self.brain_model.voxel_size[1])
    
    def _calculate_population_coherence(self, population_response: Dict) -> float:
        """Calculate population coherence metric."""
        firing_rates = population_response['firing_rates']
        if len(firing_rates) == 0:
            return 0.0
        
        # Calculate coefficient of variation of firing rates
        cv = np.std(firing_rates) / (np.mean(firing_rates) + 1e-6)
        
        # Convert to coherence measure (lower CV = higher coherence)
        coherence = 1.0 / (1.0 + cv)
        return float(coherence)
    
    def _calculate_therapeutic_window(self, improvement: float, side_effects: float) -> float:
        """Calculate therapeutic window (benefit vs side effects)."""
        if improvement <= 0:
            return 0.0
        
        # Therapeutic window balances efficacy and side effects
        window = improvement / (1.0 + side_effects * 10.0)  # Penalize side effects heavily
        return float(window)
    
    def _estimate_power_consumption(self, frequency: float, amplitude: float) -> float:
        """Estimate power consumption of DBS stimulation."""
        # Simplified power model: P = V * I
        # Voltage depends on amplitude and tissue impedance
        # Current is proportional to amplitude
        
        tissue_impedance = 1000.0  # Ohms (typical)
        voltage = amplitude * tissue_impedance / 1000.0  # Convert mA to A
        current = amplitude / 1000.0  # mA to A
        
        # Power per pulse
        pulse_power = voltage * current  # Watts
        
        # Total power depends on frequency
        duty_cycle = 0.1 / (1000.0 / frequency)  # Pulse width / period
        average_power = pulse_power * duty_cycle * frequency
        
        return average_power * 1000.0  # Convert to mW
    
    def _calculate_selectivity_score(self, field_magnitude: np.ndarray) -> float:
        """Calculate spatial selectivity score."""
        # Selectivity is inversely related to field spread
        max_field = np.max(field_magnitude)
        
        if max_field == 0:
            return 0.0
        
        # Calculate field localization
        threshold = max_field * 0.5  # 50% threshold
        activated_volume = np.sum(field_magnitude > threshold)
        total_volume = field_magnitude.size
        
        # Selectivity score (higher = more selective)
        selectivity = 1.0 - (activated_volume / total_volume)
        return float(selectivity)
    
    def _analyze_frequency_effect(self, frequency: float) -> str:
        """Analyze the educational effect of frequency parameter."""
        if frequency < 50:
            return "Low frequency: May cause muscle contractions and worsen symptoms"
        elif frequency < 100:
            return "Medium frequency: Partial therapeutic effect with some side effects"
        elif frequency < 180:
            return "High frequency: Optimal therapeutic range for most conditions"
        else:
            return "Very high frequency: May cause speech/cognitive side effects"
    
    def _analyze_amplitude_effect(self, amplitude: float) -> str:
        """Analyze the educational effect of amplitude parameter."""
        if amplitude < 1.0:
            return "Low amplitude: Minimal therapeutic effect, good selectivity"
        elif amplitude < 3.0:
            return "Medium amplitude: Good therapeutic effect with manageable side effects"
        elif amplitude < 5.0:
            return "High amplitude: Strong effect but increased side effect risk"
        else:
            return "Very high amplitude: High side effect risk, potential tissue damage"
    
    def _analyze_spatial_effect(self, field_magnitude: np.ndarray) -> str:
        """Analyze spatial effects of stimulation."""
        max_field = np.max(field_magnitude)
        mean_field = np.mean(field_magnitude[field_magnitude > 0])
        
        if max_field < 0.1:
            return "Weak spatial effect: Limited tissue activation"
        elif max_field < 0.5:
            return "Moderate spatial effect: Localized tissue activation"
        elif max_field < 1.0:
            return "Strong spatial effect: Broad tissue activation"
        else:
            return "Very strong spatial effect: Risk of off-target activation"
    
    def _identify_optimal_regions(self, parameter_map: np.ndarray, 
                                freq_range: np.ndarray, amp_range: np.ndarray) -> List[Dict]:
        """Identify optimal parameter regions from exploration map."""
        # Find peaks in the parameter map
        from scipy import ndimage
        
        # Smooth the map slightly
        smoothed_map = ndimage.gaussian_filter(parameter_map, sigma=1.0)
        
        # Find local maxima
        local_maxima = ndimage.maximum_filter(smoothed_map, size=3) == smoothed_map
        maxima_coords = np.where(local_maxima & (smoothed_map > 0.5))  # Threshold for significance
        
        optimal_regions = []
        for i, j in zip(maxima_coords[0], maxima_coords[1]):
            if i < len(freq_range) and j < len(amp_range):
                optimal_regions.append({
                    'frequency': float(freq_range[i]),
                    'amplitude': float(amp_range[j]),
                    'therapeutic_score': float(smoothed_map[i, j]),
                    'region_size': 'localized'  # Could calculate actual region size
                })
        
        # Sort by therapeutic score
        optimal_regions.sort(key=lambda x: x['therapeutic_score'], reverse=True)
        
        return optimal_regions[:5]  # Return top 5 regions
    
    def _generate_educational_insights(self, exploration_results: Dict, condition: str) -> List[str]:
        """Generate educational insights from exploration results."""
        insights = []
        
        # Frequency insights
        freq_data = exploration_results['frequency_sweep']
        if freq_data:
            best_freq_idx = max(range(len(freq_data)), 
                              key=lambda i: freq_data[i]['symptom_improvement'])
            best_freq = freq_data[best_freq_idx]['frequency']
            
            insights.append(f"Optimal frequency for {condition}: ~{best_freq:.0f} Hz")
            
            if best_freq > 100:
                insights.append("High-frequency stimulation is most effective for blocking pathological signals")
            else:
                insights.append("Lower frequencies may be needed for this condition")
        
        # Amplitude insights
        amp_data = exploration_results['amplitude_sweep']
        if amp_data:
            # Find amplitude with best therapeutic window
            best_amp_idx = max(range(len(amp_data)),
                             key=lambda i: amp_data[i]['symptom_improvement'] - amp_data[i]['side_effects'])
            best_amp = amp_data[best_amp_idx]['amplitude']
            
            insights.append(f"Optimal amplitude balance: ~{best_amp:.1f} mA")
            insights.append("Higher amplitudes increase both therapeutic effect and side effects")
        
        # Power consumption insights
        if freq_data and amp_data:
            high_power_points = [d for d in freq_data if d['power_consumption'] > 5.0]
            if high_power_points:
                insights.append("High power consumption may reduce battery life")
            else:
                insights.append("Current parameters provide good power efficiency")
        
        # Condition-specific insights
        if condition == 'parkinson':
            insights.append("Beta oscillations are disrupted by high-frequency stimulation")
            insights.append("Optimal frequency range typically 100-180 Hz for Parkinson's")
        elif condition == 'tremor':
            insights.append("Tremor responds well to moderate frequencies (60-120 Hz)")
        elif condition == 'dystonia':
            insights.append("Lower frequencies (60-100 Hz) often effective for dystonia")
        
        return insights
    
    def _analyze_parameter_sensitivity(self, optimal_parameters: Dict, condition: str) -> Dict:
        """Analyze sensitivity of optimal parameters."""
        sensitivity = {}
        
        # Test small perturbations around optimal parameters
        perturbation = 0.1  # 10% perturbation
        
        for param_name in ['frequency', 'amplitude']:
            if param_name in optimal_parameters:
                original_value = optimal_parameters[param_name]
                
                # Test positive perturbation
                test_params = optimal_parameters.copy()
                test_params[param_name] = original_value * (1 + perturbation)
                try:
                    effects_pos = self.calculate_effects(test_params)
                    score_pos = effects_pos['therapeutic_metrics']['therapeutic_window']
                except:
                    score_pos = 0
                
                # Test negative perturbation
                test_params[param_name] = original_value * (1 - perturbation)
                try:
                    effects_neg = self.calculate_effects(test_params)
                    score_neg = effects_neg['therapeutic_metrics']['therapeutic_window']
                except:
                    score_neg = 0
                
                # Calculate sensitivity
                original_score = self.calculate_effects(optimal_parameters)['therapeutic_metrics']['therapeutic_window']
                sensitivity[param_name] = {
                    'positive_change': score_pos - original_score,
                    'negative_change': score_neg - original_score,
                    'sensitivity_score': abs(score_pos - score_neg) / (2 * perturbation * original_value + 1e-6)
                }
        
        return sensitivity
