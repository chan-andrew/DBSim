"""
DBS Electrode Model
Implements realistic electrode geometry and current injection for DBS simulation
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass


@dataclass
class ElectrodeContact:
    """Represents a single electrode contact."""
    position: Tuple[float, float, float]  # (x, y, z) in mm
    radius: float  # Contact radius in mm
    height: float  # Contact height in mm
    impedance: float  # Contact impedance in Ohms
    is_active: bool = True


class DBSElectrode:
    """
    DBS electrode model with realistic geometry and electrical properties.
    Based on standard DBS electrode specifications (e.g., Medtronic 3389).
    """
    
    def __init__(self, position: Tuple[float, float, float], 
                 orientation: Tuple[float, float, float] = (0, 0, 1),
                 electrode_type: str = "quadripolar"):
        """
        Initialize DBS electrode.
        
        Args:
            position: Electrode tip position (x, y, z) in mm
            orientation: Electrode direction vector (normalized)
            electrode_type: Type of electrode ("quadripolar", "directional")
        """
        self.position = np.array(position)
        self.orientation = np.array(orientation) / np.linalg.norm(orientation)
        self.electrode_type = electrode_type
        
        # Standard DBS electrode dimensions (Medtronic 3389-like)
        self.diameter = 1.27  # mm
        self.contact_height = 1.5  # mm
        self.contact_spacing = 0.5  # mm between contacts
        self.contact_radius = self.diameter / 2
        
        # Initialize contacts
        self.contacts = self._generate_contacts()
        
        # Default stimulation parameters
        self.stimulation_mode = "monopolar"  # or "bipolar"
        self.active_contacts = [0]  # Contact indices that are active
        
    def _generate_contacts(self) -> List[ElectrodeContact]:
        """Generate electrode contacts based on electrode type."""
        contacts = []
        
        if self.electrode_type == "quadripolar":
            # Generate 4 contacts along electrode shaft
            for i in range(4):
                # Position along electrode shaft
                contact_center = (self.position + 
                                self.orientation * (i * (self.contact_height + self.contact_spacing)))
                
                # Calculate impedance (varies with contact area and tissue interface)
                base_impedance = 1000.0  # Base impedance in Ohms
                area_factor = 2 * np.pi * self.contact_radius * self.contact_height
                impedance = base_impedance / area_factor
                
                contact = ElectrodeContact(
                    position=tuple(contact_center),
                    radius=self.contact_radius,
                    height=self.contact_height,
                    impedance=impedance,
                    is_active=(i in [0, 1])  # Default: contacts 0 and 1 active
                )
                contacts.append(contact)
                
        elif self.electrode_type == "directional":
            # Directional leads with segmented contacts
            for i in range(8):  # 8 directional contacts
                if i < 4:
                    # Ring contact at tip
                    contact_center = self.position + self.orientation * 0.5
                    radius = self.contact_radius
                else:
                    # Segmented contacts
                    level = (i - 4) // 3
                    segment = (i - 4) % 3
                    contact_center = (self.position + 
                                    self.orientation * (1.5 + level * 2.0))
                    # Add angular offset for segments
                    angle = segment * 2 * np.pi / 3
                    perpendicular = np.array([-self.orientation[1], self.orientation[0], 0])
                    perpendicular = perpendicular / np.linalg.norm(perpendicular)
                    offset = perpendicular * self.contact_radius * 0.7 * np.cos(angle)
                    contact_center = contact_center + offset
                    radius = self.contact_radius * 0.6
                
                impedance = 800.0 + np.random.normal(0, 100)  # Variable impedance
                
                contact = ElectrodeContact(
                    position=tuple(contact_center),
                    radius=radius,
                    height=self.contact_height * 0.7,
                    impedance=abs(impedance),
                    is_active=False
                )
                contacts.append(contact)
        
        return contacts
    
    def set_stimulation_configuration(self, mode: str, active_contacts: List[int],
                                    amplitudes: Optional[List[float]] = None):
        """
        Configure stimulation parameters.
        
        Args:
            mode: Stimulation mode ("monopolar", "bipolar", "multipolar")
            active_contacts: List of contact indices to activate
            amplitudes: Current amplitudes for each active contact (mA)
        """
        self.stimulation_mode = mode
        self.active_contacts = active_contacts
        
        # Reset all contacts
        for contact in self.contacts:
            contact.is_active = False
        
        # Activate specified contacts
        for idx in active_contacts:
            if 0 <= idx < len(self.contacts):
                self.contacts[idx].is_active = True
        
        # Set amplitudes
        if amplitudes is None:
            if mode == "monopolar":
                amplitudes = [2.0] * len(active_contacts)  # Default 2mA
            elif mode == "bipolar":
                amplitudes = [2.0, -2.0]  # Biphasic
        
        self.amplitudes = amplitudes[:len(active_contacts)]
    
    def get_current_density_distribution(self, tissue_conductivity: np.ndarray,
                                       grid_coordinates: Tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
        """
        Calculate current density distribution from active contacts.
        
        Args:
            tissue_conductivity: 3D conductivity array
            grid_coordinates: (x, y, z) coordinate arrays
            
        Returns:
            3D current density array (A/m³)
        """
        x_coords, y_coords, z_coords = grid_coordinates
        current_density = np.zeros_like(tissue_conductivity)
        
        for i, contact_idx in enumerate(self.active_contacts):
            if contact_idx >= len(self.contacts):
                continue
                
            contact = self.contacts[contact_idx]
            if not contact.is_active:
                continue
                
            # Get contact properties
            cx, cy, cz = contact.position
            amplitude = self.amplitudes[i] if i < len(self.amplitudes) else 1.0
            
            # Calculate distance from contact
            distance = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2 + (z_coords - cz)**2)
            
            # Current density model (simplified point source with tissue impedance)
            contact_area = 2 * np.pi * contact.radius * contact.height  # mm²
            contact_area_m2 = contact_area * 1e-6  # Convert to m²
            
            # Avoid division by zero
            safe_distance = np.maximum(distance, 0.1)  # Minimum 0.1mm
            
            # Current density decreases with distance and tissue impedance
            local_current_density = (amplitude * 1e-3) / (4 * np.pi * safe_distance**2 * 1e-6)  # A/m²
            
            # Apply only near the contact (within reasonable distance)
            mask = distance < (contact.radius * 5)  # Within 5 radii
            current_density[mask] += local_current_density[mask] / contact_area_m2
        
        return current_density
    
    def calculate_voltage_at_contacts(self, potential_field: np.ndarray,
                                    grid_coordinates: Tuple[np.ndarray, np.ndarray, np.ndarray]) -> List[float]:
        """
        Calculate voltage at each contact position.
        
        Args:
            potential_field: 3D potential array (V)
            grid_coordinates: (x, y, z) coordinate arrays
            
        Returns:
            List of voltages at each contact
        """
        x_coords, y_coords, z_coords = grid_coordinates
        contact_voltages = []
        
        for contact in self.contacts:
            cx, cy, cz = contact.position
            
            # Find nearest grid point
            x_idx = np.argmin(np.abs(x_coords[:, 0, 0] - cx))
            y_idx = np.argmin(np.abs(y_coords[0, :, 0] - cy))
            z_idx = np.argmin(np.abs(z_coords[0, 0, :] - cz))
            
            # Bounds checking
            x_idx = max(0, min(x_idx, potential_field.shape[0] - 1))
            y_idx = max(0, min(y_idx, potential_field.shape[1] - 1))
            z_idx = max(0, min(z_idx, potential_field.shape[2] - 1))
            
            voltage = potential_field[x_idx, y_idx, z_idx]
            contact_voltages.append(float(voltage))
        
        return contact_voltages
    
    def get_electrode_geometry(self) -> Dict:
        """Get electrode geometry data for visualization."""
        contact_data = []
        
        for i, contact in enumerate(self.contacts):
            contact_data.append({
                'id': i,
                'position': contact.position,
                'radius': contact.radius,
                'height': contact.height,
                'is_active': contact.is_active,
                'impedance': contact.impedance
            })
        
        return {
            'electrode_position': self.position.tolist(),
            'electrode_orientation': self.orientation.tolist(),
            'electrode_type': self.electrode_type,
            'contacts': contact_data,
            'stimulation_mode': self.stimulation_mode,
            'active_contacts': self.active_contacts,
            'amplitudes': getattr(self, 'amplitudes', [])
        }
    
    def optimize_contact_selection(self, field_data: Dict, target_region: Dict) -> Dict:
        """
        Optimize contact selection for targeting specific brain region.
        
        Args:
            field_data: Electric field distribution data
            target_region: Target region specifications
            
        Returns:
            Optimized stimulation configuration
        """
        # Simplified optimization algorithm
        best_configuration = None
        best_score = 0
        
        # Test different contact combinations
        for n_contacts in range(1, min(4, len(self.contacts) + 1)):
            for contact_combination in self._generate_contact_combinations(n_contacts):
                # Test this configuration
                score = self._evaluate_configuration(contact_combination, field_data, target_region)
                
                if score > best_score:
                    best_score = score
                    best_configuration = contact_combination
        
        return {
            'best_contacts': best_configuration,
            'optimization_score': best_score,
            'recommended_amplitude': self._calculate_optimal_amplitude(best_configuration)
        }
    
    def _generate_contact_combinations(self, n_contacts: int) -> List[List[int]]:
        """Generate all possible combinations of n contacts."""
        from itertools import combinations
        contact_indices = list(range(len(self.contacts)))
        return [list(combo) for combo in combinations(contact_indices, n_contacts)]
    
    def _evaluate_configuration(self, contact_indices: List[int], 
                              field_data: Dict, target_region: Dict) -> float:
        """Evaluate how well a contact configuration targets the desired region."""
        # Simplified scoring based on field strength in target vs off-target regions
        # This would be more sophisticated in a real implementation
        
        if not contact_indices:
            return 0
        
        # Calculate field strength at target and off-target locations
        field_magnitude = np.array(field_data.get('field_magnitude', []))
        if field_magnitude.size == 0:
            return 0
        
        # Target scoring (simplified)
        target_score = np.mean(field_magnitude) * len(contact_indices)
        
        # Penalize for too many contacts (prefer selective stimulation)
        selectivity_penalty = len(contact_indices) * 0.1
        
        return max(0, target_score - selectivity_penalty)
    
    def _calculate_optimal_amplitude(self, contact_indices: List[int]) -> float:
        """Calculate optimal amplitude for given contact configuration."""
        # Simplified amplitude calculation
        base_amplitude = 2.0  # mA
        
        if not contact_indices:
            return base_amplitude
        
        # Adjust based on number of contacts
        amplitude = base_amplitude / np.sqrt(len(contact_indices))
        
        return min(amplitude, 10.0)  # Cap at 10mA for safety
