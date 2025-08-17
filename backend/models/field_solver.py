"""
Electric Field Solver for DBS Simulation
Implements finite difference solution of Poisson equation for electric field propagation
"""

import numpy as np
from scipy.sparse import diags, csr_matrix
from scipy.sparse.linalg import spsolve
from typing import List, Tuple, Optional
from .brain_tissue import BrainTissue


class ElectricFieldSolver:
    """
    Solves the Poisson equation ∇·(σ∇V) = I for electric potential in brain tissue.
    Calculates electric field as E = -∇V.
    """
    
    def __init__(self, tissue: BrainTissue):
        """
        Initialize solver with tissue model.
        
        Args:
            tissue: BrainTissue instance with conductivity distribution
        """
        self.tissue = tissue
        self.grid_size = tissue.grid_size
        self.voxel_size = tissue.voxel_size
        self.dx, self.dy, self.dz = self.voxel_size
        
        # Pre-compute coefficient matrix for efficiency
        self._build_coefficient_matrix()
    
    def _build_coefficient_matrix(self):
        """Build the coefficient matrix for the finite difference discretization."""
        nx, ny, nz = self.grid_size
        n_total = nx * ny * nz
        
        # Initialize matrix data
        data = []
        row_indices = []
        col_indices = []
        
        def get_index(i, j, k):
            """Convert 3D indices to 1D index."""
            return i * ny * nz + j * nz + k
        
        # Build finite difference stencil for each interior point
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    idx = get_index(i, j, k)
                    
                    # Current point conductivity
                    sigma_center = self.tissue.conductivity[i, j, k]
                    
                    # Initialize coefficient for center point
                    center_coeff = 0.0
                    
                    # X-direction derivatives
                    if i > 0:
                        sigma_left = (self.tissue.conductivity[i-1, j, k] + sigma_center) / 2
                        coeff = sigma_left / (self.dx**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i-1, j, k))
                        center_coeff -= coeff
                    
                    if i < nx - 1:
                        sigma_right = (self.tissue.conductivity[i+1, j, k] + sigma_center) / 2
                        coeff = sigma_right / (self.dx**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i+1, j, k))
                        center_coeff -= coeff
                    
                    # Y-direction derivatives
                    if j > 0:
                        sigma_back = (self.tissue.conductivity[i, j-1, k] + sigma_center) / 2
                        coeff = sigma_back / (self.dy**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i, j-1, k))
                        center_coeff -= coeff
                    
                    if j < ny - 1:
                        sigma_front = (self.tissue.conductivity[i, j+1, k] + sigma_center) / 2
                        coeff = sigma_front / (self.dy**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i, j+1, k))
                        center_coeff -= coeff
                    
                    # Z-direction derivatives
                    if k > 0:
                        sigma_down = (self.tissue.conductivity[i, j, k-1] + sigma_center) / 2
                        coeff = sigma_down / (self.dz**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i, j, k-1))
                        center_coeff -= coeff
                    
                    if k < nz - 1:
                        sigma_up = (self.tissue.conductivity[i, j, k+1] + sigma_center) / 2
                        coeff = sigma_up / (self.dz**2)
                        data.append(coeff)
                        row_indices.append(idx)
                        col_indices.append(get_index(i, j, k+1))
                        center_coeff -= coeff
                    
                    # Add center coefficient
                    data.append(center_coeff)
                    row_indices.append(idx)
                    col_indices.append(idx)
        
        self.coefficient_matrix = csr_matrix((data, (row_indices, col_indices)), 
                                           shape=(n_total, n_total))
    
    def solve_potential(self, electrode_positions: List[Tuple[float, float, float]], 
                       amplitudes: List[float], 
                       boundary_condition: str = 'neumann') -> np.ndarray:
        """
        Solve for electric potential distribution.
        
        Args:
            electrode_positions: List of (x, y, z) electrode contact positions in mm
            amplitudes: List of current amplitudes for each contact in mA
            boundary_condition: Type of boundary condition ('neumann' or 'dirichlet')
            
        Returns:
            3D array of electric potential values
        """
        nx, ny, nz = self.grid_size
        n_total = nx * ny * nz
        
        # Create right-hand side vector (current sources)
        rhs = np.zeros(n_total)
        
        def get_index(i, j, k):
            return i * ny * nz + j * nz + k
        
        # Add electrode current sources
        for pos, amplitude in zip(electrode_positions, amplitudes):
            x, y, z = pos
            
            # Convert to grid indices
            i = int(x / self.dx)
            j = int(y / self.dy) 
            k = int(z / self.dz)
            
            # Check bounds
            if (0 <= i < nx and 0 <= j < ny and 0 <= k < nz):
                idx = get_index(i, j, k)
                # Current density in A/m³ (convert mA to A and normalize by voxel volume)
                voxel_volume = self.dx * self.dy * self.dz * 1e-9  # Convert to m³
                current_density = (amplitude * 1e-3) / voxel_volume
                rhs[idx] += current_density
        
        # Apply boundary conditions
        if boundary_condition == 'dirichlet':
            # Set boundary potentials to zero
            self._apply_dirichlet_boundary(rhs)
        
        # Solve the linear system
        try:
            potential_1d = spsolve(self.coefficient_matrix, rhs)
        except Exception as e:
            print(f"Solver failed: {e}")
            # Return zero potential if solver fails
            potential_1d = np.zeros(n_total)
        
        # Reshape to 3D
        potential_3d = potential_1d.reshape(self.grid_size)
        
        return potential_3d
    
    def _apply_dirichlet_boundary(self, rhs: np.ndarray):
        """Apply Dirichlet boundary conditions (V=0 at boundaries)."""
        nx, ny, nz = self.grid_size
        
        def get_index(i, j, k):
            return i * ny * nz + j * nz + k
        
        # Set boundary points
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if (i == 0 or i == nx-1 or 
                        j == 0 or j == ny-1 or 
                        k == 0 or k == nz-1):
                        idx = get_index(i, j, k)
                        
                        # Modify matrix for boundary condition
                        self.coefficient_matrix[idx, :] = 0
                        self.coefficient_matrix[idx, idx] = 1
                        rhs[idx] = 0
    
    def calculate_electric_field(self, potential: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate electric field from potential: E = -∇V
        
        Args:
            potential: 3D potential array
            
        Returns:
            Tuple of (field_magnitude, field_components)
            field_components is array with shape (3, nx, ny, nz) for Ex, Ey, Ez
        """
        # Calculate gradient using numpy (central differences)
        grad_x, grad_y, grad_z = np.gradient(potential, self.dx, self.dy, self.dz)
        
        # Electric field is negative gradient
        Ex = -grad_x
        Ey = -grad_y  
        Ez = -grad_z
        
        # Field magnitude
        field_magnitude = np.sqrt(Ex**2 + Ey**2 + Ez**2)
        
        # Stack components
        field_components = np.stack([Ex, Ey, Ez], axis=0)
        
        return field_magnitude, field_components
    
    def get_field_at_points(self, potential: np.ndarray, 
                           points: List[Tuple[float, float, float]]) -> List[float]:
        """
        Get electric field magnitude at specific points.
        
        Args:
            potential: 3D potential distribution
            points: List of (x, y, z) coordinates in mm
            
        Returns:
            List of field magnitudes at each point
        """
        field_magnitude, _ = self.calculate_electric_field(potential)
        
        field_values = []
        for x, y, z in points:
            # Convert to grid indices
            i = int(x / self.dx)
            j = int(y / self.dy)
            k = int(z / self.dz)
            
            # Check bounds and interpolate
            if (0 <= i < self.grid_size[0] and 
                0 <= j < self.grid_size[1] and 
                0 <= k < self.grid_size[2]):
                field_values.append(float(field_magnitude[i, j, k]))
            else:
                field_values.append(0.0)
        
        return field_values
    
    def get_visualization_data(self, potential: np.ndarray) -> dict:
        """Get field data formatted for frontend visualization."""
        field_magnitude, field_components = self.calculate_electric_field(potential)
        
        # Get coordinate arrays
        x, y, z = self.tissue.get_coordinates()
        
        return {
            'potential': potential.tolist(),
            'field_magnitude': field_magnitude.tolist(),
            'field_components': {
                'Ex': field_components[0].tolist(),
                'Ey': field_components[1].tolist(), 
                'Ez': field_components[2].tolist()
            },
            'x_coords': x.tolist(),
            'y_coords': y.tolist(),
            'z_coords': z.tolist()
        }
