// --- CONFIGURATION & CATALOGS ---
const AVAILABLE_TRANSLATIONS = ["AMP", "ASV", "CPDV", "ERV", "ESV", "KJV", "NASB", "WEB"];

const BIBLE_BOOKS = [
    ["Genesis", 50, "OT", "GEN"], ["Exodus", 40, "OT", "EXO"], ["Leviticus", 27, "OT", "LEV"], 
    ["Numbers", 36, "OT", "NUM"], ["Deuteronomy", 34, "OT", "DEU"], ["Joshua", 24, "OT", "JOS"], 
    ["Judges", 21, "OT", "JDG"], ["Ruth", 4, "OT", "RUT"], ["1 Samuel", 31, "OT", "1SA"], 
    ["2 Samuel", 24, "OT", "2SA"], ["1 Kings", 22, "OT", "1KI"], ["2 Kings", 25, "OT", "2KI"], 
    ["1 Chronicles", 29, "OT", "1CH"], ["2 Chronicles", 36, "OT", "2CH"], ["Ezra", 10, "OT", "EZR"], 
    ["Nehemiah", 13, "OT", "NEH"], ["Esther", 10, "OT", "EST"], ["Job", 42, "OT", "JOB"], 
    ["Psalms", 150, "OT", "PSA"], ["Proverbs", 31, "OT", "PRO"], ["Ecclesiastes", 12, "OT", "ECC"], 
    ["Song of Solomon", 8, "OT", "SNG"], ["Isaiah", 66, "OT", "ISA"], ["Jeremiah", 52, "OT", "JER"], 
    ["Lamentations", 5, "OT", "LAM"], ["Ezekiel", 48, "OT", "EZK"], ["Daniel", 12, "OT", "DAN"],
    ["Hosea", 14, "OT", "HOS"], ["Joel", 3, "OT", "JOL"], ["Amos", 9, "OT", "AMO"], 
    ["Obadiah", 1, "OT", "OBA"], ["Jonah", 4, "OT", "JON"], ["Micah", 7, "OT", "MIC"], 
    ["Nahum", 3, "OT", "NAH"], ["Habakkuk", 3, "OT", "HAB"], ["Zephaniah", 3, "OT", "ZEP"], 
    ["Haggai", 2, "OT", "HAG"], ["Zechariah", 14, "OT", "ZEC"], ["Malachi", 4, "OT", "MAL"], 
    ["Matthew", 28, "NT", "MAT"], ["Mark", 16, "NT", "MRK"], ["Luke", 24, "NT", "LUK"], 
    ["John", 21, "NT", "JHN"], ["Acts", 28, "NT", "ACT"], ["Romans", 16, "NT", "ROM"], 
    ["1 Corinthians", 16, "NT", "1CO"], ["2 Corinthians", 13, "NT", "2CO"], ["Galatians", 6, "NT", "GAL"], 
    ["Ephesians", 6, "NT", "EPH"], ["Philippians", 4, "NT", "PHP"], ["Colossians", 4, "NT", "COL"], 
    ["1 Thessalonians", 5, "NT", "1TH"], ["2 Thessalonians", 3, "NT", "2TH"], ["1 Timothy", 6, "NT", "1TI"], 
    ["2 Timothy", 4, "NT", "2TI"], ["Titus", 3, "NT", "TIT"], ["Philemon", 1, "NT", "PHM"], 
    ["Hebrews", 13, "NT", "HEB"], ["James", 5, "NT", "JAS"], ["1 Peter", 5, "NT", "1PE"], 
    ["2 Peter", 3, "NT", "2PE"], ["1 John", 5, "NT", "1JN"], ["2 John", 1, "NT", "2JN"], 
    ["3 John", 1, "NT", "3JN"], ["Jude", 1, "NT", "JUD"], ["Revelation", 22, "NT", "REV"]
];

const STOP_WORDS = new Set([
    "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", 
    "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", 
    "his", "how", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most", 
    "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other", "our", 
    "ours", "ourselves", "out", "over", "own", "s", "same", "she", "should", "so", "some", "such", "t", 
    "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", 
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", 
    "when", "where", "which", "while", "who", "whom", "why", "will", "with", "you", "your", "yours", 
    "yourself", "yourselves", "shall", "unto", "thou", "thy", "thine", "ye", "also", "even", "let",
    "therefore", "upon", "whoever", "however", "whose", "lord", "god", "man", "king", "son", "israel", 
    "day", "people", "house", "hand", "word", "father", "name", "land", "earth", "city", "heaven", 
    "eye", "year", "brother", "heart", "spirit", "face", "blood", "voice", "water", "priest", "woman", 
    "law", "head", "sword", "month", "mountain", "way", "servant", "master", "peace", "truth", "world", 
    "time", "fire", "temple", "flesh", "mouth", "gold", "altar", "offering", "death", "gate", "field", 
    "sin", "soul", "tree", "wood", "morning", "night", "mother", "sister", "wife", "husband", "nation", 
    "tribe", "leader", "army", "stone", "sea", "wind", "cloud", "beast", "bird", "child", "daughter", 
    "prophet", "judge", "covenant", "sacrifice", "wine", "bread", "oil", "garment", "jesus", "say", 
    "speak", "do", "make", "go", "come", "see", "hear", "give", "take", "know", "call", "bring", 
    "let", "put", "find", "tell", "keep", "live", "die", "stand", "fall", "love", "hate", "save", 
    "destroy", "build", "send", "walk", "follow", "lead", "teach", "believe", "pray", "praise", 
    "worship", "bless", "curse", "rule", "judge", "fight", "kill", "eat", "drink", "sleep", "rise", 
    "sit", "look", "listen", "command", "remember", "forget", "forgive", "sin", "repent", "hope", 
    "trust", "fear", "wait", "show", "hide", "reveal", "cover", "open", "close", "turn", "return", 
    "leave", "remain", "depart", "good", "evil", "great", "small", "holy", "righteous", "wicked", 
    "clean", "unclean", "high", "low", "first", "last", "new", "old", "true", "false", "wise", 
    "foolish", "strong", "weak", "rich", "poor", "full", "empty", "living", "dead", "pure", 
    "defiled", "perfect", "broken", "beautiful", "light", "dark", "sweet", "bitter", "right", 
    "wrong", "just", "unjust", "faithful", "mighty", "humble", "proud", "glad", "sad", "angry", 
    "blind", "whole", "sick"
]);

const CATEGORY_COLORS = ["#f9df6d", "#a0c35a", "#b0c4ef", "#ba81c5"];

// --- GAME STATE variables ---
let translation = "ESV";
let bookChoice = "Entire Bible";
let zoomLevel = 1.0;

let versePool = {};
let boardCategories = {};
let categoryColorMap = {};
let allWords = [];
let selectedWords = [];
let solvedCategories = [];
let pastGuesses = new Set();
let lives = 7;
let isGameOver = false;

// --- INITIALIZATION ---
// We remove the DOMContentLoaded wrapper so it runs immediately
console.log("🔌 Script successfully loaded and connected to HTML!");

populateBookDropdown();
setupEventListeners();

function populateBookDropdown() {
    console.log("📚 Populating book dropdown menu...");
    const bookSelect = document.getElementById("book-select");
    BIBLE_BOOKS.forEach(book => {
        const opt = document.createElement("option");
        opt.value = book[0];
        opt.textContent = book[0];
        bookSelect.appendChild(opt);
    });
}

function setupEventListeners() {
    console.log("️ Clicking listeners activated!");
    document.getElementById("generate-btn").addEventListener("click", () => {
        console.log(" Target acquired: GENERATE BOARD button clicked!");
        startBoardGeneration();
    });
    document.getElementById("how-to-play-btn").addEventListener("click", showHowToPlay);
    document.getElementById("shuffle-btn").addEventListener("click", shuffleBoard);
    document.getElementById("deselect-btn").addEventListener("click", deselectAll);
    document.getElementById("submit-btn").addEventListener("click", submitGuess);
    document.getElementById("zoom-in-btn").addEventListener("click", () => adjustZoom(0.1));
    document.getElementById("zoom-out-btn").addEventListener("click", () => adjustZoom(-0.1));

    // --- NEW: Auto-zoom out on mobile/square aspect ---
    const mediaQuery = window.matchMedia("(max-width: 650px)");
    
    function handleScreenChange(e) {
        if (e.matches) {
            zoomLevel = 0.7; // Automatically zoom out all the way (equivalent to 3 clicks)
        } else {
            zoomLevel = 1.0; // Reset to default on wider desktop screens
        }
        
        // Apply the zoom visually
        document.documentElement.style.setProperty('--zoom', zoomLevel);
        
        // Re-render elements so the font scaling math applies cleanly
        if (allWords.length > 0 || solvedCategories.length > 0) {
            renderGrid();
            renderSolvedCategories();
        }
    }

    // Listen for users dragging their window to shrink it
    mediaQuery.addEventListener("change", handleScreenChange);
    // Fire once immediately to catch the initial screen size if they loaded on a phone
    handleScreenChange(mediaQuery);
}

function showHowToPlay() {
    alert(
        "HOW TO PLAY:\n\n" +
        "• Find groups of 4 words sharing a common Bible verse.\n" +
        "• Select 4 words and tap 'Submit' to guess.\n" +
        "• You have 7 lives to solve the entire board.\n" +
        "• Anchors represent a guaranteed word for each hidden verse.\n" +
        "• Box colors mark Bible position (Yellow = earliest, Purple = latest)."
    );
}

// --- CORE UTILITIES ---
function getWords(text) {
    const rawWords = text.toLowerCase().match(/[a-z]+(?:['\-][a-z]+)*/g) || [];
    const validWords = rawWords.filter(word => !STOP_WORDS.has(word) && word.length > 3);
    return new Set(validWords);
}

function adjustZoom(amount) {
    zoomLevel = Math.max(0.7, Math.min(2.0, round(zoomLevel + amount, 1)));
    document.documentElement.style.setProperty('--zoom', zoomLevel);
    renderGrid();
    renderSolvedCategories();
}

function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

function getVerseSortKey(ref) {
    try {
        let bookName = ref;
        let chapNum = 0;
        let verseNum = 0;

        if (ref.includes(":")) {
            const parts = ref.split(":");
            verseNum = parseInt(parts[1].replace(/\D/g, '')) || 0;
            const bookChap = parts[0].lastIndexOf(" ");
            bookName = parts[0].substring(0, bookChap).trim();
            chapNum = parseInt(parts[0].substring(bookChap).trim()) || 0;
        }
        const bookIdx = BIBLE_BOOKS.findIndex(b => b[0] === bookName);
        return [bookIdx !== -1 ? bookIdx : 999, chapNum, verseNum];
    } catch (e) {
        return [999, 0, 0];
    }
}

function sortReferencesChronologically(refs) {
    return refs.sort((a, b) => {
        const keyA = getVerseSortKey(a);
        const keyB = getVerseSortKey(b);
        if (keyA[0] !== keyB[0]) return keyA[0] - keyB[0];
        if (keyA[1] !== keyB[1]) return keyA[1] - keyB[1];
        return keyA[2] - keyB[2];
    });
}

// --- ASYNC BIBLE DATA PROCESSING ---
async function fetchVersePool(poolSize = 15) {
    let verses = {};
    let validBooks = [];

    if (bookChoice === "Entire Bible") validBooks = BIBLE_BOOKS;
    else if (bookChoice === "Old Testament") validBooks = BIBLE_BOOKS.filter(b => b[2] === "OT");
    else if (bookChoice === "New Testament") validBooks = BIBLE_BOOKS.filter(b => b[2] === "NT");
    else validBooks = BIBLE_BOOKS.filter(b => b[0] === bookChoice);

    for (let i = 0; i < poolSize; i++) {
        try {
            const randomBook = validBooks[Math.floor(Math.random() * validBooks.length)];
            const [bName, maxChapters, testament, abbrev] = randomBook;

            // Direct relative network fetch matching your folder design
            const filePath = `Bible_Data/${testament}/${abbrev}/${translation}.json`;
            const response = await fetch(filePath);
            if (!response.ok) continue;
            
            const data = await response.json();
            const chapters = data.text || [];
            if (chapters.length === 0) continue;

            const randomChapter = chapters[Math.floor(Math.random() * chapters.length)];
            const versesInChap = randomChapter.text || [];
            if (versesInChap.length === 0) continue;

            const randomVerse = versesInChap[Math.floor(Math.random() * versesInChap.length)];
            
            let rawName = String(randomChapter.name || "");
            let chapNum = rawName.split(' ').pop().replace(/\D/g, '') || "1";
            let verseNum = String(randomVerse.ID || "?");
            let key = `${bName} ${chapNum}:${verseNum}`;

            let text = (randomVerse.text || "")
                .replace(/—/g, ' ').replace(/–/g, ' ')
                .replace(/<[^>]+>/g, '')
                .replace(/[“”]/g, '"').replace(/[‘’]/g, "'");

            if (!verses[key]) {
                verses[key] = text;
            }
        } catch (err) {
            // Quiet fail to continue loop safely
        }
    }
    return verses;
}

// Helper simulating python's itertools.combinations
function getCombinations(array, k) {
    let result = [];
    function helper(start, combo) {
        if (combo.length === k) {
            result.push([...combo]);
            return;
        }
        for (let i = start; i < array.length; i++) {
            combo.push(array[i]);
            helper(i + 1, combo);
            combo.pop();
        }
    }
    helper(0, []);
    return result;
}

async function startBoardGeneration() {
    translation = document.getElementById("translation-select").value;
    bookChoice = document.getElementById("book-select").value;

    // Show loading text using system generation feedback mechanics
    const setupScreen = document.getElementById("setup-screen");
    setupScreen.innerHTML = `<h1>Searching the Scriptures...</h1><p style='color: var(--text-muted); font-size:18px;'>Generating your board...</p>`;

    let attempts = 0;
    const maxAttempts = 15;
    let success = false;

    while (attempts < maxAttempts && !success) {
        attempts++;
        versePool = await fetchVersePool(15);
        const poolKeys = Object.keys(versePool);
        
        let verseWords = {};
        poolKeys.forEach(k => { verseWords[k] = getWords(versePool[k]); });

        const combos = getCombinations(poolKeys, 4);

        for (let combo of combos) {
            let tempBoard = {};
            let validBoard = true;

            for (let k of combo) {
                let otherWords = new Set();
                for (let otherK of combo) {
                    if (k !== otherK) {
                        verseWords[otherK].forEach(w => otherWords.add(w));
                    }
                }

                let uniqueToK = [...verseWords[k]].filter(w => !otherWords.has(w));
                if (uniqueToK.length < 4) {
                    validBoard = false;
                    break;
                }

                // Sort by descending character length to isolate meaningful keywords
                uniqueToK.sort((a, b) => b.length - a.length);
                tempBoard[k] = uniqueToK.slice(0, 4);
            }

            if (validBoard) {
                boardCategories = tempBoard;
                success = true;
                break;
            }
        }
    }

    if (success) {
        allWords = [];
        Object.values(boardCategories).forEach(words => allWords.push(...words));
        // Shuffle engine
        allWords.sort(() => Math.random() - 0.5);

        const sortedRefs = sortReferencesChronologically(Object.keys(boardCategories));
        categoryColorMap = {};
        sortedRefs.forEach((ref, idx) => {
            categoryColorMap[ref] = CATEGORY_COLORS[idx % CATEGORY_COLORS.length];
        });

        // Reset global configurations
        lives = 7;
        solvedCategories = [];
        selectedWords = [];
        pastGuesses.clear();
        isGameOver = false;

        // Visual UI Transition to active play container
        document.getElementById("setup-screen").style.display = "none";
        document.getElementById("game-screen").style.display = "flex";

        // Setup Anchors Header Elements (Uses sorted chronological references)
        const anchors = sortedRefs.map(ref => boardCategories[ref][0].toUpperCase());
        document.getElementById("anchors-hint").textContent = `Anchors: ${anchors.join(", ")}`;
        document.getElementById("msg-label").textContent = "";
        document.getElementById("lives-label").textContent = `Lives: ${"❤️ ".repeat(lives)}`;
        
        renderGrid();
        renderSolvedCategories();
    } else {
        alert("Could not generate a valid board. Please pick another book combination or use Entire Bible!");
        location.reload(); // Hard reload back to original selection
    }
}

// --- INTERACTIVE LAYOUT RENDERING ---
function renderGrid() {
    const gridFrame = document.getElementById("grid-frame");
    gridFrame.innerHTML = "";

    if (isGameOver && allWords.length === 0) return;

    allWords.forEach(word => {
        const btn = document.createElement("button");
        btn.className = "grid-btn";
        if (selectedWords.includes(word)) {
            btn.classList.add("selected");
        }
        // --- Injects a break point if the word is longer than 8 characters ---
        let textToDisplay = word.toUpperCase(); 
        if (textToDisplay.length > 8) {
            textToDisplay = textToDisplay.slice(0, 5) + '\u00AD' + textToDisplay.slice(5);
        }
        btn.textContent = textToDisplay;
        btn.addEventListener("click", () => toggleWord(word));
        gridFrame.appendChild(btn);
    });
}

function toggleWord(word) {
    if (isGameOver) return;

    if (selectedWords.includes(word)) {
        selectedWords = selectedWords.filter(w => w !== word);
    } else {
        if (selectedWords.length < 4) {
            selectedWords.push(word);
        }
    }

    document.getElementById("deselect-btn").disabled = selectedWords.length === 0;
    document.getElementById("submit-btn").disabled = selectedWords.length !== 4;
    document.getElementById("msg-label").textContent = "";
    renderGrid();
}

function deselectAll() {
    selectedWords = [];
    document.getElementById("deselect-btn").disabled = true;
    document.getElementById("submit-btn").disabled = true;
    renderGrid();
}

function shuffleBoard() {
    if (isGameOver) return;
    allWords.sort(() => Math.random() - 0.5);
    renderGrid();
}

// --- CORE GUESS LOGIC MECHANICS ---
function submitGuess() {
    if (selectedWords.length !== 4 || isGameOver) return;

    const currentGuessSet = new Set(selectedWords);
    
    // Create unique identity string sorting for tracking sets accurately
    const guessFrozen = [...currentGuessSet].sort().join(",");
    const msgLabel = document.getElementById("msg-label");

    if (pastGuesses.has(guessFrozen)) {
        msgLabel.textContent = "Already guessed!";
        msgLabel.className = "msg-text status-orange";
        deselectAll();
        return;
    }
    pastGuesses.add(guessFrozen);

    let matchFound = false;

    for (let [ref, words] of Object.entries(boardCategories)) {
        const categorySet = new Set(words);
        const intersection = [...currentGuessSet].filter(w => categorySet.has(w));

        if (intersection.length === 4) {
            matchFound = true;
            solvedCategories.push(ref);
            
            // Remove guessed words entirely out of the active grid layout array
            allWords = allWords.filter(w => !currentGuessSet.has(w));
            selectedWords = [];

            msgLabel.textContent = "Correct!";
            msgLabel.className = "msg-text status-green";

            renderSolvedCategories();
            renderGrid();

            if (allWords.length === 0) {
                endGame(true);
            }
            break;
        }
    }

    if (!matchFound) {
        let oneAwayHint = null;

        for (let [ref, words] of Object.entries(boardCategories)) {
            const categorySet = new Set(words);
            const intersection = [...currentGuessSet].filter(w => categorySet.has(w));
            
            if (intersection.length === 3) {
                if (["Entire Bible", "Old Testament", "New Testament"].includes(bookChoice)) {
                    oneAwayHint = ref.substring(0, ref.lastIndexOf(" ")).trim();
                } else {
                    oneAwayHint = "Chapter " + ref.split(":")[0].split(" ").pop();
                }
                break;
            }
        }

        lives--;
        document.getElementById("lives-label").textContent = `Lives: ${"❤️ ".repeat(lives)}`;

        if (oneAwayHint) {
            msgLabel.textContent = `One Away! (Hint: 3 are from ${oneAwayHint})`;
            msgLabel.className = "msg-text status-orange";
        } else {
            msgLabel.textContent = "Incorrect.";
            msgLabel.className = "msg-text status-red";
        }

        if (lives <= 0) {
            endGame(false);
        }
    }

    document.getElementById("deselect-btn").disabled = true;
    document.getElementById("submit-btn").disabled = true;
}

// --- RENDER SOLVED CATEGORIES WITH RICH HIGHLIGHTING ---
function renderSolvedCategories() {
    const solvedFrame = document.getElementById("solved-frame");
    solvedFrame.innerHTML = "";

    solvedCategories.forEach(ref => {
        const color = categoryColorMap[ref] || CATEGORY_COLORS[0];
        const words = boardCategories[ref];
        let originalText = versePool[ref];

        // Highlight matching solution words directly in verse block
        words.forEach(w => {
            const regex = new RegExp(`\\b${w}\\b`, 'gi');
            originalText = originalText.replace(regex, match => `<strong>${match}</strong>`);
        });

        const solvedBox = document.createElement("div");
        solvedBox.className = "solved-box";
        solvedBox.style.backgroundColor = color;

        const textContent = document.createElement("div");
        textContent.className = "solved-text-content";
        textContent.innerHTML = `<span style="font-weight:bold; font-size:calc(16px * var(--zoom));">${ref}</span><br>${originalText}`;
        
        solvedBox.appendChild(textContent);
        solvedFrame.appendChild(solvedBox);
    });
}

function endGame(win) {
    isGameOver = true;
    const msgLabel = document.getElementById("msg-label");

    if (win) {
        msgLabel.textContent = "Nice job! You solved the board!";
        msgLabel.className = "msg-text status-green";
    } else {
        msgLabel.textContent = "Game Over. Better luck next time!";
        msgLabel.className = "msg-text status-red";
        
        // Expose remaining mystery solutions upon systemic failures
        Object.keys(boardCategories).forEach(ref => {
            if (!solvedCategories.includes(ref)) {
                solvedCategories.push(ref);
            }
        });
        
        renderSolvedCategories();
        renderGrid();

        // Visually lock and dim the remaining grid beneath the answers
        const grid = document.getElementById("grid-frame");
        if (grid) {
            grid.style.pointerEvents = "none";
            grid.style.opacity = "0.5";
        }
    }

    // Transform setup components for clean "Play Again" access loop execution
    const ctrlFrame = document.querySelector(".ctrl-frame");
    if (ctrlFrame) {
        ctrlFrame.innerHTML = `<button id="play-again-btn" class="ctk-btn primary-btn" style="width:200px;">Play Again</button>`;
        document.getElementById("play-again-btn").addEventListener("click", () => {
            location.reload();
        });
    }
}