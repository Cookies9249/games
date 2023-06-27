const cardObjectDefinitions = [
    {id: 1, imgPath:'/images/card-KingHearts.png'},
    {id: 2, imgPath:'/images/card-JackClubs.png'},
    {id: 3, imgPath:'/images/card-QueenDiamonds.png'},
    {id: 4, imgPath:'/images/card-AceSpades.png'}
]

const cardContainerElem = document.querySelector('.card-container')
const playGameButtonElem = document.getElementById('playGame')
const currentGameStatusElem = document.querySelector('.current-status')

const scoreContainerElem = document.querySelector('.header-score-container')
const scoreElem = document.querySelector('.score')
const roundContainerElem = document.querySelector('.header-round-container')
const roundElem = document.querySelector('.round')

const cardBackImgPath = '/images/card-back-Blue.png'
const collaspedGridAreaTemplate = '"a a" "a a"'
const cardCollectionCellClass = ".card-pos-a"

const winColor = "green"
const loseColor = "red"
const primaryColor = "black"

let cards = []
let cardPositions = []

const numCards = cardObjectDefinitions.length
const maxRounds = 4
const aceId = 4

let gameInProgress = false
let shufflingInProgress = false 
let cardsRevealed = false

let roundNum = 0
let score = 0

// INITIALIZE GAME
function loadGame() {
    createCards()
    cardFlyInEffect()
    cards = document.querySelectorAll('.card')
    playGameButtonElem.addEventListener('click', ()=>startGame())  // listen for button click

    updateStatusElement(scoreContainerElem, "none")
    updateStatusElement(roundContainerElem, "none")
}
function startGame() {
    initializeGame()
    startRound()
}
function initializeGame() {
    score = 0
    roundNum = 0

    shufflingInProgress = false
    gameInProgress = true
    cardsRevealed = false

    checkForIncompleteGame()

    updateStatusElement(scoreContainerElem, "flex")
    updateStatusElement(roundContainerElem, "flex")

    updateStatusElement(scoreElem, "block", primaryColor, `Score <span class="badge">${score}</span>`)
    updateStatusElement(roundElem, "block", primaryColor, `Round <span class="badge">${roundNum}</span>`)
}
function startRound() {
    roundNum++
    playGameButtonElem.disabled = true
    
    shufflingInProgress = true
    gameInProgress = true
    cardsRevealed = false

    updateStatusElement(currentGameStatusElem, "block", primaryColor, "Shuffling...")
    updateStatusElement(roundElem, "block", primaryColor, `Round <span class="badge">${roundNum}</span>`)
    
    flipCards(true)
    setTimeout(() => {
        collectCards()
        shuffleCards()
    }, 1500)
}
function cardFlyInEffect() {
    const id = setInterval(flyIn, 500)
    let cardCount = 1

    function flyIn() {
        if (cardCount == numCards) {
            clearInterval(id)
            playGameButtonElem.style.display = "inline-block"
        }
        
        let card = document.getElementById(cardCount)
        card.classList.remove("fly-in")
        cardCount++
    }
}

// CREATE CARDS
function createCards() {
    cardObjectDefinitions.forEach((cardItem) => {  // for cardItem in cardObjectDefinitions: createCard(cardItem)
        createCard(cardItem)
    })
}
function createCard(cardItem) {

    // create div elements that make up a card
    const cardElem = document.createElement('div')
    const cardInnerElem = document.createElement('div')
    const cardFrontElem = document.createElement('div')
    const cardBackElem = document.createElement('div')

    // create front and back image elements for a card
    const cardFrontImg = document.createElement('img')
    const cardBackImg = document.createElement('img')

    // add class and id to 'card' element
    cardElem.classList.add('card')
    cardElem.classList.add('fly-in')
    cardElem.id = cardItem.id

    // elem.classList.add(className)
    // elem.id = id

    // add class to card elements
    cardInnerElem.classList.add('card-inner')
    cardFrontElem.classList.add('card-front')
    cardBackElem.classList.add('card-back')

    // add image src to image elements
    cardFrontImg.src = cardItem.imgPath
    cardBackImg.src = cardBackImgPath

    // add class to image element
    cardFrontImg.classList.add('card-img')
    cardBackImg.classList.add('card-img')

    // add image element as child to card element
    cardFrontElem.appendChild(cardFrontImg)
    cardBackElem.appendChild(cardBackImg)

    // add child elements to inner element
    cardInnerElem.appendChild(cardFrontElem)
    cardInnerElem.appendChild(cardBackElem)

    // add inner element as child to card element
    cardElem.appendChild(cardInnerElem)

    // add card element as child to grid cell
    addCardToGridId(cardElem)

    cardPositions.push(cardElem.id) // add element to array of cardPositions
    cardElem.addEventListener('click', () => chooseCard(cardElem))
}
function addCardToGridId(card) {
    const cardPositionClassName = mapCardIdToGridCell(card) // will return '.card-pos-a', etc.
    const cardPosElem = document.querySelector(cardPositionClassName) // find elem with '.card-pos-x' class
    cardPosElem.appendChild(card) // add card as child to container
}
function mapCardIdToGridCell(card) {
    if (card.id == 1) {
        return '.card-pos-a'
    }
    else if (card.id == 2) {
        return '.card-pos-b'
    }
    else if (card.id == 3) {
        return '.card-pos-c'
    }
    else if (card.id == 4) {
        return '.card-pos-d'
    }
}

// COLLECT CARDS IN MIDDLE
function collectCards() {
    cardContainerElem.style.gridTemplateAreas = collaspedGridAreaTemplate
    const cellPositionElem = document.querySelector(cardCollectionCellClass)

    cards.forEach((card, index) => {
        cellPositionElem.appendChild(card)
    })
}

// FLIP CARDS
function flipCards(flipToBack) {
    cards.forEach((card, index) => {
        setTimeout(() => {
            flipCard(card, flipToBack)
        }, index * 100)
    })
}
function flipCard(card, flipToBack) {
    const innerCardElem = card.firstChild
    if (flipToBack && !innerCardElem.classList.contains('flip-it')) {
        innerCardElem.classList.add('flip-it')
    }
    else if (innerCardElem.classList.contains('flip-it')) [
        innerCardElem.classList.remove('flip-it')
    ]
}

// SHUFFLE CARDS
function shuffleCards() {
    let shuffleCount = 0
    const id = setInterval(shuffle, 12)

    function shuffle() {
        randomizeCardPositions()
        animateShuffle(shuffleCount)

        if (shuffleCount == 500) {
            clearInterval(id)
            shufflingInProgress = false
            removeShuffleClasses()

            setTimeout(() => {
                dealCards()
            }, 1500)
            
            updateStatusElement(currentGameStatusElem, "block", primaryColor, "Choose Your Card Below...")
        }
        shuffleCount++
    }
}
function randomizeCardPositions() {
    const random1 = Math.floor(Math.random() * numCards)
    const random2 = Math.floor(Math.random() * numCards)

    const temp = cardPositions[random1]
    cardPositions[random1] = cardPositions[random2]
    cardPositions[random2] = temp
}
function animateShuffle(shuffleCount) {
    const random1 = Math.floor(Math.random() * numCards) + 1
    const random2 = Math.floor(Math.random() * numCards) + 1

    let card1 = document.getElementById(random1)
    let card2 = document.getElementById(random2)

    if (shuffleCount % 4 == 0) {
        card1.classList.toggle("shuffle-left")
        card1.style.zIndex = 100
    }
    if (shuffleCount % 10 == 0) {
        card2.classList.toggle("shuffle-right")
        card2.style.zIndex = 200
    }
}
function removeShuffleClasses() {
    cards.forEach((card) => {
        card.classList.remove("shuffle-left")
        card.classList.remove("shuffle-right")
    })
}

// DEAL CARDS
function dealCards() {
    cards.forEach((card, index) => {
        addCardToGridId(card)
    })

    const areasTemplate = returnGridAreasMappedToCardPos()
    cardContainerElem.style.gridTemplateAreas = areasTemplate
}
function returnGridAreasMappedToCardPos() {
    let firstPart = ""
    let secondPart = ""
    let areas = ""

    cards.forEach((card, index) => {
        if (cardPositions[index] == 1) {
            areas = areas + "a "
        }
        else if (cardPositions[index] == 2) {
            areas = areas + "b "
        }
        else if (cardPositions[index] == 3) {
            areas = areas + "c "
        }
        else if (cardPositions[index] == 4) {
            areas = areas + "d "
        }
        if (index == 1) {
            firstPart = areas.substring(0, areas.length - 1)
            areas = ""
        }
        else if (index == 3) {
            secondPart = areas.substring(0, areas.length - 1)
        }
    })
    return `"${firstPart}" "${secondPart}"`
}

// CHOOSE CARD
function chooseCard(card) {
    if (gameInProgress == true && !shufflingInProgress && !cardsRevealed) {  // if can choose card
        evaluateChoice(card)
        saveGameObjectToLocalStorage()

        flipCard(card, false)

        setTimeout(() => {
            flipCards(false)
            updateStatusElement(currentGameStatusElem, "block", primaryColor, "Card Positions Revealed")
            endRound()
        }, 3000)
        cardsRevealed = true
    }
}
function evaluateChoice(card) {
    if (card.id == aceId) {
        updateStatusElement(currentGameStatusElem, "block", winColor, "You Picked the Ace of Spades!!!")
        updateScore()
    }
    else {
        updateStatusElement(currentGameStatusElem, "block", loseColor, "You Picked the Wrong Card...")
    }
}
function updateStatusElement(elem, display, color, innerHTML) {
    elem.style.display = display

    if (arguments.length > 2) {
        elem.style.color = color
        elem.innerHTML = innerHTML
    }
}

// UPDATE SCORE
function updateScore() {
    const scoreToAdd = calculateScoreToAdd(roundNum)
    score += scoreToAdd

    updateStatusElement(scoreElem, "block", primaryColor, `Score <span class='badge'>${score}</span>`)
}
function calculateScoreToAdd(roundNum) {
    if (roundNum == 1) {
        return 100
    }
    else if (roundNum == 2) {
        return 50
    }
    else if (roundNum == 3) {
        return 25
    }
    else {
        return 10
    }
}

// END ROUND
function endRound() {
    setTimeout(() => {
        if (roundNum == maxRounds) {
            gameOver()
            return
        }
        else {
            startRound()
        }
    }, 3000)
}
function gameOver() {
    updateStatusElement(roundContainerElem, "none")
    updateStatusElement(currentGameStatusElem, "block", primaryColor, "Click 'Play Game' Button to Play Again!")
    gameInProgress = false
    playGameButtonElem.disabled = false
}

// LOCAL STORAGE FUNCTIONALITY
let gameObject = {}
const localStorageGameKey = "HTA"
function saveGameObjectToLocalStorage() {
    gameObject.score = score
    gameObject.round = roundNum

    json = JSON.stringify(gameObject)
    localStorage.setItem(localStorageGameKey, json) // update local storage item
}
function checkForIncompleteGame() {
    const serializedGameObject = localStorage.getItem(localStorageGameKey) // get item from local storage
    if (serializedGameObject) {
        gameObject = JSON.parse(serializedGameObject) // convert json to object
        
        if (gameObject.round >= maxRounds) {
            localStorage.removeItem(serializedGameObject) // remove item from local storage
        }
        else {
            score = gameObject.score
            roundNum = gameObject.round
        }
    }
}

loadGame()
