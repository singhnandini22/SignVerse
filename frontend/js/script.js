// ================================
// DASHBOARD
// ================================

const dashboard = document.querySelector(".dashboard");

if (dashboard) {
    const savedUser = localStorage.getItem("user");
    const token = localStorage.getItem("access_token");

    // Check login information
    if (!savedUser || !token) {
        window.location.href = "login.html";
    } else {
        try {
            const user = JSON.parse(savedUser);

            if (!user || typeof user !== "object") {
                throw new Error("Invalid saved user data");
            }

            // USER NAME
            const userName = document.getElementById("user-name");

            if (userName) {
                userName.textContent = user.name || "User";
            }

            // GET AND VALIDATE PROGRESS
            let lettersProgress = Number(user.letters_progress) || 0;
            let numbersProgress = Number(user.numbers_progress) || 0;

            lettersProgress = Math.max(0, Math.min(100, lettersProgress));
            numbersProgress = Math.max(0, Math.min(100, numbersProgress));

            // LETTERS PROGRESS
            const lettersPercentage =
                document.getElementById("letters-progress");

            const lettersFill =
                document.getElementById("letters-progress-fill");

            const lettersCount =
                document.getElementById("letters-count");

            if (lettersPercentage) {
                lettersPercentage.textContent =
                    Math.round(lettersProgress) + "%";
            }

            if (lettersFill) {
                lettersFill.style.width = lettersProgress + "%";
            }

            const completedLetters =
                Math.round((lettersProgress / 100) * 26);

            if (lettersCount) {
                lettersCount.textContent =
                    completedLetters + " of 26 letters";
            }

            // NUMBERS PROGRESS
            const numbersPercentage =
                document.getElementById("numbers-progress");

            const numbersFill =
                document.getElementById("numbers-progress-fill");

            const numbersCount =
                document.getElementById("numbers-count");

            if (numbersPercentage) {
                numbersPercentage.textContent =
                    Math.round(numbersProgress) + "%";
            }

            if (numbersFill) {
                numbersFill.style.width = numbersProgress + "%";
            }

            const completedNumbers =
                Math.round((numbersProgress / 100) * 10);

            if (numbersCount) {
                numbersCount.textContent =
                    completedNumbers + " of 10 numbers";
            }

            // RESUME LEARNING FROM NEXT ITEM
            const letters = [
                "A", "B", "C", "D", "E", "F",
                "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X",
                "Y", "Z"
            ];

            const numbers = [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10"
            ];

            // LETTERS LEARNING BUTTON
            const lettersLearningButton =
                document.querySelector(".letters-button");

            if (lettersLearningButton) {
                let nextLetterIndex = completedLetters;

                if (nextLetterIndex >= letters.length) {
                    nextLetterIndex = 0;
                }

                lettersLearningButton.href =
                    "learning.html?type=letters&item=" +
                    letters[nextLetterIndex];
            }

            // NUMBERS LEARNING BUTTON
            const numbersLearningButton =
                document.querySelector(".numbers-button");

            if (numbersLearningButton) {
                let nextNumberIndex = completedNumbers;

                if (nextNumberIndex >= numbers.length) {
                    nextNumberIndex = 0;
                }

                numbersLearningButton.href =
                    "learning.html?type=numbers&item=" +
                    numbers[nextNumberIndex];
            }

        } catch (error) {
            // Do not clear login information for a missing progress element.
            console.error("Dashboard error:", error);

            // Clear storage only if the saved user data is invalid.
            localStorage.removeItem("user");
            localStorage.removeItem("access_token");

            window.location.href = "login.html";
        }
    }
}


// ================================
// LOGOUT
// ================================

const logoutButton = document.getElementById("logout-button");

if (logoutButton) {
    logoutButton.addEventListener("click", function () {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        window.location.href = "login.html";
    });
}


// ================================
// MORE BUTTON
// ================================

const moreButton = document.getElementById("more-button");
const logoutContainer = document.getElementById("logout-container");

if (moreButton && logoutContainer) {
    moreButton.addEventListener("click", function () {
        logoutContainer.classList.toggle("show");
    });
}


// ================================
// INDEX PAGE LOGIN STATE
// ================================

const loggedOutButtons =
    document.getElementById("logged-out-buttons");

const indexLogoutButton =
    document.getElementById("index-logout-button");

const accessToken = localStorage.getItem("access_token");

if (accessToken) {
    // Hide Sign In and Create Account buttons
    if (loggedOutButtons) {
        loggedOutButtons.style.display = "none";
    }

    // Show Logout button
    if (indexLogoutButton) {
        indexLogoutButton.classList.add("show");
    }
}


// ================================
// INDEX PAGE LOGOUT
// ================================

if (indexLogoutButton) {
    indexLogoutButton.addEventListener("click", function () {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        window.location.href = "index.html";
    });
}