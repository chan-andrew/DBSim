"""
Neuron Models for DBS Simulation
Implements simplified Hodgkin-Huxley and Leaky Integrate-and-Fire models
"""

import numpy as np
from scipy.integrate import odeint
from typing import List, Tuple, Optional


class SimplifiedHodgkinHuxley:
    """
    Simplified Hodgkin-Huxley neuron model for DBS response simulation.
    Educational implementation focusing on membrane dynamics under electrical stimulation.
    """
    
    def __init__(self):
        """Initialize HH model parameters."""
        # Membrane parameters
        self.C_m = 1.0      # Membrane capacitance (μF/cm²)
        self.g_Na = 120.0   # Sodium conductance (mS/cm²)
        self.g_K = 36.0     # Potassium conductance (mS/cm²)
        self.g_L = 0.3      # Leak conductance (mS/cm²)
        
        # Reversal potentials (mV)
        self.E_Na = 50.0    # Sodium reversal potential
        self.E_K = -77.0    # Potassium reversal potential
        self.E_L = -54.387  # Leak reversal potential
        
        # Initial conditions
        self.V_rest = -65.0  # Resting potential (mV)
        
    def alpha_m(self, V):
        """Sodium activation rate function."""
        return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))
    
    def beta_m(self, V):
        """Sodium activation rate function."""
        return 4.0 * np.exp(-(V + 65.0) / 18.0)
    
    def alpha_h(self, V):
        """Sodium inactivation rate function."""
        return 0.07 * np.exp(-(V + 65.0) / 20.0)
    
    def beta_h(self, V):
        """Sodium inactivation rate function."""
        return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
    
    def alpha_n(self, V):
        """Potassium activation rate function."""
        return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))
    
    def beta_n(self, V):
        """Potassium activation rate function."""
        return 0.125 * np.exp(-(V + 65.0) / 80.0)
    
    def derivatives(self, state, t, I_ext):
        """
        Calculate derivatives for HH differential equations.
        
        Args:
            state: [V, m, h, n] current state
            t: Time
            I_ext: External current (μA/cm²)
        """
        V, m, h, n = state
        
        # Rate functions
        am = self.alpha_m(V)
        bm = self.beta_m(V)
        ah = self.alpha_h(V)
        bh = self.beta_h(V)
        an = self.alpha_n(V)
        bn = self.beta_n(V)
        
        # Ionic currents
        I_Na = self.g_Na * m**3 * h * (V - self.E_Na)
        I_K = self.g_K * n**4 * (V - self.E_K)
        I_L = self.g_L * (V - self.E_L)
        
        # Derivatives
        dV_dt = (I_ext - I_Na - I_K - I_L) / self.C_m
        dm_dt = am * (1 - m) - bm * m
        dh_dt = ah * (1 - h) - bh * h
        dn_dt = an * (1 - n) - bn * n
        
        return [dV_dt, dm_dt, dh_dt, dn_dt]
    
    def simulate_response(self, stimulus_current: np.ndarray, 
                         time_array: np.ndarray,
                         initial_state: Optional[List[float]] = None) -> Tuple[np.ndarray, dict]:
        """
        Simulate neuron response to stimulus current.
        
        Args:
            stimulus_current: Array of stimulus currents over time (μA/cm²)
            time_array: Time points for simulation (ms)
            initial_state: Initial [V, m, h, n] values
            
        Returns:
            Tuple of (voltage_trace, response_metrics)
        """
        if initial_state is None:
            # Calculate steady-state values at rest
            V0 = self.V_rest
            m0 = self.alpha_m(V0) / (self.alpha_m(V0) + self.beta_m(V0))
            h0 = self.alpha_h(V0) / (self.alpha_h(V0) + self.beta_h(V0))
            n0 = self.alpha_n(V0) / (self.alpha_n(V0) + self.beta_n(V0))
            initial_state = [V0, m0, h0, n0]
        
        # Simulate for each time step
        voltage_trace = []
        state = initial_state
        
        for i, t in enumerate(time_array[:-1]):
            dt = time_array[i+1] - time_array[i]
            I_current = stimulus_current[i] if i < len(stimulus_current) else 0.0
            
            # Integrate over time step
            t_span = [t, t + dt]
            sol = odeint(self.derivatives, state, t_span, args=(I_current,))
            state = sol[-1]
            voltage_trace.append(state[0])
        
        voltage_trace = np.array(voltage_trace)
        
        # Calculate response metrics
        metrics = self._calculate_response_metrics(voltage_trace, time_array[:-1])
        
        return voltage_trace, metrics
    
    def _calculate_response_metrics(self, voltage: np.ndarray, time: np.ndarray) -> dict:
        """Calculate firing rate and other response metrics."""
        # Detect spikes (voltage crossings above threshold)
        threshold = -20.0  # mV
        spikes = []
        
        for i in range(1, len(voltage)):
            if voltage[i-1] < threshold and voltage[i] >= threshold:
                spikes.append(time[i])
        
        # Calculate firing rate
        if len(spikes) > 1:
            total_time = time[-1] - time[0]  # ms
            firing_rate = (len(spikes) - 1) / (total_time / 1000.0)  # Hz
            
            # Calculate inter-spike intervals
            isi = np.diff(spikes)
            cv_isi = np.std(isi) / np.mean(isi) if len(isi) > 1 else 0.0
        else:
            firing_rate = 0.0
            cv_isi = 0.0
        
        return {
            'firing_rate': firing_rate,
            'spike_times': spikes,
            'cv_isi': cv_isi,
            'mean_voltage': np.mean(voltage),
            'voltage_std': np.std(voltage)
        }


class LeakyIntegrateFire:
    """
    Leaky Integrate-and-Fire neuron model for population simulations.
    Computationally efficient for large-scale DBS effect modeling.
    """
    
    def __init__(self):
        """Initialize LIF model parameters."""
        self.tau_m = 10.0       # Membrane time constant (ms)
        self.V_rest = -70.0     # Resting potential (mV)
        self.V_threshold = -55.0 # Spike threshold (mV)
        self.V_reset = -70.0    # Reset potential after spike (mV)
        self.R_m = 10.0         # Membrane resistance (MΩ)
        self.tau_ref = 2.0      # Refractory period (ms)
    
    def simulate_single_neuron(self, stimulus_current: np.ndarray, 
                              time_array: np.ndarray,
                              noise_std: float = 0.1) -> Tuple[np.ndarray, List[float]]:
        """
        Simulate single LIF neuron response.
        
        Args:
            stimulus_current: Stimulus current over time (nA)
            time_array: Time points (ms)
            noise_std: Standard deviation of membrane noise (mV)
            
        Returns:
            Tuple of (voltage_trace, spike_times)
        """
        dt = time_array[1] - time_array[0]
        voltage = np.zeros_like(time_array)
        voltage[0] = self.V_rest
        
        spike_times = []
        refractory_time = 0.0
        
        for i in range(1, len(time_array)):
            current_time = time_array[i]
            
            # Check if in refractory period
            if refractory_time > 0:
                voltage[i] = self.V_reset
                refractory_time -= dt
                continue
            
            # Get stimulus current
            I_stim = stimulus_current[i-1] if i-1 < len(stimulus_current) else 0.0
            
            # Add membrane noise
            noise = np.random.normal(0, noise_std)
            
            # Membrane equation: tau_m * dV/dt = -(V - V_rest) + R_m * I
            dV_dt = (-(voltage[i-1] - self.V_rest) + self.R_m * I_stim) / self.tau_m + noise
            voltage[i] = voltage[i-1] + dV_dt * dt
            
            # Check for spike
            if voltage[i] >= self.V_threshold:
                spike_times.append(current_time)
                voltage[i] = self.V_reset
                refractory_time = self.tau_ref
        
        return voltage, spike_times
    
    def simulate_population(self, electric_field_strength: np.ndarray,
                           n_neurons: int = 1000,
                           simulation_time: float = 1000.0,
                           dt: float = 0.1) -> dict:
        """
        Simulate population of LIF neurons under electric field stimulation.
        
        Args:
            electric_field_strength: Field strength over time (V/m)
            n_neurons: Number of neurons in population
            simulation_time: Total simulation time (ms)
            dt: Time step (ms)
            
        Returns:
            Dictionary with population response data
        """
        time_array = np.arange(0, simulation_time, dt)
        
        # Convert electric field to equivalent current for each neuron
        # Simplified model: I = field_strength * cell_factor
        cell_factor = 0.1  # nA per V/m (simplified conversion)
        
        population_spikes = []
        firing_rates = []
        
        for neuron_id in range(n_neurons):
            # Add some heterogeneity to neuron parameters
            heterogeneity = np.random.normal(1.0, 0.1)
            
            # Scale current based on field strength
            if len(electric_field_strength) == len(time_array):
                stimulus_current = electric_field_strength * cell_factor * heterogeneity
            else:
                # If field strength is constant
                stimulus_current = np.full_like(time_array, 
                                              float(electric_field_strength) * cell_factor * heterogeneity)
            
            # Simulate this neuron
            _, spike_times = self.simulate_single_neuron(stimulus_current, time_array)
            
            # Calculate firing rate for this neuron
            firing_rate = len(spike_times) / (simulation_time / 1000.0)  # Hz
            firing_rates.append(firing_rate)
            
            # Store spikes with neuron ID
            for spike_time in spike_times:
                population_spikes.append((neuron_id, spike_time))
        
        # Calculate population statistics
        mean_firing_rate = np.mean(firing_rates)
        firing_rate_std = np.std(firing_rates)
        
        # Calculate population synchrony (simplified measure)
        synchrony = self._calculate_population_synchrony(population_spikes, time_array)
        
        return {
            'population_spikes': population_spikes,
            'firing_rates': firing_rates,
            'mean_firing_rate': mean_firing_rate,
            'firing_rate_std': firing_rate_std,
            'population_synchrony': synchrony,
            'time_array': time_array.tolist()
        }
    
    def _calculate_population_synchrony(self, spikes: List[Tuple[int, float]], 
                                       time_array: np.ndarray) -> float:
        """
        Calculate population synchrony measure.
        
        Args:
            spikes: List of (neuron_id, spike_time) tuples
            time_array: Time array for binning
            
        Returns:
            Synchrony index (0 = asynchronous, 1 = perfectly synchronous)
        """
        if len(spikes) < 2:
            return 0.0
        
        # Create spike count histogram
        bin_width = 10.0  # ms
        bins = np.arange(time_array[0], time_array[-1] + bin_width, bin_width)
        spike_times = [spike[1] for spike in spikes]
        
        spike_counts, _ = np.histogram(spike_times, bins)
        
        # Calculate coefficient of variation of spike counts
        if np.mean(spike_counts) > 0:
            cv = np.std(spike_counts) / np.mean(spike_counts)
            # Normalize to 0-1 range (higher CV = higher synchrony for bursting)
            synchrony = min(cv / 2.0, 1.0)
        else:
            synchrony = 0.0
        
        return synchrony


class NeuronPopulationManager:
    """
    Manages multiple neuron populations for DBS simulation.
    Handles different neuron types and their responses to electrical stimulation.
    """
    
    def __init__(self):
        """Initialize population manager."""
        self.hh_model = SimplifiedHodgkinHuxley()
        self.lif_model = LeakyIntegrateFire()
    
    def simulate_dbs_effects(self, electric_field_data: dict, 
                           stimulation_frequency: float,
                           stimulation_amplitude: float,
                           simulation_time: float = 1000.0) -> dict:
        """
        Simulate DBS effects on neuron populations.
        
        Args:
            electric_field_data: Electric field distribution from field solver
            stimulation_frequency: DBS frequency (Hz)  
            stimulation_amplitude: DBS amplitude (mA)
            simulation_time: Simulation duration (ms)
            
        Returns:
            Dictionary with neural response data
        """
        dt = 0.1  # ms
        time_array = np.arange(0, simulation_time, dt)
        
        # Generate DBS stimulus pattern
        dbs_stimulus = self._generate_dbs_pattern(time_array, 
                                                 stimulation_frequency, 
                                                 stimulation_amplitude)
        
        # Extract field magnitude for neural stimulation
        field_magnitude = np.array(electric_field_data['field_magnitude'])
        mean_field_strength = np.mean(field_magnitude[field_magnitude > 0])
        
        # Simulate population response using LIF model (more efficient for populations)
        population_response = self.lif_model.simulate_population(
            electric_field_strength=mean_field_strength * dbs_stimulus,
            n_neurons=500,
            simulation_time=simulation_time
        )
        
        # Simulate detailed single neuron response using HH model
        hh_voltage, hh_metrics = self.hh_model.simulate_response(
            stimulus_current=mean_field_strength * dbs_stimulus * 0.01,  # Scale to μA/cm²
            time_array=time_array
        )
        
        return {
            'population_response': population_response,
            'hh_response': {
                'voltage_trace': hh_voltage.tolist(),
                'metrics': hh_metrics,
                'time_array': time_array.tolist()
            },
            'dbs_stimulus': dbs_stimulus.tolist(),
            'mean_field_strength': float(mean_field_strength)
        }
    
    def _generate_dbs_pattern(self, time_array: np.ndarray, 
                             frequency: float, amplitude: float) -> np.ndarray:
        """
        Generate DBS stimulation pattern.
        
        Args:
            time_array: Time points (ms)
            frequency: Stimulation frequency (Hz)
            amplitude: Stimulation amplitude (relative units)
            
        Returns:
            DBS stimulus pattern
        """
        # Generate square wave pattern typical of DBS
        period = 1000.0 / frequency  # ms
        pulse_width = 0.1  # ms (typical DBS pulse width)
        
        stimulus = np.zeros_like(time_array)
        
        for i, t in enumerate(time_array):
            phase = (t % period) / period
            if phase < (pulse_width / period):
                stimulus[i] = amplitude
            elif phase < (2 * pulse_width / period):  # Biphasic pulse
                stimulus[i] = -amplitude
        
        return stimulus
