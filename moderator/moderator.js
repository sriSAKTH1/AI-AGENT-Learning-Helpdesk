const API_URL = "http://127.0.0.1:8000";

let currentThreadId = null;
let currentUserId = null;

const userIdElement = document.getElementById("userId");
const questionElement = document.getElementById("question");
const reasonElement = document.getElementById("reason");
const statusElement = document.getElementById("reviewStatus");
const resultElement = document.getElementById("result");

const answerButton = document.getElementById("answerButton");
const rejectButton = document.getElementById("rejectButton");
const blockButton = document.getElementById("blockButton");


function showResult(message) {
    resultElement.textContent = message;
    resultElement.style.display = "block";
}


function clearReview() {

    currentThreadId = null;
    currentUserId = null;

    userIdElement.textContent = "-";
    questionElement.textContent = "No pending request.";
    reasonElement.textContent = "-";
    statusElement.textContent = "Waiting";

    answerButton.disabled = true;
    rejectButton.disabled = true;
    blockButton.disabled = true;
}


function showReview(request) {

    currentThreadId = request.thread_id;
    currentUserId = request.user_id;

    userIdElement.textContent =
        request.user_id;

    questionElement.textContent =
        request.question;

    reasonElement.textContent =
        request.reason || "Human review required";

    statusElement.textContent =
        "Review Required";

    answerButton.disabled = false;
    rejectButton.disabled = false;
    blockButton.disabled = false;

    resultElement.style.display = "none";
}


async function loadPendingRequest() {

    try {

        const response = await fetch(
            `${API_URL}/moderator/pending`
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                `HTTP ${response.status}`
            );
        }

        console.log(
            "Pending moderator requests:",
            data.pending
        );

        if (
            data.pending &&
            data.pending.length > 0
        ) {

            showReview(
                data.pending[0]
            );

        } else {

            clearReview();
        }

    } catch (error) {

        console.error(
            "Pending request error:",
            error
        );

        statusElement.textContent =
            "Connection Error";

        showResult(
            `Error: ${error.message}`
        );
    }
}


async function moderatorAction(action) {

    if (!currentThreadId) {

        showResult(
            "No pending moderator request."
        );

        return;
    }

    answerButton.disabled = true;
    rejectButton.disabled = true;
    blockButton.disabled = true;

    statusElement.textContent =
        "Processing...";

    try {

        const response =
            await fetch(
                `${API_URL}/moderator/action`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        thread_id:
                            currentThreadId,

                        action:
                            action
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                `HTTP ${response.status}`
            );
        }

        console.log(
            "Moderator action result:",
            data
        );

        statusElement.textContent =
            "Completed";

        if (action === "answer") {

            showResult(
                "✅ Question approved by moderator."
            );

        } else if (action === "reject") {

            showResult(
                "❌ Request rejected."
            );

        } else if (action === "block") {

            showResult(
                "🚫 User blocked for 1 hour."
            );
        }

        currentThreadId = null;

        setTimeout(
            loadPendingRequest,
            500
        );

    } catch (error) {

        console.error(
            "Moderator action error:",
            error
        );

        showResult(
            `Error: ${error.message}`
        );

        answerButton.disabled = false;
        rejectButton.disabled = false;
        blockButton.disabled = false;

        statusElement.textContent =
            "Review Required";
    }
}


answerButton.addEventListener(
    "click",
    () => moderatorAction("answer")
);

rejectButton.addEventListener(
    "click",
    () => moderatorAction("reject")
);

blockButton.addEventListener(
    "click",
    () => moderatorAction("block")
);


// Initial load
loadPendingRequest();


// Automatically check every 10 seconds
setInterval(
    loadPendingRequest,
    10000
);