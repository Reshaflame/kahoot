<script>
    import { onMount, onDestroy } from 'svelte';
    import ProgressBar from './ProgressBar.svelte';
    // if you want run these via localhost, you can change the ip_address to 'your_ip_device_host:5000'
    import { ip_address } from './API.svelte';
    const ip_address_module = ip_address;
    let question = '';
    let answers = [];
    let selectedAnswer = '';
    let quizCompleted = false;
    let timeLeft = 0;
    let totalTime = 30;
    let timer;
    let isSubmitting = false;
    let feedback = '';
    let score = 0;
    let allScores = {};
    let isLoading = true;
    let currentQuestionIndex = 0;
    const totalQuestions = 5;

    // start a new game by resetting variables and fetching the first question
    async function startNewGame() {
        isLoading = true;
        currentQuestionIndex = 0;
        quizCompleted = false;
        score = 0;
        selectedAnswer = ''; 
        answers = [];  
        question = 'Loading new question...';  
        await getQuestion(); 
        isLoading = false;
    }

    // fetch a new question from the server
    async function getQuestion() {
        clearInterval(timer);  
        try {
            const response = await fetch(`http://${ip_address_module}/get_question`);
            if (response.ok) {
                const data = await response.json();
                if (data.type === 'question') {
                    question = data.question;
                    answers = data.answers;
                    timeLeft = data.time_limit;
                    totalTime = data.time_limit;
                    quizCompleted = false;
                    currentQuestionIndex++;
                    selectedAnswer = '';  
                    startTimer();  
                } else if (data.type === 'end') {
                    handleEndOfQuiz(data);
                }
            } else {
                feedback = 'Failed to fetch question. Please try again.';
            }
        } catch (error) {
            feedback = 'Error fetching question. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    // handle the end of the quiz
    function handleEndOfQuiz(data) {
        question = data.message;
        answers = [];
        quizCompleted = true;
        score = data.score;
        allScores = data.all_scores;
        setTimeout(async () => {
            await startNewGame();
        }, 3000);
    }

    // start the countdown timer for the current question
    function startTimer() {
        clearInterval(timer);  
        timer = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
            } else {
                clearInterval(timer);
                autoSubmitAnswer();  
            }
        }, 1000);
    }

    // automatically submit an answer if time runs out
    function autoSubmitAnswer() {
        if (!selectedAnswer) {
            const randomIndex = Math.floor(Math.random() * answers.length);
            selectedAnswer = answers[randomIndex];
        }
        submitAnswer();  
    }

    // submit the selected answer to the server
    async function submitAnswer() {
        if (isSubmitting) return;
        if (!selectedAnswer) {
            feedback = 'Please select an answer before submitting.';
            return;
        }
        isSubmitting = true;
        feedback = 'Submitting answer...';
        clearInterval(timer); 
        
        try {
            const response = await fetch(`http://${ip_address_module}/submit_answer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ answer: selectedAnswer })
            });
            if (response.ok) {
                const data = await response.json();
                if (data.type === 'question') {
                    updateQuestionData(data);
                } else if (data.type === 'end') {
                    handleEndOfQuiz(data);
                }
            } else {
                feedback = 'Failed to submit answer. Please try again.';
            }
        } catch (error) {
            feedback = 'Error submitting answer. Please try again.';
        } finally {
            isSubmitting = false;
        }
    }

    // update the question data after submitting an answer
    function updateQuestionData(data) {
        question = data.question;
        answers = data.answers;
        timeLeft = data.time_limit;
        totalTime = data.time_limit;
        selectedAnswer = ''; 
        feedback = '';
        currentQuestionIndex++;
        startTimer();
    }

    // select an answer
    function selectAnswer(answer) {
        if (!isSubmitting) {
            selectedAnswer = answer;  
        }
    }

    // get color for answer blocks
    function getColor(index) {
        const colors = ['#DFFFEC', '#FF9797', '#F9DADA', '#D4C6FE'];  
        return colors[index % colors.length];  
    }

    // fetch the first question when the component mounts
    onMount(async () => {
        await getQuestion();
    });

    // clear the timer when the component is destroyed
    onDestroy(() => {
        clearInterval(timer);
    });
</script>

<main style="margin-top: 3%;">
    {#if isLoading}
        <div class="loading">Loading...</div>
    {:else}
        <div>
            {#if quizCompleted}
                <h2>Quiz completed! Your score: {score}</h2>
                <h3>All Players' Scores:</h3>
                <ul>
                    {#each Object.entries(allScores) as [player, playerScore]}
                        <li>{player}: {playerScore} points</li>
                    {/each}
                </ul>
                <div class="new-game-message">
                    <span>N</span><span>e</span><span>w</span>
                    <span>g</span><span>a</span><span>m</span><span>e</span>
                    <span>s</span><span>t</span><span>a</span><span>r</span><span>t</span><span>i</span><span>n</span><span>g</span>
                    <span>s</span><span>o</span><span>o</span><span>n</span><span>.</span><span>.</span><span>.</span>
                </div>
            {:else}
                <h1 class="question">{question}</h1>
                <p class="timer">Time left: {timeLeft} seconds</p> 
                <ProgressBar current={currentQuestionIndex} total={totalQuestions} />  
                <div class="answers-container">
                    {#each answers as answer, index}
                        <button 
                            class="answer-block {selectedAnswer === answer ? 'selected' : ''}" 
                            style="background-color: {getColor(index)};"  
                            on:click={() => selectAnswer(answer)}
                            disabled={isSubmitting}>
                            <span class="answer-text">{answer}</span>
                        </button>
                    {/each}
                </div>
                <button 
                    class="submit-button" 
                    on:click={submitAnswer} 
                    disabled={!selectedAnswer || isSubmitting}>
                    {isSubmitting ? 'Submitting...' : 'Submit Answer'}
                </button>
                {#if feedback}
                    <p class="feedback">{feedback}</p>
                {/if}
            {/if}
        </div>
    {/if}
</main>

<style>
    .question {
        font-size: 18px;
        margin-bottom: 15px;
        text-align: center;
    }
    .timer {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    .answers-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 20px;
        width: 100%;
        margin-bottom: 20px;
    }
    .answer-block {
        width: 150px;
        height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        border-radius: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        text-align: center;
        border: 2px solid #D3D3D3; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .answer-block:hover:not(:disabled) {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .answer-block.selected {
        border: 3px solid #fdd1d9; 
    }
    .answer-block:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .answer-text {
        font-weight: bold;
        text-align: center;
    }
    .submit-button {
        background-color: #201c1f;
        color: white;
        width: 150px;
        border: none;
        cursor: pointer;
        padding: 5px;
        font-size: 16px;
        margin: 0 auto;
        display: block;
    }
    .submit-button:hover:not(:disabled) {
        background-color: #fdd1d9;
        color: black;
    }
    .submit-button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
        color: white;
    }
    .feedback {
        margin-top: 10px;
        font-style: italic;
        color: #666;
        text-align: center;
    }
    ul {
        text-align: center;
        list-style-type: none;
        padding: 0;
    }
    ul li {
        font-size: 16px;
        margin-bottom: 5px;
    }
    h2, h3 {
        text-align: center;
        margin-top: 20px;
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
    }
    .new-game-message {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        color: #201c1f;
    }
    .new-game-message span {
        display: inline-block;
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.2s forwards;
    }
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .new-game-message span:nth-child(1) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(2) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(3) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(4) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(5) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(6) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(7) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(8) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(9) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(10) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(11) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(12) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(13) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(14) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(15) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(16) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(17) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(18) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(19) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(20) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(21) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(22) { animation-delay: 0.01s; }
    .new-game-message span:nth-child(23) { animation-delay: 0.01s; }
</style>