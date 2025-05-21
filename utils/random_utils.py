# Utility functions for random generation, etc.
import random

def random_category():
    return random.choice([
        "fan", "hater", "silent", "random", "neutral", "humorous", "provocative", "roleplayer"
    ])

def random_name():
    return random.choice([
        "Alex", "Sam", "Chris", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Jamie", "Robin"
    ]) + str(random.randint(100, 999))

def random_gender():
    return random.choice(["Male", "Female", "Other"])
