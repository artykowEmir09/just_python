// ===============================
// TYPING ANIMATION
// ===============================

const words = [
    "Software Engineer",
    "Python Developer",
    "Web Developer",
    "Future Full-Stack Developer"
];

let wordIndex = 0;
let charIndex = 0;

const typingElement = document.getElementById("typing");

function typeEffect() {

    if (charIndex < words[wordIndex].length) {

        typingElement.textContent +=
            words[wordIndex].charAt(charIndex);

        charIndex++;

        setTimeout(typeEffect, 100);

    } else {

        setTimeout(deleteEffect, 1500);
    }
}

function deleteEffect() {

    if (charIndex > 0) {

        typingElement.textContent =
            words[wordIndex].substring(0, charIndex - 1);

        charIndex--;

        setTimeout(deleteEffect, 50);

    } else {

        wordIndex++;

        if (wordIndex >= words.length) {
            wordIndex = 0;
        }

        setTimeout(typeEffect, 300);
    }
}

typeEffect();


// ===============================
// MOUSE GLOW EFFECT
// ===============================

document.addEventListener("mousemove", (event) => {

    const x = event.clientX;
    const y = event.clientY;

    document.body.style.background =
        `radial-gradient(
            circle at ${x}px ${y}px,
            #071b1d,
            #080808 35%
        )`;

});


// ===============================
// SCROLL REVEAL
// ===============================

const sections = document.querySelectorAll(".section");

const observer = new IntersectionObserver(
    (entries) => {

        entries.forEach((entry) => {

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

sections.forEach((section) => {

    section.style.opacity = "0";
    section.style.transform = "translateY(50px)";
    section.style.transition = "1s ease";

    observer.observe(section);

});