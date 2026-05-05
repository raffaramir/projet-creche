// Little Future — interactive 3D course scene (Three.js)
// Renders letters/numbers/objects per course category with auto-rotation,
// pointer drag, prev/next stepping, and a child-friendly TTS read-aloud.

import * as THREE from "three";

const canvas = document.getElementById("stage3d");
if (!canvas) {
    console.warn("[course_3d] No #stage3d canvas on page; aborting.");
} else {
    initStage(canvas);
}

function initStage(canvas) {
    const category = canvas.dataset.category || "letters";
    const items = buildItems(category);
    const label = document.getElementById("stage3dLabel");

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xfff8fb);

    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 1.1, 5.2);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.65));
    const key = new THREE.DirectionalLight(0xffffff, 1.1);
    key.position.set(4, 6, 5);
    scene.add(key);
    const fill = new THREE.PointLight(0xc9a7ff, 0.8, 20);
    fill.position.set(-4, 3, -3);
    scene.add(fill);

    // Ground sparkles (decorative)
    const sparklesGeo = new THREE.BufferGeometry();
    const sparkCount = 80;
    const sp = new Float32Array(sparkCount * 3);
    for (let i = 0; i < sparkCount; i++) {
        sp[i * 3 + 0] = (Math.random() - 0.5) * 14;
        sp[i * 3 + 1] = (Math.random() - 0.5) * 6 - 1;
        sp[i * 3 + 2] = (Math.random() - 0.5) * 10 - 4;
    }
    sparklesGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
    const sparkles = new THREE.Points(
        sparklesGeo,
        new THREE.PointsMaterial({ color: 0xc9a7ff, size: 0.05, sizeAttenuation: true })
    );
    scene.add(sparkles);

    // Pivot group for the active item
    const pivot = new THREE.Group();
    scene.add(pivot);

    let activeMesh = null;
    let currentIndex = 0;
    let autoRotate = true;

    function setItem(index) {
        currentIndex = ((index % items.length) + items.length) % items.length;
        if (activeMesh) {
            pivot.remove(activeMesh);
            activeMesh.traverse((o) => {
                if (o.geometry) o.geometry.dispose();
                if (o.material) {
                    if (Array.isArray(o.material)) o.material.forEach((m) => m.dispose());
                    else o.material.dispose();
                }
            });
        }
        const item = items[currentIndex];
        activeMesh = buildMeshForItem(item);
        // Pop-in animation
        activeMesh.scale.setScalar(0.01);
        pivot.add(activeMesh);
        if (label) label.textContent = item.label;
    }

    function buildMeshForItem(item) {
        const group = new THREE.Group();

        // Floating ring beneath the item
        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(1.4, 0.04, 16, 80),
            new THREE.MeshStandardMaterial({ color: 0xc9a7ff, emissive: 0xc9a7ff, emissiveIntensity: 0.4, metalness: 0.3, roughness: 0.4 })
        );
        ring.rotation.x = Math.PI / 2;
        ring.position.y = -1.1;
        group.add(ring);

        // The "subject" — text for letters/numbers/languages, fruit for science, etc.
        let subject;
        if (item.kind === "text") {
            subject = buildTextMesh(item.text, item.color || 0xf78aa0);
        } else if (item.kind === "shape") {
            subject = buildShape(item.shape, item.color || 0xf7b6c2);
        } else {
            subject = buildShape("sphere", 0xf78aa0);
        }
        group.add(subject);

        // Animation hooks
        group.userData = {
            popTarget: 1.0,
            spin: 0.6 + Math.random() * 0.4,
        };

        return group;
    }

    setItem(0);

    // Pointer drag
    let dragging = false;
    let lastX = 0;
    let lastY = 0;
    canvas.addEventListener("pointerdown", (e) => {
        dragging = true;
        autoRotate = false;
        lastX = e.clientX;
        lastY = e.clientY;
        canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener("pointermove", (e) => {
        if (!dragging) return;
        const dx = (e.clientX - lastX) / 120;
        const dy = (e.clientY - lastY) / 120;
        pivot.rotation.y += dx;
        pivot.rotation.x = Math.max(-0.6, Math.min(0.6, pivot.rotation.x + dy));
        lastX = e.clientX;
        lastY = e.clientY;
    });
    const stopDrag = (e) => {
        dragging = false;
        try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
    };
    canvas.addEventListener("pointerup", stopDrag);
    canvas.addEventListener("pointercancel", stopDrag);
    canvas.addEventListener("pointerleave", stopDrag);

    // Toolbar buttons
    document.querySelectorAll('[data-3d-action]').forEach((btn) => {
        btn.addEventListener("click", () => {
            const action = btn.dataset["3dAction"];
            if (action === "next") setItem(currentIndex + 1);
            if (action === "prev") setItem(currentIndex - 1);
            if (action === "rotate") autoRotate = !autoRotate;
            if (action === "speak") speak(items[currentIndex].label);
        });
    });

    // Keyboard navigation
    window.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") setItem(currentIndex + 1);
        if (e.key === "ArrowLeft") setItem(currentIndex - 1);
    });

    // Resize
    function resize() {
        const rect = canvas.getBoundingClientRect();
        const w = Math.max(rect.width, 320);
        const h = Math.max(rect.height || w * 0.6, 320);
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }
    window.addEventListener("resize", resize);
    resize();

    // Loop
    const clock = new THREE.Clock();
    function tick() {
        const dt = clock.getDelta();
        if (activeMesh) {
            // Smooth pop-in
            const target = activeMesh.userData.popTarget;
            activeMesh.scale.lerp(new THREE.Vector3(target, target, target), 0.18);
            if (autoRotate) pivot.rotation.y += dt * 0.6;
        }
        sparkles.rotation.y += dt * 0.05;
        renderer.render(scene, camera);
        requestAnimationFrame(tick);
    }
    tick();
}

// --- Item generators per category ---------------------------------------
function buildItems(category) {
    switch (category) {
        case "numbers":
            return Array.from({ length: 10 }, (_, i) => ({
                kind: "text", text: String(i), label: `Le chiffre ${i}`, color: 0x9b73f0,
            }));
        case "languages":
            return [
                { kind: "text", text: "Bonjour", label: "Bonjour 🇫🇷", color: 0xf78aa0 },
                { kind: "text", text: "Hello", label: "Hello 🇬🇧", color: 0x9b73f0 },
                { kind: "text", text: "مرحبا", label: "Marhaba 🌙", color: 0xf7b6c2 },
                { kind: "text", text: "Hola", label: "Hola 🇪🇸", color: 0xc9a7ff },
            ];
        case "islamic":
            return [
                { kind: "text", text: "نوح", label: "Histoire de Nouh (Noé)", color: 0x9b73f0 },
                { kind: "text", text: "موسى", label: "Histoire de Moussa (Moïse)", color: 0xf78aa0 },
                { kind: "text", text: "عيسى", label: "Histoire de Aïssa (Jésus)", color: 0xc9a7ff },
                { kind: "text", text: "محمد", label: "Le Prophète Mohamed ﷺ", color: 0x6db59f },
            ];
        case "science":
            return [
                { kind: "shape", shape: "sphere",     label: "La planète Terre 🌍",    color: 0x6cb1ff },
                { kind: "shape", shape: "torusKnot",  label: "Une molécule",            color: 0xf78aa0 },
                { kind: "shape", shape: "cone",       label: "Un volcan",               color: 0xff9a6c },
                { kind: "shape", shape: "icosahedron",label: "Un cristal",              color: 0x9b73f0 },
            ];
        case "art":
            return [
                { kind: "shape", shape: "torusKnot",  label: "La spirale magique", color: 0xf78aa0 },
                { kind: "shape", shape: "icosahedron",label: "Le diamant",         color: 0x9b73f0 },
                { kind: "shape", shape: "sphere",     label: "La bulle",           color: 0xc9a7ff },
                { kind: "shape", shape: "cone",       label: "Le chapeau",         color: 0xffd76c },
            ];
        case "letters":
        default: {
            const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
            return alphabet.map((ch) => ({
                kind: "text", text: ch, label: `La lettre ${ch}`,
                color: ["aeiouy".includes(ch.toLowerCase()) ? 0xf78aa0 : 0x9b73f0][0],
            }));
        }
    }
}

// --- Mesh builders ------------------------------------------------------

function buildTextMesh(text, color) {
    // Render text onto a canvas, then onto a plane — works without font loaders.
    const size = 512;
    const off = document.createElement("canvas");
    off.width = size;
    off.height = size;
    const ctx = off.getContext("2d");

    // Background: soft gradient bubble
    const grad = ctx.createRadialGradient(size / 2, size / 2, 30, size / 2, size / 2, size / 2);
    grad.addColorStop(0, "#ffffff");
    grad.addColorStop(0.7, "#ffe9f3");
    grad.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(size / 2, size / 2, size / 2 - 4, 0, Math.PI * 2);
    ctx.fill();

    // Text
    ctx.fillStyle = "#" + new THREE.Color(color).getHexString();
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const fontSize = text.length > 2 ? 150 : 320;
    ctx.font = `700 ${fontSize}px "Fredoka", "Inter", system-ui, sans-serif`;
    ctx.fillText(text, size / 2, size / 2 + 12);

    const tex = new THREE.CanvasTexture(off);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;

    // Two-sided plane so it reads from both sides
    const mat = new THREE.MeshStandardMaterial({
        map: tex,
        transparent: true,
        side: THREE.DoubleSide,
        roughness: 0.4,
        metalness: 0.05,
    });
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 2.4), mat);

    // A subtle backing disc for depth
    const disc = new THREE.Mesh(
        new THREE.CylinderGeometry(1.25, 1.25, 0.08, 64),
        new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 })
    );
    disc.rotation.x = Math.PI / 2;
    disc.position.z = -0.06;

    const group = new THREE.Group();
    group.add(disc);
    group.add(plane);
    return group;
}

function buildShape(shape, color) {
    const mat = new THREE.MeshStandardMaterial({
        color, metalness: 0.25, roughness: 0.35,
    });
    let geo;
    switch (shape) {
        case "torusKnot":   geo = new THREE.TorusKnotGeometry(0.7, 0.22, 120, 16); break;
        case "cone":        geo = new THREE.ConeGeometry(0.9, 1.6, 32); break;
        case "icosahedron": geo = new THREE.IcosahedronGeometry(1.0, 0); break;
        case "sphere":
        default:            geo = new THREE.SphereGeometry(1.0, 48, 32); break;
    }
    return new THREE.Mesh(geo, mat);
}

// --- Read-aloud (Web Speech API) ----------------------------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "fr-FR";
    u.rate = 0.95;
    u.pitch = 1.1;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}
