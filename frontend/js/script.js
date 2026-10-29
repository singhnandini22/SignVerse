```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Progress | SignVerse</title>

    <style>
        :root {
            --primary: #5146e5;
            --primary-dark: #4035c7;
            --primary-light: #eeecff;
            --success: #16a085;
            --success-light: #e4f7f1;
            --background: #f5f7fb;
            --surface: #ffffff;
            --text: #22243a;
            --muted: #74778a;
            --border: #e8eaf2;
            --shadow: 0 8px 28px rgba(34, 36, 58, 0.06);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: var(--background);
            color: var(--text);
            min-height: 100vh;
        }

        a {
            color: inherit;
        }

        /* HEADER */
        header {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            box-shadow: 0 2px 10px rgba(34, 36, 58, 0.04);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .header-inner {
            width: 84%;
            max-width: 1400px;
            min-height: 78px;
            margin: auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        .logo {
            color: var(--primary);
            text-decoration: none;
            font-size: 27px;
            font-weight: 800;
            letter-spacing: -0.7px;
        }

        .header-nav {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .header-nav a {
            text-decoration: none;
            color: #55576a;
            font-size: 15px;
            font-weight: 600;
            padding: 29px 0;
            position: relative;
            transition: color 0.2s ease;
        }

        .header-nav a:hover,
        .header-nav a.active {
            color: var(--primary);
        }

        .header-nav a.active::after {
            content: "";
            position: absolute;
            bottom: 19px;
            left: 0;
            width: 100%;
            height: 3px;
            border-radius: 5px;
            background: var(--primary);
        }

        /* PAGE LAYOUT */
        .container {
            width: 84%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 48px 0 64px;
        }

        .welcome-section {
            margin-bottom: 38px;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: var(--primary-light);
            color: var(--primary);
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 18px;
        }

        .eyebrow-dot {
            width: 7px;
            height: 7px;
            background: var(--primary);
            border-radius: 50%;
        }

        .welcome-section h1 {
            font-size: clamp(29px, 4vw, 38px);
            letter-spacing: -1px;
            line-height: 1.2;
            margin-bottom: 13px;
        }

        .welcome-section p {
            color: var(--muted);
            line-height: 1.8;
            font-size: 16px;
            max-width: 680px;
        }

        /* SECTION HEADING */
        .section-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 20px;
        }

        .section-heading h2 {
            font-size: 23px;
            letter-spacing: -0.4px;
        }

        .section-heading p {
            font-size: 13px;
            color: var(--muted);
        }

        /* PROGRESS CARDS */
        .progress-cards {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 24px;
        }

        .progress-card {
            background: var(--surface);
            border: 1px solid rgba(232, 234, 242, 0.9);
            padding: 28px;
            border-radius: 18px;
            box-shadow: var(--shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            min-width: 0;
        }

        .progress-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(34, 36, 58, 0.09);
        }

        .card-top {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 23px;
        }

        .card-icon {
            width: 54px;
            height: 54px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            background: var(--primary-light);
            color: var(--primary);
            font-size: 23px;
            font-weight: 800;
        }

        .numbers-card .card-icon {
            background: var(--success-light);
            color: var(--success);
        }

        .card-title {
            font-size: 20px;
            margin-bottom: 6px;
        }

        .card-subtitle {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .progress-description {
            color: #696c7e;
            font-size: 14px;
            line-height: 1.7;
            margin-bottom: 26px;
        }

        .progress-info {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 14px;
        }

        .progress-label {
            display: block;
            color: var(--muted);
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .progress-percentage {
            display: block;
            color: var(--primary);
            font-size: 35px;
            line-height: 1.1;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .numbers-card .progress-percentage {
            color: var(--success);
        }

        .progress-count {
            color: #65687b;
            background: #f5f6fa;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        }

        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e9eaf2;
            border-radius: 20px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: var(--primary);
            border-radius: inherit;
            transition: width 0.6s ease;
        }

        .numbers-fill {
            background: var(--success);
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-top: 13px;
            color: var(--muted);
            font-size: 12px;
        }

        /* FOOTER ACTION */
        .page-actions {
            display: flex;
            justify-content: flex-end;
            margin-top: 30px;
        }

        .logout-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: var(--primary);
            color: #fff;
            border: none;
            border-radius: 10px;
            padding: 13px 22px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(81, 70, 229, 0.18);
            transition: background 0.2s ease, transform 0.2s ease;
        }

        .logout-button:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
        }

        .logout-button:focus-visible,
        .header-nav a:focus-visible {
            outline: 3px solid rgba(81, 70, 229, 0.35);
            outline-offset: 4px;
        }

        /* RESPONSIVE */
        @media (max-width: 850px) {
            .header-inner,
            .container {
                width: 90%;
            }

            .progress-cards {
                gap: 18px;
            }

            .progress-card {
                padding: 23px;
            }

            .header-nav {
                gap: 22px;
            }
        }

        @media (max-width: 650px) {
            .header-inner {
                min-height: auto;
                padding-top: 17px;
                flex-direction: column;
                gap: 8px;
            }

            .logo {
                font-size: 25px;
            }

            .header-nav {
                width: 100%;
                justify-content: center;
                gap: 30px;
            }

            .header-nav a {
                padding: 14px 0 17px;
                font-size: 14px;
            }

            .header-nav a.active::after {
                bottom: 8px;
            }

            .container {
                padding-top: 32px;
                padding-bottom: 40px;
            }

            .welcome-section {
                margin-bottom: 30px;
            }

            .welcome-section h1 {
                font-size: 29px;
            }

            .welcome-section p {
                font-size: 14px;
            }

            .section-heading h2 {
                font-size: 21px;
            }

            .section-heading p {
                display: none;
            }

            .progress-cards {
                grid-template-columns: 1fr;
            }

            .progress-card {
                padding: 23px;
                border-radius: 15px;
            }

            .page-actions {
                margin-top: 24px;
            }

            .logout-button {
                width: 100%;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }
        }
    </style>
</head>

<body>

    <!-- HEADER -->
    <header>
        <div class="header-inner">
            <a href="index.html" class="logo">SignVerse</a>

            <nav class="header-nav" aria-label="Main navigation">
                <a href="index.html">Home</a>
                <a href="dashboard.html">Learn</a>
                <a href="progress.html" class="active"
                   aria-current="page">Progress</a>
            </nav>
        </div>
    </header>

    <!-- MAIN CONTENT -->
    <main class="container">

        <section class="welcome-section">
            <div class="eyebrow">
                <span class="eyebrow-dot"></span>
                Your learning journey
            </div>

            <h1>Your Learning Progress</h1>

            <p>
                Every sign you learn is a step forward.
                Track your progress through the alphabet and numbers
                as you build your sign language skills.
            </p>
        </section>

        <!-- PROGRESS SECTION -->
        <section class="progress-section">
            <div class="section-heading">
                <h2>My Progress</h2>
                <p>Keep learning, one sign at a time.</p>
            </div>

            <div class="progress-cards">

                <!-- LETTERS -->
                <article class="progress-card">
                    <div class="card-top">
                        <div class="card-icon" aria-hidden="true">A–Z</div>

                        <div>
                            <h3 class="card-title">Letters</h3>
                            <p class="card-subtitle">
                                The sign language alphabet
                            </p>
                        </div>
                    </div>

                    <p class="progress-description">
                        Learn the signs for all 26 letters and build
                        a strong foundation for communication.
                    </p>

                    <div class="progress-info">
                        <div>
                            <span class="progress-label">Completed</span>
                            <span class="progress-percentage"
                                  id="letters-progress">0%</span>
                        </div>

                        <span class="progress-count"
                              id="letters-progress-text">
                            0 of 26 letters
                        </span>
                    </div>

                    <div
                        class="progress-bar"
                        role="progressbar"
                        aria-label="Letters learning progress"
                        aria-valuemin="0"
                        aria-valuemax="100"
                        aria-valuenow="0"
                        id="letters-progress-bar"
                    >
                        <div
                            class="progress-fill"
                            id="letters-progress-fill"
                        ></div>
                    </div>

                    <div class="card-footer">
                        <span>Alphabet practice</span>
                        <span>26 letters total</span>
                    </div>
                </article>

                <!-- NUMBERS -->
                <article class="progress-card numbers-card">
                    <div class="card-top">
                        <div class="card-icon" aria-hidden="true">123</div>

                        <div>
                            <h3 class="card-title">Numbers</h3>
                            <p class="card-subtitle">
                                Sign language numbers 1–10
                            </p>
                        </div>
                    </div>

                    <p class="progress-description">
                        Practice number signs from 1 to 10 and grow
                        more confident recognising each sign.
                    </p>

                    <div class="progress-info">
                        <div>
                            <span class="progress-label">Completed</span>
                            <span class="progress-percentage"
                                  id="numbers-progress">0%</span>
                        </div>

                        <span class="progress-count"
                              id="numbers-progress-text">
                            0 of 10 numbers
                        </span>
                    </div>

                    <div
                        class="progress-bar"
                        role="progressbar"
                        aria-label="Numbers learning progress"
                        aria-valuemin="0"
                        aria-valuemax="100"
                        aria-valuenow="0"
                        id="numbers-progress-bar"
                    >
                        <div
                            class="progress-fill numbers-fill"
                            id="numbers-progress-fill"
                        ></div>
                    </div>

                    <div class="card-footer">
                        <span>Number practice</span>
                        <span>10 numbers total</span>
                    </div>
                </article>

            </div>
        </section>

        <div class="page-actions">
            <button class="logout-button"
                    id="logout-button"
                    type="button">
                Log out
                <span aria-hidden="true">→</span>
            </button>
        </div>

    </main>

    <script>
        // Read saved user information without redirecting to login
        let user = {};

        try {
            const savedUser = localStorage.getItem("user");
            user = savedUser ? JSON.parse(savedUser) || {} : {};

            if (!user || typeof user !== "object" || Array.isArray(user)) {
                user = {};
            }
        } catch (error) {
            console.error("Could not read saved user:", error);
            user = {};
        }

        // Display saved progress
        function displayProgress(value, type) {
            const percentage = Math.max(
                0,
                Math.min(100, Number(value) || 0)
            );

            const total = type === "letters" ? 26 : 10;
            const completed = Math.round((percentage / 100) * total);

            const progressElement =
                document.getElementById(type + "-progress");

            const textElement =
                document.getElementById(type + "-progress-text");

            const fillElement =
                document.getElementById(type + "-progress-fill");

            const barElement =
                document.getElementById(type + "-progress-bar");

            const itemName = type === "letters" ? "letters" : "numbers";

            if (progressElement) {
                progressElement.textContent = Math.round(percentage) + "%";
            }

            if (textElement) {
                textElement.textContent =
                    completed + " of " + total + " " + itemName;
            }

            if (fillElement) {
                fillElement.style.width = percentage + "%";
            }

            if (barElement) {
                barElement.setAttribute("aria-valuenow", percentage);
            }
        }

        displayProgress(user.letters_progress, "letters");
        displayProgress(user.numbers_progress, "numbers");

        // Logout
        document
            .getElementById("logout-button")
            .addEventListener("click", function () {
                localStorage.removeItem("access_token");
                localStorage.removeItem("user");
                window.location.href = "login.html";
            });
    </script>

</body>
</html>
```