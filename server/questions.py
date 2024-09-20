import random

def get_regular_questions():
    return [
        {
            "question": "In 'Akira', what is the name of the biker gang Kaneda leads?",
            "answers": ["The Capsules", "The Clowns", "The Jokers", "The Dragons"],
            "correct_answer": "The Capsules",
            "time_limit": 15
        },
        {
            "question": "Who is the main protagonist in the anime 'Neon Genesis Evangelion'?",
            "answers": ["Shinji Ikari", "Gendo Ikari", "Asuka Langley", "Rei Ayanami"],
            "correct_answer": "Shinji Ikari",
            "time_limit": 15
        },
        {
            "question": "Which comic book character famously said 'With great power comes great responsibility'?",
            "answers": ["Spider-Man", "Superman", "Batman", "The Flash"],
            "correct_answer": "Spider-Man",
            "time_limit": 15
        },
        {
            "question": "In 'Fullmetal Alchemist', what is the law that governs alchemy?",
            "answers": ["Equivalent Exchange", "The Philosopher's Code", "Conservation of Energy", "Alchemy's Law"],
            "correct_answer": "Equivalent Exchange",
            "time_limit": 15
        },
        {
            "question": "Which comic book villain was the archenemy of Batman in 'The Killing Joke'?",
            "answers": ["The Joker", "Two-Face", "Riddler", "Bane"],
            "correct_answer": "The Joker",
            "time_limit": 15
        }
    ]

def get_math_questions():
    math_questions = []
    for _ in range(5):  
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        math_questions.append({
            "question": f"In the anime 'Death Note', Light Yagami plans for {num1} killings each day. How many total people are killed in {num2} days?",
            "answers": [str(num1 * num2), str(num1 * num2 - 2), str(num1 * num2 + 3), str(num1 * num2 + 5)],
            "correct_answer": str(num1 * num2),
            "time_limit": 15
        })
    return math_questions

def get_science_questions():
    return [
        {
            "question": "In 'Akira', what is the psychic power that Tetsuo develops?",
            "answers": ["Telekinesis", "Mind Reading", "Invisibility", "Telepathy"],
            "correct_answer": "Telekinesis",
            "time_limit": 15
        },
        {
            "question": "In the anime 'Steins;Gate', what scientific concept is central to the story?",
            "answers": ["Time Travel", "Teleportation", "Cryogenics", "Cloning"],
            "correct_answer": "Time Travel",
            "time_limit": 15
        }
    ]

def get_history_questions():
    return [
        {
            "question": "Who created the character Superman?",
            "answers": ["Jerry Siegel and Joe Shuster", "Stan Lee", "Jack Kirby", "Bob Kane"],
            "correct_answer": "Jerry Siegel and Joe Shuster",
            "time_limit": 15
        },
        {
            "question": "Which year was the first Batman comic published?",
            "answers": ["1939", "1942", "1950", "1960"],
            "correct_answer": "1939",
            "time_limit": 15
        }
    ]

def get_sports_questions():
    return [
        {
            "question": "In 'Dragon Ball Z', who won the World Martial Arts Tournament at the end of the Buu Saga?",
            "answers": ["Mr. Satan", "Goku", "Vegeta", "Gohan"],
            "correct_answer": "Mr. Satan",
            "time_limit": 15
        },
        {
            "question": "In 'Yu Yu Hakusho', who wins the final fight of the Dark Tournament?",
            "answers": ["Yusuke Urameshi", "Hiei", "Kurama", "Toguro"],
            "correct_answer": "Yusuke Urameshi",
            "time_limit": 15
        }
    ]

def get_movies_questions():
    return [
        {
            "question": "In the movie 'Akira', who is the leader of the government project that turns children into powerful psychics?",
            "answers": ["Colonel Shikishima", "Doctor Onishi", "Masaru", "Lady Miyako"],
            "correct_answer": "Colonel Shikishima",
            "time_limit": 15
        },
        {
            "question": "In 'Blade Runner', what are the androids known as?",
            "answers": ["Replicants", "Synths", "Cyborgs", "Bots"],
            "correct_answer": "Replicants",
            "time_limit": 15
        }
    ]

def get_geography_questions():
    return [
        {
            "question": "In 'Attack on Titan', which wall is closest to the Titans?",
            "answers": ["Wall Maria", "Wall Rose", "Wall Sina", "Wall Rose and Maria"],
            "correct_answer": "Wall Maria",
            "time_limit": 15
        },
        {
            "question": "In 'One Piece', what is the name of the Grand Line’s entrance?",
            "answers": ["Reverse Mountain", "Fishman Island", "Marineford", "Enies Lobby"],
            "correct_answer": "Reverse Mountain",
            "time_limit": 15
        }
    ]

def get_horror_literature_questions():
    return [
        {
            "question": "Who wrote 'Dracula'?",
            "answers": ["Bram Stoker", "Mary Shelley", "H.P. Lovecraft", "Edgar Allan Poe"],
            "correct_answer": "Bram Stoker",
            "time_limit": 15
        },
        {
            "question": "In 'Frankenstein', who is Frankenstein’s monster’s first victim?",
            "answers": ["William Frankenstein", "Elizabeth Lavenza", "Henry Clerval", "Alphonse Frankenstein"],
            "correct_answer": "William Frankenstein",
            "time_limit": 15
        },
        {
            "question": "Which classic horror story is set in the fictional town of Innsmouth?",
            "answers": ["The Shadow Over Innsmouth", "The Call of Cthulhu", "At the Mountains of Madness", "The Dunwich Horror"],
            "correct_answer": "The Shadow Over Innsmouth",
            "time_limit": 15
        }
    ]
