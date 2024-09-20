document.addEventListener('DOMContentLoaded', function() {
    const flashcardContainer = document.getElementById('flashcard-container');
    const progressItems = document.querySelectorAll('.progress-item');
    const quizForm = document.getElementById('quiz-form');
    const nextQuestionBtn = document.getElementById('next-question-btn');

    // Function to navigate to a specific question
    function navigateToQuestion(questionId) {
        window.location.href = `/quiz?question_id=${questionId}`;
    }

    // Attach click events to progress items
    progressItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const questionId = this.getAttribute('onclick').match(/\d+/)[0];
            navigateToQuestion(questionId);
        });
    });

    // Handle Next Question button click
    nextQuestionBtn.addEventListener('click', function() {
        // Simulate clicking the "Submit Answer" button to get a new question
        quizForm.submit();
    });
});
