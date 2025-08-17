import React, { useState, useEffect } from 'react';

const TutorialMode = ({ onComplete, onParameterChange, onRunSimulation, simulationState }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const [isSimulationRunning, setIsSimulationRunning] = useState(false);

    const tutorialSteps = [
        {
            title: "Welcome to NeuroTwin! 🧠",
            content: (
                <div>
                    <h3>Deep Brain Stimulation Simulator</h3>
                    <p>NeuroTwin is an educational tool that lets you explore how electrical stimulation affects brain tissue and neural activity.</p>
                    <div className="tutorial-highlights">
                        <div className="highlight-item">
                            <span className="icon">⚡</span>
                            <div>
                                <strong>Electric Field Simulation</strong>
                                <p>See how electrical current spreads through brain tissue</p>
                            </div>
                        </div>
                        <div className="highlight-item">
                            <span className="icon">🧠</span>
                            <div>
                                <strong>Neural Activity Modeling</strong>
                                <p>Understand how neurons respond to stimulation</p>
                            </div>
                        </div>
                        <div className="highlight-item">
                            <span className="icon">🎛️</span>
                            <div>
                                <strong>Parameter Exploration</strong>
                                <p>Learn how different settings affect outcomes</p>
                            </div>
                        </div>
                    </div>
                    <div className="tutorial-note">
                        <strong>Note:</strong> This is an educational simulation, not a clinical tool. It demonstrates DBS principles in a simplified but scientifically-grounded way.
                    </div>
                </div>
            ),
            action: null
        },
        {
            title: "Understanding Brain Conditions 🩺",
            content: (
                <div>
                    <h3>Neurological Conditions</h3>
                    <p>Let's start by understanding different brain conditions that DBS can help treat:</p>
                    <div className="condition-cards">
                        <div className="condition-card">
                            <h4>🏃‍♂️ Parkinson's Disease</h4>
                            <p>Characterized by excessive beta oscillations (13-30 Hz) that disrupt normal movement control.</p>
                            <ul>
                                <li>Tremor at rest</li>
                                <li>Bradykinesia (slow movements)</li>
                                <li>Muscle rigidity</li>
                            </ul>
                        </div>
                        <div className="condition-card">
                            <h4>🌀 Dystonia</h4>
                            <p>Involves irregular muscle contractions causing abnormal postures and movements.</p>
                            <ul>
                                <li>Involuntary muscle contractions</li>
                                <li>Abnormal postures</li>
                                <li>Irregular activity patterns</li>
                            </ul>
                        </div>
                        <div className="condition-card">
                            <h4>📳 Essential Tremor</h4>
                            <p>Rhythmic shaking movements, especially during voluntary actions.</p>
                            <ul>
                                <li>Action tremor (6-12 Hz)</li>
                                <li>Affects hands, head, voice</li>
                                <li>Worsens with stress</li>
                            </ul>
                        </div>
                    </div>
                </div>
            ),
            action: () => onParameterChange('condition', 'parkinson')
        },
        {
            title: "DBS Parameters: Frequency ⚡",
            content: (
                <div>
                    <h3>Understanding Frequency</h3>
                    <p>Frequency is how many electrical pulses are delivered per second, measured in Hertz (Hz).</p>
                    <div className="frequency-guide">
                        <div className="freq-range low">
                            <h4>Low Frequency (1-50 Hz)</h4>
                            <p>❌ Can worsen symptoms</p>
                            <p>❌ May cause muscle contractions</p>
                            <p>❌ Generally avoided in DBS</p>
                        </div>
                        <div className="freq-range medium">
                            <h4>Medium Frequency (50-100 Hz)</h4>
                            <p>⚠️ Partial therapeutic effects</p>
                            <p>⚠️ Some side effects possible</p>
                            <p>⚠️ Used in specific cases</p>
                        </div>
                        <div className="freq-range high">
                            <h4>High Frequency (100-180 Hz)</h4>
                            <p>✅ Optimal therapeutic range</p>
                            <p>✅ Disrupts pathological signals</p>
                            <p>✅ Standard for most conditions</p>
                        </div>
                    </div>
                    <p><strong>Try this:</strong> Let's set frequency to 130 Hz (a common therapeutic setting)</p>
                </div>
            ),
            action: () => onParameterChange('frequency', 130)
        },
        {
            title: "DBS Parameters: Amplitude 📊",
            content: (
                <div>
                    <h3>Understanding Amplitude</h3>
                    <p>Amplitude controls how much electrical current is delivered, measured in milliamps (mA).</p>
                    <div className="amplitude-guide">
                        <div className="amp-level">
                            <h4>Low Amplitude (0.5-1.5 mA)</h4>
                            <p>• Minimal side effects</p>
                            <p>• Limited therapeutic benefit</p>
                            <p>• Good for testing tolerance</p>
                        </div>
                        <div className="amp-level">
                            <h4>Medium Amplitude (1.5-4.0 mA)</h4>
                            <p>• Good therapeutic balance</p>
                            <p>• Manageable side effects</p>
                            <p>• Most common range</p>
                        </div>
                        <div className="amp-level">
                            <h4>High Amplitude (4.0+ mA)</h4>
                            <p>• Strong therapeutic effect</p>
                            <p>• Increased side effect risk</p>
                            <p>• Used when necessary</p>
                        </div>
                    </div>
                    <p><strong>Key Concept:</strong> Higher amplitude creates a larger "volume of tissue activated" (VTA)</p>
                    <p><strong>Try this:</strong> Let's set amplitude to 2.0 mA (a typical starting point)</p>
                </div>
            ),
            action: () => onParameterChange('amplitude', 2.0)
        },
        {
            title: "Electrode Contacts 🔌",
            content: (
                <div>
                    <h3>DBS Electrode Contacts</h3>
                    <p>DBS electrodes have multiple contacts (usually 4) that can be activated individually.</p>
                    <div className="electrode-diagram">
                        <div className="electrode-visual">
                            <div className="contact active">Contact 0 (deepest)</div>
                            <div className="contact">Contact 1</div>
                            <div className="contact">Contact 2</div>
                            <div className="contact">Contact 3 (shallowest)</div>
                        </div>
                        <div className="contact-info">
                            <h4>Contact Selection Strategy:</h4>
                            <ul>
                                <li><strong>Contact 0:</strong> Deepest, targets deep brain structures</li>
                                <li><strong>Contact 1:</strong> Mid-deep level</li>
                                <li><strong>Contact 2:</strong> Mid-shallow level</li>
                                <li><strong>Contact 3:</strong> Shallowest, closer to surface</li>
                            </ul>
                            <p><strong>Clinical Tip:</strong> Start with contact 1 or 2, then adjust based on response</p>
                        </div>
                    </div>
                    <p><strong>Try this:</strong> Let's use Contact 0 (deepest contact)</p>
                </div>
            ),
            action: () => onParameterChange('contact', 0)
        },
        {
            title: "Running Your First Simulation 🚀",
            content: (
                <div>
                    <h3>Let's Run a Simulation!</h3>
                    <p>Now we'll run a simulation with the parameters we've set:</p>
                    <div className="current-params">
                        <h4>Current Parameters:</h4>
                        <ul>
                            <li>Condition: {simulationState.parameters.condition}</li>
                            <li>Frequency: {simulationState.parameters.frequency} Hz</li>
                            <li>Amplitude: {simulationState.parameters.amplitude} mA</li>
                            <li>Contact: {simulationState.parameters.contact}</li>
                        </ul>
                    </div>
                    <div className="simulation-info">
                        <h4>What the simulation calculates:</h4>
                        <ul>
                            <li>🔄 Electric field distribution in brain tissue</li>
                            <li>🧠 Neural population responses</li>
                            <li>📊 Therapeutic effectiveness metrics</li>
                            <li>⚡ Power consumption estimates</li>
                            <li>🎯 Side effect predictions</li>
                        </ul>
                    </div>
                    <p><strong>Click the button below to run your first simulation!</strong></p>
                </div>
            ),
            action: () => {
                setIsSimulationRunning(true);
                onRunSimulation();
            }
        },
        {
            title: "Understanding Results 📈",
            content: (
                <div>
                    <h3>Interpreting Your Results</h3>
                    {simulationState.results ? (
                        <div>
                            <p>Great! Your simulation is complete. Here's what to look for:</p>
                            <div className="results-guide">
                                <div className="result-section">
                                    <h4>🎯 Therapeutic Metrics</h4>
                                    <p>• <strong>Symptom Improvement:</strong> How much the condition improves</p>
                                    <p>• <strong>Side Effect Score:</strong> Risk of adverse effects</p>
                                    <p>• <strong>Therapeutic Window:</strong> Benefit vs. side effect ratio</p>
                                </div>
                                <div className="result-section">
                                    <h4>⚡ Field Metrics</h4>
                                    <p>• <strong>VTA Volume:</strong> How much tissue is activated</p>
                                    <p>• <strong>Field Strength:</strong> Intensity of electrical stimulation</p>
                                    <p>• <strong>Penetration Depth:</strong> How deep the effect reaches</p>
                                </div>
                                <div className="result-section">
                                    <h4>🧠 Neural Metrics</h4>
                                    <p>• <strong>Firing Rate Change:</strong> How neuron activity changes</p>
                                    <p>• <strong>Synchrony Index:</strong> Population coordination</p>
                                </div>
                            </div>
                            <p><strong>Check the Results panel on the right to see your detailed metrics!</strong></p>
                        </div>
                    ) : (
                        <div>
                            <p>Waiting for simulation to complete...</p>
                            <div className="loading-message">
                                <div className="spinner"></div>
                                <p>Running computational models...</p>
                            </div>
                        </div>
                    )}
                </div>
            ),
            action: null
        },
        {
            title: "3D Visualization 🌟",
            content: (
                <div>
                    <h3>Exploring the 3D Brain View</h3>
                    <p>The center panel shows a 3D visualization of your simulation:</p>
                    <div className="viz-guide">
                        <div className="viz-element">
                            <h4>🧠 Brain Tissue</h4>
                            <p>Different colors represent different tissue types:</p>
                            <ul>
                                <li><span className="color-sample csf"></span> CSF (Cerebrospinal Fluid)</li>
                                <li><span className="color-sample white"></span> White Matter</li>
                                <li><span className="color-sample gray"></span> Gray Matter</li>
                            </ul>
                        </div>
                        <div className="viz-element">
                            <h4>⚡ Electric Field</h4>
                            <p>Color-coded field strength:</p>
                            <ul>
                                <li><span className="color-sample field-low"></span> Low Field (Blue)</li>
                                <li><span className="color-sample field-med"></span> Medium Field (Green/Yellow)</li>
                                <li><span className="color-sample field-high"></span> High Field (Red)</li>
                            </ul>
                        </div>
                        <div className="viz-element">
                            <h4>📍 DBS Electrode</h4>
                            <p>Red dots show active contacts, gray dots show inactive contacts</p>
                        </div>
                    </div>
                    <p><strong>Try:</strong> Use the visualization controls to change view modes and explore the 3D model!</p>
                </div>
            ),
            action: null
        },
        {
            title: "Parameter Exploration 🔍",
            content: (
                <div>
                    <h3>Exploring Parameter Effects</h3>
                    <p>Now let's learn how different parameters affect the outcomes:</p>
                    <div className="exploration-exercises">
                        <div className="exercise">
                            <h4>Exercise 1: Frequency Effects</h4>
                            <p>Try changing the frequency and running new simulations:</p>
                            <ul>
                                <li>Low frequency: 50 Hz</li>
                                <li>Medium frequency: 100 Hz</li>
                                <li>High frequency: 180 Hz</li>
                            </ul>
                            <p><strong>Observe:</strong> How does therapeutic improvement change?</p>
                        </div>
                        <div className="exercise">
                            <h4>Exercise 2: Amplitude Effects</h4>
                            <p>Try different amplitudes:</p>
                            <ul>
                                <li>Low amplitude: 1.0 mA</li>
                                <li>Medium amplitude: 3.0 mA</li>
                                <li>High amplitude: 5.0 mA</li>
                            </ul>
                            <p><strong>Observe:</strong> How do side effects and power consumption change?</p>
                        </div>
                        <div className="exercise">
                            <h4>Exercise 3: Different Conditions</h4>
                            <p>Try different brain conditions:</p>
                            <ul>
                                <li>Healthy brain</li>
                                <li>Parkinson's disease</li>
                                <li>Essential tremor</li>
                                <li>Dystonia</li>
                            </ul>
                            <p><strong>Observe:</strong> How do optimal parameters differ?</p>
                        </div>
                    </div>
                </div>
            ),
            action: null
        },
        {
            title: "Advanced Features 🚀",
            content: (
                <div>
                    <h3>Advanced NeuroTwin Features</h3>
                    <p>Once you're comfortable with basic simulations, explore these advanced features:</p>
                    <div className="advanced-features">
                        <div className="feature">
                            <h4>🌐 Parameter Space Exploration</h4>
                            <p>Use the left panel's exploration tools to systematically test parameter combinations and find optimal settings.</p>
                        </div>
                        <div className="feature">
                            <h4>🎯 Automatic Optimization</h4>
                            <p>Let NeuroTwin automatically find the best parameters for your chosen condition and optimization target.</p>
                        </div>
                        <div className="feature">
                            <h4>📊 Detailed Metrics</h4>
                            <p>Explore the Results panel tabs for detailed therapeutic, neural, and efficiency metrics.</p>
                        </div>
                        <div className="feature">
                            <h4>💡 Educational Insights</h4>
                            <p>Check the Insights tab for personalized recommendations and educational explanations.</p>
                        </div>
                    </div>
                    <div className="learning-tips">
                        <h4>💡 Learning Tips:</h4>
                        <ul>
                            <li>Start with standard parameters (130 Hz, 2 mA) and adjust gradually</li>
                            <li>Pay attention to the therapeutic window - it balances benefit vs. side effects</li>
                            <li>Compare results across different conditions to understand DBS mechanisms</li>
                            <li>Use parameter exploration to build intuition about parameter relationships</li>
                        </ul>
                    </div>
                </div>
            ),
            action: null
        },
        {
            title: "Ready to Explore! 🎓",
            content: (
                <div>
                    <h3>Congratulations!</h3>
                    <p>You've completed the NeuroTwin tutorial. You now understand:</p>
                    <div className="completion-checklist">
                        <div className="check-item">✅ How DBS parameters affect brain stimulation</div>
                        <div className="check-item">✅ The importance of frequency, amplitude, and contact selection</div>
                        <div className="check-item">✅ How to interpret simulation results</div>
                        <div className="check-item">✅ How to use the 3D visualization</div>
                        <div className="check-item">✅ Advanced exploration and optimization features</div>
                    </div>
                    <div className="next-steps">
                        <h4>🚀 Next Steps:</h4>
                        <ol>
                            <li>Experiment with different parameter combinations</li>
                            <li>Compare how different conditions respond to DBS</li>
                            <li>Use parameter exploration to find optimal settings</li>
                            <li>Try the optimization features for automatic parameter tuning</li>
                            <li>Explore the educational insights for deeper understanding</li>
                        </ol>
                    </div>
                    <div className="reminder">
                        <p><strong>Remember:</strong> NeuroTwin is for educational purposes only. It demonstrates DBS principles but should not be used for clinical decisions.</p>
                    </div>
                    <p><strong>Click "Complete Tutorial" to start your exploration!</strong></p>
                </div>
            ),
            action: null
        }
    ];

    useEffect(() => {
        if (isSimulationRunning && simulationState.results && !simulationState.isRunning) {
            setIsSimulationRunning(false);
        }
    }, [simulationState.results, simulationState.isRunning, isSimulationRunning]);

    const nextStep = () => {
        if (tutorialSteps[currentStep].action) {
            tutorialSteps[currentStep].action();
        }
        if (currentStep < tutorialSteps.length - 1) {
            setCurrentStep(currentStep + 1);
        }
    };

    const prevStep = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const skipTutorial = () => {
        onComplete();
    };

    return (
        <div className="tutorial-overlay">
            <div className="tutorial-container">
                <div className="tutorial-header">
                    <div className="tutorial-progress">
                        <div className="progress-bar">
                            <div 
                                className="progress-fill" 
                                style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
                            ></div>
                        </div>
                        <span className="progress-text">
                            Step {currentStep + 1} of {tutorialSteps.length}
                        </span>
                    </div>
                    <button onClick={skipTutorial} className="skip-button">
                        Skip Tutorial
                    </button>
                </div>

                <div className="tutorial-content">
                    <h2>{tutorialSteps[currentStep].title}</h2>
                    <div className="tutorial-body">
                        {tutorialSteps[currentStep].content}
                    </div>
                </div>

                <div className="tutorial-navigation">
                    <button 
                        onClick={prevStep}
                        disabled={currentStep === 0}
                        className="nav-button prev"
                    >
                        ← Previous
                    </button>
                    
                    <div className="nav-center">
                        {currentStep === tutorialSteps.length - 1 ? (
                            <button onClick={onComplete} className="complete-button">
                                Complete Tutorial
                            </button>
                        ) : (
                            <button 
                                onClick={nextStep}
                                className="nav-button next"
                                disabled={isSimulationRunning}
                            >
                                {isSimulationRunning ? 'Running Simulation...' : 'Next →'}
                            </button>
                        )}
                    </div>
                    
                    <div className="nav-spacer"></div>
                </div>
            </div>
        </div>
    );
};

export default TutorialMode;
