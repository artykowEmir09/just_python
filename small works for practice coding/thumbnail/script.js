// ======================================
// CANVAS
// ======================================

const canvas =
    document.getElementById("thumbnailCanvas");

const ctx = canvas.getContext("2d");


// ======================================
// ELEMENTS
// ======================================

const imageInput =
    document.getElementById("imageInput");

const titleInput =
    document.getElementById("titleInput");

const subtitleInput =
    document.getElementById("subtitleInput");

const sizeInput =
    document.getElementById("sizeInput");

const sizeValue =
    document.getElementById("sizeValue");

const zoomInput =
    document.getElementById("zoomInput");

const zoomValue =
    document.getElementById("zoomValue");

const backgroundInput =
    document.getElementById("backgroundInput");

const downloadBtn =
    document.getElementById("downloadBtn");

const resetBtn =
    document.getElementById("resetBtn");


// ======================================
// VARIABLES
// ======================================

let backgroundColor = "#111111";

let textColor = "#ffffff";

let image = null;

let imageZoom = 1;


// Text positions

let titleX = 640;
let titleY = 400;

let subtitleX = 640;
let subtitleY = 510;


// Dragging

let dragging = null;

let mouseX = 0;
let mouseY = 0;


// ======================================
// DRAW THUMBNAIL
// ======================================

function drawThumbnail() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // ----------------------------
    // BACKGROUND
    // ----------------------------

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            canvas.width,
            canvas.height
        );

    gradient.addColorStop(
        0,
        backgroundColor
    );

    gradient.addColorStop(
        1,
        "#000000"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // ----------------------------
    // IMAGE
    // ----------------------------

    if (image) {

        const scale =
            Math.max(
                canvas.width / image.width,
                canvas.height / image.height
            ) * imageZoom;

        const width =
            image.width * scale;

        const height =
            image.height * scale;

        const x =
            (canvas.width - width) / 2;

        const y =
            (canvas.height - height) / 2;


        ctx.save();

        ctx.globalAlpha = 0.8;

        ctx.drawImage(
            image,
            x,
            y,
            width,
            height
        );

        ctx.restore();

    }


    // ----------------------------
    // DARK OVERLAY
    // ----------------------------

    const overlay =
        ctx.createLinearGradient(
            0,
            0,
            canvas.width,
            canvas.height
        );

    overlay.addColorStop(
        0,
        "rgba(0,0,0,0.15)"
    );

    overlay.addColorStop(
        0.5,
        "rgba(0,0,0,0.05)"
    );

    overlay.addColorStop(
        1,
        "rgba(0,0,0,0.75)"
    );

    ctx.fillStyle = overlay;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // ----------------------------
    // TOP LABEL
    // ----------------------------

    ctx.font =
        "bold 25px Arial";

    ctx.fillStyle =
        "#00ffff";

    ctx.textAlign =
        "left";

    ctx.fillText(
        "▶ NEW VIDEO",
        45,
        55
    );


    // ----------------------------
    // TITLE
    // ----------------------------

    const titleSize =
        Number(sizeInput.value);

    ctx.font =
        `900 ${titleSize}px Arial`;

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


    // Glow

    ctx.shadowColor =
        textColor;

    ctx.shadowBlur =
        20;


    ctx.fillStyle =
        textColor;

    ctx.strokeStyle =
        "#000000";

    ctx.lineWidth =
        15;


    const title =
        titleInput.value;


    ctx.strokeText(
        title,
        titleX,
        titleY
    );

    ctx.fillText(
        title,
        titleX,
        titleY
    );


    // Remove glow

    ctx.shadowBlur = 0;


    // ----------------------------
    // SUBTITLE
    // ----------------------------

    ctx.font =
        "bold 38px Arial";

    ctx.fillStyle =
        "#ffffff";

    ctx.strokeStyle =
        "#000000";

    ctx.lineWidth =
        10;

    const subtitle =
        subtitleInput.value;


    ctx.strokeText(
        subtitle,
        subtitleX,
        subtitleY
    );

    ctx.fillText(
        subtitle,
        subtitleX,
        subtitleY
    );


    // ----------------------------
    // DECORATION
    // ----------------------------

    ctx.fillStyle =
        textColor;

    ctx.fillRect(
        45,
        canvas.height - 55,
        250,
        6
    );


    ctx.font =
        "bold 20px Arial";

    ctx.fillStyle =
        "#ffffff";

    ctx.textAlign =
        "right";

    ctx.fillText(
        "THUMBLAB",
        canvas.width - 40,
        canvas.height - 35
    );

}


// ======================================
// IMAGE UPLOAD
// ======================================

imageInput.addEventListener(
    "change",
    function () {

        const file =
            this.files[0];

        if (!file) return;

        const reader =
            new FileReader();

        reader.onload =
            function (event) {

                image =
                    new Image();

                image.onload =
                    function () {

                        drawThumbnail();

                    };

                image.src =
                    event.target.result;

            };

        reader.readAsDataURL(file);

    }
);


// ======================================
// TEXT INPUTS
// ======================================

titleInput.addEventListener(
    "input",
    drawThumbnail
);

subtitleInput.addEventListener(
    "input",
    drawThumbnail
);


// ======================================
// FONT SIZE
// ======================================

sizeInput.addEventListener(
    "input",
    function () {

        sizeValue.textContent =
            this.value;

        drawThumbnail();

    }
);


// ======================================
// ZOOM
// ======================================

zoomInput.addEventListener(
    "input",
    function () {

        imageZoom =
            Number(this.value) / 100;

        zoomValue.textContent =
            this.value + "%";

        drawThumbnail();

    }
);


// ======================================
// BACKGROUND
// ======================================

backgroundInput.addEventListener(
    "input",
    function () {

        backgroundColor =
            this.value;

        drawThumbnail();

    }
);


// ======================================
// TEXT COLORS
// ======================================

const colors =
    document.querySelectorAll(".color");

colors.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                colors.forEach(
                    b => b.classList.remove("active")
                );

                this.classList.add("active");

                textColor =
                    this.dataset.color;

                drawThumbnail();

            }
        );

    }
);


// ======================================
// THEMES
// ======================================

const themes =
    document.querySelectorAll(".theme");

themes.forEach(
    function (theme) {

        theme.addEventListener(
            "click",
            function () {

                backgroundColor =
                    this.dataset.bg;

                textColor =
                    this.dataset.accent;

                backgroundInput.value =
                    backgroundColor;

                colors.forEach(
                    b => {

                        b.classList.remove(
                            "active"
                        );

                        if (
                            b.dataset.color ===
                            textColor
                        ) {

                            b.classList.add(
                                "active"
                            );

                        }

                    }
                );

                drawThumbnail();

            }
        );

    }
);


// ======================================
// MOUSE POSITION
// ======================================

function getMousePosition(event) {

    const rect =
        canvas.getBoundingClientRect();

    return {

        x:
            (event.clientX - rect.left)
            *
            (canvas.width / rect.width),

        y:
            (event.clientY - rect.top)
            *
            (canvas.height / rect.height)

    };

}


// ======================================
// DETECT TEXT
// ======================================

function isNearText(
    x,
    y,
    textX,
    textY,
    width,
    height
) {

    return (
        x > textX - width / 2 &&
        x < textX + width / 2 &&
        y > textY - height / 2 &&
        y < textY + height / 2
    );

}


// ======================================
// START DRAG
// ======================================

canvas.addEventListener(
    "mousedown",
    function (event) {

        const pos =
            getMousePosition(event);

        const titleSize =
            Number(sizeInput.value);

        const titleWidth =
            ctx.measureText(
                titleInput.value
            ).width;


        if (
            isNearText(
                pos.x,
                pos.y,
                titleX,
                titleY,
                titleWidth,
                titleSize
            )
        ) {

            dragging = "title";

        }

        else {

            const subtitleWidth =
                ctx.measureText(
                    subtitleInput.value
                ).width;

            if (
                isNearText(
                    pos.x,
                    pos.y,
                    subtitleX,
                    subtitleY,
                    subtitleWidth,
                    50
                )
            ) {

                dragging = "subtitle";

            }

        }

    }
);


// ======================================
// DRAG
// ======================================

canvas.addEventListener(
    "mousemove",
    function (event) {

        if (!dragging) return;

        const pos =
            getMousePosition(event);


        if (dragging === "title") {

            titleX = pos.x;
            titleY = pos.y;

        }


        if (dragging === "subtitle") {

            subtitleX = pos.x;
            subtitleY = pos.y;

        }


        drawThumbnail();

    }
);


// ======================================
// STOP DRAG
// ======================================

window.addEventListener(
    "mouseup",
    function () {

        dragging = null;

    }
);


// ======================================
// DOWNLOAD
// ======================================

downloadBtn.addEventListener(
    "click",
    function () {

        const link =
            document.createElement("a");

        link.download =
            "my-thumbnail.png";

        link.href =
            canvas.toDataURL("image/png");

        link.click();

    }
);


// ======================================
// RESET
// ======================================

resetBtn.addEventListener(
    "click",
    function () {

        titleInput.value =
            "YOU WON'T BELIEVE THIS!";

        subtitleInput.value =
            "THE TRUTH REVEALED";

        sizeInput.value =
            100;

        sizeValue.textContent =
            "100";

        zoomInput.value =
            100;

        zoomValue.textContent =
            "100%";

        backgroundColor =
            "#111111";

        textColor =
            "#ffffff";

        backgroundInput.value =
            "#111111";

        titleX = 640;
        titleY = 400;

        subtitleX = 640;
        subtitleY = 510;

        image = null;

        imageInput.value = "";

        drawThumbnail();

    }
);


// ======================================
// INITIAL DRAW
// ======================================

drawThumbnail();
