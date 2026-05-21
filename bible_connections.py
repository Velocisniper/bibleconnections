import customtkinter as ctk
import random
import re
import json
import itertools
import sys
import os
import threading
from PIL import Image

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Path Handling (Crucial for ONE-FILE auto-py-to-exe!)
def get_base_path():
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return sys._MEIPASS
    except Exception:
        return os.path.dirname(os.path.abspath(__file__))

APPLICATION_PATH = get_base_path()
BIBLE_DATA_DIR = os.path.join(APPLICATION_PATH, "Bible_Data")

# Available Translations
AVAILABLE_TRANSLATIONS = ["AMP", "ASV", "CPDV", "ERV", "ESV", "KJV", "NASB", "WEB"]

# Catalog of all 66 books
BIBLE_BOOKS = [
    ("Genesis", 50, "OT", "GEN"), ("Exodus", 40, "OT", "EXO"), ("Leviticus", 27, "OT", "LEV"), 
    ("Numbers", 36, "OT", "NUM"), ("Deuteronomy", 34, "OT", "DEU"), ("Joshua", 24, "OT", "JOS"), 
    ("Judges", 21, "OT", "JDG"), ("Ruth", 4, "OT", "RUT"), ("1 Samuel", 31, "OT", "1SA"), 
    ("2 Samuel", 24, "OT", "2SA"), ("1 Kings", 22, "OT", "1KI"), ("2 Kings", 25, "OT", "2KI"), 
    ("1 Chronicles", 29, "OT", "1CH"), ("2 Chronicles", 36, "OT", "2CH"), ("Ezra", 10, "OT", "EZR"), 
    ("Nehemiah", 13, "OT", "NEH"), ("Esther", 10, "OT", "EST"), ("Job", 42, "OT", "JOB"), 
    ("Psalms", 150, "OT", "PSA"), ("Proverbs", 31, "OT", "PRO"), ("Ecclesiastes", 12, "OT", "ECC"), 
    ("Song of Solomon", 8, "OT", "SNG"), ("Isaiah", 66, "OT", "ISA"), ("Jeremiah", 52, "OT", "JER"), 
    ("Lamentations", 5, "OT", "LAM"), ("Ezekiel", 48, "OT", "EZK"), ("Daniel", 12, "OT", "DAN"),
    ("Hosea", 14, "OT", "HOS"), ("Joel", 3, "OT", "JOL"), ("Amos", 9, "OT", "AMO"), 
    ("Obadiah", 1, "OT", "OBA"), ("Jonah", 4, "OT", "JON"), ("Micah", 7, "OT", "MIC"), 
    ("Nahum", 3, "OT", "NAH"), ("Habakkuk", 3, "OT", "HAB"), ("Zephaniah", 3, "OT", "ZEP"), 
    ("Haggai", 2, "OT", "HAG"), ("Zechariah", 14, "OT", "ZEC"), ("Malachi", 4, "OT", "MAL"), 
    ("Matthew", 28, "NT", "MAT"), ("Mark", 16, "NT", "MRK"), ("Luke", 24, "NT", "LUK"), 
    ("John", 21, "NT", "JHN"), ("Acts", 28, "NT", "ACT"), ("Romans", 16, "NT", "ROM"), 
    ("1 Corinthians", 16, "NT", "1CO"), ("2 Corinthians", 13, "NT", "2CO"), ("Galatians", 6, "NT", "GAL"), 
    ("Ephesians", 6, "NT", "EPH"), ("Philippians", 4, "NT", "PHP"), ("Colossians", 4, "NT", "COL"), 
    ("1 Thessalonians", 5, "NT", "1TH"), ("2 Thessalonians", 3, "NT", "2TH"), ("1 Timothy", 6, "NT", "1TI"), 
    ("2 Timothy", 4, "NT", "2TI"), ("Titus", 3, "NT", "TIT"), ("Philemon", 1, "NT", "PHM"), 
    ("Hebrews", 13, "NT", "HEB"), ("James", 5, "NT", "JAS"), ("1 Peter", 5, "NT", "1PE"), 
    ("2 Peter", 3, "NT", "2PE"), ("1 John", 5, "NT", "1JN"), ("2 John", 1, "NT", "2JN"), 
    ("3 John", 1, "NT", "3JN"), ("Jude", 1, "NT", "JUD"), ("Revelation", 22, "NT", "REV")
]

STOP_WORDS = {
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
}

# Ordered from Earliest (Yellow) to Latest (Purple)
CATEGORY_COLORS = ["#f9df6d", "#a0c35a", "#b0c4ef", "#ba81c5"] 

class BibleConnectionsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bible Verse Connections")
        self.geometry("800x700")
        self.minsize(500, 600)

        # Game State Variables
        self.translation = "ESV"
        self.book_choice = "Entire Bible"
        
        # Saved preferences for Play Again
        self.saved_translation = "ESV"
        self.saved_book = "Entire Bible"
        
        # Display settings
        self.zoom_level = 1.0

        self.verse_pool = {}
        self.board_categories = {}
        self.category_color_map = {}
        self.all_words = []
        self.selected_words = []
        self.solved_categories = []
        self.past_guesses = set() # Track previous guesses
        self.lives = 7
        self.buttons = {}
        
        self.show_setup_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- SCREEN: HOW TO PLAY ---
    def show_how_to_play_screen(self):
        self.clear_window()
        
        # Wrapped in a scrollable frame
        self.help_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.help_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(self.help_scroll, text="HOW TO PLAY", font=("Arial", 32, "bold"))
        title.pack(pady=(50, 20))
        
        rules_text = (
            "Welcome to Bible Verse Connections!\n\n"
            "Your goal is to find groups of 4 words that all share a common Bible verse.\n\n"
            "• Select 4 words and tap 'Submit' to guess.\n"
            "• You have 7 lives to solve the entire board.\n"
            "• Anchor words represent a guaranteed word for each of the four hidden verses.\n"
            "• Color mapping indicates position in the Bible (Yellow = earliest, Purple = latest).\n"
            "• Remember, each word is unique to its respective verse. Good luck!"
        )
        
        rules_lbl = ctk.CTkLabel(self.help_scroll, text=rules_text, font=("Arial", 16), justify="left", wraplength=500)
        rules_lbl.pack(pady=20)
        
        back_btn = ctk.CTkButton(self.help_scroll, text="BACK TO MENU", font=("Arial", 16, "bold"), 
                                 command=self.show_setup_screen, height=50, width=200)
        back_btn.pack(pady=40)

    # --- SCREEN 1: SETUP ---
    def show_setup_screen(self):
        self.clear_window()
        
        # Wrapped in a scrollable frame
        self.setup_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.setup_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not os.path.exists(BIBLE_DATA_DIR):
            lbl = ctk.CTkLabel(self.setup_scroll, text=f"CRITICAL ERROR:\nMissing 'Bible_Data' folder in:\n{APPLICATION_PATH}", 
                               text_color="red", font=("Arial", 18, "bold"))
            lbl.pack(expand=True, pady=50)
            return

        title = ctk.CTkLabel(self.setup_scroll, text="BIBLE VERSE CONNECTIONS", font=("Arial", 32, "bold"))
        title.pack(pady=(40, 20))

        # --- LOGO INTEGRATION ---
        logo_path = os.path.join(BIBLE_DATA_DIR, "logo.png") 
        if os.path.exists(logo_path):
            try:
                img_data = Image.open(logo_path)
                logo_image = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(120, 120))
                logo_lbl = ctk.CTkLabel(self.setup_scroll, text="", image=logo_image)
                logo_lbl.pack(pady=(0, 20))
            except Exception as e:
                print(f"Error loading logo: {e}")

        ctk.CTkLabel(self.setup_scroll, text="Select Translation:", font=("Arial", 16)).pack(pady=(10, 0))
        self.trans_var = ctk.StringVar(value=self.saved_translation)
        trans_dropdown = ctk.CTkOptionMenu(self.setup_scroll, variable=self.trans_var, values=AVAILABLE_TRANSLATIONS)
        trans_dropdown.pack(pady=(5, 20))

        ctk.CTkLabel(self.setup_scroll, text="Select Book:", font=("Arial", 16)).pack(pady=(10, 0))
        
        # Added OT and NT options
        book_options = ["Entire Bible", "Old Testament", "New Testament"] + [b[0] for b in BIBLE_BOOKS]
        
        self.book_var = ctk.StringVar(value=self.saved_book)
        book_dropdown = ctk.CTkOptionMenu(self.setup_scroll, variable=self.book_var, values=book_options, width=200)
        book_dropdown.pack(pady=(5, 30))

        start_btn = ctk.CTkButton(self.setup_scroll, text="GENERATE BOARD", font=("Arial", 16, "bold"), 
                                  command=self.start_generation_thread, height=50, width=200)
        start_btn.pack(pady=(10, 10))
        
        # How to Play Button
        help_btn = ctk.CTkButton(self.setup_scroll, text="HOW TO PLAY", font=("Arial", 14, "bold"),
                                 command=self.show_how_to_play_screen, height=40, width=200)
        help_btn.pack(pady=10)

    # --- LOGIC: BOARD GENERATION ---
    def start_generation_thread(self):
        # Save choices for "Play Again" functionality
        self.saved_translation = self.trans_var.get()
        self.saved_book = self.book_var.get()
        
        self.translation = self.saved_translation
        self.book_choice = self.saved_book
        
        self.clear_window()
        loading_lbl = ctk.CTkLabel(self, text="Searching the Scriptures...\nGenerating your board...", 
                                   font=("Arial", 24, "bold"))
        loading_lbl.pack(expand=True)

        threading.Thread(target=self.generate_board_logic, daemon=True).start()

    def get_words(self, text):
        raw_words = re.findall(r"[a-z]+(?:['\-][a-z]+)*", text.lower())
        return set(word for word in raw_words if word not in STOP_WORDS and len(word) > 3)

    def fetch_verse_pool(self, pool_size=12):
        verses = {}
        
        # Determine valid books based on user selection
        if self.book_choice == "Entire Bible":
            valid_books = BIBLE_BOOKS
        elif self.book_choice == "Old Testament":
            valid_books = [b for b in BIBLE_BOOKS if b[2] == "OT"]
        elif self.book_choice == "New Testament":
            valid_books = [b for b in BIBLE_BOOKS if b[2] == "NT"]
        else:
            valid_books = [b for b in BIBLE_BOOKS if b[0] == self.book_choice]

        for _ in range(pool_size):
            try:
                b_name, max_chapters, testament, abbrev = random.choice(valid_books)
                
                file_path = os.path.join(BIBLE_DATA_DIR, testament, abbrev, f"{self.translation}.json")
                if not os.path.exists(file_path): continue

                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                chapters = data.get("text", [])
                if not chapters: continue
                
                random_chapter = random.choice(chapters)
                verses_in_chap = random_chapter.get("text", [])
                if not verses_in_chap: continue
                
                random_verse = random.choice(verses_in_chap)
                
                # Format securely for chronological sorting ("Book Chapter:Verse")
                raw_name = str(random_chapter.get("name", ""))
                chap_num = re.sub(r'\D', '', raw_name.split(' ')[-1] if ' ' in raw_name else raw_name)
                if not chap_num: chap_num = "1"
                
                verse_num = str(random_verse.get("ID", "?"))
                key = f"{b_name} {chap_num}:{verse_num}"
                
                verse_text = random_verse.get("text", "")
                
                # Fix em dashes and en dashes by replacing with spaces before parsing
                text = verse_text.replace('—', ' ').replace('–', ' ')
                text = re.sub(r'<[^>]+>', '', text)
                text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
                text = text.encode('ascii', 'ignore').decode('ascii')
                
                if key not in verses:
                    verses[key] = text
            except Exception:
                continue
        return verses

    def get_verse_sort_key(self, ref):
        """Helper to chronologically sort a verse reference key."""
        try:
            # Extract verse
            if ":" in ref:
                chap_book, verse_str = ref.rsplit(':', 1)
                verse_num = int(re.sub(r'\D', '', verse_str) or 0)
            else:
                chap_book = ref
                verse_num = 0
                
            # Extract chapter and book
            parts = chap_book.rsplit(' ', 1)
            if len(parts) == 2 and parts[1].isdigit():
                book = parts[0]
                chap_num = int(parts[1])
            else:
                book = chap_book
                chap_num = 0
                
            # Find book index
            book_names = [b[0] for b in BIBLE_BOOKS]
            book_idx = book_names.index(book) if book in book_names else 999
            
            return (book_idx, chap_num, verse_num)
        except Exception:
            return (999, 0, 0)

    def generate_board_logic(self):
        attempts, max_attempts = 0, 15
        success = False
        
        while attempts < max_attempts and not success:
            attempts += 1
            self.verse_pool = self.fetch_verse_pool(15)
            pool_keys = list(self.verse_pool.keys())
            verse_words = {k: self.get_words(self.verse_pool[k]) for k in pool_keys}
            
            for combo in itertools.combinations(pool_keys, 4):
                temp_board = {}
                valid_board = True
                
                for k in combo:
                    other_words = set()
                    for other_k in combo:
                        if k != other_k: other_words.update(verse_words[other_k])
                    
                    unique_to_k = verse_words[k] - other_words
                    if len(unique_to_k) < 4:
                        valid_board = False
                        break
                    
                    sorted_unique = sorted(list(unique_to_k), key=len, reverse=True)
                    temp_board[k] = sorted_unique[:4]
                
                if valid_board:
                    self.board_categories = temp_board
                    success = True
                    break

        if success:
            self.all_words = []
            for words in self.board_categories.values():
                self.all_words.extend(words)
            random.shuffle(self.all_words)
            
            # Pre-calculate chronological colors
            sorted_refs = sorted(self.board_categories.keys(), key=self.get_verse_sort_key)
            self.category_color_map = {}
            for i, ref in enumerate(sorted_refs):
                self.category_color_map[ref] = CATEGORY_COLORS[i % len(CATEGORY_COLORS)]
            
            # Reset states for a new game
            self.lives = 7
            self.solved_categories = []
            self.selected_words = []
            self.past_guesses = set()
            
            self.after(0, self.show_game_screen)
        else:
            self.after(0, self.show_error_screen)

    def show_error_screen(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Could not generate a valid board.", font=("Arial", 24, "bold"), text_color="red").pack(pady=(100,20))
        ctk.CTkLabel(self, text="This usually happens if a chosen book is too short.\nTry a different book or the Entire Bible.").pack(pady=20)
        ctk.CTkButton(self, text="Go Back", command=self.show_setup_screen).pack(pady=20)

    # --- SCREEN 2: GAME BOARD ---
    def show_game_screen(self):
        self.clear_window()
        
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=5, pady=0)
        
        header_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        header_frame.pack(pady=(10, 0), fill="x")
        
        title_lbl = ctk.CTkLabel(header_frame, text="BIBLE CONNECTIONS", font=("Arial", 24, "bold"))
        title_lbl.pack(pady=(0, 0))
        
        anchors = [words[0] for words in self.board_categories.values()]
        hint_lbl = ctk.CTkLabel(header_frame, text=f"Anchors: {', '.join(anchors).upper()}", font=("Arial", 14), text_color="gray")
        hint_lbl.pack(pady=(0, 0))

        self.solved_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent", height=1)
        self.solved_frame.pack(pady=0)

        self.grid_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.grid_frame.pack(pady=(5, 5))
        
        self.render_grid()

        ctrl_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        ctrl_frame.pack(pady=(5, 10))

        self.shuffle_btn = ctk.CTkButton(ctrl_frame, text="Shuffle", command=self.shuffle_board, width=100)
        self.shuffle_btn.grid(row=0, column=0, padx=10)

        self.deselect_btn = ctk.CTkButton(ctrl_frame, text="Deselect All", command=self.deselect_all, width=100, state="disabled")
        self.deselect_btn.grid(row=0, column=1, padx=10)

        self.submit_btn = ctk.CTkButton(ctrl_frame, text="Submit", command=self.submit_guess, width=100, state="disabled")
        self.submit_btn.grid(row=0, column=2, padx=10)

        self.msg_label = ctk.CTkLabel(self.main_scroll, text="", font=("Arial", 16, "bold"))
        self.msg_label.pack(pady=(0, 0))

        self.lives_label = ctk.CTkLabel(self.main_scroll, text=self.get_lives_text(), font=("Arial", 16))
        self.lives_label.pack(pady=(0, 10))

        # --- ZOOM BUTTONS EXTRACTED ---
        zoom_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        zoom_frame.pack(pady=(0, 20))

        self.zoom_out_btn = ctk.CTkButton(zoom_frame, text="Zoom -", command=self.zoom_out, width=70)
        self.zoom_out_btn.grid(row=0, column=0, padx=5)

        self.zoom_in_btn = ctk.CTkButton(zoom_frame, text="Zoom +", command=self.zoom_in, width=70)
        self.zoom_in_btn.grid(row=0, column=1, padx=5)

    def get_lives_text(self):
        return f"Lives: {'❤️ ' * self.lives}"

    # --- ZOOM LOGIC ---
    def zoom_in(self):
        if self.zoom_level < 2.0:
            self.zoom_level = round(self.zoom_level + 0.1, 1)
            self.render_grid()
            self.render_solved_categories()

    def zoom_out(self):
        if self.zoom_level > 0.7:
            self.zoom_level = round(self.zoom_level - 0.1, 1)
            self.render_grid()
            self.render_solved_categories()

    def render_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        self.buttons = {}
        
        btn_w = int(140 * self.zoom_level)
        btn_h = int(90 * self.zoom_level)
        f_size = max(8, int(14 * self.zoom_level))
        
        for idx, word in enumerate(self.all_words):
            row, col = divmod(idx, 4)
            btn = ctk.CTkButton(self.grid_frame, text=word.upper(), font=("Arial", f_size, "bold"), 
                                width=btn_w, height=btn_h, fg_color="#333333", text_color="white",
                                command=lambda w=word: self.toggle_word(w))
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            if word in self.selected_words:
                btn.configure(fg_color="#5a5a5a")
                
            self.buttons[word] = btn

    def toggle_word(self, word):
        if word in self.selected_words:
            self.selected_words.remove(word)
            self.buttons[word].configure(fg_color="#333333")
        else:
            if len(self.selected_words) < 4:
                self.selected_words.append(word)
                self.buttons[word].configure(fg_color="#5a5a5a")
        
        self.deselect_btn.configure(state="normal" if self.selected_words else "disabled")
        self.submit_btn.configure(state="normal" if len(self.selected_words) == 4 else "disabled")
        self.msg_label.configure(text="")

    def deselect_all(self):
        for word in self.selected_words:
            self.buttons[word].configure(fg_color="#333333")
        self.selected_words.clear()
        self.deselect_btn.configure(state="disabled")
        self.submit_btn.configure(state="disabled")

    def shuffle_board(self):
        random.shuffle(self.all_words)
        self.render_grid()

    def submit_guess(self):
        selected_set = set(self.selected_words)
        
        guess_frozen = frozenset(selected_set)
        if guess_frozen in self.past_guesses:
            self.msg_label.configure(text="Already guessed!", text_color="orange")
            self.deselect_all()
            return
        
        self.past_guesses.add(guess_frozen)

        match_found = False
        
        for verse_ref, verse_words in self.board_categories.items():
            if selected_set == set(verse_words):
                match_found = True
                self.solved_categories.append(verse_ref)
                
                self.all_words = [w for w in self.all_words if w not in selected_set]
                self.selected_words.clear()
                
                self.msg_label.configure(text="Correct!", text_color="green")
                self.render_solved_categories()
                self.render_grid()
                
                if len(self.all_words) == 0:
                    self.end_game(win=True)
                break
                
        if not match_found:
            one_away_hint = None
            for verse_ref, verse_words in self.board_categories.items():
                if len(set(verse_words).intersection(selected_set)) == 3:
                    if self.book_choice in ["Entire Bible", "Old Testament", "New Testament"]:
                        one_away_hint = verse_ref.rsplit(' ', 1)[0]
                    else:
                        one_away_hint = "Chapter " + verse_ref.split(':')[0].split(' ')[-1]
                    break
            
            self.lives -= 1
            self.lives_label.configure(text=self.get_lives_text())
            
            if one_away_hint:
                self.msg_label.configure(text=f"One Away! (Hint: 3 are from {one_away_hint})", text_color="orange")
            else:
                self.msg_label.configure(text="Incorrect.", text_color="red")
                
            if self.lives <= 0:
                self.end_game(win=False)

        self.deselect_btn.configure(state="disabled")
        self.submit_btn.configure(state="disabled")

    def render_solved_categories(self):
        for widget in self.solved_frame.winfo_children():
            widget.destroy()
            
        box_w = int(590 * self.zoom_level)
        box_h = int(90 * self.zoom_level) 
        f_size = max(10, int(14 * self.zoom_level))
        
        # Store widgets so we can center them after layout
        textboxes_to_center = []
            
        for ref in self.solved_categories:
            color = self.category_color_map.get(ref, CATEGORY_COLORS[0])
            words = self.board_categories[ref]
            
            # Standardize newlines so Python regex character counts match Tkinter Text indices perfectly
            verse_text = self.verse_pool[ref].replace('\r\n', '\n').replace('\r', '')
            full_text = f"{ref}\n{verse_text}"
            
            # Using CTkTextbox to support rich text formatting
            textbox = ctk.CTkTextbox(self.solved_frame, width=box_w, height=box_h, 
                                     fg_color=color, text_color="black", wrap="word", 
                                     font=("Arial", f_size))
            textbox.pack(pady=5)
            
            # Safely access the underlying tk.Text widget to prevent CustomTkinter wrapper crashes
            tk_txt = textbox._textbox
            
            tk_txt.insert("1.0", full_text)
            
            try:
                # Configure tags on the internal tk.Text widget directly
                tk_txt.tag_configure("center", justify="center")
                tk_txt.tag_configure("ref_tag", font=("Arial", f_size + 2, "bold"), justify="center")
                tk_txt.tag_configure("bold_word", font=("Arial", f_size, "bold"), justify="center")
                
                tk_txt.tag_add("center", "1.0", "end")
                tk_txt.tag_add("ref_tag", "1.0", "1.end")
                
                # Bold the specific 4 clue words wherever they appear in the text
                for w in words:
                    for match in re.finditer(r'\b' + re.escape(w) + r'\b', full_text, re.IGNORECASE):
                        # Using standard Tkinter character indexing format (1.0+Xc)
                        tk_txt.tag_add("bold_word", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
            except Exception as e:
                print(f"Text formatting error skipped: {e}")
                
            textboxes_to_center.append((textbox, tk_txt))

        # --- VERTICAL CENTERING LOGIC ---
        # Force Tkinter to calculate layouts first so we can measure the exact text height
        self.update_idletasks()
        
        for textbox, tk_txt in textboxes_to_center:
            try:
                # bbox("end-1c") gets the layout bounding box of the very last character
                bbox = tk_txt.bbox("end-1c")
                if bbox:
                    # bbox[1] is the y-coord, bbox[3] is the height of the character
                    text_height = bbox[1] + bbox[3]
                    pad_y = max(0, (box_h - text_height) // 2)
                    tk_txt.configure(pady=pad_y)
            except Exception as e:
                print(f"Vertical centering skipped: {e}")
                
            # Disable interaction after configuring padding
            textbox.configure(state="disabled")

    # --- SCREEN 3: GAME OVER ---
    def end_game(self, win):
        self.clear_window()

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if win:
            msg = "Nice job! You solved the board!"
            color = "green"
        else:
            msg = "Game Over. Better luck next time!"
            color = "red"
            for ref in self.board_categories:
                if ref not in self.solved_categories:
                    self.solved_categories.append(ref)

        end_lbl = ctk.CTkLabel(self.main_scroll, text=msg, font=("Arial", 28, "bold"), text_color=color)
        end_lbl.pack(pady=20)
        
        self.solved_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent", height=1)
        self.solved_frame.pack(pady=10)
        self.render_solved_categories()

        play_again_btn = ctk.CTkButton(self.main_scroll, text="Play Again", font=("Arial", 16, "bold"), 
                                       command=self.show_setup_screen, height=50, width=200)
        play_again_btn.pack(pady=30)

if __name__ == "__main__":
    app = BibleConnectionsApp()
    app.mainloop()