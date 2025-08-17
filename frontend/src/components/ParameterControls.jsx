import React, { useState, useEffect } from 'react';
import { getAvailableConditions, getElectrodeConfigurations } from '../utils/apiClient';

const ParameterControls = ({ parameters, onParameterChange, onRunSimulation, isRunning }) => {
    const [conditions, setConditions] = useState({});
    const [electrodeInfo, setElectrodeInfo] = useState(null);
    const [showAdvanced, setShowAdvanced] = useState(false);

    useEffect(() => {
        // Load available conditions and electrode info
        const loadData = async () => {
            try {
                const [conditionsData, electrodeData] = await Promise.all([
                    getAvailableConditions(),
                    getElectrodeConfigurations()
                ]);
                setConditions(conditionsData.conditions || {});
                setElectrodeInfo(electrodeData);
            } catch (error) {
                console.error('Failed to load parameter data:', error);
            }
        };
        
        loadData();
    }, []);

    const handleSliderChange = (paramName, value) => {
        onParameterChange(paramName, value);
    };

    const getFrequencyDescription = (freq) => {
        if (freq < 50) return "Low frequency: May cause muscle effects";
        if (freq < 100) return "Medium frequency: Partial therapeutic effect";
        if (freq < 180) return "High frequency: Optimal therapeutic range";
        return "Very high frequency: Risk of side effects";
    };

    const getAmplitudeDescription = (amp) => {
        if (amp < 1.0) return "Low amplitude: Minimal effect, good selectivity";
        if (amp < 3.0) return "Medium amplitude: Good therapeutic balance";
        if (amp < 5.0) return "High amplitude: Strong effect, increased side effects";
        return "Very high amplitude: High side effect risk";
    };

    return (
        <div className="parameter-panel">
            <div className="panel-header">
                <h3>🎛️ DBS Parameters</h3>
                <p className="help-text">Adjust settings to see how they affect brain activity</p>
            </div>
            
            <div className="control-group">
                <label htmlFor="condition-select">Brain Condition Simulation:</label>
                <select 
                    id="condition-select"
                    value={parameters.condition}
                    onChange={(e) => onParameterChange('condition', e.target.value)}
                    className="condition-select"
                >
                    {Object.entries(conditions).map(([key, condition]) => (
                        <option key={key} value={key}>
                            {condition.name || key}
                        </option>
                    ))}
                </select>
                {conditions[parameters.condition] && (
                    <small className="condition-description">
                        {conditions[parameters.condition].description}
                    </small>
                )}
            </div>

            <div className="control-group">
                <label htmlFor="frequency-slider">
                    Frequency: <span className="parameter-value">{parameters.frequency} Hz</span>
                </label>
                <input 
                    id="frequency-slider"
                    type="range" 
                    min="1" 
                    max="250" 
                    step="1"
                    value={parameters.frequency}
                    onChange={(e) => handleSliderChange('frequency', e.target.value)}
                    className="parameter-slider"
                />
                <small className="parameter-description">
                    {getFrequencyDescription(parameters.frequency)}
                </small>
            </div>

            <div className="control-group">
                <label htmlFor="amplitude-slider">
                    Amplitude: <span className="parameter-value">{parameters.amplitude} mA</span>
                </label>
                <input 
                    id="amplitude-slider"
                    type="range" 
                    min="0.1" 
                    max="10.0" 
                    step="0.1"
                    value={parameters.amplitude}
                    onChange={(e) => handleSliderChange('amplitude', e.target.value)}
                    className="parameter-slider"
                />
                <small className="parameter-description">
                    {getAmplitudeDescription(parameters.amplitude)}
                </small>
            </div>

            <div className="control-group">
                <label htmlFor="contact-select">
                    Active Contact: <span className="parameter-value">Contact {parameters.contact}</span>
                </label>
                <input 
                    id="contact-slider"
                    type="range" 
                    min="0" 
                    max={electrodeInfo ? electrodeInfo.contact_count - 1 : 3} 
                    step="1"
                    value={parameters.contact}
                    onChange={(e) => handleSliderChange('contact', e.target.value)}
                    className="parameter-slider"
                />
                <small className="parameter-description">
                    Lower contacts = deeper stimulation, Higher contacts = shallower
                </small>
            </div>

            <div className="advanced-toggle">
                <button 
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="toggle-button"
                >
                    {showAdvanced ? '▼' : '▶'} Advanced Parameters
                </button>
            </div>

            {showAdvanced && (
                <div className="advanced-parameters">
                    <div className="control-group">
                        <label htmlFor="pulse-width-slider">
                            Pulse Width: <span className="parameter-value">{parameters.pulse_width} μs</span>
                        </label>
                        <input 
                            id="pulse-width-slider"
                            type="range" 
                            min="30" 
                            max="450" 
                            step="10"
                            value={parameters.pulse_width}
                            onChange={(e) => handleSliderChange('pulse_width', e.target.value)}
                            className="parameter-slider"
                        />
                        <small className="parameter-description">
                            Wider pulses = more charge per pulse, longer neural activation
                        </small>
                    </div>
                </div>
            )}

            <div className="simulation-controls">
                <button 
                    onClick={onRunSimulation}
                    disabled={isRunning}
                    className={`run-simulation-btn ${isRunning ? 'loading' : ''}`}
                >
                    {isRunning ? (
                        <>
                            <div className="spinner"></div>
                            Running Simulation...
                        </>
                    ) : (
                        '🧠 Run Simulation'
                    )}
                </button>
                
                <div className="quick-presets">
                    <p className="presets-label">Quick Presets:</p>
                    <div className="preset-buttons">
                        <button 
                            onClick={() => {
                                onParameterChange('frequency', 130);
                                onParameterChange('amplitude', 2.0);
                                onParameterChange('contact', 0);
                            }}
                            className="preset-btn"
                            title="Standard clinical DBS parameters"
                        >
                            Standard DBS
                        </button>
                        <button 
                            onClick={() => {
                                onParameterChange('frequency', 185);
                                onParameterChange('amplitude', 3.5);
                                onParameterChange('contact', 1);
                            }}
                            className="preset-btn"
                            title="High-frequency parameters for Parkinson's"
                        >
                            High Frequency
                        </button>
                        <button 
                            onClick={() => {
                                onParameterChange('frequency', 60);
                                onParameterChange('amplitude', 4.0);
                                onParameterChange('contact', 0);
                            }}
                            className="preset-btn"
                            title="Lower frequency for dystonia"
                        >
                            Low Frequency
                        </button>
                    </div>
                </div>
            </div>

            <div className="parameter-info">
                <h4>💡 Parameter Tips</h4>
                <ul>
                    <li><strong>Frequency:</strong> Higher values (100-180 Hz) typically provide better symptom control</li>
                    <li><strong>Amplitude:</strong> Start low and increase gradually to find therapeutic window</li>
                    <li><strong>Contact:</strong> Different contacts target different brain regions</li>
                    <li><strong>Condition:</strong> Each condition responds differently to stimulation</li>
                </ul>
            </div>
        </div>
    );
};

export default ParameterControls;
