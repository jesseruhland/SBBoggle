// Establish in-game memory to check words against
const guessedWords = [];

// global variable
const $score = $("#score");

// increment in-game score in DOM based on word length
function incrementScore(word, responseText) {
  if (responseText === "ok") {
    const currentScore = $score.text();
    const wordScore = word.length;
    const newScore = parseInt(currentScore) + wordScore;
    $score.text(newScore);
  }
}

// check if word guess is a word against API database
async function checkWord(word) {
  let responseText = "";

  if (word.length <= 0) {
    responseText = "please enter a word";
  } else if (!guessedWords.includes(word)) {
    const resp = await axios.get(`/guess?guess=${word}`);
    responseText = resp.data.result;
  } else {
    responseText = "already played";
  }

  return responseText;
}

// when a user submits a new word
async function handleClick(event) {
  event.preventDefault();

  // clear previously played word from the DOM
  $("#word-result").empty();

  // get user submission from form
  const word = $("#guess-input").val();

  // check word in API database
  const responseText = await checkWord(word);

  // add word to in-game played-words memory
  guessedWords.push(word);

  // display played word and result from database
  const result = document.createElement("p");
  result.innerText = `${word} : ${responseText}`;
  $("#word-result").append(result);

  // if a valid word, this will increment the DOM score by the word length
  incrementScore(word, responseText);

  // clear input form
  $("#guess-input").val("");
}

// event listener for the submit button
$("body").on("click", "#submit-button", handleClick);

// start the DOM timer, when the timer reaches 0, disable submissions, send stats to database
const startTimer = () => {
  const timer = setInterval(function () {
    const time = $("#timer");
    const currentTime = parseInt(time.text());
    const newTime = currentTime - 1;
    time.text(newTime);
    if (newTime === 0) {
      $("#submit-button").prop("disabled", true);
      sendStats();
      clearInterval(timer);
    }
  }, 1000);
};

// start timer on page load
document.onload = startTimer();

// send stats to API for storage on server
function sendStats() {
  axios.post("/times_played");
  const post = {
    method: "POST",
    url: "/high_score",
    data: {
      high_score: `${$score.text()}`,
    },
  };
  axios(post);
}
