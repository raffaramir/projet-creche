// Little Future — 3D parent tracking visualization.
// Each course = a sphere orbiting a magical core. Height encodes completion %,
// color encodes category. Hovering a sphere highlights the corresponding row.

import * as THREE from "three";

const canvas = document.getElementById("progress3d");
const dataNode = document.getElementById("progressData");
if (canvas) initProgress(canvas, parseData(dataNode));

function parseData(node) {
    if (!node) return [];
    try { return JSON.parse(node.textContent); } catch (e) { return []; }
}

const palette = {
    letters:   0xf7b6c2,
    numbers:   0xc9a7ff,
    languages: 0x9b73f0,
    islamic:   0x6db59f,
    science:   0x6cb1ff,
    art:       0xffaa6c,
};

function initProgress(canvas, data) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xfff8fb);

    const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 100);
    camera.position.set(0, 4.5, 9);
    camera.lookAt(0, 1.5, 0);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const sun = new THREE.DirectionalLight(0xffffff, 1.0);
    sun.position.set(5, 8, 5);
    scene.add(sun);

    // Floor
    const floor = new THREE.Mesh(
        new THREE.CircleGeometry(6, 64),
        new THREE.MeshStandardMaterial({ color: 0xf4ecff, roughness: 0.9 })
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // Concentric guide rings
    for (let r = 1.5; r <= 4.5; r += 1) {
        const ring = new THREE.Mesh(
            new THREE.RingGeometry(r - 0.01, r + 0.01, 64),
            new THREE.MeshBasicMaterial({ color: 0xc9a7ff, transparent: true, opacity: 0.25, side: THREE.DoubleSide })
        );
        ring.rotation.x = -Math.PI / 2;
        ring.position.y = 0.02;
        scene.add(ring);
    }

    // Magical central core
    const core = new THREE.Mesh(
        new THREE.IcosahedronGeometry(0.7, 1),
        new THREE.MeshStandardMaterial({
            color: 0xc9a7ff, emissive: 0xc9a7ff, emissiveIntensity: 0.4,
            metalness: 0.4, roughness: 0.25,
        })
    );
    core.position.y = 1.5;
    scene.add(core);

    // Orbiting course spheres
    const orbiters = [];
    const N = data.length;
    if (N === 0) {
        // Friendly empty-state: a lonely glowing sphere
        const empty = new THREE.Mesh(
            new THREE.SphereGeometry(0.4, 24, 16),
            new THREE.MeshStandardMaterial({ color: 0xf7b6c2, emissive: 0xf7b6c2, emissiveIntensity: 0.3 })
        );
        empty.position.set(2.5, 1, 0);
        scene.add(empty);
        orbiters.push({ mesh: empty, base: empty.position.clone(), phase: 0, speed: 0.4, radius: 2.5 });
    } else {
        data.forEach((d, i) => {
            const color = palette[d.category] || 0xf7b6c2;
            const radius = 1.8 + (i % 3) * 0.9;
            const angle = (i / N) * Math.PI * 2;
            // height encodes percent (0..100 -> 0.4..3.5)
            const height = 0.4 + (d.percent / 100) * 3.1;

            const sphere = new THREE.Mesh(
                new THREE.SphereGeometry(0.34, 32, 24),
                new THREE.MeshStandardMaterial({
                    color, emissive: color, emissiveIntensity: 0.25,
                    metalness: 0.3, roughness: 0.35,
                })
            );
            sphere.position.set(Math.cos(angle) * radius, height, Math.sin(angle) * radius);
            sphere.userData = { title: d.title, percent: d.percent };
            scene.add(sphere);

            // Vertical pillar from floor to sphere
            const pillar = new THREE.Mesh(
                new THREE.CylinderGeometry(0.04, 0.04, height, 12),
                new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.55 })
            );
            pillar.position.set(sphere.position.x, height / 2, sphere.position.z);
            scene.add(pillar);

            orbiters.push({
                mesh: sphere, pillar, radius, phase: angle,
                speed: 0.18 + Math.random() * 0.12,
                height,
            });
        });
    }

    // Hover highlight ↔ list rows
    const list = document.getElementById("progressList");
    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    let hovered = null;

    canvas.addEventListener("pointermove", (e) => {
        const rect = canvas.getBoundingClientRect();
        pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    });

    function updateHover() {
        raycaster.setFromCamera(pointer, camera);
        const meshes = orbiters.map((o) => o.mesh);
        const hits = raycaster.intersectObjects(meshes);
        const next = hits[0]?.object || null;
        if (next !== hovered) {
            if (hovered) hovered.scale.setScalar(1);
            hovered = next;
            if (hovered) hovered.scale.setScalar(1.35);
            // Sync list highlight
            if (list) {
                list.querySelectorAll("li").forEach((li) => li.classList.remove("active"));
                if (hovered?.userData?.title) {
                    const li = list.querySelector(`li[data-course="${cssEscape(hovered.userData.title)}"]`);
                    if (li) li.classList.add("active");
                }
            }
        }
    }

    function resize() {
        const r = canvas.getBoundingClientRect();
        const w = Math.max(r.width, 320);
        const h = Math.max(r.height || w * 0.6, 360);
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }
    window.addEventListener("resize", resize);
    resize();

    const clock = new THREE.Clock();
    function tick() {
        const dt = clock.getDelta();
        const t = clock.getElapsedTime();

        core.rotation.x += dt * 0.4;
        core.rotation.y += dt * 0.6;

        orbiters.forEach((o) => {
            o.phase += dt * o.speed;
            const x = Math.cos(o.phase) * o.radius;
            const z = Math.sin(o.phase) * o.radius;
            const bob = Math.sin(t * 1.6 + o.phase) * 0.08;
            o.mesh.position.set(x, o.height + bob, z);
            if (o.pillar) o.pillar.position.set(x, o.height / 2, z);
        });

        updateHover();
        renderer.render(scene, camera);
        requestAnimationFrame(tick);
    }
    tick();
}

// Tiny CSS escape for our [data-course] selector.
function cssEscape(s) {
    return String(s).replace(/(["\\])/g, "\\$1");
}
