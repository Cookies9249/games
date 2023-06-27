const cardReferences = [
    {id: 1, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Playing_card_diamond_A.svg'},
    {id: 2, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/3/36/Playing_card_club_A.svg'},
    {id: 3, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/5/57/Playing_card_heart_A.svg'},
    {id: 4, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/2/25/Playing_card_spade_A.svg'},
    {id: 5, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/5/59/Playing_card_diamond_2.svg'},
    {id: 6, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Playing_card_club_2.svg'},
    {id: 7, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Playing_card_heart_2.svg'},
    {id: 8, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Playing_card_spade_2.svg'},

    {id: 9, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Playing_card_diamond_A.svg'},
    {id: 10, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/3/36/Playing_card_club_A.svg'},
    {id: 11, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/5/57/Playing_card_heart_A.svg'},
    {id: 12, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/2/25/Playing_card_spade_A.svg'},
    {id: 13, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/5/59/Playing_card_diamond_2.svg'},
    {id: 14, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Playing_card_club_2.svg'},
    {id: 15, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Playing_card_heart_2.svg'},
    {id: 16, imgPath: 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Playing_card_spade_2.svg'},
]

const cardBackImgPath = 'https://upload.wikimedia.org/wikipedia/commons/e/ea/PLAYING_CARD_BACK.svg';
const numCards = cardReferences.length;

const gameStatus = document.querySelector('.game-status');
const gameButton = document.querySelector('.game-button');
const gameScore = document.querySelector('.score')
const gameContainer = document.querySelector('.game-container');

let cards = [];

// CREATE CARDS
let choicesMax = 2;
let choices = [];  // current choices in round
let correctChoices = [];  // correct choices in past rounds
let turns = 0;
let gameInProgress = false;

loadGame();

function loadGame() {
    // create all cards
    cardReferences.forEach((cardRef) => createCard(cardRef));

    // start game with button click
    gameButton.addEventListener('click', () => startGame())

    // update output
    gameStatus.innerHTML = "Press 'Play Game' to Start!"
    gameInProgress = false;
}

function startGame() {
    // initialize variables
    gameButton.disabled = true;
    gameInProgress = false;

    turns = 0;
    gameScore.innerHTML = `Turns <span class="badge">${turns}</span>`;
    correctChoices = [];

    // flip every card
    cards.forEach((card) => flipCard(card));
    gameStatus.innerHTML = "Starting a Game...";
    
    shuffleCards();
    gameStatus.innerHTML = "Randomizing Cards...";
}

function createCard(cardRef) {
    // create elements
    const card = document.createElement('div');
    const cardInner = document.createElement('div');
    const cardFront = document.createElement('div');
    const cardBack = document.createElement('div');
    const cardFrontImg = document.createElement('img');
    const cardBackImg = document.createElement('img');

    // add classes
    card.classList.add('card');
    cardInner.classList.add('card-inner');
    cardFront.classList.add('card-front');
    cardBack.classList.add('card-back');
    cardFrontImg.classList.add('card-img');
    cardBackImg.classList.add('card-img');

    // add id and src
    card.id = cardRef.id;
    cardFrontImg.src = cardRef.imgPath;
    cardBackImg.src = cardBackImgPath;

    // add child elements
    card.appendChild(cardInner);
    cardInner.appendChild(cardFront);
    cardInner.appendChild(cardBack);
    cardFront.appendChild(cardFrontImg);
    cardBack.appendChild(cardBackImg);

    // add card element to container
    const cardContainerClass = getCardContainer(card);
    const cardContainer = document.querySelector(cardContainerClass);
    cardContainer.appendChild(card);

    // add event listener
    card.addEventListener('click', () => chooseCard(card));

    // add card and card id to lists
    cards.push(card);
}

// given a card id, returns respective container class
function getCardContainer(card) {
    const id = parseInt(card.id);
    if (id >= 1 && id <= 16) {
        return (".card-pos-" + String.fromCharCode(id + 96));  // id + 96 gives ascii char
    }
}

// flips given card
function flipCard(card) {
    const cardInner = card.firstChild;
    if (!cardInner.classList.contains('flip')) {
        cardInner.classList.add('flip');
    }
    else {
        cardInner.classList.remove('flip');
    }
}

// randomizes placement of cards
function shuffleCards() {
    let shuffleCount = 0;
    const id = setInterval(shuffle, 5);
    
    function shuffle() {
        randomizeCards();
        
        if (shuffleCount == numCards * 20) {
            clearInterval(id);
            gameContainer.style.gridTemplateAreas = mapGridTemplate();  // change grid template
            startTurn();
        }
        shuffleCount++;
    }
}

function randomizeCards() {
    const random1 = Math.floor(Math.random() * numCards);
    const random2 = Math.floor(Math.random() * numCards);

    const tmp = cards[random1];
    cards[random1] = cards[random2];
    cards[random2] = tmp;
}

function mapGridTemplate() {
    let areas = "";
    let firstRow = "";
    let secondRow = "";

    cards.forEach((card, index) => {
        const id = parseInt(cards[index].id);
        areas += String.fromCharCode(id + 96) + " ";  // if id = 1, areas += "a ", etc.

        if (index == numCards / 2 - 1) {
            firstRow = areas.substring(0, areas.length - 1);
            areas = "";
        }
        else if (index == numCards - 1) {
            secondRow = areas.substring(0, areas.length - 1);
        }
    })
    return `"${firstRow}" "${secondRow}"`;
}

// starts turn for player
function startTurn() {
    gameInProgress = true;
    gameStatus.innerHTML = "Choose a Pair of Cards From Below...";
    cards.forEach((card) => {card.style.cursor = 'pointer';})
}

// occurs after player chooses a card
function chooseCard(card) {
    // if player picks two cards that aren't picked already
    if (gameInProgress && choices.length < choicesMax && !choices.includes(card.id) && !correctChoices.includes(card.id)) {
        choices.push(card.id);
        flipCard(card);

        if (choices.length == choicesMax) {
            turns++;
            gameScore.innerHTML = `Turns <span class="badge">${turns}</span>`;
            
            if (calculateResult(choices[0], choices[1])) {
                correctChoices.push(choices[0]);
                correctChoices.push(choices[1]);
                choices = [];
                checkGameOver();
            }
            else {
                setTimeout(() => {
                    choices.forEach((choiceId) => {
                        const choice = document.getElementById(choiceId);
                        flipCard(choice);
                        choice.style.cursor = 'pointer';
                    })
                    choices = [];
                }, 1000)
            }
        }
    } 
}

// returns true for match and false for no match
function calculateResult(choice1, choice2) {
    if (choice1 % (numCards / 2) == choice2 % (numCards / 2)) {
        return true;
    }
    return false;
}

// checks for game over
function checkGameOver() {
    if (correctChoices.length == numCards) {
        gameStatus.innerHTML = `Game Over! Press 'Play Game' to Play Again!`
        gameButton.disabled = false;
        gameInProgress = false;

        cards.forEach((card) => {card.style.cursor = 'auto';})
    }
}