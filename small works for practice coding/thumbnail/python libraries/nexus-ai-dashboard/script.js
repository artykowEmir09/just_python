
/* ================================
   NEXUS AI - JAVASCRIPT
================================ */


/* ================================
   MOUSE GLOW
================================ */

const glow = document.createElement("div");

glow.classList.add("mouse-glow");

document.body.appendChild(glow);

document.addEventListener("mousemove", function (event) {

    glow.style.left = event.clientX + "px";
    glow.style.top = event.clientY + "px";

});


/* ================================
   START SYSTEM
================================ */

function startSystem() {

    const button = document.querySelector("button");

    button.innerText = "SYSTEM STARTED";

    button.style.color = "#39ff88";
    button.style.borderColor = "#39ff88";

    button.style.boxShadow =
        "0 0 15px #39ff88, 0 0 35px #39ff88";

    setTimeout(function () {

        document
            .getElementById("dashboard")
            .scrollIntoView({
                behavior: "smooth"
            });

    }, 700);

}


/* ================================
   RANDOM SYSTEM VALUES
================================ */

function randomNumber(min, max) {

    return Math.floor(
        Math.random() * (max - min + 1)
    ) + min;

}


/* ================================
   UPDATE DASHBOARD
================================ */

function updateDashboard() {

    const cpu = randomNumber(35, 85);

    const memory = randomNumber(40, 90);


    document.getElementById("cpu").innerText =
        cpu + "%";

    document.getElementById("memory").innerText =
        memory + "%";


    document.getElementById("cpuBar").style.width =
        cpu + "%";

    document.getElementById("memoryBar").style.width =
        memory + "%";

}


/* ================================
   INITIAL DASHBOARD
================================ */

setTimeout(function () {

    updateDashboard();

}, 1000);


/* ================================
   UPDATE EVERY 3 SECONDS
================================ */

setInterval(function () {

    updateDashboard();

}, 3000);


/* ================================
   CARD 3D EFFECT
================================ */

const cards = document.querySelectorAll(".card");

cards.forEach(function (card) {

    card.addEventListener("mousemove", function (event) {

        const rect = card.getBoundingClientRect();

        const x =
            event.clientX - rect.left;

        const y =
            event.clientY - rect.top;

        const centerX =
            rect.width / 2;

        const centerY =
            rect.height / 2;

        const rotateX =
            (y - centerY) / 15;

        const rotateY =
            (centerX - x) / 15;


        card.style.transform =
            `perspective(600px)
             rotateX(${rotateX}deg)
             rotateY(${rotateY}deg)
             translateY(-10px)`;

    });


    card.addEventListener("mouseleave", function () {

        card.style.transform =
            "perspective(600px) rotateX(0) rotateY(0)";

    });

});


/* ================================
   RANDOM PARTICLES
================================ */

function createParticle() {

    const particle =
        document.createElement("div");

    particle.style.position = "fixed";

    particle.style.width = "3px";
    particle.style.height = "3px";

    particle.style.borderRadius = "50%";

    particle.style.background = "#00eaff";

    particle.style.boxShadow =
        "0 0 10px #00eaff";

    particle.style.left =
        Math.random() * 100 + "vw";

    particle.style.top =
        Math.random() * 100 + "vh";

    particle.style.pointerEvents = "none";

    particle.style.zIndex = "-1";

    document.body.appendChild(particle);


    const duration =
        randomNumber(4000, 9000);


    particle.animate(

        [
            {
                transform: "translateY(0)",
                opacity: 0
            },

            {
                transform: "translateY(-200px)",
                opacity: 1
            },

            {
                transform: "translateY(-400px)",
                opacity: 0
            }
        ],

        {
            duration: duration,
            iterations: 1
        }

    );


    setTimeout(function () {

        particle.remove();

    }, duration);

}


/* ================================
   CREATE PARTICLES
================================ */

setInterval(function () {

    createParticle();

}, 300);


/* ================================
   SCROLL REVEAL
================================ */

const sections =
    document.querySelectorAll("section:not(.hero)");


const observer =
    new IntersectionObserver(

        function (entries) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.style.opacity = "1";

                    entry.target.style.transform =
                        "translateY(0)";

                }

            });

        },

        {
            threshold: 0.15
        }

    );


sections.forEach(function (section) {

    section.style.opacity = "0";

    section.style.transform =
        "translateY(50px)";

    section.style.transition =
        "opacity 1s ease, transform 1s ease";

    observer.observe(section);

});


/* ================================
   KEYBOARD EASTER EGG
================================ */

let secretCode = "";

document.addEventListener("keydown", function (event) {

    secretCode += event.key.toLowerCase();

    if (secretCode.includes("nexus")) {

        document.body.style.filter =
            "hue-rotate(120deg)";

        setTimeout(function () {

            document.body.style.filter =
                "none";

        }, 2000);

        secretCode = "";

    }

});

