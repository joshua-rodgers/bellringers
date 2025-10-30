# **Project Brief: Tiny CS Bell Ringers**

## **1\. Core Philosophy**

* **Tool, not a Task:** The app should feel like a fun, powerful assistant, not another chore.  
* **Speed to Value:** A teacher should be able to get a high-quality, printable bell ringer within 30 seconds of landing on the page.  
* **Community, Not Competition:** The social features should feel like a shared staff room, not a leaderboard.

## **2\. Unique Mechanic: The "Bell Ringer Mixer" (Generator)**

Instead of a boring form with dropdowns, the generation UI should be more tactile and playful.

Imagine three "slots" or "knobs" that the user can tune.

1. **The Topic:** (Variables, Loops, Conditionals, Data Structures, AI Ethics, Cybersecurity, Binary)  
2. **The Format:** (Debug the Code, Predict the Output, Vocabulary Match, Code Tracing, Short Answer, Pseudocode Challenge)  
3. **The Constraint:** (5-Minute Timer, Partner Discussion, No Computers, Analogy Time, Introductory, AP-Level Review)

**The "Addictive" Mechanic: Lock & Spin**

This is the key. The user doesn't just fill out a form; they *discover* a combination.

* The user can **"lock"** any slot they care about. For example, they lock Topic: Loops.  
* They then hit a big, friendly "Generate\!" button.  
* The other two "unlocked" slots (Format and Constraint) spin like a slot machine and land on a random-but-curated combination.  
* The app then generates a bell ringer for: **"A 'Loops' question, as a 'Debug the Code' challenge, for an 'AP-Level Review'."**

**Why this is unique and addictive:**

* **Variable Reward:** The user doesn't know exactly what they'll get, which is a core principle of addictive design.  
* **User Control:** The "lock" feature gives them just enough control to feel like they are *tuning* the results, not just rolling the dice.  
* **Discovery:** It encourages exploration. "I wonder what a 'Cybersecurity' question for a 'Partner Discussion' looks like?"

## **3\. Unique Mechanic: "No-Sign-Up" Accounts & Social**

You can absolutely do this without a traditional sign-up, which is a huge win.

**The "Anonymous Handle" Mechanic**

1. **First Visit:** When a user first visits, the site generates a unique, friendly, anonymous handle for them (e.g., electric-python-256 or clever-query-88).  
2. **Store It:** This handle is stored *only* in their browser's localStorage.  
3. **No PII:** You store no email, no name, nothing. The user is just electric-python-256.  
4. **Database:** You'll use a database (like Firestore or even a simple SQLite DB on PythonAnywhere for an MVP) to link this handle to their saved content.  
5. **The "Hook":** The user is immediately "logged in" without doing anything. They can start saving and sharing instantly. (You can add an optional "Claim this Account" button later that links it to an email, but *don't* do this for the MVP).

**Social Features ("My Binder" & "The Feed")**

When a user generates a bell ringer they love, they have two options:

1. **Save to "My Binder" (Private):** This saves the generation to your database, linked *only* to their anonymous handle. This is their private collection.  
2. **Publish to "The Feed" (Public):** This flags the generation as public.

This creates two simple, powerful destinations:

* **"My Binder" Page:** A gallery of just their saved items.  
* **"The Feed" Page:** A gallery of all user-published items, browsable by everyone. This is your community hub.

## **4\. Unique Mechanic: Gamification & Quality Control**

Your gamification and quality control can be the *same mechanic*.

**The "Game" is Impact, Not Points**

Don't use points or badges. Teachers are too busy for that. The "game" is professional validation and making an impact.

1. **"Add to Binder" as the "Like" Button:** When a user (clever-query-88) is browsing "The Feed" and sees a great bell ringer published by electric-python-256, they don't "like" it. They **"Add to My Binder"**.  
2. **The "Used By" Metric:** On "The Feed," every public bell ringer shows one simple stat: **"Used by 15 Teachers."**  
3. **The Reward:** The "addiction" for creators is logging in and seeing their published bell ringer has been "Used by 30 Teachers." This is an incredibly powerful, intrinsic motivator.  
4. **The Quality Control:** This *is* your quality filter\! You can now have a "Trending" or "Most Used" sort on "The Feed." Bad generations get ignored and disappear. High-quality generations rise to the top, curated by the community.

## **5\. The MVP Feature Set (Flask Blueprint)**

This plan is simple enough for an MVP.

1. **Blueprint 1: generator.py**  
   * /: The main page with the "Lock & Spin" UI.  
   * /api/generate: The backend API that takes the locked/unlocked slots and returns a generated bell ringer (using your generation logic, maybe a combination of templates and an LLM).  
2. **Blueprint 2: document.py**  
   * /print/\<generation\_id\>: This is the **critical** "Print-Optimized" page. It's a "chrome-less" view (no site UI, just the document) with clean, large-font formatting. A "Print this" button would just run window.print().  
3. **Blueprint 3: community.py**  
   * /binder: ("My Binder") Shows a gallery of generations where owner\_handle \== current\_user\_handle.  
   * /feed: ("The Feed") Shows a gallery of all generations where is\_public \== true. Allows sorting by created\_at (New) and binder\_count (Most Used).  
   * /api/save: Saves a generation to the DB with owner\_handle and is\_public=false.  
   * /api/publish: Saves a generation to the DB with owner\_handle and is\_public=true.  
   * /api/add\_to\_binder: Copies a public generation and saves it as a private one for the current user. Increments the binder\_count on the original.