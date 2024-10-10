document.addEventListener('DOMContentLoaded', () => {
    const game = new SpaceClawGame(document.getElementById('game-canvas'));
    
    const grabButtons = {
        'one': document.getElementById('grab-one'),
        'five': document.getElementById('grab-five'),
        'ten': document.getElementById('grab-ten')
    };

    for (const [type, button] of Object.entries(grabButtons)) {
        button.addEventListener('click', () => grab(type));
    }

    async function grab(type) {
        try {
            const response = await fetch('/grab', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ type }),
            });
            const result = await response.json();
            if (result.success) {
                updateScore(result.score);
                updateRank(result.rank);
                game.animateGrab(result.prizes);
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('發生錯誤，請稍後再試。');
        }
    }

    function updateScore(score) {
        document.getElementById('score-value').textContent = score;
    }

    function updateRank(rank) {
        document.getElementById('rank-value').textContent = rank;
    }
});