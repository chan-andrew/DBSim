import React, { useState } from 'react';

const ResultsDisplay = ({ results, parameters, explorationData }) => {
    const [activeTab, setActiveTab] = useState('metrics');

    if (!results) {
        return (
            <div className="results-panel">
                <div className="panel-header">
                    <h3>📊 Simulation Results</h3>
                    <p className="help-text">Results will appear here after running a simulation</p>
                </div>
                <div className="no-results">
                    <div className="placeholder-icon">📈</div>
                    <p>Run a simulation to see detailed results including:</p>
                    <ul>
                        <li>Therapeutic effectiveness</li>
                        <li>Field penetration analysis</li>
                        <li>Neural activity changes</li>
                        <li>Power consumption</li>
                    </ul>
                </div>
            </div>
        );
    }

    const { effects } = results;

    return (
        <div className="results-panel">
            <div className="panel-header">
                <h3>📊 Simulation Results</h3>
                <div className="tab-buttons">
                    <button 
                        className={`tab-btn ${activeTab === 'metrics' ? 'active' : ''}`}
                        onClick={() => setActiveTab('metrics')}
                    >
                        Metrics
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'neural' ? 'active' : ''}`}
                        onClick={() => setActiveTab('neural')}
                    >
                        Neural Activity
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'insights' ? 'active' : ''}`}
                        onClick={() => setActiveTab('insights')}
                    >
                        Insights
                    </button>
                </div>
            </div>

            <div className="tab-content">
                {activeTab === 'metrics' && (
                    <MetricsTab effects={effects} parameters={parameters} />
                )}
                {activeTab === 'neural' && (
                    <NeuralTab results={results} />
                )}
                {activeTab === 'insights' && (
                    <InsightsTab effects={effects} parameters={parameters} explorationData={explorationData} />
                )}
            </div>
        </div>
    );
};

const MetricsTab = ({ effects, parameters }) => {
    const {
        field_metrics,
        neural_metrics,
        therapeutic_metrics,
        efficiency_metrics,
        parameter_effects
    } = effects;

    const formatNumber = (num, decimals = 2) => {
        if (typeof num !== 'number' || isNaN(num)) return 'N/A';
        return num.toFixed(decimals);
    };

    const getScoreColor = (score, thresholds = [0.3, 0.7]) => {
        if (score < thresholds[0]) return 'low';
        if (score < thresholds[1]) return 'medium';
        return 'high';
    };

    return (
        <div className="metrics-content">
            <div className="metric-category">
                <h4>⚡ Electric Field Metrics</h4>
                <div className="metric-grid">
                    <div className="metric-card">
                        <div className="metric-label">Max Field Strength</div>
                        <div className="metric-value">{formatNumber(field_metrics.max_field_strength)} V/m</div>
                        <div className="metric-description">Peak electric field intensity</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">VTA Volume</div>
                        <div className="metric-value">{formatNumber(field_metrics.vta_volume_mm3)} mm³</div>
                        <div className="metric-description">Volume of tissue activated</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Penetration Depth</div>
                        <div className="metric-value">{formatNumber(field_metrics.field_penetration_depth)} mm</div>
                        <div className="metric-description">How deep the field reaches</div>
                    </div>
                </div>
            </div>

            <div className="metric-category">
                <h4>🧠 Neural Response Metrics</h4>
                <div className="metric-grid">
                    <div className="metric-card">
                        <div className="metric-label">Firing Rate Change</div>
                        <div className="metric-value">{formatNumber(neural_metrics.firing_rate_change)} Hz</div>
                        <div className="metric-description">Change in neural firing rate</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Synchrony Index</div>
                        <div className="metric-value score-value">
                            <span className={`score ${getScoreColor(neural_metrics.synchrony_index)}`}>
                                {formatNumber(neural_metrics.synchrony_index)}
                            </span>
                        </div>
                        <div className="metric-description">Population synchronization</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Population Coherence</div>
                        <div className="metric-value">{formatNumber(neural_metrics.population_coherence)}</div>
                        <div className="metric-description">Neural population coordination</div>
                    </div>
                </div>
            </div>

            <div className="metric-category">
                <h4>🎯 Therapeutic Metrics</h4>
                <div className="metric-grid">
                    <div className="metric-card highlight">
                        <div className="metric-label">Symptom Improvement</div>
                        <div className="metric-value large">
                            {formatNumber(therapeutic_metrics.symptom_improvement_percent)}%
                        </div>
                        <div className="metric-description">Primary therapeutic outcome</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Side Effect Score</div>
                        <div className="metric-value score-value">
                            <span className={`score ${getScoreColor(therapeutic_metrics.side_effect_score, [0.2, 0.5])}`}>
                                {formatNumber(therapeutic_metrics.side_effect_score)}
                            </span>
                        </div>
                        <div className="metric-description">Risk of adverse effects</div>
                    </div>
                    <div className="metric-card highlight">
                        <div className="metric-label">Therapeutic Window</div>
                        <div className="metric-value large">
                            {formatNumber(therapeutic_metrics.therapeutic_window)}
                        </div>
                        <div className="metric-description">Benefit vs side effect ratio</div>
                    </div>
                </div>
            </div>

            <div className="metric-category">
                <h4>⚙️ Efficiency Metrics</h4>
                <div className="metric-grid">
                    <div className="metric-card">
                        <div className="metric-label">Power Consumption</div>
                        <div className="metric-value">{formatNumber(efficiency_metrics.power_consumption_mw)} mW</div>
                        <div className="metric-description">Battery drain estimate</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Selectivity Score</div>
                        <div className="metric-value score-value">
                            <span className={`score ${getScoreColor(efficiency_metrics.selectivity_score)}`}>
                                {formatNumber(efficiency_metrics.selectivity_score)}
                            </span>
                        </div>
                        <div className="metric-description">Spatial targeting precision</div>
                    </div>
                    <div className="metric-card">
                        <div className="metric-label">Efficiency Ratio</div>
                        <div className="metric-value">{formatNumber(efficiency_metrics.efficiency_ratio)}</div>
                        <div className="metric-description">Benefit per unit power</div>
                    </div>
                </div>
            </div>

            <div className="parameter-effects-summary">
                <h4>🎛️ Parameter Effects Summary</h4>
                <div className="effects-list">
                    <div className="effect-item">
                        <strong>Frequency Effect:</strong> {parameter_effects.frequency_effect}
                    </div>
                    <div className="effect-item">
                        <strong>Amplitude Effect:</strong> {parameter_effects.amplitude_effect}
                    </div>
                    <div className="effect-item">
                        <strong>Spatial Effect:</strong> {parameter_effects.spatial_effect}
                    </div>
                </div>
            </div>
        </div>
    );
};

const NeuralTab = ({ results }) => {
    const { neural_activity } = results;
    
    if (!neural_activity || !neural_activity.pathological_pattern) {
        return (
            <div className="neural-content">
                <p>Neural activity data not available</p>
            </div>
        );
    }

    const { pathological_pattern, time_array } = neural_activity;

    return (
        <div className="neural-content">
            <div className="neural-section">
                <h4>🔬 Pathological Activity Pattern</h4>
                <div className="pattern-info">
                    <div className="info-card">
                        <div className="info-label">Condition</div>
                        <div className="info-value">{pathological_pattern.condition}</div>
                    </div>
                    {pathological_pattern.pathological_markers && (
                        <>
                            {pathological_pattern.pathological_markers.beta_power_ratio && (
                                <div className="info-card">
                                    <div className="info-label">Beta Power Ratio</div>
                                    <div className="info-value">
                                        {pathological_pattern.pathological_markers.beta_power_ratio.toFixed(2)}
                                    </div>
                                </div>
                            )}
                            {pathological_pattern.pathological_markers.tremor_strength !== undefined && (
                                <div className="info-card">
                                    <div className="info-label">Tremor Strength</div>
                                    <div className="info-value">
                                        {pathological_pattern.pathological_markers.tremor_strength.toFixed(2)}
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>

            <div className="neural-section">
                <h4>📈 Activity Analysis</h4>
                <div className="activity-stats">
                    <div className="stat-item">
                        <div className="stat-label">Mean Activity</div>
                        <div className="stat-value">
                            {(pathological_pattern.neural_activity.reduce((a, b) => a + b, 0) / 
                              pathological_pattern.neural_activity.length).toFixed(2)} Hz
                        </div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-label">Activity Range</div>
                        <div className="stat-value">
                            {Math.min(...pathological_pattern.neural_activity).toFixed(1)} - 
                            {Math.max(...pathological_pattern.neural_activity).toFixed(1)} Hz
                        </div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-label">Variability</div>
                        <div className="stat-value">
                            {(Math.sqrt(pathological_pattern.neural_activity.reduce((acc, val, _, arr) => {
                                const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
                                return acc + Math.pow(val - mean, 2);
                            }, 0) / pathological_pattern.neural_activity.length)).toFixed(2)}
                        </div>
                    </div>
                </div>
            </div>

            <div className="neural-visualization">
                <h4>📊 Activity Pattern Visualization</h4>
                <div className="pattern-preview">
                    <p>Neural activity pattern showing {pathological_pattern.condition} characteristics</p>
                    <small>Full time-series visualization would appear here in a production version</small>
                </div>
            </div>
        </div>
    );
};

const InsightsTab = ({ effects, parameters, explorationData }) => {
    const generateInsights = () => {
        const insights = [];
        
        // Parameter-specific insights
        if (parameters.frequency < 50) {
            insights.push({
                type: 'warning',
                title: 'Low Frequency Warning',
                message: 'Frequencies below 50 Hz may cause muscle contractions and worsen symptoms. Consider increasing frequency.'
            });
        } else if (parameters.frequency > 180) {
            insights.push({
                type: 'caution',
                title: 'High Frequency Caution',
                message: 'Very high frequencies may cause speech or cognitive side effects. Monitor carefully.'
            });
        } else {
            insights.push({
                type: 'success',
                title: 'Optimal Frequency Range',
                message: 'Current frequency is in the therapeutic range for most DBS applications.'
            });
        }

        // Amplitude insights
        if (parameters.amplitude > 5.0) {
            insights.push({
                type: 'warning',
                title: 'High Amplitude Risk',
                message: 'High amplitude increases side effect risk. Consider reducing amplitude or optimizing other parameters.'
            });
        }

        // Therapeutic window insights
        const therapeuticWindow = effects.therapeutic_metrics?.therapeutic_window || 0;
        if (therapeuticWindow > 0.7) {
            insights.push({
                type: 'success',
                title: 'Excellent Therapeutic Window',
                message: 'Great balance between therapeutic benefit and side effects.'
            });
        } else if (therapeuticWindow < 0.3) {
            insights.push({
                type: 'warning',
                title: 'Poor Therapeutic Window',
                message: 'Consider parameter optimization to improve benefit-to-side-effect ratio.'
            });
        }

        // Power consumption insights
        const powerConsumption = effects.efficiency_metrics?.power_consumption_mw || 0;
        if (powerConsumption > 10) {
            insights.push({
                type: 'info',
                title: 'High Power Consumption',
                message: 'Current settings may reduce battery life. Consider efficiency optimization.'
            });
        }

        // Condition-specific insights
        if (parameters.condition === 'parkinson') {
            insights.push({
                type: 'info',
                title: 'Parkinson\'s Disease Optimization',
                message: 'For Parkinson\'s, focus on disrupting beta oscillations (13-30 Hz) with high-frequency stimulation.'
            });
        }

        return insights;
    };

    const insights = generateInsights();

    return (
        <div className="insights-content">
            <div className="insights-section">
                <h4>💡 Parameter Insights</h4>
                <div className="insights-list">
                    {insights.map((insight, index) => (
                        <div key={index} className={`insight-card ${insight.type}`}>
                            <div className="insight-header">
                                <span className="insight-icon">
                                    {insight.type === 'success' && '✅'}
                                    {insight.type === 'warning' && '⚠️'}
                                    {insight.type === 'caution' && '⚡'}
                                    {insight.type === 'info' && 'ℹ️'}
                                </span>
                                <h5>{insight.title}</h5>
                            </div>
                            <p>{insight.message}</p>
                        </div>
                    ))}
                </div>
            </div>

            {explorationData && (
                <div className="insights-section">
                    <h4>🔍 Exploration Insights</h4>
                    <div className="exploration-insights">
                        {explorationData.insights && explorationData.insights.map((insight, index) => (
                            <div key={index} className="insight-card info">
                                <p>{insight}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className="insights-section">
                <h4>📚 Educational Notes</h4>
                <div className="educational-notes">
                    <div className="note-card">
                        <h5>🧠 DBS Mechanism</h5>
                        <p>DBS works by modulating abnormal neural activity patterns. High-frequency stimulation typically disrupts pathological oscillations and restores more normal brain function.</p>
                    </div>
                    <div className="note-card">
                        <h5>⚖️ Parameter Balance</h5>
                        <p>Effective DBS requires balancing therapeutic benefit with side effects. The therapeutic window represents this balance.</p>
                    </div>
                    <div className="note-card">
                        <h5>🎯 Targeting Precision</h5>
                        <p>Selectivity is crucial - you want to stimulate target regions while avoiding off-target effects that cause side effects.</p>
                    </div>
                </div>
            </div>

            <div className="recommendations-section">
                <h4>🎯 Optimization Recommendations</h4>
                <div className="recommendations-list">
                    <div className="recommendation-item">
                        <strong>Next Steps:</strong> Try parameter exploration to find optimal settings for this condition
                    </div>
                    <div className="recommendation-item">
                        <strong>Frequency:</strong> Test frequencies between 100-180 Hz for best therapeutic results
                    </div>
                    <div className="recommendation-item">
                        <strong>Amplitude:</strong> Start low and gradually increase to find minimum effective dose
                    </div>
                    <div className="recommendation-item">
                        <strong>Contacts:</strong> Try different electrode contacts to optimize targeting
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultsDisplay;
