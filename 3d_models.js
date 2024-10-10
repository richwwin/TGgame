import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

export class SpaceClawGame {
    constructor(canvas) {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);

        this.loader = new THREE.TextureLoader();
        this.gltfLoader = new GLTFLoader();

        this.spaceship = null;
        this.claw = null;
        this.prizes = [];

        this.init();
    }

    init() {
        this.loadSpaceship();
        this.loadClaw();
        this.createPrizes();
        this.setupLights();
        this.animate();
    }

    loadSpaceship() {
        const texture = this.loader.load('images/1.png');
        const geometry = new THREE.PlaneGeometry(2, 2);
        const material = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
        this.spaceship = new THREE.Mesh(geometry, material);
        this.spaceship.position.set(0, 3, -5);
        this.scene.add(this.spaceship);
    }

    loadClaw() {
        const texture = this.loader.load('images/2.png');
        const geometry = new THREE.PlaneGeometry(1, 1);
        const material = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
        this.claw = new THREE.Mesh(geometry, material);
        this.claw.position.set(0, 2, -5);
        this.scene.add(this.claw);
    }

    createPrizes() {
        const texture = this.loader.load('images/3.png');
        const geometry = new THREE.PlaneGeometry(1, 1);
        const material = new THREE.MeshBasicMaterial({ map: texture, transparent: true });

        for (let i = 0; i < 10; i++) {
            const prize = new THREE.Mesh(geometry, material);
            prize.position.set(
                Math.random() * 10 - 5,
                Math.random() * 5 - 2.5,
                Math.random() * 5 - 10
            );
            this.prizes.push(prize);
            this.scene.add(prize);
        }
    }

    setupLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(0, 1, 0);
        this.scene.add(directionalLight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));

        if (this.claw) {
            this.claw.position.y = 2 + Math.sin(Date.now() * 0.001) * 0.1;
        }

        this.prizes.forEach((prize) => {
            prize.rotation.z += 0.01;
        });

        this.renderer.render(this.scene, this.camera);
    }
}