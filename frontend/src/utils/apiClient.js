/**
 * API Client for NeuroTwin Backend Communication
 * Handles all HTTP requests to the Flask backend
 */

const API_BASE_URL = '/api';

/**
 * Generic API request function with error handling
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const requestOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (!data.success && data.error) {
            throw new Error(data.error);
        }
        
        return data;
    } catch (error) {
        console.error(`API request failed for ${endpoint}:`, error);
        throw error;
    }
}

/**
 * Simulate DBS with given parameters
 * @param {Object} parameters - DBS parameters
 * @returns {Promise<Object>} Simulation results
 */
export async function simulateDBSParameters(parameters) {
    return apiRequest('/simulate', {
        method: 'POST',
        body: JSON.stringify(parameters),
    });
}

/**
 * Explore parameter space for educational insights
 * @param {Object} explorationParams - Exploration configuration
 * @returns {Promise<Object>} Exploration results
 */
export async function exploreParameterSpace(explorationParams) {
    return apiRequest('/explore', {
        method: 'POST',
        body: JSON.stringify(explorationParams),
    });
}

/**
 * Optimize DBS parameters for given condition
 * @param {Object} optimizationParams - Optimization configuration
 * @returns {Promise<Object>} Optimization results
 */
export async function optimizeParameters(optimizationParams) {
    return apiRequest('/optimize', {
        method: 'POST',
        body: JSON.stringify(optimizationParams),
    });
}

/**
 * Get available neurological conditions
 * @returns {Promise<Object>} Available conditions
 */
export async function getAvailableConditions() {
    return apiRequest('/conditions');
}

/**
 * Get electrode configurations
 * @returns {Promise<Object>} Electrode configurations
 */
export async function getElectrodeConfigurations() {
    return apiRequest('/electrode-configs');
}

/**
 * Get educational content about DBS
 * @returns {Promise<Object>} Educational content
 */
export async function getEducationalContent() {
    return apiRequest('/educational-content');
}

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export async function checkApiHealth() {
    return apiRequest('/health');
}
