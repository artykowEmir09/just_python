let THREE = null;

const $ = (id) => document.getElementById(id);

const museum = $("museum");

const works = [
  {
    title: "The shape of silence",
    subtitle: "01 / DIGITAL STUDY",
    palette: ["#e1d5b5", "#b76743", "#313f35"],
    description:
      "A suspended circle meets a quiet horizon. This original digital study explores balance through an almost empty landscape.",
    kind: "landscape"
  },
  {
    title: "A sun held still",
    subtitle: "02 / DIGITAL STUDY",
    palette: ["#c36b44", "#edbe76", "#752e27"],
    description:
      "An imagined sun rests above a field of warm terracotta. Hard edges and soft grain create a conversation between stillness and heat.",
    kind: "sun"
  },
  {
    title: "Between two tides",
    subtitle: "03 / DIGITAL STUDY",
    palette: ["#c2d2d0", "#5f8c8e", "#224f60"],
    description:
      "Layered waves fold into one another. An abstract study of the boundary between water, sky, and memory.",
    kind: "waves"
  },
  {
    title: "Earth remembers",
    subtitle: "04 / DIGITAL STUDY",
    palette: ["#cdc29b", "#7c8962", "#b06e49"],
    description:
      "Olive, clay, and sand become a landscape with no fixed location. A small meditation on the colours we carry with us.",
    kind: "earth"
  },
  {
    title: "Soft architecture",
    subtitle: "05 / DIGITAL STUDY",
    palette: ["#dac2a2", "#a87959", "#5e634e"],
    description:
      "An arrangement of arches and shadows, built from the simplest shapes. Architecture becomes a rhythm rather than a place.",
    kind: "arches"
  },
  {
    title: "The blue hour",
    subtitle: "06 / DIGITAL STUDY",
    palette: ["#31465c", "#9baeb1", "#e6d7a6"],
    description:
      "A moonlit composition in indigo and pale gold. The last light creates a quiet space between day and night.",
    kind: "moon"
  }
];

let scene;
let camera;
let renderer;
let raycaster;
let clock;

let active = false;
let selectedWork = null;
let previousFocus = null;

let yaw = 0;
let pitch = 0;
let dragging = false;

let lastPointer = {
  x: 0,
  y: 0
};

const pressed = new Set();

const artworkMeshes = [];

const moveVector = new THREE.Vector3();
const direction = new THREE.Vector3();

const velocity = 3.2;

const bounds = {
  x: 5.75,
  z: 12.0
};

let audioContext = null;
let ambientOscillator = null;
let ambientGain = null;
let soundOn = false;


// ========================================
// CREATE ARTWORK TEXTURES
// ========================================

function makeArtworkTexture(work, index) {
  const canvas = document.createElement("canvas");

  canvas.width = 600;
  canvas.height = 760;

  const ctx = canvas.getContext("2d");

  const [bg, mid, dark] = work.palette;

  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, 600, 760);

  if (work.kind === "arches") {

    ctx.fillStyle = mid;

    for (let i = 0; i < 3; i++) {

      ctx.beginPath();

      ctx.roundRect(
        55 + i * 175,
        160 + (i % 2) * 35,
        135,
        560,
        [75, 75, 0, 0]
      );

      ctx.fill();
    }

    ctx.fillStyle = dark;
    ctx.fillRect(0, 625, 600, 135);

  } else {

    ctx.fillStyle = mid;

    ctx.beginPath();

    ctx.arc(
      300,
      265,
      work.kind === "sun" ? 150 : 112,
      0,
      Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle = dark;

    ctx.beginPath();

    ctx.moveTo(0, 505);

    for (let x = 0; x <= 600; x += 5) {

      ctx.lineTo(
        x,
        480 + Math.sin(x / 115 + index) * 55
      );

    }

    ctx.lineTo(600, 760);
    ctx.lineTo(0, 760);

    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = mid;

    ctx.beginPath();

    ctx.moveTo(0, 640);

    for (let x = 0; x <= 600; x += 5) {

      ctx.lineTo(
        x,
        630 + Math.cos(x / 125 + index) * 28
      );

    }

    ctx.lineTo(600, 760);
    ctx.lineTo(0, 760);

    ctx.closePath();
    ctx.fill();
  }

  // Add subtle grain.

  let seed = 913 + index * 31;

  for (let i = 0; i < 12000; i++) {

    seed = (seed * 16807) % 2147483647;

    const x = seed % 600;

    seed = (seed * 16807) % 2147483647;

    ctx.fillStyle =
      i % 2 ? "#ffffff10" : "#0000000b";

    ctx.fillRect(x, seed % 760, 1, 1);
  }

  const texture = new THREE.CanvasTexture(canvas);

  texture.colorSpace = THREE.SRGBColorSpace;

  return texture;
}


// ========================================
// CREATE BOXES
// ========================================

function addBox(w, h, d, x, y, z, color, materialOptions = {}) {

  const mesh = new THREE.Mesh(

    new THREE.BoxGeometry(w, h, d),

    new THREE.MeshStandardMaterial({
      color,
      roughness: 0.92,
      ...materialOptions
    })

  );

  mesh.position.set(x, y, z);

  scene.add(mesh);

  return mesh;
}


// ========================================
// BUILD 3D GALLERY
// ========================================

function buildGallery() {

  scene = new THREE.Scene();

  scene.background = new THREE.Color("#c8cbc1");

  scene.fog = new THREE.Fog("#c8cbc1", 18, 34);


  camera = new THREE.PerspectiveCamera(
    68,
    1,
    0.1,
    80
  );

  camera.position.set(0, 1.65, 10.5);


  renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
  });

  renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
  );

  renderer.outputColorSpace = THREE.SRGBColorSpace;

  renderer.toneMapping = THREE.ACESFilmicToneMapping;

  renderer.toneMappingExposure = 1.15;

  museum.prepend(renderer.domElement);


  renderer.domElement.setAttribute(
    "aria-label",
    "Interactive 3D museum. Use WASD to walk, drag to look, and click an artwork to inspect it."
  );

  renderer.domElement.setAttribute("tabindex", "0");


  // LIGHTING

  scene.add(
    new THREE.HemisphereLight(
      "#fff8e9",
      "#747b68",
      2.0
    )
  );


  const sun = new THREE.DirectionalLight(
    "#fff1d6",
    2.2
  );

  sun.position.set(-5, 9, 7);

  scene.add(sun);


  const fill = new THREE.DirectionalLight(
    "#d8e0d3",
    0.8
  );

  fill.position.set(6, 5, -8);

  scene.add(fill);


  // FLOOR

  const floor = new THREE.Mesh(

    new THREE.PlaneGeometry(14, 29),

    new THREE.MeshStandardMaterial({
      color: "#bdbba9",
      roughness: 1
    })

  );

  floor.rotation.x = -Math.PI / 2;

  floor.position.set(0, 0, 1);

  scene.add(floor);


  // CEILING

  const ceiling = new THREE.Mesh(

    new THREE.PlaneGeometry(14, 29),

    new THREE.MeshStandardMaterial({
      color: "#e8e5d9",
      roughness: 1,
      side: THREE.DoubleSide
    })

  );

  ceiling.rotation.x = Math.PI / 2;

  ceiling.position.set(0, 5.5, 1);

  scene.add(ceiling);
           

  // WALLS

  addBox(14, 5.5, 0.22, 0, 2.75, -13.5, "#d8dbcf");

  addBox(0.22, 5.5, 29, -7, 2.75, 1, "#e3e2d6");

  addBox(0.22, 5.5, 29, 7, 2.75, 1, "#d5d8cc");


  // FLOOR DETAILS

  for (let z = -12; z <= 14; z += 2) {

    addBox(
      13.9,
      0.012,
      0.018,
      0,
      0.012,
      z,
      "#a8aa9a"
    );

  }

  for (let x = -6; x <= 6; x += 2) {

    addBox(
      0.015,
      0.012,
      27.8,
      x,
      0.014,
      1,
      "#a8aa9a"
    );

  }


  // CEILING LIGHTS

  for (let z = -10; z <= 10; z += 5) {

    const lightPanel = new THREE.Mesh(

      new THREE.PlaneGeometry(6, 0.42),

      new THREE.MeshBasicMaterial({
        color: "#fffdf1"
      })

    );

    lightPanel.rotation.x = Math.PI / 2;

    lightPanel.position.set(0, 5.46, z);

    scene.add(lightPanel);


    const glow = new THREE.PointLight(
      "#fff0d7",
      0.38,
      8
    );

    glow.position.set(0, 4.9, z);

    scene.add(glow);

  }


  // ARTWORK POSITIONS

  const placements = [

    {
      pos: [-3.15, 2.9, -13.34],
      rot: [0, 0, 0]
    },

    {
      pos: [3.15, 2.9, -13.34],
      rot: [0, 0, 0]
    },

    {
      pos: [-6.83, 2.9, -5.1],
      rot: [0, Math.PI / 2, 0]
    },

    {
      pos: [-6.83, 2.9, 4.1],
      rot: [0, Math.PI / 2, 0]
    },

    {
      pos: [6.83, 2.9, -5.1],
      rot: [0, -Math.PI / 2, 0]
    },

    {
      pos: [6.83, 2.9, 4.1],
      rot: [0, -Math.PI / 2, 0]
    }

  ];


  // CREATE ARTWORK

  works.forEach((work, i) => {

    const p = placements[i];


    const frame = new THREE.Mesh(

      new THREE.BoxGeometry(2.62, 3.18, 0.16),

      new THREE.MeshStandardMaterial({
        color: "#514c3f",
        roughness: 0.8
      })

    );

    frame.position.set(...p.pos);

    frame.rotation.set(...p.rot);

    scene.add(frame);


    const art = new THREE.Mesh(

      new THREE.PlaneGeometry(2.34, 2.9),

      new THREE.MeshBasicMaterial({
        map: makeArtworkTexture(work, i),
        side: THREE.DoubleSide
      })

    );

    art.position.copy(frame.position);


    const normal = new THREE.Vector3(0, 0, 1)
      .applyEuler(frame.rotation);

    art.position.addScaledVector(normal, 0.09);

    art.rotation.copy(frame.rotation);

    art.userData.workIndex = i;

    scene.add(art);

    artworkMeshes.push(art);

  });


  // CENTRAL BENCH

  addBox(3, 0.5, 2, -0.2, 0.55, 0, "#b4ac94");

  addBox(3, 0.55, 0.12, -0.2, 0.275, 1.0, "#8c8d7d");

  addBox(0.12, 0.55, 2, -1.7, 0.275, 0, "#969884");

  addBox(0.12, 0.55, 2, 1.3, 0.275, 0, "#858977");


  raycaster = new THREE.Raycaster();

  clock = new THREE.Clock();


  resize();


  // EVENTS

  renderer.domElement.addEventListener(
    "pointerdown",
    onPointerDown
  );

  renderer.domElement.addEventListener(
    "pointermove",
    onPointerMove
  );

  renderer.domElement.addEventListener(
    "pointerup",
    onPointerUp
  );

  renderer.domElement.addEventListener(
    "pointercancel",
    onPointerUp
  );

  renderer.domElement.addEventListener(
    "click",
    inspectAtCenter
  );

  window.addEventListener("resize", resize);


  // FINISH LOADING

  $("loading").classList.add("done");

  animate();

}


// ========================================
// RESIZE
// ========================================

function resize() {

  if (!renderer) return;

  const width = museum.clientWidth;

  const height = museum.clientHeight;

  camera.aspect = width / height;

  camera.updateProjectionMatrix();

  renderer.setSize(width, height, false);

}


// ========================================
// CAMERA
// ========================================

function updateCamera() {

  camera.rotation.order = "YXZ";

  camera.rotation.y = yaw;

  camera.rotation.x = pitch;

}


// ========================================
// MOUSE CONTROLS
// ========================================

function onPointerDown(event) {

  if (!active || event.target.closest("button")) {
    return;
  }

  dragging = true;

  lastPointer = {
    x: event.clientX,
    y: event.clientY
  };

  renderer.domElement.setPointerCapture?.(
    event.pointerId
  );

}


function onPointerMove(event) {

  if (!dragging || !active) return;

  const dx = event.clientX - lastPointer.x;

  const dy = event.clientY - lastPointer.y;


  yaw -= dx * 0.0045;

  pitch = Math.max(
    -0.65,
    Math.min(0.65, pitch - dy * 0.003)
  );


  lastPointer = {
    x: event.clientX,
    y: event.clientY
  };


  updateCamera();

}


function onPointerUp() {

  dragging = false;

}


// ========================================
// PLAYER MOVEMENT
// ========================================

function tryMove(dt) {

  if (
    !active ||
    $("modal").classList.contains("open")
  ) {
    return;
  }


  if (pressed.has("ArrowLeft")) {
    yaw += dt * 1.25;
  }

  if (pressed.has("ArrowRight")) {
    yaw -= dt * 1.25;
  }


  const forward =

    (pressed.has("KeyW") || pressed.has("ArrowUp") ? 1 : 0) -

    (pressed.has("KeyS") || pressed.has("ArrowDown") ? 1 : 0);


  const side =

    (pressed.has("KeyD") ? 1 : 0) -

    (pressed.has("KeyA") ? 1 : 0);


  if (!forward && !side) return;


  direction.set(
    -Math.sin(yaw),
    0,
    -Math.cos(yaw)
  );


  const right = new THREE.Vector3(
    Math.cos(yaw),
    0,
    -Math.sin(yaw)
  );


  moveVector.copy(direction)
    .multiplyScalar(forward)
    .addScaledVector(right, side);


  if (moveVector.lengthSq() > 0) {

    moveVector.normalize()
      .multiplyScalar(velocity * dt);

  }


  const nx = THREE.MathUtils.clamp(
    camera.position.x + moveVector.x,
    -bounds.x,
    bounds.x
  );


  const nz = THREE.MathUtils.clamp(
    camera.position.z + moveVector.z,
    -bounds.z,
    bounds.z
  );


  // Avoid walking through the central bench.

  const insideBench =

    Math.abs(nx + 0.2) < 1.85 &&

    Math.abs(nz) < 1.3;


  if (!insideBench) {

    camera.position.x = nx;

    camera.position.z = nz;

  }

}


// ========================================
// ARTWORK DETECTION
// ========================================

function findTarget() {

  raycaster.setFromCamera(
    new THREE.Vector2(0, 0),
    camera
  );


  const hits = raycaster.intersectObjects(
    artworkMeshes,
    false
  );


  selectedWork = hits.length
    ? hits[0].object.userData.workIndex
    : null;


  $("inspectBtn").style.display =

    active && selectedWork !== null
      ? "block"
      : "none";


  $("crosshair").style.display =
    active ? "block" : "none";


  $("statusText").textContent =

    selectedWork !== null
      ? `In view: ${works[selectedWork].title}`
      : "Wander through the collection.";

}


// ========================================
// ANIMATION LOOP
// ========================================

function animate() {

  requestAnimationFrame(animate);

  const dt = Math.min(clock.getDelta(), 0.05);

  tryMove(dt);

  updateCamera();

  if (active) {
    findTarget();
  }

  renderer.render(scene, camera);

}


// ========================================
// ENTER GALLERY
// ========================================

function enterGallery() {

  active = true;

  $("welcome").classList.add("hidden");

  $("statusText").textContent =
    "WASD to walk · Drag to look · Click a work to explore";

  renderer.domElement.focus();

}


// ========================================
// RETURN HOME
// ========================================

function goHome() {

  camera.position.set(0, 1.65, 10.5);

  yaw = 0;

  pitch = 0;

  updateCamera();

}


// ========================================
// INSPECT ARTWORK
// ========================================

function inspectAtCenter(event) {

  if (!active || event.target.closest("button")) {
    return;
  }

  if (selectedWork !== null) {

    showArtwork(selectedWork);

  }

}


// ========================================
// MODAL
// ========================================

function openModal(html) {

  previousFocus = document.activeElement;

  pressed.clear();

  $("modalContent").innerHTML = html;

  $("modal").classList.add("open");

  $("modal").setAttribute("aria-hidden", "false");

  $("closeModal").focus();

}


function closeModal() {

  $("modal").classList.remove("open");

  $("modal").setAttribute("aria-hidden", "true");

  previousFocus?.focus();

}


// ========================================
// SHOW ARTWORK
// ========================================

function showArtwork(index) {

  const work = works[index];

  const texture = makeArtworkTexture(work, index);

  const image = new Image();

  image.src = texture.image.toDataURL();


  openModal(`

    <p class="eyebrow">
      ORIGINAL DIGITAL STUDY · ${String(index + 1).padStart(2, "0")}
    </p>

    <h2 id="modalTitle">${work.title}</h2>

    <img
      class="art-detail-image"
      alt="${work.title}"
      src="${image.src}"
    >

    <p>${work.description}</p>

    <p class="eyebrow">
      ATELIER COLLECTION / GENERATIVE CANVAS
    </p>

  `);

}


// ========================================
// COLLECTION
// ========================================

function showCollection() {

  openModal(`

    <p class="eyebrow">
      THE QUIET COLLECTION
    </p>

    <h2 id="modalTitle">
      Six ways of seeing.
    </h2>

    <p>
      Original digital compositions created for this virtual exhibition.
      Select a work to look closer.
    </p>

    <div class="art-grid">

      ${works.map((w, i) => `

        <button class="art-card" data-art="${i}">

          <strong>${w.title}</strong>

          <small>
            ${String(i + 1).padStart(2, "0")} / DIGITAL STUDY
          </small>

        </button>

      `).join("")}

    </div>

  `);


  document.querySelectorAll("[data-art]").forEach(button => {

    button.addEventListener("click", () => {

      showArtwork(Number(button.dataset.art));

    });

  });

}


// ========================================
// ABOUT
// ========================================

function showAbout() {

  openModal(`

    <p class="eyebrow">
      WELCOME TO ATELIER
    </p>

    <h2 id="modalTitle">
      Room to be curious.
    </h2>

    <p>
      ATELIER is a virtual museum designed for a slower kind of browsing.
      Walk through a light-filled gallery, find a composition that draws
      you in, and take a moment to look.
    </p>

    <p>
      This first exhibition, Studies in Stillness, brings together
      six original, procedurally drawn digital studies of landscape
      and abstract form.
    </p>

    <p>
      No tickets. No rush. Just a space to explore.
    </p>

  `);

}


// ========================================
// VISITOR GUIDE
// ========================================

function showGuide() {

  openModal(`

    <p class="eyebrow">
      MAKE YOURSELF AT HOME
    </p>

    <h2 id="modalTitle">
      Your visit, your pace.
    </h2>

    <p>

      <span class="key">W A S D</span>
      Walk forward, left, backward, and right.

      <br><br>

      <span class="key">↑ ↓</span>
      Walk.

      <span class="key">← →</span>
      Turn.

      <br><br>

      Drag across the gallery to look around.

      <br><br>

      Click an artwork when it is in the centre of your view.

      <br><br>

      On a phone, use the arrow pad and swipe to look around.

      <br><br>

      Press <span class="key">E</span> to inspect artwork.

      <br><br>

      Press <span class="key">Esc</span> to close an exhibit.

    </p>

  `);

}


// ========================================
// FULLSCREEN
// ========================================

function toggleFullscreen() {

  if (document.fullscreenElement) {

    document.exitFullscreen?.();

  } else {

    museum.requestFullscreen?.();

  }

}


// ========================================
// AMBIENT SOUND
// ========================================

function toggleSound() {

  if (!audioContext) {

    const AudioCtx =
      window.AudioContext ||
      window.webkitAudioContext;

    if (!AudioCtx) return;


    audioContext = new AudioCtx();

    ambientOscillator =
      audioContext.createOscillator();

    ambientGain =
      audioContext.createGain();


    ambientOscillator.type = "sine";

    ambientOscillator.frequency.value = 110;

    ambientGain.gain.value = 0;


    ambientOscillator
      .connect(ambientGain)
      .connect(audioContext.destination);


    ambientOscillator.start();

  }


  if (audioContext.state === "suspended") {

    audioContext.resume();

  }


  soundOn = !soundOn;


  ambientGain.gain.setTargetAtTime(

    soundOn ? 0.018 : 0,

    audioContext.currentTime,

    0.35

  );


  $("soundBtn").classList.toggle(
    "sound-active",
    soundOn
  );


  $("soundBtn").setAttribute(

    "aria-label",

    soundOn
      ? "Turn ambient sound off"
      : "Turn ambient sound on"

  );

}


// ========================================
// BUTTON EVENTS
// ========================================

$("enterBtn").addEventListener(
  "click",
  enterGallery
);

$("collectionBtn").addEventListener(
  "click",
  showCollection
);

$("aboutBtn").addEventListener(
  "click",
  showAbout
);

$("guideBtn").addEventListener(
  "click",
  showGuide
);

$("closeModal").addEventListener(
  "click",
  closeModal
);


$("modal").addEventListener("click", event => {

  if (event.target === $("modal")) {

    closeModal();

  }

});


$("homeBtn").addEventListener(
  "click",
  goHome
);

$("fullscreenBtn").addEventListener(
  "click",
  toggleFullscreen
);

$("soundBtn").addEventListener(
  "click",
  toggleSound
);


$("inspectBtn").addEventListener("click", () => {

  if (selectedWork !== null) {

    showArtwork(selectedWork);

  }

});


// ========================================
// KEYBOARD EVENTS
// ========================================

window.addEventListener("keydown", event => {

  if (
    event.key === "Escape" &&
    $("modal").classList.contains("open")
  ) {

    closeModal();

  }


  if (
    ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "]
      .includes(event.key) &&
    active
  ) {

    event.preventDefault();

  }


  if (
    event.code === "KeyE" &&
    active &&
    selectedWork !== null &&
    !$("modal").classList.contains("open")
  ) {

    showArtwork(selectedWork);

    return;

  }


  if (
    event.code.startsWith("Key") ||
    event.code.startsWith("Arrow")
  ) {

    pressed.add(event.code);

  }

});


window.addEventListener("keyup", event => {

  pressed.delete(event.code);

});


window.addEventListener("blur", () => {

  pressed.clear();

  dragging = false;

});


// ========================================
// MOBILE MOVEMENT BUTTONS
// ========================================

document.querySelectorAll("[data-move]").forEach(button => {

  const map = {

    forward: "KeyW",

    back: "KeyS",

    left: "KeyA",

    right: "KeyD"

  };


  const code = map[button.dataset.move];


  button.addEventListener("pointerdown", event => {

    event.preventDefault();

    if (!active) {

      enterGallery();

    }

    pressed.add(code);

    button.setPointerCapture?.(event.pointerId);

  });


  const release = () => {

    pressed.delete(code);

  };


  button.addEventListener("pointerup", release);

  button.addEventListener("pointercancel", release);

  button.addEventListener("lostpointercapture", release);

});


// ========================================
// MODAL KEYBOARD ACCESSIBILITY
// ========================================

$("modal").addEventListener("keydown", event => {

  if (event.key !== "Tab") return;


  const focusable = [

    ...$("modal").querySelectorAll(

      "button, [href], input, [tabindex]:not([tabindex='-1'])"

    )

  ];


  if (!focusable.length) return;


  if (
    event.shiftKey &&
    document.activeElement === focusable[0]
  ) {

    event.preventDefault();

    focusable.at(-1).focus();

  } else if (

    !event.shiftKey &&
    document.activeElement === focusable.at(-1)

  ) {

    event.preventDefault();

    focusable[0].focus();

  }

});


// ========================================
// START GALLERY
// ========================================

async function startGallery() {

  try {

    $("loading").innerHTML = `

      <div class="loading-mark">A</div>

      <p>Preparing the gallery...</p>

    `;


    // Load Three.js dynamically.
    // If the CDN fails, the error will be displayed.

    const module = await import(

      "https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js"

    );


    THREE = module;


    // Build the 3D gallery only after Three.js loads.

    buildGallery();


  } catch (error) {

    console.error("Gallery loading error:", error);


    $("loading").classList.remove("done");


    $("loading").innerHTML = `

      <div style="max-width:450px;padding:25px;text-align:center">

        <h2 style="font-family:Georgia,serif;font-weight:normal">
          Gallery could not load
        </h2>

        <p style="line-height:1.7">
          Something went wrong while loading the 3D gallery.
        </p>

        <p style="font-size:12px;color:#a14d3b;word-break:break-word">
          ${error.message}
        </p>

        <button
          onclick="location.reload()"
          style="
            padding:12px 22px;
            margin-top:12px;
            background:#344536;
            color:white;
            border:0;
            cursor:pointer;
          "
        >
          Try again
        </button>

      </div>

    `;

  }

}


// Start the application.

startGallery();