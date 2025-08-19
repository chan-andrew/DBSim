import React, { useRef, useEffect, useState, useCallback } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';

const ThreeBrainVisualization = ({ simulationData, parameters, isLoading }) => {
    const mountRef = useRef(null);
    const sceneRef = useRef(null);
    const rendererRef = useRef(null);
    const cameraRef = useRef(null);
    const brainRef = useRef(null);
    const electrodesRef = useRef([]);
    const animationFrameRef = useRef(null);
    const [isInitialized, setIsInitialized] = useState(false);
    const [electrodePosition, setElectrodePosition] = useState({ x: 0, y: 0, z: 0 });

    // Initialize Three.js scene
    const initializeScene = useCallback(() => {
        if (!mountRef.current || isInitialized) return;

        const container = mountRef.current;
        const width = container.clientWidth;
        const height = container.clientHeight;

        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0a);
        sceneRef.current = scene;

        // Camera
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.set(0, 0, 5);
        cameraRef.current = camera;

        // Renderer
        const renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true 
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);
        rendererRef.current = renderer;

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        scene.add(directionalLight);

        // Create brain geometry
        createBrainModel();

        // Add orbital controls
        addOrbitControls(camera, renderer);

        setIsInitialized(true);
    }, [isInitialized]);

    // Create simplified brain model
    const createBrainModel = () => {
        const scene = sceneRef.current;
        
        // Brain group
        const brainGroup = new THREE.Group();
        
        // Main brain structure - hemisphere shapes
        const leftHemisphere = createHemisphere(-0.5, 0x8a2be2);
        const rightHemisphere = createHemisphere(0.5, 0x9370db);
        
        brainGroup.add(leftHemisphere);
        brainGroup.add(rightHemisphere);
        
        // Add some brain detail structures
        const brainstem = createBrainstem();
        const cerebellum = createCerebellum();
        
        brainGroup.add(brainstem);
        brainGroup.add(cerebellum);
        
        scene.add(brainGroup);
        brainRef.current = brainGroup;

        // Add subtle animation
        gsap.to(brainGroup.rotation, {
            y: Math.PI * 2,
            duration: 40,
            repeat: -1,
            ease: "none"
        });

        // Add gentle floating animation
        gsap.to(brainGroup.position, {
            y: 0.1,
            duration: 3,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        });
    };

    // Create hemisphere geometry
    const createHemisphere = (offsetX, color) => {
        const geometry = new THREE.SphereGeometry(1.2, 32, 16, 0, Math.PI);
        const material = new THREE.MeshPhongMaterial({ 
            color: color,
            transparent: true,
            opacity: 0.8,
            shininess: 30
        });
        
        const hemisphere = new THREE.Mesh(geometry, material);
        hemisphere.position.x = offsetX;
        hemisphere.castShadow = true;
        hemisphere.receiveShadow = true;
        
        // Add some surface detail
        const wireframe = new THREE.WireframeGeometry(geometry);
        const line = new THREE.LineSegments(wireframe, 
            new THREE.LineBasicMaterial({ 
                color: 0x444444, 
                transparent: true, 
                opacity: 0.3 
            })
        );
        line.position.x = offsetX;
        
        const group = new THREE.Group();
        group.add(hemisphere);
        group.add(line);
        
        return group;
    };

    // Create brainstem
    const createBrainstem = () => {
        const geometry = new THREE.CylinderGeometry(0.3, 0.4, 1.5, 8);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x6a5acd,
            transparent: true,
            opacity: 0.7
        });
        
        const brainstem = new THREE.Mesh(geometry, material);
        brainstem.position.set(0, -1.2, 0);
        brainstem.castShadow = true;
        brainstem.receiveShadow = true;
        
        return brainstem;
    };

    // Create cerebellum
    const createCerebellum = () => {
        const geometry = new THREE.SphereGeometry(0.6, 16, 8);
        const material = new THREE.MeshPhongMaterial({ 
            color: 0x9932cc,
            transparent: true,
            opacity: 0.7
        });
        
        const cerebellum = new THREE.Mesh(geometry, material);
        cerebellum.position.set(0, -0.8, -1.2);
        cerebellum.scale.set(1, 0.6, 1);
        cerebellum.castShadow = true;
        cerebellum.receiveShadow = true;
        
        return cerebellum;
    };

    // Add orbit controls
    const addOrbitControls = (camera, renderer) => {
        let isMouseDown = false;
        let mouseX = 0;
        let mouseY = 0;
        let targetRotationX = 0;
        let targetRotationY = 0;
        let rotationX = 0;
        let rotationY = 0;

        const onMouseMove = (event) => {
            if (!isMouseDown) return;
            
            const deltaX = event.clientX - mouseX;
            const deltaY = event.clientY - mouseY;
            
            targetRotationY += deltaX * 0.01;
            targetRotationX += deltaY * 0.01;
            
            mouseX = event.clientX;
            mouseY = event.clientY;
        };

        const onMouseDown = (event) => {
            isMouseDown = true;
            mouseX = event.clientX;
            mouseY = event.clientY;
        };

        const onMouseUp = () => {
            isMouseDown = false;
        };

        const onWheel = (event) => {
            camera.position.z += event.deltaY * 0.01;
            camera.position.z = Math.max(2, Math.min(10, camera.position.z));
        };

        renderer.domElement.addEventListener('mousemove', onMouseMove);
        renderer.domElement.addEventListener('mousedown', onMouseDown);
        renderer.domElement.addEventListener('mouseup', onMouseUp);
        renderer.domElement.addEventListener('wheel', onWheel);

        // Animation loop for smooth rotation
        const updateRotation = () => {
            rotationX += (targetRotationX - rotationX) * 0.1;
            rotationY += (targetRotationY - rotationY) * 0.1;
            
            if (brainRef.current) {
                brainRef.current.rotation.x = rotationX;
                brainRef.current.rotation.y = rotationY;
            }
        };

        // Store update function for cleanup
        renderer.updateRotation = updateRotation;
    };

    // Create electrodes based on simulation parameters
    const createElectrodes = useCallback(() => {
        if (!sceneRef.current || !parameters) return;

        // Clear existing electrodes
        electrodesRef.current.forEach(electrode => {
            sceneRef.current.remove(electrode);
        });
        electrodesRef.current = [];

        // Create DBS electrode
        const electrodeGroup = createDBSElectrode();
        
        // Position electrode based on parameters
        const position = calculateElectrodePosition(parameters);
        electrodeGroup.position.set(position.x, position.y, position.z);
        
        sceneRef.current.add(electrodeGroup);
        electrodesRef.current.push(electrodeGroup);

        // Update electrode position state
        setElectrodePosition(position);
    }, [parameters]);

    // Calculate electrode position based on simulation parameters
    const calculateElectrodePosition = (params) => {
        // Map simulation parameters to 3D coordinates
        // This is a simplified mapping - in reality, you'd want more sophisticated positioning
        const contact = params.contact || 0;
        const frequency = params.frequency || 130;
        const amplitude = params.amplitude || 2.0;

        // Calculate position based on target brain region
        let x = 0;
        let y = 0;
        let z = 0;

        // Adjust position based on contact selection (0-3)
        switch (contact) {
            case 0: // Contact 0 - deeper, more ventral
                x = -0.8;
                y = -0.3;
                z = 0.2;
                break;
            case 1: // Contact 1 - mid-depth
                x = -0.6;
                y = -0.1;
                z = 0.3;
                break;
            case 2: // Contact 2 - more superficial
                x = -0.4;
                y = 0.1;
                z = 0.4;
                break;
            case 3: // Contact 3 - most superficial
                x = -0.2;
                y = 0.3;
                z = 0.5;
                break;
            default:
                x = -0.6;
                y = 0;
                z = 0.3;
        }

        // Add slight variation based on frequency and amplitude
        x += (frequency - 130) * 0.001;
        y += (amplitude - 2.0) * 0.05;

        return { x, y, z };
    };

    // Create DBS electrode model
    const createDBSElectrode = () => {
        const electrodeGroup = new THREE.Group();

        // Electrode shaft
        const shaftGeometry = new THREE.CylinderGeometry(0.02, 0.02, 0.8, 8);
        const shaftMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x444444,
            shininess: 100,
            specular: 0x333333
        });
        const shaft = new THREE.Mesh(shaftGeometry, shaftMaterial);
        shaft.position.y = 0.4;
        electrodeGroup.add(shaft);

        // Electrode contacts (4 contacts)
        for (let i = 0; i < 4; i++) {
            const contactGeometry = new THREE.CylinderGeometry(0.025, 0.025, 0.08, 8);
            const isActive = i === (parameters?.contact || 0);
            const contactMaterial = new THREE.MeshPhongMaterial({ 
                color: isActive ? 0xff4444 : 0x888888,
                emissive: isActive ? 0x441111 : 0x000000,
                shininess: isActive ? 80 : 30,
                specular: isActive ? 0x444444 : 0x222222
            });
            
            const contact = new THREE.Mesh(contactGeometry, contactMaterial);
            contact.position.y = 0.1 + (i * 0.1);
            electrodeGroup.add(contact);

            // Add glow effect for active contact
            if (isActive) {
                const glowGeometry = new THREE.SphereGeometry(0.05, 16, 8);
                const glowMaterial = new THREE.MeshBasicMaterial({ 
                    color: 0xff4444,
                    transparent: true,
                    opacity: 0.3
                });
                const glow = new THREE.Mesh(glowGeometry, glowMaterial);
                glow.position.y = 0.1 + (i * 0.1);
                electrodeGroup.add(glow);

                // Animate glow
                gsap.to(glow.scale, {
                    x: 1.5,
                    y: 1.5,
                    z: 1.5,
                    duration: 1,
                    repeat: -1,
                    yoyo: true,
                    ease: "power2.inOut"
                });
            }
        }

        // Lead wire
        const wireGeometry = new THREE.CylinderGeometry(0.01, 0.01, 1.0, 6);
        const wireMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x222222,
            transparent: true,
            opacity: 0.7
        });
        const wire = new THREE.Mesh(wireGeometry, wireMaterial);
        wire.position.y = -0.1;
        wire.rotation.z = Math.PI * 0.1; // Slight angle
        electrodeGroup.add(wire);

        return electrodeGroup;
    };

    // Animation loop
    const animate = useCallback(() => {
        if (!rendererRef.current || !sceneRef.current || !cameraRef.current) return;

        // Update rotation controls
        if (rendererRef.current.updateRotation) {
            rendererRef.current.updateRotation();
        }

        // Render scene
        rendererRef.current.render(sceneRef.current, cameraRef.current);
        
        animationFrameRef.current = requestAnimationFrame(animate);
    }, []);

    // Handle window resize
    const handleResize = useCallback(() => {
        if (!mountRef.current || !rendererRef.current || !cameraRef.current) return;

        const container = mountRef.current;
        const width = container.clientWidth;
        const height = container.clientHeight;

        cameraRef.current.aspect = width / height;
        cameraRef.current.updateProjectionMatrix();
        rendererRef.current.setSize(width, height);
    }, []);

    // Initialize scene on mount
    useEffect(() => {
        initializeScene();
        
        // Handle resize
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
            if (rendererRef.current && mountRef.current) {
                mountRef.current.removeChild(rendererRef.current.domElement);
            }
        };
    }, [initializeScene, handleResize]);

    // Start animation when initialized
    useEffect(() => {
        if (isInitialized) {
            animate();
        }
        
        return () => {
            if (animationFrameRef.current) {
                cancelAnimationFrame(animationFrameRef.current);
            }
        };
    }, [isInitialized, animate]);

    // Update electrodes when parameters change
    useEffect(() => {
        if (isInitialized && parameters) {
            createElectrodes();
        }
    }, [isInitialized, parameters, createElectrodes]);

    if (isLoading) {
        return (
            <div style={{ 
                width: '100%', 
                height: '500px', 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center',
                background: '#0a0a0a',
                borderRadius: '10px'
            }}>
                <div style={{ color: '#ffffff', textAlign: 'center' }}>
                    <div className="loading-spinner large"></div>
                    <p>Loading 3D Brain Model...</p>
                </div>
            </div>
        );
    }

    return (
        <div style={{ width: '100%', height: '500px', position: 'relative' }}>
            <div 
                ref={mountRef} 
                style={{ 
                    width: '100%', 
                    height: '100%',
                    borderRadius: '10px',
                    overflow: 'hidden',
                    border: '2px solid #333'
                }} 
            />
            
            {/* Info overlay */}
            <div style={{
                position: 'absolute',
                top: '10px',
                left: '10px',
                background: 'rgba(0, 0, 0, 0.7)',
                color: 'white',
                padding: '10px',
                borderRadius: '5px',
                fontSize: '12px',
                fontFamily: 'monospace'
            }}>
                <div>Contact: {parameters?.contact || 0}</div>
                <div>Frequency: {parameters?.frequency || 0} Hz</div>
                <div>Amplitude: {parameters?.amplitude || 0} mA</div>
                <div>Position: ({electrodePosition.x.toFixed(2)}, {electrodePosition.y.toFixed(2)}, {electrodePosition.z.toFixed(2)})</div>
            </div>

            {/* Controls overlay */}
            <div style={{
                position: 'absolute',
                bottom: '10px',
                right: '10px',
                background: 'rgba(0, 0, 0, 0.7)',
                color: 'white',
                padding: '10px',
                borderRadius: '5px',
                fontSize: '11px',
                textAlign: 'right'
            }}>
                <div>🖱️ Click & Drag: Rotate</div>
                <div>🖲️ Scroll: Zoom</div>
                <div>🔴 Red Glow: Active Contact</div>
            </div>
        </div>
    );
};

export default ThreeBrainVisualization;