"""
Brain Tissue Model for DBS Simulation
Educational implementation of 3D brain tissue with electrical properties
"""

import numpy as np
from typing import Tuple, Optional


class BrainTissue:
    """
    3D brain tissue model with realistic electrical properties for DBS simulation.
    Implements gray matter, white matter regions with conductivity variations.
    """
    
    def __init__(self, grid_size: Tuple[int, int, int] = (50, 50, 50)):
        """
        Initialize 3D brain tissue model.
        
        Args:
            grid_size: Dimensions of 3D grid (x, y, z)
        """
        self.grid_size = grid_size
        self.x_dim, self.y_dim, self.z_dim = grid_size
        
        # Physical dimensions in mm
        self.physical_size = (20.0, 20.0, 20.0)  # 20mm x 20mm x 20mm
        self.voxel_size = tuple(p/g for p, g in zip(self.physical_size, grid_size))
        
        # Tissue conductivity values (S/m)
        self.GRAY_MATTER_CONDUCTIVITY = 0.33
        self.WHITE_MATTER_CONDUCTIVITY = 0.14
        self.CSF_CONDUCTIVITY = 1.79
        
        # Initialize tissue properties
        self.conductivity = np.zeros(grid_size)
        self.tissue_type = np.zeros(grid_size, dtype=int)  # 0=CSF, 1=white, 2=gray
        
        self._generate_tissue_structure()
        self._apply_tissue_heterogeneity()
    
    def _generate_tissue_structure(self):
        """Generate realistic brain tissue structure."""
        x, y, z = np.meshgrid(
            np.linspace(0, 1, self.x_dim),
            np.linspace(0, 1, self.y_dim), 
            np.linspace(0, 1, self.z_dim),
            indexing='ij'
        )
        
        # Create center coordinates
        center_x, center_y, center_z = 0.5, 0.5, 0.5
        
        # Distance from center
        distance_from_center = np.sqrt(
            (x - center_x)**2 + (y - center_y)**2 + (z - center_z)**2
        )
        
        # Create brain-like structure
        # Core region (deep structures - white matter dominant)
        core_mask = distance_from_center < 0.2
        self.tissue_type[core_mask] = 1  # White matter
        self.conductivity[core_mask] = self.WHITE_MATTER_CONDUCTIVITY
        
        # Intermediate region (mixed white/gray matter)
        intermediate_mask = (distance_from_center >= 0.2) & (distance_from_center < 0.35)
        # Mix of white and gray matter based on position
        gray_probability = (distance_from_center[intermediate_mask] - 0.2) / 0.15
        random_vals = np.random.random(np.sum(intermediate_mask))
        gray_mask_intermediate = random_vals < gray_probability
        
        intermediate_indices = np.where(intermediate_mask)
        white_indices = tuple(arr[~gray_mask_intermediate] for arr in intermediate_indices)
        gray_indices = tuple(arr[gray_mask_intermediate] for arr in intermediate_indices)
        
        self.tissue_type[white_indices] = 1
        self.conductivity[white_indices] = self.WHITE_MATTER_CONDUCTIVITY
        self.tissue_type[gray_indices] = 2  
        self.conductivity[gray_indices] = self.GRAY_MATTER_CONDUCTIVITY
        
        # Outer region (gray matter - cortical)
        cortical_mask = (distance_from_center >= 0.35) & (distance_from_center < 0.45)
        self.tissue_type[cortical_mask] = 2
        self.conductivity[cortical_mask] = self.GRAY_MATTER_CONDUCTIVITY
        
        # CSF and boundary regions
        boundary_mask = distance_from_center >= 0.45
        self.tissue_type[boundary_mask] = 0
        self.conductivity[boundary_mask] = self.CSF_CONDUCTIVITY
    
    def _apply_tissue_heterogeneity(self):
        """Add realistic tissue variations (±10% conductivity)."""
        # Add heterogeneity only to tissue, not CSF
        tissue_mask = self.tissue_type > 0
        variation = np.random.normal(1.0, 0.1, self.grid_size)
        variation = np.clip(variation, 0.8, 1.2)  # Limit to ±20%
        
        self.conductivity[tissue_mask] *= variation[tissue_mask]
        
        # Ensure positive conductivity
        self.conductivity = np.maximum(self.conductivity, 0.01)
    
    def get_conductivity_at(self, x: float, y: float, z: float) -> float:
        """
        Get conductivity at specific physical coordinates.
        
        Args:
            x, y, z: Physical coordinates in mm
            
        Returns:
            Conductivity value at the specified location
        """
        # Convert physical coordinates to grid indices
        i = int(x / self.voxel_size[0])
        j = int(y / self.voxel_size[1]) 
        k = int(z / self.voxel_size[2])
        
        # Check bounds
        if (0 <= i < self.x_dim and 0 <= j < self.y_dim and 0 <= k < self.z_dim):
            return self.conductivity[i, j, k]
        else:
            return self.CSF_CONDUCTIVITY  # Default to CSF outside tissue
    
    def get_tissue_type_at(self, x: float, y: float, z: float) -> int:
        """Get tissue type at specific coordinates."""
        i = int(x / self.voxel_size[0])
        j = int(y / self.voxel_size[1])
        k = int(z / self.voxel_size[2])
        
        if (0 <= i < self.x_dim and 0 <= j < self.y_dim and 0 <= k < self.z_dim):
            return self.tissue_type[i, j, k]
        else:
            return 0  # CSF
    
    def get_coordinates(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get physical coordinate arrays for visualization."""
        x = np.linspace(0, self.physical_size[0], self.x_dim)
        y = np.linspace(0, self.physical_size[1], self.y_dim)
        z = np.linspace(0, self.physical_size[2], self.z_dim)
        return x, y, z
    
    def get_visualization_data(self) -> dict:
        """Get data formatted for frontend visualization."""
        x, y, z = self.get_coordinates()
        
        return {
            'x_coords': x.tolist(),
            'y_coords': y.tolist(), 
            'z_coords': z.tolist(),
            'conductivity': self.conductivity.tolist(),
            'tissue_type': self.tissue_type.tolist(),
            'grid_size': self.grid_size,
            'physical_size': self.physical_size
        }
