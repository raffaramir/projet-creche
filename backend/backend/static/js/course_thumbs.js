// Little Future — animated 3D thumbnail per course card
// One small WebGL scene per <canvas.course-mini>. Lightweight, single shape
// rotating in place with a glow halo, color keyed to the course category.

import * as THREE from "three";

const palette = {
    letters:   0xf7b6c2,
    numbers:   0xc9a7ff,
    languages: 0x9b73f0,
    islamic:   0x6db59f,
    science:   0x6cb1ff,
    art:       0xffaa6c,
};

const shapes = {
    letters:   "torusKnot",
    numbers:   "icosahedron",
    languages: "sphere",
    islamic:   "octahedron",
    science:   "torus",
    art:       "cone",
};

document.querySelectorAll(".course-mini").forEach((canvas) => {
    const cat = canvas.dataset.cat || "letters";
    initThumb(canvas, palette[cat] || 0xf7b6c2, shapes[cat] || "icosahedron");
});

function initThumb(canvas, color, shapeName) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 4.2);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const dl = new THREE.DirectionalLight(0xffffff, 1.2);
    dl.position.set(3, 4, 5);
    scene.add(dl);

    let geo;
    switch (shapeName) {
        case "icosahedron": geo = new THREE.IcosahedronGeometry(1, 0); break;
        case "octahedron":  geo = new THREE.OctahedronGeometry(1, 0); break;
        case "sphere":      geo = new THREE.SphereGeometry(0.95, 32, 24); break;
        case "torus":       geo = new THREE.TorusGeometry(0.8, 0.28, 16, 64); break;
        case "cone":        geo = new THREE.ConeGeometry(0.85, 1.6, 32); break;
        case "torusKnot":
        default:            geo = new THREE.TorusKnotGeometry(0.6, 0.22, 100, 14); break;
    }

    const mat = new THREE.MeshStandardMaterial({
        color, metalness: 0.3, roughness: 0.35,
    });
    const mesh = new THREE.Mesh(geo, mat);
    scene.add(mesh);

    // Halo
    const halo = new THREE.Mesh(
        new THREE.RingGeometry(1.3, 1.42, 64),
        new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
    );
    halo.rotation.x = Math.PI / 2;
    halo.position.y = -0.9;
    scene.add(halo);

    function resize() {
        const r = canvas.getBoundingClientRect();
        const w = Math.max(r.width, 80);
        const h = Math.max(r.height, 80);
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }
    window.addEventListener("resize", resize);
    resize();

    const clock = new THREE.Clock();
    function tick() {
        const dt = clock.getDelta();
        mesh.rotation.x += dt * 0.6;
        mesh.rotation.y += dt * 0.9;
        halo.rotation.z += dt * 0.4;
        renderer.render(scene, camera);
        requestAnimationFrame(tick);
    }
    tick();
}
