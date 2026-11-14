// ==============================
// CUSTOM CURSOR
// ==============================

const cursor = document.querySelector(".cursor");

document.addEventListener("mousemove", (event) => {

    cursor.style.left = event.clientX + "px";
    cursor.style.top = event.clientY + "px";

});


// ==============================
// COUNTDOWN
// ==============================

const targetDate =
    new Date("January 1, 2077 00:00:00").getTime();

function updateCountdown() {

    const now = new Date().getTime();

    const difference = targetDate - now;

    if (difference <= 0) {
        return;
    }

    const days =
        Math.floor(difference / (1000 * 60 * 60 * 24));

    const hours =
        Math.floor(
            (difference / (1000 * 60 * 60)) % 24
        );

    const minutes =
        Math.floor(
            (difference / (1000 * 60)) % 60
        );

    const seconds =
        Math.floor(
            (difference / 1000) % 60
        );

    document.getElementById("days").textContent =
        String(days).padStart(2, "0");

    document.getElementById("hours").textContent =
        String(hours).padStart(2, "0");

    document.getElementById("minutes").textContent =
        String(minutes).padStart(2, "0");

    document.getElementById("seconds").textContent =
        String(seconds).padStart(2, "0");
}

setInterval(updateCountdown, 1000);

updateCountdown();


// ==============================
// BUTTON EFFECT
// ==============================

const neonButton =
    document.querySelector(".neon-btn");

neonButton.addEventListener("click", () => {

    neonButton.textContent = "SYSTEM ACTIVE";

    setTimeout(() => {

        neonButton.textContent = "ENTER SYSTEM";

    }, 2000);

});


// ==============================
// CARD 3D EFFECT
// ==============================

const cards =
    document.querySelectorAll(".card");

cards.forEach((card) => {

    card.addEventListener("mousemove", (event) => {

        const rect = card.getBoundingClientRect();

        const x =
            event.clientX - rect.left;

        const y =
            event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

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

    card.addEventListener("mouseleave", () => {

        card.style.transform =
            "perspective(600px) rotateX(0) rotateY(0)";

    });

});
