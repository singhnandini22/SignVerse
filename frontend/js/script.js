// DASHBOARD
const dashboard = document.querySelector(".dashboard");
if (dashboard) {

    // GET SAVED USER
    const savedUser = localStorage.getItem("user");

    // CHECK LOGIN
    if (!savedUser) {
        window.location.href = "login.html";
    } else {
        try {
            const user =
                JSON.parse(savedUser);

            // USER NAME
            const userName = document.getElementById("user-name");
            if (userName) {
                userName.textContent =
                    user.name || "User";
            }

            // GET PROGRESS
            let lettersProgress = Number(user.letters_progress) || 0;
            let numbersProgress = Number(user.numbers_progress) || 0;

            // Keep progress between 0 and 100
            lettersProgress = Math.max(0,Math.min(100,lettersProgress));
            numbersProgress = Math.max(0,Math.min(100,numbersProgress));

            // LETTERS PROGRESS
            const lettersPercentage = document.getElementById("letters-progress");
            const lettersFill = document.getElementById("letters-progress-fill");
            const lettersCount = document.getElementById("letters-count");

            if (lettersPercentage) {
                lettersPercentage.textContent = Math.round(lettersProgress) + "%";
            }

            if (lettersFill) {
                lettersFill.style.width =lettersProgress + "%";
            }

            if (lettersCount) {
                const completedLetters = Math.round((lettersProgress / 100) * 26);
                lettersCount.textContent = completedLetters +" of 26 letters";
            }

            //NUMBERS PROGRESS
            const numbersPercentage = document.getElementById("numbers-progress");
            const numbersFill = document.getElementById("numbers-progress-fill");
            const numbersCount =document.getElementById("numbers-count");

            if (numbersPercentage) {
                numbersPercentage.textContent = Math.round(numbersProgress) + "%";
            }

            if (numbersFill) {
                numbersFill.style.width = numbersProgress + "%";
            }

            if (numbersCount) {
                const completedNumbers = Math.round((numbersProgress / 100) * 10);
                numbersCount.textContent = completedNumbers +" of 10 numbers";
            }

        } catch (error) {
            console.error( "Unable to read user data:",error);
            localStorage.removeItem("user");
            localStorage.removeItem("access_token");
            window.location.href ="login.html";
        }
    }
}

//LOGOUT
const logoutButton = document.getElementById("logout-button");
if (logoutButton) {

    logoutButton.addEventListener("click",function ()
    {
            // Remove saved login information
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");

            // Go back to login page
            window.location.href ="login.html";
        }
    );
}

//MORE BUTTON
const moreButton = document.getElementById("more-button");
const logoutContainer = document.getElementById("logout-container");

if (moreButton && logoutContainer) {
    moreButton.addEventListener("click",function ()
        {
            logoutContainer.classList.toggle("show");
        }
    );
}

//DASHBOARD PROGRESS AND RESUME LEARNING
const userNameElement = document.getElementById("user-name");
const lettersProgressElement = document.getElementById("letters-progress");
const numbersProgressElement = document.getElementById("numbers-progress");
const lettersProgressText = document.getElementById("letters-progress-text");
const numbersProgressText = document.getElementById("numbers-progress-text");
const lettersProgressFill = document.getElementById("letters-progress-fill");
const numbersProgressFill = document.getElementById("numbers-progress-fill");

// CHECK IF DASHBOARD EXISTS
if (userNameElement) {

    //GET LOGIN INFORMATION
    const token =localStorage.getItem("access_token");
    const savedUser = localStorage.getItem("user");

    // REDIRECT IF USER IS NOT LOGGED IN
    if (!token || !savedUser)
    {
        window.location.href ="login.html";

    } else {
        try {
            //GET USER DATA
            const user = JSON.parse(savedUser);

            // DISPLAY USER NAME
            userNameElement.textContent = user.name || "User";

            // GET PROGRESS
            let lettersProgress = Number(user.letters_progress) || 0;
            let numbersProgress = Number(user.numbers_progress) || 0;

            //KEEP PROGRESS BETWEEN 0 AND 100
            lettersProgress = Math.max(0,Math.min(100,lettersProgress));
            numbersProgress = Math.max(0,Math.min(100,numbersProgress));

            // DISPLAY LETTERS PROGRESS
            lettersProgressElement.textContent =Math.round(lettersProgress) + "%";
            lettersProgressFill.style.width =lettersProgress + "%";

            // Calculate completed letters
            const completedLetters = Math.round((lettersProgress / 100) * 26);
            lettersProgressText.textContent = completedLetters +" of 26 letters";

            // DISPLAY NUMBERS PROGRESS
            numbersProgressElement.textContent = Math.round(numbersProgress) + "%";
            numbersProgressFill.style.width = numbersProgress + "%";

            // Calculate completed numbers
            const completedNumbers = Math.round((numbersProgress / 100) * 10);
            numbersProgressText.textContent = completedNumbers +" of 10 numbers";

            // RESUME LEARNING FROM NEXT ITEM
            const letters = [
                "A", "B", "C", "D", "E", "F","G", "H", "I", "J", "K", "L","M", "N", "O", "P", "Q", "R","S", "T", "U", "V", "W", "X","Y", "Z"
            ];
            const numbers = [
                "1", "2", "3", "4", "5","6", "7", "8", "9", "10"
            ];

            //LETTERS START LEARNING BUTTON
            const lettersLearningButton = document.querySelector(".letters-button");
            if (lettersLearningButton) {
                let nextLetterIndex = completedLetters;

                // If all letters are completed,start again from A
                if (nextLetterIndex >= letters.length)
                {
                    nextLetterIndex = 0;
                }
                lettersLearningButton.href ="learning.html?type=letters&item=" +letters[nextLetterIndex];
            }

            //NUMBERS START LEARNING BUTTON
            const numbersLearningButton = document.querySelector(".numbers-button");
            if (numbersLearningButton) {
                let nextNumberIndex =completedNumbers;

                // If all numbers are completed, start again from 1
                if (nextNumberIndex >=numbers.length)
                {
                    nextNumberIndex = 0;
                }
                numbersLearningButton.href ="learning.html?type=numbers&item=" +numbers[nextNumberIndex];
            }

        } catch (error) {
            console.error("Dashboard error:",error);

            // If saved user data is corrupted,send the user back to login.
            localStorage.removeItem("user");
            localStorage.removeItem("access_token");
            window.location.href ="login.html";
        }
    }
}

//INDEX PAGE LOGIN STATE
const loggedOutButtons = document.getElementById("logged-out-buttons");
const indexLogoutButton = document.getElementById("index-logout-button");

// Check if user is logged in
const accessToken =localStorage.getItem("access_token");

//USER IS LOGGED IN
if (accessToken) {

    // Hide Sign In + Create Account
    if (loggedOutButtons) {
        loggedOutButtons.style.display ="none";
    }
    // Show Logout
    if (indexLogoutButton) {
        indexLogoutButton.classList.add("show");
    }
}

//INDEX PAGE LOGOUT
if (indexLogoutButton) {
    indexLogoutButton.addEventListener("click",function ()
    {
            // Remove saved login information
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");

            // Refresh the index page
            window.location.href ="index.html";
        }
    );
}

