import random

def getLifeAdvice(type, seed=None) :
    '''
    Returns a randomized piece of life advice if the second given argument is life advice
    '''
    learning = [
        "Whatever you do, give it 100%",
        "Never stop learning",
        "Your thinking changes your life",
        "Be kind to people; treat people as you'd like to be treated",
        "Starting is the hardest part"
    ]

    detach = [
        "Forgive and let go",
        "You can't control others",
        "Find your own happy",
        "Don't react, respond",
        "Meditate on it"
    ]
    if seed is not None:
        random.seed(seed)

    if (type == "learning"):
        return random.choice(learning)

    elif (type == "detach"):
        return random.choice(detach)


def getCSFortune(question, debug, seed=None):
    '''
    Return CS fortune or debugging help
    '''
    if seed is not None:
        random.seed(seed)
    possibleErrors = [
        "You forgot a semicolon",
        "You forgot to close a bracket",
        "You misspelled a keyword",
        "Incorrect indentation",
        "Incorrect version",
        "There is no saving this one"
    ]
    var = random.random() * 10
    #print(var);
    if var >= 5:
        if debug:
            return random.choice(possibleErrors)
        else:
            days = int(random.random() * 100) + 1
            return "You are on the right track and will finish your assignment/project in " + str(days) + " days."
    else:
        return "You are screwed. Switch major. Go next."

def getInspiration(name):
    '''
    Returns inspirational quotes
    '''
    quotes = {
        "Lemony Snicket": [
            "Do the scary thing first, and get scared later.",
            "All cannot be lost when there is still so much being found.",
            "When things don\'t go right, go left.",
            "Sometimes the things you\'ve lost can be found again in unexpected places."
        ],
        "Amelia Earhart": [
            "The most difficult thing is the decision to act, the rest is merely tenacity."
        ],
        "Angela Bassett": [
            ("Don't settle for average. Bring your best to the moment. Then, whether it fails or succeeds, "
            "at least you know you gave all you had.")
        ],
        "Barbara Elaine Smith": [
            "I have stood on a mountain of no\'s for one yes."
        ],
        "Mary Anne Radmacher": [
            ("Courage doesn't always roar. Sometimes courage is a quiet voice at the end of the day saying, "
            "\"I will try again tomorrow.\"")
        ],
        "Maya Angelou": [
            ("Courage is the most important of all the virtues because without courage, "
            "you can't practice any other virtue consistently.")
        ],
        "Frederick Douglass": [
            "If there is no struggle, there is no progress."
        ]
    }

    if name in quotes.keys():
        quote = random.choice(quotes.get(name))
    elif name == "":
        someName = random.choice(list(quotes.keys()))
        quote = random.choice(quotes.get(someName))
    else:
        print("Sorry, we don\'t seem to have any quotes from anyone by that name yet!\n")
        quote = "NO SUCH AUTHOR"

    return quote


def funny(name):
    '''
    Returns happy/funny quotes
    '''
    quotes = {

        "Steven Wright": ["I wish the first word I ever said was the word quote, so right before I die I could say unquote."],

        "Issac Asimov": ["Though sleep is called our best friend, it is a friend who often keeps us waiting!"],

        "Leo Tolstoy": ["Happiness is an allegory, unhappiness a story."],

        "J.K Rowling": ["Happiness can be found even in the darkest of times; if only one remembers to turn on the light."],

        "Oscar Wilde": ["Some cause happiness wherever they go; others, whenever they go."],

        "Mark Twain": ["When your friends begin to flatter you on how young you look, it's a sure sign you're getting old."]
    }

    if name in quotes.keys():
        return random.choice(quotes.get(name))
    elif name == "":
        return random.choice(quotes.get(random.choice(list(quotes.keys()))))
    else:
        return "The author doesn't exist"
