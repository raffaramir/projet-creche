// Little Future — main client script (vanilla JS for landing + reveal animations)

(function () {
    "use strict";

    // Mobile nav toggle
    const toggle = document.getElementById("navToggle");
    const header = document.getElementById("siteHeader");
    if (toggle && header) {
        toggle.addEventListener("click", () => header.classList.toggle("open"));
    }

    // Header shadow on scroll
    const onScroll = () => {
        if (!header) return;
        if (window.scrollY > 8) header.classList.add("scrolled");
        else header.classList.remove("scrolled");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // Reveal-on-scroll using IntersectionObserver
    const reveal = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && reveal.length) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        reveal.forEach((el) => io.observe(el));
    } else {
        reveal.forEach((el) => el.classList.add("visible"));
    }

    // Smooth-scroll for in-page anchors
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", (e) => {
            const id = anchor.getAttribute("href");
            if (id.length > 1 && document.querySelector(id)) {
                e.preventDefault();
                document.querySelector(id).scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });
})();
