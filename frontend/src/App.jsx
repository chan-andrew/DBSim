import React, { useState, useCallback, useEffect } from 'react';
import BrainVisualization from './components/BrainVisualization';
import ParameterControls from './components/ParameterControls';
import ExplorationPanel from './components/ExplorationPanel';
import ResultsDisplay from './components/ResultsDisplay';
import TutorialMode from './components/TutorialMode';
import DarkVeil from './components/DarkVeil';
import { simulateDBSParameters, exploreParameterSpace } from './utils/apiClient';
import './App.css';

function App() {
    const [simulationState, setSimulationState] = useState({
        parameters: { 
            frequency: 130, 
            amplitude: 2.0, 
            contact: 0, 
            condition: 'healthy',
            pulse_width: 90
        },
        results: null,
        isRunning: false,
        error: null
    });

    const [explorationData, setExplorationData] = useState(null);
    const [showTutorial, setShowTutorial] = useState(false);
    const [apiHealth, setApiHealth] = useState('checking');

    // Check API health on startup
    useEffect(() => {
        checkApiHealth();
    }, []);

    const checkApiHealth = async () => {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                setApiHealth('healthy');
            } else {
                setApiHealth('error');
            }
        } catch (error) {
            setApiHealth('error');
            console.error('API health check failed:', error);
        }
    };

    const handleParameterChange = useCallback((parameterName, value) => {
        setSimulationState(prev => ({
            ...prev,
            parameters: {
                ...prev.parameters,
                [parameterName]: parameterName === 'contact' ? parseInt(value) : 
                               parameterName === 'condition' ? value : parseFloat(value)
            },
            error: null
        }));
    }, []);

    const runSimulation = useCallback(async () => {
        setSimulationState(prev => ({ ...prev, isRunning: true, error: null }));
        
        try {
            const results = await simulateDBSParameters(simulationState.parameters);
            setSimulationState(prev => ({
                ...prev,
                results: results,
                isRunning: false
            }));
        } catch (error) {
            console.error('Simulation failed:', error);
            setSimulationState(prev => ({
                ...prev,
                error: error.message || 'Simulation failed',
                isRunning: false
            }));
        }
    }, [simulationState.parameters]);

    const handleExploration = useCallback(async (explorationParams) => {
        try {
            const results = await exploreParameterSpace(explorationParams);
            setExplorationData(results);
        } catch (error) {
            console.error('Exploration failed:', error);
            setSimulationState(prev => ({
                ...prev,
                error: error.message || 'Parameter exploration failed'
            }));
        }
    }, []);

    const handleTutorialComplete = useCallback(() => {
        setShowTutorial(false);
    }, []);

    if (apiHealth === 'checking') {
        return (
            <div className="app-container">
                <div className="loading-screen">
                    <div className="loading-spinner"></div>
                    <h2>Initializing NeuroTwin...</h2>
                    <p>Loading computational models</p>
                </div>
            </div>
        );
    }

    if (apiHealth === 'error') {
        return (
            <div className="app-container">
                <div className="error-screen">
                    <h2>⚠️ Backend Connection Error</h2>
                    <p>Unable to connect to the NeuroTwin API server.</p>
                    <p>Please ensure the backend is running on port 5000.</p>
                    <button onClick={checkApiHealth} className="retry-button">
                        Retry Connection
                    </button>
                </div>
            </div>
        );
    }

    if (showTutorial) {
        return (
            <TutorialMode 
                onComplete={handleTutorialComplete}
                onParameterChange={handleParameterChange}
                onRunSimulation={runSimulation}
                simulationState={simulationState}
            />
        );
    }

    return (
        <div className="app-container">
            <div className="background-animation">
                <DarkVeil 
                    speed={0.3}
                    hueShift={220}
                    noiseIntensity={0.1}
                    warpAmount={0.2}
                />
            </div>
            <header className="app-header">
                <div className="header-content">
                    <h1>NeuroTwin</h1>
                    <p className="subtitle">Interactive Deep Brain Stimulation Simulator</p>
                    <p className="description">
                        Explore how electrical stimulation affects neural activity in real-time
                    </p>
                    <div className="header-buttons">
                        <button 
                            onClick={() => setShowTutorial(true)}
                            className="tutorial-button"
                        >
                            📚 Tutorial Mode
                        </button>
                        <div className="status-indicator">
                            <span className={`status-dot ${apiHealth}`}></span>
                            Backend: {apiHealth}
                        </div>
                    </div>
                </div>
            </header>

            {simulationState.error && (
                <div className="error-banner">
                    <span>⚠️ {simulationState.error}</span>
                    <button onClick={() => setSimulationState(prev => ({ ...prev, error: null }))}>
                        ✕
                    </button>
                </div>
            )}

            <div className="main-grid">
                <div className="left-panel">
                    <ParameterControls 
                        parameters={simulationState.parameters}
                        onParameterChange={handleParameterChange}
                        onRunSimulation={runSimulation}
                        isRunning={simulationState.isRunning}
                    />
                    
                    <ExplorationPanel 
                        onExplore={handleExploration}
                        currentCondition={simulationState.parameters.condition}
                        explorationData={explorationData}
                    />
                </div>

                <div className="center-panel">
                    <BrainVisualization 
                        simulationData={simulationState.results}
                        isLoading={simulationState.isRunning}
                        parameters={simulationState.parameters}
                    />
                </div>

                <div className="right-panel">
                    <ResultsDisplay 
                        results={simulationState.results}
                        parameters={simulationState.parameters}
                        explorationData={explorationData}
                    />
                </div>
            </div>

            <footer className="app-footer">
                <p>
                    NeuroTwin is an educational simulation tool for understanding DBS mechanisms.
                    Not intended for clinical use.
                </p>
            </footer>
        </div>
    );
}

export default App;
