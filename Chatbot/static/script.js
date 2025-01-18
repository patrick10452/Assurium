// Import questions from individual files
import { autoQuestions } from './autoQuestions.js';
import { houseQuestions } from './houseQuestions.js';
import { commercialQuestions } from './commercialQuestions.js';

// Quiz state variables
let currentQuestions = [];
let currentQuestionIndex = 0;
let correctAnswers = 0;
let selectedCategory = null;
let isExitClicked = false; // Track if Exit Quiz has been clicked

// DOM elements
let quizContainer, quizQuestion, quizOptions, nextQuizBtn, quizResult, scoreDisplay, percentageDisplay, quizProgress, quizCategorySelector;

// Wait for the DOM to load before running the script
document.addEventListener("DOMContentLoaded", function () {
    // Initialize DOM elements
    quizContainer = document.getElementById("quiz-container");
    quizQuestion = document.getElementById("quiz-question");
    quizOptions = document.getElementById("quiz-options");
    nextQuizBtn = document.getElementById("next-quiz-btn");
    quizResult = document.getElementById("quiz-result");
    scoreDisplay = document.getElementById("score");
    percentageDisplay = document.getElementById("percentage");
    quizProgress = document.getElementById("quiz-progress");
    quizCategorySelector = document.getElementById("quiz-category-selector");

    // Attach event listeners to category buttons
    document.getElementById("auto-btn").addEventListener("click", () => loadQuestions('auto'));
    document.getElementById("home-btn").addEventListener("click", () => loadQuestions('home'));
    document.getElementById("commercial-btn").addEventListener("click", () => loadQuestions('commercial'));
    document.getElementById("all-btn").addEventListener("click", () => loadQuestions('all'));

    // Attach event listeners to quiz buttons
    nextQuizBtn.addEventListener("click", nextQuestion);
    document.getElementById("restart-quiz-btn").addEventListener("click", restartQuiz);
    document.getElementById("exit-quiz-btn").addEventListener("click", exitQuiz);
});

// Load questions based on category
function loadQuestions(category) {
    console.log(`Loading questions for category: ${category}`); // Debugging line

    // Reset quiz state
    currentQuestionIndex = 0;
    correctAnswers = 0;
    quizResult.style.display = "none"; // Hide the result section
    quizContainer.style.display = "block"; // Ensure the quiz container is visible
    quizCategorySelector.style.display = "none"; // Hide the category selector
    isExitClicked = false; // Reset exit state

    // Clear any existing options
    quizOptions.innerHTML = "";

    // Load questions based on the selected category
    switch (category) {
        case 'auto':
            currentQuestions = autoQuestions;
            break;
        case 'home':
            currentQuestions = houseQuestions;
            break;
        case 'commercial':
            currentQuestions = commercialQuestions;
            break;
        case 'all':
            currentQuestions = [...autoQuestions, ...houseQuestions, ...commercialQuestions];
            break;
        default:
            currentQuestions = [];
    }

    console.log(`Loaded ${currentQuestions.length} questions`); // Debugging line
    console.log(`First question: ${currentQuestions[0]?.question}`); // Debugging line

    // Display the first question
    showQuestion();
}

// Display the current question
function showQuestion() {
    console.log(`Displaying question ${currentQuestionIndex + 1}`); // Debugging line

    // Clear any existing options
    quizOptions.innerHTML = "";

    // Check if currentQuestions is defined and has questions
    if (!currentQuestions || currentQuestions.length === 0) {
        console.error("No questions loaded for the selected category."); // Debugging line
        quizQuestion.textContent = "No questions available for this category.";
        return;
    }

    // Display the current question
    const question = currentQuestions[currentQuestionIndex];
    quizQuestion.textContent = question.question;

    // Add options for the current question
    question.answers.forEach((answer, index) => {
        const button = document.createElement("button");
        button.textContent = answer.text;
        button.addEventListener("click", () => selectAnswer(answer));
        quizOptions.appendChild(button);
    });

    // Update quiz progress
    quizProgress.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuestions.length}`;
}

// Handle answer selection
function selectAnswer(answer) {
    const buttons = quizOptions.querySelectorAll("button");
    buttons.forEach(button => {
        button.disabled = true;
        if (button.textContent === answer.text && answer.correct) {
            button.classList.add("correct");
        } else if (button.textContent === answer.text && !answer.correct) {
            button.classList.add("incorrect");
        }
    });

    if (answer.correct) {
        correctAnswers++;
    }

    nextQuizBtn.style.display = "block";
}

// Move to the next question
function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < currentQuestions.length) {
        showQuestion();
        nextQuizBtn.style.display = "none";
    } else {
        showResult();
    }
}

// Display the quiz result
function showResult() {
    quizContainer.style.display = "none";
    quizResult.style.display = "block";
    const totalQuestions = currentQuestions.length;
    const percentage = ((correctAnswers / totalQuestions) * 100).toFixed(2);
    scoreDisplay.textContent = `Correct Answers: ${correctAnswers} / ${totalQuestions}`;
    percentageDisplay.textContent = `Percentage: ${percentage}%`;
}

// Restart the quiz
function restartQuiz() {
    loadQuestions(selectedCategory);
}

// Exit the quiz
function exitQuiz() {
    if (!isExitClicked) {
        // Show the result when Exit Quiz is clicked for the first time
        const totalQuestions = currentQuestions.length;
        const incorrectAnswers = totalQuestions - correctAnswers;
        const percentage = ((correctAnswers / totalQuestions) * 100).toFixed(2);

        quizResult.innerHTML = `
            <h3>Quiz Result</h3>
            <p>Correct Answers: ${correctAnswers}</p>
            <p>Incorrect Answers: ${incorrectAnswers}</p>
            <p>Percentage: ${percentage}%</p>
        `;
        quizResult.style.display = "block";
        isExitClicked = true; // Mark exit as clicked
    } else {
        // Reset the quiz to the original page when Exit Quiz is clicked again
        quizContainer.style.display = "none";
        quizResult.style.display = "none";
        currentQuestions = [];
        currentQuestionIndex = 0;
        correctAnswers = 0;
        isExitClicked = false; // Reset exit state

        // Show the category selection buttons
        quizCategorySelector.style.display = "block";
    }
}

// Tab switching logic
function switchTab(tab) {
    const chatTab = document.getElementById("chat-tab-content");
    const quizTab = document.getElementById("quiz-tab-content");
    const chatButton = document.getElementById("chat-tab");
    const quizButton = document.getElementById("quiz-tab");

    if (tab === 'chat') {
        chatTab.classList.add("active");
        quizTab.classList.remove("active");
        chatButton.classList.add("active");
        quizButton.classList.remove("active");
    } else if (tab === 'quiz') {
        quizTab.classList.add("active");
        chatTab.classList.remove("active");
        quizButton.classList.add("active");
        chatButton.classList.remove("active");
    }
}

// Chatbot functionality
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");

    const userMessage = userInput.value.trim();
    if (userMessage === "") return;

    // Display user message
    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user-message");
    userMessageElement.textContent = userMessage;
    chatBox.appendChild(userMessageElement);

    // Clear input
    userInput.value = "";

    // Show typing indicator
    typingIndicator.style.display = "block";

    // Simulate bot response
    setTimeout(() => {
        typingIndicator.style.display = "none";

        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");
        botMessageElement.textContent = "This is a bot response.";
        chatBox.appendChild(botMessageElement);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000); // Simulate a 1-second delay for the bot response
}

// Make functions globally available
window.switchTab = switchTab;
window.handleKeyPress = handleKeyPress;
window.sendMessage = sendMessage;