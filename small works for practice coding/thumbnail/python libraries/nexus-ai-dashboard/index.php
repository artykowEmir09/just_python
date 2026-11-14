<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>NEXUS AI</title>

    <link rel="stylesheet" href="style.css">
</head>

<body>

    <nav>
        <div class="logo">NEXUS<span>AI</span></div>

        <div class="nav-links">
            <a href="#home">Home</a>
            <a href="#dashboard">Dashboard</a>
            <a href="#about">About</a>
        </div>
    </nav>

    <main id="home">

        <section class="hero">

            <div class="hero-text">

                <p class="status">
                    ● SYSTEM ONLINE
                </p>

                <h1>
                    Welcome to
                    <span>NEXUS AI</span>
                </h1>

                <p>
                    The next generation of intelligent
                    digital experiences.
                </p>

                <button onclick="startSystem()">
                    START SYSTEM
                </button>

            </div>

            <div class="orb">
                <div class="orb-core"></div>
            </div>

        </section>


        <section id="dashboard">

            <h2>System Dashboard</h2>

            <div class="cards">

                <div class="card">
                    <h3>CPU</h3>
                    <strong id="cpu">0%</strong>

                    <div class="progress">
                        <div id="cpuBar"></div>
                    </div>
                </div>

                <div class="card">
                    <h3>Memory</h3>
                    <strong id="memory">0%</strong>

                    <div class="progress">
                        <div id="memoryBar"></div>
                    </div>
                </div>

                <div class="card">
                    <h3>AI Status</h3>
                    <strong class="online">ONLINE</strong>
                </div>

            </div>

        </section>


        <section id="about">

            <h2>About NEXUS</h2>

            <p>
                NEXUS is an experimental AI interface
                built using HTML, CSS, JavaScript and PHP.
            </p>

        </section>

    </main>


    <footer>
        NEXUS AI © <?php echo date("Y"); ?>
    </footer>


    <script src="script.js"></script>

</body>
</html>