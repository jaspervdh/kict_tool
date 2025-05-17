function increaseLevel(barId) {
    const bar = document.getElementById(barId);
    const currentHeight = parseInt(bar.style.height);
    if (currentHeight < 150) {
        const newHeight = currentHeight + 50;
        bar.style.height = newHeight + 'px';
        if (newHeight >= 150) {
            triggerStars();
        }
    }
}

function triggerStars() {
    const container = document.getElementById('stars');
    container.innerHTML = '';

    for (let i = 0; i < 30; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.innerText = '✨';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.fontSize = (Math.random() * 1.5 + 1) + 'rem';
        star.style.animationDelay = (Math.random() * 0.5) + 's';
        container.appendChild(star);
    }

    setTimeout(() => {
        container.innerHTML = '';
    }, 2000);
}

let currentQuestion = null;

function loadQuestion() {
    const number = parseInt(document.getElementById('questionNumber').value);
    if (isNaN(number) || number < 1 || number > 180) {
        alert("Ongeldig nummer");
        return;
    }

    fetch(`/vraag?nummer=${number}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                currentQuestion = { text: data.vraag, perspective: data.perspectief };
                document.getElementById('questionText').innerText = currentQuestion.text;
                document.getElementById('perspectiveLabel').innerText = currentQuestion.perspective;
                document.getElementById('questionSection').style.display = 'block';
                document.getElementById('inputSection').style.display = 'none';
            }
        })
        .catch(error => {
            console.error("Fout bij het ophalen van vraag:", error);
            alert("Er is een probleem met het ophalen van de vraag.");
        });
}

const perspectiveToBarId = {
    'Politiek': 'bar1',
    'Economisch': 'bar2',
    'Sociaal-cultureel': 'bar3',
    'Technologisch': 'bar4',
    'Ecologisch': 'bar5',
    'Juridisch': 'bar6',
    'Ethisch': 'bar7',
    'Gezondheid': 'bar8',
    'Veiligheid': 'bar9'
}

function evaluateAnswer(isCorrect) {
    if (isCorrect && currentQuestion) {
        const barId = perspectiveToBarId[currentQuestion.perspective]
        if (barId) {
            increaseLevel(barId);
        } else {
            console.warn("Geen barId gevonden voor perspectief", currentQuestion.perspective)
        }
    }

    currentQuestion = null;
    document.getElementById('questionSection').style.display = 'none';
    document.getElementById('inputSection').style.display = 'block';
    document.getElementById('questionNumber').value = '';
}