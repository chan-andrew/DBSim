import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';

const CustomBrainAnimation = () => {
    const mountRef = useRef(null);
    const sceneRef = useRef(null);
    const rendererRef = useRef(null);
    const cameraRef = useRef(null);
    const brainRef = useRef(null);
    const animationFrameRef = useRef(null);

    useEffect(() => {
        if (!mountRef.current) return;

        const container = mountRef.current;
        const width = container.clientWidth;
        const height = container.clientHeight;

        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0a);
        sceneRef.current = scene;

        // Camera
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.set(0, 0, 6);
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
        const ambientLight = new THREE.AmbientLight(0x404040, 0.8);
        scene.add(ambientLight);

        const directionalLight1 = new THREE.DirectionalLight(0x8a2be2, 1.0);
        directionalLight1.position.set(5, 5, 5);
        scene.add(directionalLight1);

        const directionalLight2 = new THREE.DirectionalLight(0x9370db, 0.8);
        directionalLight2.position.set(-5, -5, 5);
        scene.add(directionalLight2);

        // Create animated brain
        createAnimatedBrain();

        // Animation loop
        const animate = () => {
            if (rendererRef.current && sceneRef.current && cameraRef.current) {
                rendererRef.current.render(sceneRef.current, cameraRef.current);
            }
            animationFrameRef.current = requestAnimationFrame(animate);
        };
        animate();

        // Handle resize
        const handleResize = () => {
            if (!mountRef.current || !rendererRef.current || !cameraRef.current) return;
            
            const newWidth = mountRef.current.clientWidth;
            const newHeight = mountRef.current.clientHeight;
            
            cameraRef.current.aspect = newWidth / newHeight;
            cameraRef.current.updateProjectionMatrix();
            rendererRef.current.setSize(newWidth, newHeight);
        };

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
    }, []);

    const createAnimatedBrain = () => {
        const scene = sceneRef.current;
        const brainGroup = new THREE.Group();

        // Create main brain structure
        const brainGeometry = new THREE.SphereGeometry(2, 32, 32);
        
        // Create brain material with animated properties
        const brainMaterial = new THREE.MeshPhongMaterial({
            color: 0x8a2be2,
            transparent: true,
            opacity: 0.9,
            shininess: 100,
            specular: 0x444444
        });

        const brain = new THREE.Mesh(brainGeometry, brainMaterial);
        brainGroup.add(brain);

        // Create brain cortex details (wrinkles/folds)
        for (let i = 0; i < 20; i++) {
            const foldGeometry = new THREE.TorusGeometry(
                Math.random() * 1.5 + 0.5, 
                Math.random() * 0.1 + 0.05, 
                8, 
                16
            );
            
            const foldMaterial = new THREE.MeshPhongMaterial({
                color: new THREE.Color().setHSL(0.8 + Math.random() * 0.1, 0.7, 0.5),
                transparent: true,
                opacity: 0.6
            });

            const fold = new THREE.Mesh(foldGeometry, foldMaterial);
            
            // Random positioning on brain surface
            const phi = Math.random() * Math.PI * 2;
            const theta = Math.random() * Math.PI;
            const radius = 1.8;
            
            fold.position.x = radius * Math.sin(theta) * Math.cos(phi);
            fold.position.y = radius * Math.sin(theta) * Math.sin(phi);
            fold.position.z = radius * Math.cos(theta);
            
            fold.lookAt(0, 0, 0);
            
            brainGroup.add(fold);

            // Animate individual folds
            gsap.to(fold.rotation, {
                x: Math.PI * 2,
                y: Math.PI * 2,
                duration: 10 + Math.random() * 20,
                repeat: -1,
                ease: "none"
            });
        }

        // Create neural network connections
        for (let i = 0; i < 50; i++) {
            const points = [];
            const startRadius = 1.5 + Math.random() * 0.5;
            const endRadius = 1.5 + Math.random() * 0.5;
            
            // Start point
            const startPhi = Math.random() * Math.PI * 2;
            const startTheta = Math.random() * Math.PI;
            points.push(new THREE.Vector3(
                startRadius * Math.sin(startTheta) * Math.cos(startPhi),
                startRadius * Math.sin(startTheta) * Math.sin(startPhi),
                startRadius * Math.cos(startTheta)
            ));
            
            // Control points for curve
            const midPoint1 = new THREE.Vector3(
                (Math.random() - 0.5) * 4,
                (Math.random() - 0.5) * 4,
                (Math.random() - 0.5) * 4
            );
            points.push(midPoint1);
            
            // End point
            const endPhi = Math.random() * Math.PI * 2;
            const endTheta = Math.random() * Math.PI;
            points.push(new THREE.Vector3(
                endRadius * Math.sin(endTheta) * Math.cos(endPhi),
                endRadius * Math.sin(endTheta) * Math.sin(endPhi),
                endRadius * Math.cos(endTheta)
            ));

            const curve = new THREE.CatmullRomCurve3(points);
            const tubeGeometry = new THREE.TubeGeometry(curve, 20, 0.02, 8, false);
            
            const connectionMaterial = new THREE.MeshPhongMaterial({
                color: new THREE.Color().setHSL(0.6 + Math.random() * 0.3, 0.8, 0.6),
                transparent: true,
                opacity: 0.4,
                emissive: new THREE.Color().setHSL(0.6 + Math.random() * 0.3, 0.3, 0.2)
            });

            const connection = new THREE.Mesh(tubeGeometry, connectionMaterial);
            brainGroup.add(connection);

            // Animate neural connections
            gsap.to(connectionMaterial, {
                opacity: 0.1,
                duration: 2 + Math.random() * 3,
                repeat: -1,
                yoyo: true,
                ease: "power2.inOut"
            });
        }

        // Add particle system for neural activity
        const particleCount = 200;
        const particleGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            const radius = 2.5 + Math.random() * 1.5;
            const phi = Math.random() * Math.PI * 2;
            const theta = Math.random() * Math.PI;

            positions[i * 3] = radius * Math.sin(theta) * Math.cos(phi);
            positions[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
            positions[i * 3 + 2] = radius * Math.cos(theta);

            const color = new THREE.Color().setHSL(0.7 + Math.random() * 0.2, 0.8, 0.7);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        }

        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const particleMaterial = new THREE.PointsMaterial({
            size: 0.1,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(particleGeometry, particleMaterial);
        brainGroup.add(particles);

        // Animate particles
        gsap.to(particles.rotation, {
            x: Math.PI * 2,
            y: Math.PI * 2,
            z: Math.PI * 2,
            duration: 30,
            repeat: -1,
            ease: "none"
        });

        scene.add(brainGroup);
        brainRef.current = brainGroup;

        // Main brain rotation
        gsap.to(brainGroup.rotation, {
            y: Math.PI * 2,
            duration: 20,
            repeat: -1,
            ease: "none"
        });

        // Floating animation
        gsap.to(brainGroup.position, {
            y: 0.2,
            duration: 4,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        });

        // Pulsing animation for the main brain
        gsap.to(brain.scale, {
            x: 1.05,
            y: 1.05,
            z: 1.05,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        });

        // Color cycling animation
        gsap.to(brainMaterial.color, {
            r: 0.6,
            g: 0.2,
            b: 0.9,
            duration: 5,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        });
    };

    return (
        <div style={{ width: '100%', height: '100%', position: 'relative' }}>
            <div 
                ref={mountRef} 
                style={{ 
                    width: '100%', 
                    height: '100%',
                    borderRadius: '10px',
                    overflow: 'hidden',
                    border: '2px solid #444'
                }} 
            />
            
            {/* Info overlay */}
            <div style={{
                position: 'absolute',
                bottom: '10px',
                left: '10px',
                background: 'rgba(0, 0, 0, 0.7)',
                color: 'white',
                padding: '8px 12px',
                borderRadius: '5px',
                fontSize: '12px',
                fontFamily: 'monospace'
            }}>
                Interactive 3D Brain Model
            </div>
        </div>
    );
};

export default CustomBrainAnimation;