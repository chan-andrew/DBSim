"""
Disease Models for DBS Simulation
Educational implementations of pathological neural activity patterns
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import signal


class BaseNeurologicalCondition:
    """Base class for neurological condition simulations."""
    
    def __init__(self):
        self.condition_name = "Base Condition"
        self.pathological_frequency_bands = {}
        self.baseline_activity_level = 1.0
        
    def generate_pathological_activity(self, time_array: np.ndarray, 
                                     baseline_firing_rate: float = 10.0) -> Dict:
        """Generate pathological neural activity pattern."""
        raise NotImplementedError
    
    def calculate_symptom_severity(self, neural_activity: np.ndarray) -> float:
        """Calculate symptom severity from neural activity."""
        raise NotImplementedError
    
    def _apply_bandpass_filter(self, signal_data: np.ndarray, 
                              frequency_band: Tuple[float, float],
                              fs: float) -> np.ndarray:
        """Apply bandpass filter to signal."""
        from scipy import signal as scipy_signal
        
        low_freq, high_freq = frequency_band
        nyquist = fs / 2
        
        if low_freq >= nyquist or high_freq >= nyquist:
            return np.zeros_like(signal_data)
        
        low_norm = low_freq / nyquist
        high_norm = high_freq / nyquist
        
        try:
            b, a = scipy_signal.butter(4, [low_norm, high_norm], btype='band')
            filtered_signal = scipy_signal.filtfilt(b, a, signal_data)
            return filtered_signal
        except:
            return np.zeros_like(signal_data)
    
    def _calculate_band_powers(self, frequencies: np.ndarray, 
                              psd: np.ndarray) -> Dict[str, float]:
        """Calculate power in different frequency bands."""
        bands = {
            'delta': (1, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 100)
        }
        
        band_powers = {}
        for band_name, (low_freq, high_freq) in bands.items():
            mask = (frequencies >= low_freq) & (frequencies <= high_freq)
            band_powers[band_name] = np.mean(psd[mask]) if np.any(mask) else 0.0
        
        return band_powers


class ParkinsonSimulation(BaseNeurologicalCondition):
    """
    Parkinson's Disease simulation focusing on beta oscillations and bradykinesia.
    Educational model demonstrating key pathophysiological features.
    """
    
    def __init__(self):
        super().__init__()
        self.condition_name = "Parkinson's Disease"
        
        # Characteristic frequency bands
        self.pathological_frequency_bands = {
            'beta': (13, 30),      # Pathological beta oscillations
            'low_gamma': (30, 45), # Reduced gamma activity
            'tremor': (4, 6)       # Tremor frequency
        }
        
        # Disease parameters
        self.beta_power_increase = 3.0      # 3x increase in beta power
        self.baseline_reduction = 0.6       # 40% reduction in baseline activity
        self.tremor_amplitude = 0.8         # Tremor strength
        self.motor_impairment_factor = 2.5  # Motor circuit dysfunction
        
    def generate_pathological_activity(self, time_array: np.ndarray,
                                     baseline_firing_rate: float = 10.0,
                                     add_tremor: bool = True) -> Dict:
        """
        Generate Parkinson's pathological activity pattern.
        
        Args:
            time_array: Time points for simulation (ms)
            baseline_firing_rate: Normal baseline firing rate (Hz)
            add_tremor: Whether to include tremor oscillations
            
        Returns:
            Dictionary with pathological activity data
        """
        dt = time_array[1] - time_array[0] if len(time_array) > 1 else 0.1
        fs = 1000.0 / dt  # Sampling frequency in Hz
        
        # Generate reduced baseline activity
        reduced_baseline = baseline_firing_rate * self.baseline_reduction
        baseline_activity = np.random.poisson(reduced_baseline * dt, len(time_array))
        
        # Generate pathological beta oscillations (13-30 Hz)
        beta_freq = 20.0  # Hz (peak beta frequency)
        beta_phase = np.random.uniform(0, 2*np.pi)
        beta_oscillation = (self.beta_power_increase * 
                           np.sin(2 * np.pi * beta_freq * time_array / 1000.0 + beta_phase))
        
        # Add beta band noise
        beta_noise = np.random.normal(0, 0.5, len(time_array))
        beta_filtered = self._apply_bandpass_filter(beta_noise, 
                                                   self.pathological_frequency_bands['beta'], 
                                                   fs)
        
        # Generate tremor oscillations if enabled
        tremor_component = np.zeros_like(time_array)
        if add_tremor:
            tremor_freq = 5.0  # Hz (typical PD tremor)
            tremor_phase = np.random.uniform(0, 2*np.pi)
            tremor_component = (self.tremor_amplitude * 
                              np.sin(2 * np.pi * tremor_freq * time_array / 1000.0 + tremor_phase))
        
        # Combine pathological components
        pathological_activity = (baseline_activity.astype(float) + 
                               beta_oscillation + 
                               beta_filtered * 0.5 + 
                               tremor_component)
        
        # Ensure non-negative firing rates
        pathological_activity = np.maximum(pathological_activity, 0)
        
        # Calculate power spectral density
        frequencies, psd = signal.welch(pathological_activity, fs=fs, nperseg=min(256, len(time_array)//4))
        
        # Calculate specific band powers
        band_powers = self._calculate_band_powers(frequencies, psd)
        
        return {
            'neural_activity': pathological_activity.tolist(),
            'baseline_component': baseline_activity.tolist(),
            'beta_component': beta_oscillation.tolist(),
            'tremor_component': tremor_component.tolist(),
            'time_array': time_array.tolist(),
            'frequencies': frequencies.tolist(),
            'power_spectral_density': psd.tolist(),
            'band_powers': band_powers,
            'pathological_markers': {
                'beta_power_ratio': band_powers['beta'] / (band_powers['alpha'] + 1e-6),
                'tremor_strength': np.std(tremor_component),
                'baseline_reduction': self.baseline_reduction
            }
        }
    
    def calculate_symptom_severity(self, neural_activity: np.ndarray) -> float:
        """
        Calculate Parkinson's symptom severity from neural activity.
        
        Args:
            neural_activity: Neural activity time series
            
        Returns:
            Symptom severity score (0-1, higher = more severe)
        """
        # Calculate beta power (main pathological marker)
        frequencies, psd = signal.welch(neural_activity, fs=1000, nperseg=min(256, len(neural_activity)//4))
        band_powers = self._calculate_band_powers(frequencies, psd)
        
        # Symptom components
        beta_severity = min(band_powers['beta'] / 10.0, 1.0)  # Normalize beta power
        bradykinesia_severity = max(0, 1.0 - np.mean(neural_activity) / 10.0)  # Reduced activity
        
        # Combined symptom severity
        total_severity = 0.6 * beta_severity + 0.4 * bradykinesia_severity
        
        return min(total_severity, 1.0)
    
    def simulate_dbs_response(self, pathological_activity: np.ndarray,
                            dbs_frequency: float, dbs_amplitude: float) -> Dict:
        """
        Simulate response to DBS stimulation.
        
        Args:
            pathological_activity: Baseline pathological activity
            dbs_frequency: DBS stimulation frequency (Hz)
            dbs_amplitude: DBS amplitude (relative units)
            
        Returns:
            Dictionary with DBS response data
        """
        # DBS effects model
        if dbs_frequency < 50:
            # Low frequency DBS may worsen symptoms
            suppression_factor = 0.8  # Less suppression
            side_effect_factor = 1.2  # More side effects
        elif dbs_frequency > 100:
            # High frequency DBS (therapeutic range)
            suppression_factor = max(0.2, 1.0 - dbs_amplitude * 0.3)  # Strong suppression
            side_effect_factor = 1.0 + dbs_amplitude * 0.1  # Minimal side effects
        else:
            # Medium frequency
            suppression_factor = 0.6
            side_effect_factor = 1.1
        
        # Apply DBS effects
        treated_activity = pathological_activity * suppression_factor
        
        # Add high-frequency DBS artifacts if frequency > 100 Hz
        if dbs_frequency > 100:
            time_array = np.arange(len(pathological_activity))
            dbs_artifact = 0.1 * dbs_amplitude * np.sin(2 * np.pi * dbs_frequency * time_array / 1000.0)
            treated_activity += dbs_artifact
        
        # Calculate improvement metrics
        baseline_severity = self.calculate_symptom_severity(pathological_activity)
        treated_severity = self.calculate_symptom_severity(treated_activity)
        improvement = max(0, baseline_severity - treated_severity)
        
        return {
            'treated_activity': treated_activity.tolist(),
            'baseline_severity': baseline_severity,
            'treated_severity': treated_severity,
            'improvement_percentage': improvement / baseline_severity * 100 if baseline_severity > 0 else 0,
            'side_effect_score': side_effect_factor - 1.0,
            'suppression_factor': suppression_factor
        }


class DystoniaSimulation(BaseNeurologicalCondition):
    """
    Dystonia simulation focusing on irregular muscle activation patterns.
    Educational model of abnormal movement disorder.
    """
    
    def __init__(self):
        super().__init__()
        self.condition_name = "Dystonia"
        
        # Characteristic features
        self.pathological_frequency_bands = {
            'low_frequency': (3, 12),    # Irregular low-frequency activity
            'muscle_coherence': (15, 25)  # Abnormal muscle synchronization
        }
        
        self.irregular_burst_rate = 0.3      # Probability of irregular bursts
        self.muscle_cocontraction = 1.5      # Increased muscle coactivation
        self.movement_irregularity = 2.0     # Movement pattern disruption
        
    def generate_pathological_activity(self, time_array: np.ndarray,
                                     baseline_firing_rate: float = 8.0) -> Dict:
        """
        Generate dystonia pathological activity pattern.
        
        Args:
            time_array: Time points for simulation (ms)
            baseline_firing_rate: Normal baseline firing rate (Hz)
            
        Returns:
            Dictionary with pathological activity data
        """
        dt = time_array[1] - time_array[0] if len(time_array) > 1 else 0.1
        
        # Generate irregular baseline activity
        baseline_activity = np.random.poisson(baseline_firing_rate * dt, len(time_array))
        
        # Add irregular bursting patterns
        burst_activity = np.zeros_like(time_array, dtype=float)
        for i in range(len(time_array)):
            if np.random.random() < self.irregular_burst_rate * dt / 1000.0:
                # Create burst
                burst_duration = np.random.exponential(50)  # ms
                burst_end = min(i + int(burst_duration / dt), len(time_array))
                burst_intensity = np.random.exponential(5)
                burst_activity[i:burst_end] += burst_intensity
        
        # Add low-frequency irregular oscillations
        irregular_freq = np.random.uniform(3, 12)  # Hz
        irregular_phase = np.random.uniform(0, 2*np.pi)
        irregular_amplitude = np.random.uniform(0.5, 2.0)
        
        irregular_oscillation = (irregular_amplitude * 
                               np.sin(2 * np.pi * irregular_freq * time_array / 1000.0 + irregular_phase))
        
        # Add noise to simulate muscle cocontraction
        cocontraction_noise = np.random.normal(0, self.muscle_cocontraction, len(time_array))
        
        # Combine components
        pathological_activity = (baseline_activity.astype(float) + 
                               burst_activity + 
                               irregular_oscillation + 
                               cocontraction_noise)
        
        # Ensure non-negative
        pathological_activity = np.maximum(pathological_activity, 0)
        
        # Calculate irregularity metrics
        activity_variability = np.std(pathological_activity) / (np.mean(pathological_activity) + 1e-6)
        burst_frequency = np.sum(np.diff(pathological_activity) > 2) / (time_array[-1] / 1000.0)
        
        return {
            'neural_activity': pathological_activity.tolist(),
            'baseline_component': baseline_activity.tolist(),
            'burst_component': burst_activity.tolist(),
            'irregular_component': irregular_oscillation.tolist(),
            'time_array': time_array.tolist(),
            'pathological_markers': {
                'activity_variability': activity_variability,
                'burst_frequency': burst_frequency,
                'irregularity_index': self.movement_irregularity
            }
        }
    
    def calculate_symptom_severity(self, neural_activity: np.ndarray) -> float:
        """Calculate dystonia symptom severity."""
        # Measure irregularity and variability
        activity_cv = np.std(neural_activity) / (np.mean(neural_activity) + 1e-6)
        
        # Count irregular bursts
        burst_count = np.sum(np.diff(neural_activity) > 2 * np.std(neural_activity))
        burst_severity = min(burst_count / len(neural_activity) * 100, 1.0)
        
        # Combined severity
        total_severity = 0.7 * min(activity_cv / 3.0, 1.0) + 0.3 * burst_severity
        
        return min(total_severity, 1.0)


class TremorSimulation(BaseNeurologicalCondition):
    """
    Essential Tremor simulation focusing on rhythmic oscillatory activity.
    """
    
    def __init__(self):
        super().__init__()
        self.condition_name = "Essential Tremor"
        
        self.pathological_frequency_bands = {
            'tremor': (6, 12),  # Essential tremor frequency range
            'harmonics': (12, 24)  # Harmonic components
        }
        
        self.tremor_frequency = 8.0    # Hz
        self.tremor_amplitude = 2.0    # Tremor strength
        self.tremor_variability = 0.2  # Frequency variability
        
    def generate_pathological_activity(self, time_array: np.ndarray,
                                     baseline_firing_rate: float = 12.0) -> Dict:
        """Generate essential tremor pathological activity."""
        dt = time_array[1] - time_array[0] if len(time_array) > 1 else 0.1
        
        # Generate baseline activity
        baseline_activity = np.random.poisson(baseline_firing_rate * dt, len(time_array))
        
        # Generate tremor oscillation with frequency variability
        instantaneous_freq = (self.tremor_frequency + 
                            self.tremor_variability * np.random.normal(0, 1, len(time_array)))
        
        # Integrate frequency to get phase
        phase = np.cumsum(instantaneous_freq) * 2 * np.pi * dt / 1000.0
        tremor_oscillation = self.tremor_amplitude * np.sin(phase)
        
        # Add harmonics for more realistic tremor
        harmonic_component = 0.3 * self.tremor_amplitude * np.sin(2 * phase)
        
        # Combine components
        pathological_activity = (baseline_activity.astype(float) + 
                               tremor_oscillation + 
                               harmonic_component)
        
        pathological_activity = np.maximum(pathological_activity, 0)
        
        # Calculate tremor metrics
        tremor_power = np.mean(tremor_oscillation**2)
        frequency_stability = 1.0 / (np.std(instantaneous_freq) + 1e-6)
        
        return {
            'neural_activity': pathological_activity.tolist(),
            'baseline_component': baseline_activity.tolist(),
            'tremor_component': tremor_oscillation.tolist(),
            'harmonic_component': harmonic_component.tolist(),
            'instantaneous_frequency': instantaneous_freq.tolist(),
            'time_array': time_array.tolist(),
            'pathological_markers': {
                'tremor_power': tremor_power,
                'tremor_frequency': self.tremor_frequency,
                'frequency_stability': frequency_stability
            }
        }
    
    def calculate_symptom_severity(self, neural_activity: np.ndarray) -> float:
        """Calculate tremor symptom severity."""
        # Calculate power in tremor frequency band
        frequencies, psd = signal.welch(neural_activity, fs=1000, nperseg=min(256, len(neural_activity)//4))
        
        tremor_band_power = np.mean(psd[(frequencies >= 6) & (frequencies <= 12)])
        total_power = np.mean(psd)
        
        tremor_ratio = tremor_band_power / (total_power + 1e-6)
        
        return min(tremor_ratio * 2.0, 1.0)  # Normalize to 0-1


class DiseaseModelManager:
    """
    Manages different disease models for educational DBS simulation.
    """
    
    def __init__(self):
        """Initialize disease model manager."""
        self.available_conditions = {
            'healthy': None,  # No pathological model
            'parkinson': ParkinsonSimulation(),
            'dystonia': DystoniaSimulation(),
            'tremor': TremorSimulation()
        }
        
        self.current_condition = 'healthy'
        
    def set_condition(self, condition_name: str):
        """Set the current neurological condition."""
        if condition_name in self.available_conditions:
            self.current_condition = condition_name
        else:
            raise ValueError(f"Unknown condition: {condition_name}")
    
    def generate_pathological_pattern(self, time_array: np.ndarray,
                                    baseline_firing_rate: float = 10.0) -> Dict:
        """
        Generate pathological activity pattern for current condition.
        
        Args:
            time_array: Time points for simulation (ms)
            baseline_firing_rate: Normal baseline firing rate (Hz)
            
        Returns:
            Dictionary with pathological activity data
        """
        if self.current_condition == 'healthy':
            # Generate healthy baseline activity
            dt = time_array[1] - time_array[0] if len(time_array) > 1 else 0.1
            healthy_activity = np.random.poisson(baseline_firing_rate * dt, len(time_array))
            
            return {
                'neural_activity': healthy_activity.tolist(),
                'time_array': time_array.tolist(),
                'condition': 'healthy',
                'pathological_markers': {
                    'is_healthy': True
                }
            }
        
        else:
            condition_model = self.available_conditions[self.current_condition]
            result = condition_model.generate_pathological_activity(time_array, baseline_firing_rate)
            result['condition'] = self.current_condition
            return result
    
    def calculate_symptom_severity(self, neural_activity: np.ndarray) -> float:
        """Calculate symptom severity for current condition."""
        if self.current_condition == 'healthy':
            return 0.0
        
        condition_model = self.available_conditions[self.current_condition]
        return condition_model.calculate_symptom_severity(neural_activity)
    
    def simulate_dbs_response(self, pathological_activity: np.ndarray,
                            dbs_frequency: float, dbs_amplitude: float) -> Dict:
        """Simulate DBS response for current condition."""
        if self.current_condition == 'healthy':
            # Healthy brain - DBS may have minimal effect or side effects
            return {
                'treated_activity': pathological_activity.tolist(),
                'improvement_percentage': 0.0,
                'side_effect_score': dbs_amplitude * 0.1,  # Potential side effects
                'baseline_severity': 0.0,
                'treated_severity': 0.0
            }
        
        elif self.current_condition == 'parkinson':
            condition_model = self.available_conditions[self.current_condition]
            return condition_model.simulate_dbs_response(pathological_activity, 
                                                       dbs_frequency, dbs_amplitude)
        
        else:
            # Generic DBS response for other conditions
            suppression_factor = max(0.3, 1.0 - dbs_amplitude * 0.2)
            treated_activity = pathological_activity * suppression_factor
            
            baseline_severity = self.calculate_symptom_severity(pathological_activity)
            treated_severity = self.calculate_symptom_severity(treated_activity)
            improvement = max(0, baseline_severity - treated_severity)
            
            return {
                'treated_activity': treated_activity.tolist(),
                'baseline_severity': baseline_severity,
                'treated_severity': treated_severity,
                'improvement_percentage': improvement / baseline_severity * 100 if baseline_severity > 0 else 0,
                'side_effect_score': dbs_amplitude * 0.05,
                'suppression_factor': suppression_factor
            }
    
    def get_condition_info(self) -> Dict:
        """Get information about available conditions."""
        info = {}
        for name, model in self.available_conditions.items():
            if model is None:
                info[name] = {
                    'name': 'Healthy Brain',
                    'description': 'Normal brain activity patterns',
                    'pathological_markers': None
                }
            else:
                info[name] = {
                    'name': model.condition_name,
                    'description': f'Simulation of {model.condition_name} pathophysiology',
                    'frequency_bands': model.pathological_frequency_bands
                }
        
        return info
