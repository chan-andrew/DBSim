import React, { useState } from 'react';
import { optimizeParameters } from '../utils/apiClient';

const ExplorationPanel = ({ onExplore, currentCondition, explorationData }) => {
    const [isExploring, setIsExploring] = useState(false);
    const [isOptimizing, setIsOptimizing] = useState(false);
    const [explorationMode, setExplorationMode] = useState('comprehensive');
    const [optimizationTarget, setOptimizationTarget] = useState('therapeutic_window');

    const handleParameterExploration = async () => {
        setIsExploring(true);
        
        try {
            const explorationParams = {
                condition: currentCondition,
                exploration_type: explorationMode,
                parameter_ranges: {
                    frequency: [1, 250],
                    amplitude: [0.1, 10.0]
                }
            };
            
            await onExplore(explorationParams);
        } catch (error) {
            console.error('Exploration failed:', error);
        } finally {
            setIsExploring(false);
        }
    };

    const handleOptimization = async () => {
        setIsOptimizing(true);
        
        try {
            const optimizationParams = {
                condition: currentCondition,
                optimization_target: optimizationTarget,
                method: 'differential_evolution'
            };
            
            const results = await optimizeParameters(optimizationParams);
            
            // You could emit these optimal parameters back to the parent
            console.log('Optimization results:', results);
            
        } catch (error) {
            console.error('Optimization failed:', error);
        } finally {
            setIsOptimizing(false);
        }
    };

    return (
        <div className="exploration-panel">
            <div className="panel-header">
                <h3>🔍 Parameter Exploration</h3>
                <p className="help-text">Discover optimal DBS parameters through systematic exploration</p>
            </div>

            <div className="exploration-section">
                <h4>🌐 Parameter Space Exploration</h4>
                <div className="exploration-controls">
                    <div className="control-group">
                        <label>Exploration Mode:</label>
                        <select 
                            value={explorationMode}
                            onChange={(e) => setExplorationMode(e.target.value)}
                            className="mode-select"
                        >
                            <option value="comprehensive">Comprehensive Analysis</option>
                            <option value="frequency_sweep">Frequency Sweep</option>
                            <option value="amplitude_sweep">Amplitude Sweep</option>
                            <option value="quick_survey">Quick Survey</option>
                        </select>
                    </div>
                    
                    <div className="control-description">
                        {explorationMode === 'comprehensive' && 
                            <small>Full 2D parameter space exploration across frequency and amplitude</small>
                        }
                        {explorationMode === 'frequency_sweep' && 
                            <small>Systematic frequency variation at fixed amplitude</small>
                        }
                        {explorationMode === 'amplitude_sweep' && 
                            <small>Systematic amplitude variation at fixed frequency</small>
                        }
                        {explorationMode === 'quick_survey' && 
                            <small>Rapid exploration of key parameter combinations</small>
                        }
                    </div>
                    
                    <button 
                        onClick={handleParameterExploration}
                        disabled={isExploring}
                        className={`explore-btn ${isExploring ? 'loading' : ''}`}
                    >
                        {isExploring ? (
                            <>
                                <div className="spinner small"></div>
                                Exploring...
                            </>
                        ) : (
                            '🗺️ Explore Parameters'
                        )}
                    </button>
                </div>
            </div>

            <div className="optimization-section">
                <h4>🎯 Parameter Optimization</h4>
                <div className="optimization-controls">
                    <div className="control-group">
                        <label>Optimization Target:</label>
                        <select 
                            value={optimizationTarget}
                            onChange={(e) => setOptimizationTarget(e.target.value)}
                            className="target-select"
                        >
                            <option value="therapeutic_window">Therapeutic Window</option>
                            <option value="symptom_improvement">Symptom Improvement</option>
                            <option value="efficiency">Power Efficiency</option>
                        </select>
                    </div>
                    
                    <div className="target-description">
                        {optimizationTarget === 'therapeutic_window' && 
                            <small>Optimize for best balance between efficacy and side effects</small>
                        }
                        {optimizationTarget === 'symptom_improvement' && 
                            <small>Maximize therapeutic benefit regardless of side effects</small>
                        }
                        {optimizationTarget === 'efficiency' && 
                            <small>Optimize for lowest power consumption while maintaining efficacy</small>
                        }
                    </div>
                    
                    <button 
                        onClick={handleOptimization}
                        disabled={isOptimizing}
                        className={`optimize-btn ${isOptimizing ? 'loading' : ''}`}
                    >
                        {isOptimizing ? (
                            <>
                                <div className="spinner small"></div>
                                Optimizing...
                            </>
                        ) : (
                            '⚡ Optimize Parameters'
                        )}
                    </button>
                </div>
            </div>

            {explorationData && (
                <div className="exploration-results">
                    <h4>📈 Exploration Results</h4>
                    <div className="results-summary">
                        {explorationData.exploration_results && (
                            <>
                                {explorationData.exploration_results.frequency_sweep && (
                                    <div className="result-section">
                                        <h5>Frequency Analysis</h5>
                                        <div className="mini-chart">
                                            <p>Frequency sweep completed with {explorationData.exploration_results.frequency_sweep.length} data points</p>
                                            <small>Best frequency range identified</small>
                                        </div>
                                    </div>
                                )}
                                
                                {explorationData.exploration_results.amplitude_sweep && (
                                    <div className="result-section">
                                        <h5>Amplitude Analysis</h5>
                                        <div className="mini-chart">
                                            <p>Amplitude sweep completed with {explorationData.exploration_results.amplitude_sweep.length} data points</p>
                                            <small>Optimal amplitude range determined</small>
                                        </div>
                                    </div>
                                )}
                                
                                {explorationData.exploration_results.optimal_regions && (
                                    <div className="result-section">
                                        <h5>Optimal Regions</h5>
                                        <div className="optimal-regions-list">
                                            {explorationData.exploration_results.optimal_regions.slice(0, 3).map((region, index) => (
                                                <div key={index} className="optimal-region">
                                                    <div className="region-params">
                                                        <span>F: {region.frequency.toFixed(0)} Hz</span>
                                                        <span>A: {region.amplitude.toFixed(1)} mA</span>
                                                    </div>
                                                    <div className="region-score">
                                                        Score: {region.therapeutic_score.toFixed(2)}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </>
                        )}
                        
                        {explorationData.insights && explorationData.insights.length > 0 && (
                            <div className="exploration-insights">
                                <h5>Key Insights</h5>
                                <ul>
                                    {explorationData.insights.slice(0, 3).map((insight, index) => (
                                        <li key={index}>{insight}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            )}

            <div className="exploration-info">
                <h4>📚 Exploration Guide</h4>
                <div className="info-cards">
                    <div className="info-card">
                        <h5>🔬 Parameter Relationships</h5>
                        <p>Frequency and amplitude interact in complex ways. Higher frequencies typically require lower amplitudes for the same effect.</p>
                    </div>
                    
                    <div className="info-card">
                        <h5>⚖️ Trade-offs</h5>
                        <p>Every parameter choice involves trade-offs between therapeutic benefit, side effects, and power consumption.</p>
                    </div>
                    
                    <div className="info-card">
                        <h5>🎯 Optimization Strategy</h5>
                        <p>Start with broad exploration, then use optimization to fine-tune promising parameter regions.</p>
                    </div>
                </div>
            </div>

            <div className="quick-actions">
                <h4>⚡ Quick Actions</h4>
                <div className="action-buttons">
                    <button 
                        onClick={() => onExplore({
                            condition: currentCondition,
                            exploration_type: 'frequency_sweep',
                            parameter_ranges: { frequency: [80, 200], amplitude: [2.0, 2.0] }
                        })}
                        className="quick-action-btn"
                        disabled={isExploring}
                    >
                        🔄 Frequency Sweep
                    </button>
                    
                    <button 
                        onClick={() => onExplore({
                            condition: currentCondition,
                            exploration_type: 'amplitude_sweep',
                            parameter_ranges: { frequency: [130, 130], amplitude: [0.5, 5.0] }
                        })}
                        className="quick-action-btn"
                        disabled={isExploring}
                    >
                        📊 Amplitude Sweep
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ExplorationPanel;
