import React, { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-dist';

const BrainVisualization = ({ simulationData, isLoading, parameters }) => {
    const plotRef = useRef(null);
    const [visualizationMode, setVisualizationMode] = useState('field');
    const [showElectrode, setShowElectrode] = useState(true);
    const [fieldThreshold, setFieldThreshold] = useState(0.1);

    useEffect(() => {
        if (simulationData && plotRef.current) {
            renderVisualization();
        }
    }, [simulationData, visualizationMode, showElectrode, fieldThreshold]);

    const renderVisualization = () => {
        if (!simulationData || !plotRef.current) return;

        try {
            const { field_data, tissue_data, electrode_data } = simulationData;
            
            if (!field_data || !tissue_data) {
                console.warn('Missing visualization data');
                return;
            }

            const traces = [];

            // Add tissue structure visualization
            if (visualizationMode === 'tissue' || visualizationMode === 'combined') {
                const tissueTrace = createTissueTrace(tissue_data);
                if (tissueTrace) traces.push(tissueTrace);
            }

            // Add electric field visualization
            if (visualizationMode === 'field' || visualizationMode === 'combined') {
                const fieldTrace = createFieldTrace(field_data, fieldThreshold);
                if (fieldTrace) traces.push(fieldTrace);
            }

            // Add electrode visualization
            if (showElectrode && electrode_data) {
                const electrodeTrace = createElectrodeTrace(electrode_data);
                if (electrodeTrace) traces.push(electrodeTrace);
            }

            const layout = {
                title: {
                    text: 'Brain Tissue and Electric Field Distribution',
                    font: { size: 16, color: '#333' }
                },
                scene: {
                    xaxis: { 
                        title: 'X (mm)', 
                        range: [0, tissue_data.physical_size[0]],
                        showgrid: true,
                        gridcolor: '#ddd'
                    },
                    yaxis: { 
                        title: 'Y (mm)', 
                        range: [0, tissue_data.physical_size[1]],
                        showgrid: true,
                        gridcolor: '#ddd'
                    },
                    zaxis: { 
                        title: 'Z (mm)', 
                        range: [0, tissue_data.physical_size[2]],
                        showgrid: true,
                        gridcolor: '#ddd'
                    },
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.5 },
                        center: { x: 0, y: 0, z: 0 }
                    },
                    bgcolor: '#f8f9fa'
                },
                paper_bgcolor: '#ffffff',
                plot_bgcolor: '#f8f9fa',
                margin: { l: 50, r: 50, t: 60, b: 50 },
                showlegend: true,
                legend: {
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255,255,255,0.9)',
                    bordercolor: '#ddd',
                    borderwidth: 1
                }
            };

            const config = {
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
                displaylogo: false,
                toImageButtonOptions: {
                    format: 'png',
                    filename: 'neurotwin_visualization',
                    height: 800,
                    width: 1200,
                    scale: 1
                }
            };

            Plotly.newPlot(plotRef.current, traces, layout, config);

        } catch (error) {
            console.error('Visualization error:', error);
            displayErrorMessage('Failed to render 3D visualization');
        }
    };

    const createTissueTrace = (tissueData) => {
        try {
            const { x_coords, y_coords, z_coords, tissue_type } = tissueData;
            
            if (!x_coords || !y_coords || !z_coords || !tissue_type) return null;

            // Create isosurface for tissue boundaries
            return {
                type: 'isosurface',
                x: x_coords,
                y: y_coords,
                z: z_coords,
                value: tissue_type,
                isomin: 0.5,
                isomax: 2.5,
                surface: { count: 3 },
                colorscale: [
                    [0, '#e8f4fd'],      // CSF - light blue
                    [0.5, '#fff2cc'],    // White matter - light yellow  
                    [1, '#ffe6e6']       // Gray matter - light pink
                ],
                opacity: 0.3,
                name: 'Brain Tissue',
                showscale: false
            };
        } catch (error) {
            console.error('Error creating tissue trace:', error);
            return null;
        }
    };

    const createFieldTrace = (fieldData, threshold) => {
        try {
            const { x_coords, y_coords, z_coords, field_magnitude } = fieldData;
            
            if (!field_magnitude || field_magnitude.length === 0) return null;

            // Flatten arrays for plotly
            const flatField = field_magnitude.flat(3);
            const maxField = Math.max(...flatField);
            
            if (maxField === 0) return null;

            return {
                type: 'volume',
                x: x_coords,
                y: y_coords,
                z: z_coords,
                value: field_magnitude,
                isomin: threshold,
                isomax: maxField,
                surface_count: 5,
                colorscale: [
                    [0, 'rgba(0,0,255,0)'],      // Transparent blue (low field)
                    [0.2, 'rgba(0,100,255,0.3)'], // Light blue
                    [0.4, 'rgba(0,255,100,0.5)'], // Green
                    [0.6, 'rgba(255,255,0,0.7)'], // Yellow
                    [0.8, 'rgba(255,100,0,0.8)'], // Orange
                    [1, 'rgba(255,0,0,0.9)']      // Red (high field)
                ],
                opacity: 0.7,
                name: 'Electric Field',
                colorbar: {
                    title: 'Field Strength (V/m)',
                    titleside: 'right',
                    thickness: 15,
                    len: 0.7
                }
            };
        } catch (error) {
            console.error('Error creating field trace:', error);
            return null;
        }
    };

    const createElectrodeTrace = (electrodeData) => {
        try {
            const { contacts, electrode_position } = electrodeData;
            
            if (!contacts || contacts.length === 0) return null;

            const x = contacts.map(contact => contact.position[0]);
            const y = contacts.map(contact => contact.position[1]);
            const z = contacts.map(contact => contact.position[2]);
            
            const colors = contacts.map(contact => 
                contact.is_active ? '#ff0000' : '#888888'
            );
            
            const sizes = contacts.map(contact => 
                contact.is_active ? 12 : 8
            );

            return {
                type: 'scatter3d',
                mode: 'markers',
                x: x,
                y: y,
                z: z,
                marker: {
                    size: sizes,
                    color: colors,
                    symbol: 'circle',
                    line: {
                        color: '#000000',
                        width: 2
                    }
                },
                name: 'DBS Electrode',
                text: contacts.map((contact, i) => 
                    `Contact ${i}: ${contact.is_active ? 'Active' : 'Inactive'}`
                ),
                hovertemplate: '%{text}<br>Position: (%{x:.1f}, %{y:.1f}, %{z:.1f}) mm<extra></extra>'
            };
        } catch (error) {
            console.error('Error creating electrode trace:', error);
            return null;
        }
    };

    const displayErrorMessage = (message) => {
        if (plotRef.current) {
            plotRef.current.innerHTML = `
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; color: #666;">
                    <div style="text-align: center;">
                        <h3>⚠️ Visualization Error</h3>
                        <p>${message}</p>
                    </div>
                </div>
            `;
        }
    };

    if (isLoading) {
        return (
            <div className="visualization-container">
                <div className="visualization-header">
                    <h3>🧠 Brain Visualization</h3>
                </div>
                <div className="loading-visualization">
                    <div className="loading-spinner large"></div>
                    <p>Running simulation...</p>
                    <small>Computing electric field distribution</small>
                </div>
            </div>
        );
    }

    if (!simulationData) {
        return (
            <div className="visualization-container">
                <div className="visualization-header">
                    <h3>🧠 Brain Visualization</h3>
                </div>
                <div className="no-data-message">
                    <h3>No Simulation Data</h3>
                    <p>Run a simulation to see the 3D brain visualization</p>
                    <p>The visualization will show:</p>
                    <ul>
                        <li>Brain tissue structure</li>
                        <li>Electric field distribution</li>
                        <li>DBS electrode placement</li>
                    </ul>
                </div>
            </div>
        );
    }

    return (
        <div className="visualization-container">
            <div className="visualization-header">
                <h3>🧠 Brain Visualization</h3>
                <div className="visualization-controls">
                    <div className="control-group">
                        <label>View Mode:</label>
                        <select 
                            value={visualizationMode}
                            onChange={(e) => setVisualizationMode(e.target.value)}
                            className="mode-select"
                        >
                            <option value="field">Electric Field Only</option>
                            <option value="tissue">Tissue Only</option>
                            <option value="combined">Combined View</option>
                        </select>
                    </div>
                    
                    <div className="control-group">
                        <label>
                            <input 
                                type="checkbox"
                                checked={showElectrode}
                                onChange={(e) => setShowElectrode(e.target.checked)}
                            />
                            Show Electrode
                        </label>
                    </div>
                    
                    <div className="control-group">
                        <label>Field Threshold:</label>
                        <input 
                            type="range"
                            min="0.01"
                            max="1.0"
                            step="0.01"
                            value={fieldThreshold}
                            onChange={(e) => setFieldThreshold(parseFloat(e.target.value))}
                            className="threshold-slider"
                        />
                        <span className="threshold-value">{fieldThreshold.toFixed(2)} V/m</span>
                    </div>
                </div>
            </div>
            
            <div className="plot-container">
                <div ref={plotRef} style={{ width: '100%', height: '500px' }} />
            </div>
            
            <div className="visualization-info">
                <div className="info-section">
                    <h4>Current Parameters:</h4>
                    <ul>
                        <li>Frequency: {parameters.frequency} Hz</li>
                        <li>Amplitude: {parameters.amplitude} mA</li>
                        <li>Contact: {parameters.contact}</li>
                        <li>Condition: {parameters.condition}</li>
                    </ul>
                </div>
                
                <div className="color-legend">
                    <h4>Color Legend:</h4>
                    <div className="legend-item">
                        <div className="color-box" style={{backgroundColor: '#e8f4fd'}}></div>
                        <span>CSF (Cerebrospinal Fluid)</span>
                    </div>
                    <div className="legend-item">
                        <div className="color-box" style={{backgroundColor: '#fff2cc'}}></div>
                        <span>White Matter</span>
                    </div>
                    <div className="legend-item">
                        <div className="color-box" style={{backgroundColor: '#ffe6e6'}}></div>
                        <span>Gray Matter</span>
                    </div>
                    <div className="legend-item">
                        <div className="color-box" style={{backgroundColor: '#ff0000'}}></div>
                        <span>Active Electrode Contact</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BrainVisualization;
