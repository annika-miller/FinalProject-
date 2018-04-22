"""Stable Roommate Algorithm
Alonda Robichaud, Rachel Cooke, Annika Miller, Matty Kulke
CSC 220 Final Project"""

import math

people = [{'name': 'John', 'is_free': True, 'preferences': ['Amanda', 'Georgia', 'Nikki', 'Riley','Jack', 'Tim'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Amanda', 'is_free': True, 'preferences': ['Riley', 'Nikke', 'John', 'Georgia', 'Jack','Tim'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Georgia', 'is_free': True, 'preferences': ['Nikki', 'John', 'Amanda', 'Riley', 'Tim','Jack'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Nikki', 'is_free': True, 'preferences': ['Tim', 'Georgia', 'John', 'Amanda', 'Riley','Jack'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Tim', 'is_free': True, 'preferences': ['Nikki', 'Amanda', 'John', 'Riley', 'Georgia','Jack'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Jack', 'is_free': True, 'preferences': ['Nikki', 'Amanda', 'John', 'Tim', 'Riley', 'Georgia'], 'matched_with': '', 'proposed_to': []},
              {'name': 'Riley', 'is_free': True, 'preferences': ['Georgia', 'Amanda', 'John', 'Nikki', 'Tim','Jack'], 'matched_with': '', 'proposed_to': []},]
single = ""

def break_match(person):
    breaking_with = is_matched_with(person)
    for p in people:
        if p["name"]==person:
            if p["matched_with"] != "":
                p["matched_with"] = ""
                p["is_free"] = True

def is_matched_with(person):
    for p in people:
        if p["name"] == person:
            return p["matched_with"]

    return False

def is_matched(person):
    for p in people:
        if p["name"] == person:
            if p["matched_with"] != "":
                return True
    return False

def who_is_better(person, roomie1, roomie2):
    for p in people:
        if p["name"] == person:
            for x in range(0, len(person)):
                if roomie1 == p["preferences"][x]:
                    return roomie1
                if roomie2 == p["preferences"][x]:
                    return roomie2

def match(roomieA, roomieB):
    for p in people:
        if p["name"] == roomieA:
            p["matched_with"] = roomieB
            p["is_free"] = False
        if p["name"] == roomieB:
            p["matched_with"] = roomieA
            p["is_free"] = False

def get_name_from_ranking(person, rank):
    for p in people:
        if p["name"] == person:
            return p["preferences"][rank]

def least_desired():
    nPreferences = len(people[1]["preferences"])
    lastRanked = {}
    for p in people:
        lastPerson = p["preferences"][nPreferences-1]
        if lastPerson not in lastRanked:
            lastRanked[lastPerson] = 1
        else:
            lastRanked[lastPerson] += 1
    leastDesired = next(iter(lastRanked))
    for p in lastRanked.keys():
        if lastRanked[p] > lastRanked[leastDesired]:
            leastDesired = p
    return leastDesired
        

def main():
    if len(people)%2 != 0:
        single = least_desired()
        nPairs = (math.floor(len(people)/2)) +1
    else:
        math.floor(len(people)/2)
    while (True):
        nPreferences = len(people[1]["preferences"])
        count = 0
        for p in people:
            person = p["name"]
            if person == single:
                p["is_free"] = False
                p["matched_with"] = single
            if (p["is_free"] == False and len(p["proposed_to"]) != nPairs):
                count += 1
                if count == nPairs:
                    return
            for x in range(0, nPreferences):
                if not is_matched(person):
                    p["proposed_to"].append(x)

                    seeker = get_name_from_ranking(person, x)

                    if is_matched(seeker):
                        currentMatch = is_matched_with(seeker)

                        betterMatch = who_is_better(seeker, person, currentMatch)

                        match(betterMatch, seeker)

                        if betterMatch != currentMatch:
                            break_match(currentMatch)
                            
                    else:
                        match(person, seeker)


def result():
    print("Stable matched roommates:\n")
    for p in people:
        roommate1 = p["name"]
        roommate2 = p["matched_with"]

        print("{} <---> {}".format(roommate1, roommate2))

            
            
    
