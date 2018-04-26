import math
import smtplib
from collections import Counter
"""Stable Roommate Algorithm
Alonda Robichaud, Rachel Cooke, Annika Miller, Matty Kulke
CSC 220 Final Project"""

#dictionary with the person as the key and a list of their information as the value 
people = {}
#indexed list of names of all respondents
respondents = []
#stores names and survey answer
dictionary = {}
#person who is assigned a single
single = ""
#index in the list of their information(list that is the value in the dictionary) of whether the person is free
isFreeInd = 0
#index in the list of their information of their preference list
preferencesInd = 1
#index in the list of their information of the person they're matched with
matchInd = 2
#index in the list of their information of the person they proposed to and accept
proposedInd = 3
#index in the list of their information of the person they accepted a proposal from 
acceptInd = 4
#index in the list of their information of the count that keeps track of how many people rejected them
rejectInd = 5
#index in the list of their information of the person they requested as a roommate, if any
requestInd = 6

#method to read csv and put relevant information into necessary data structures
def extractInfo(reader):
    #make sure only pulling cells that have info in them
    result = [[item for item in row if item != ''] for row in reader]
    result = [x for x in result if x]
    #iterate through rows in file and sort information from the rows
    for row in result:
        if row != result[0]: #the first row is just headers
            name = row[2] 
            respondents.append(name) #add name to list of respondents
            responses = [row[i] for i in range(3,len(row)-1, 2)] #person's responses go in one array
            weights = [row[i] for i in range(4, len(row)-1, 2)] #person's weights to responses go in another array
            info = [row[1], row[-1]] #save email and misc. info separately
            dictionary[name] = [responses, weights, info] #add a dictionary entry with name as key and value as array of arrays with answers, weights, and info

#method to compute each person's list of compatible roommates    
def computeCompatibility():
    for person in respondents: #deal with one person at a time
        array1 = dictionary[person] #person's responses and weights
        sums = Counter({}) #list of people and their compatibility sum in relation to the primary person
        for respondent in respondents: # compare every other person to the primary person
            if respondent != person:
                array2 = dictionary[respondent] #potential roommate's responses
                sums[respondent] = 0 #compatibility sum starts at 0
                for i in range(0, len(array2[0])): #iterate through every response 
                    own_answer = array1[0][i] #primary person's response to the question
                    response = array2[0][i] #potential roommate's response to same question
                    if own_answer != array1[0][-1]: #if the response is not the last one in the array
                        if own_answer == response: #if person's answer matches potential roommate's, add to their compatibility sum
                            sums[respondent] += int(array1[1][i]) #add the number of importance that the person assigned the question
                    else: #if response is last one in array, which is the specific roommate request question
                        if own_answer == respondent: #if the primary person requested the responsent
                            sums[respondent] += 900 #add to their compatibility sum so that they will be the first choice
        compatibilitylist = [key[0] for key in sums.most_common()] #create an ordered list of potential roommates in order of compatibility sums
        dictlist = [True, compatibilitylist, "","","", 0,""] #list of information needed to find roommate matches
        people[person] = dictlist #add dictlist to people dict with person as key

def who_is_better(person, roomie1, roomie2):
    '''decides which proposer is a better roomate option'''
    preferences = people[person][preferencesInd]
    for p in preferences:
        if roomie1 == p:
            return roomie1
        if roomie2 == p:
            return roomie2

def match(roomie1, roomie2):
    '''match 2 people as roommates'''
    people[roomie1][matchInd] = roomie2
    people[roomie2][matchInd] = roomie1
    people[roomie1][isFreeInd] = False
    people[roomie2][isFreeInd] = False

def least_desired():
    '''find the least desired person in everyone's list and give them a single'''
    nPreferences = len(people)-1
    lastRanked = {}
    for p in people:
        lastPerson = people[p][preferencesInd][-1]
        if people[lastPerson][isFreeInd]:
            if lastPerson not in lastRanked:
                lastRanked[lastPerson] = 1
            else:
                lastRanked[lastPerson] += 1
    leastDesired = next(iter(lastRanked))
    for p in lastRanked.keys():
        if lastRanked[p] > lastRanked[leastDesired]:
            leastDesired = p
    return leastDesired

def single(person):
    '''assgins the person in the parameter a single'''
    people[person][isFreeInd] = False
    people[person][matchInd] = person
    people[person][preferencesInd][0] = person
    people[person][acceptInd] = person
    people[person][proposedInd] = person

def propose(proposer, index):
    '''propose to the best option on their list who would accept'''
    #propose to the first person
    proposeTo = people[proposer][preferencesInd][index]
    if people[proposeTo][isFreeInd] and not people[proposeTo][acceptInd]:
        #if havent accepted any proposals, accept
        accept(proposeTo, proposer)
    elif people[proposeTo][acceptInd] and people[proposeTo][isFreeInd]:
        #if accepted a proposal already, check if this one is better
        if is_better(proposeTo, proposer):
            #if better, accept this proposal over the old one
            new_tie(proposeTo, proposer)
        else:
            #if not better, propose to person at next index
            propose(proposer, index+1)
    else:
        propose(proposer, index+1)

def new_tie(proposeTo, proposer):
    '''removes link with old potential pair and finds a new pair for the person dumped'''
    oldProposer = people[proposeTo][acceptInd]
    break_tie(proposeTo, oldProposer)
    accept(proposeTo,proposer)
    #find new pair for old proposer, starting at next index(kept track by number of rejections
    propose(oldProposer, people[oldProposer][rejectInd])
                    
def break_tie(acceptor, proposer):
    '''breaks the tie between 2 people'''
    people[proposer][proposedInd] = ""
    people[proposer][rejectInd] += 1
    people[acceptor][acceptInd] = ""

def is_better(person, potentialMatch):
    '''check if the potentialMatch is the better option'''
    currentMatch = people[person][acceptInd]
    if potentialMatch == who_is_better(person, potentialMatch, currentMatch):
        return True
    else:
        return False
            
def accept(acceptor, proposer):
    '''accept proposal'''
    people[acceptor][acceptInd] = proposer
    people[proposer][proposedInd] = acceptor

def remove(person1, person2):
    '''remove mention of person1 from person2's list and vice versa'''
    if person2 in people[person1][preferencesInd]:
        people[person1][preferencesInd].remove(person2)
    elif person1 in people[person2][preferencesInd]:
        people[person2][preferencesInd].remove(person1)

def clear(person):
    '''remove person from everyone's list'''
    for p in people[person][preferencesInd]:
        remove(p,person)

def pref_cycle(person,lst):
    '''check for a preference cycle in the ranking to help with match elimination'''
    if people[person][preferencesInd]:
        #pick the person's last choice because want to get rid of them
        last = people[person][preferencesInd][-1]
        if last in lst:
            lst.append(last)
            #once cycle is found, remove "diagonal pairs" as possibilities
            for i in range(1, len(lst)-1,2):
                remove(lst[i],lst[i+1])
        else:
            lst.append(last)
            pref_cycle(last,lst)

def clear_pref_list():
    '''after all proposals have been made, clear preference list of anyone ranked lower
        than person currently accepted since you can do worse'''
    for person in people:
        preferences = people[person][preferencesInd]
        accepted = people[person][acceptInd]
        proposed = people[person][proposedInd]
        a = people[person][preferencesInd].index(accepted)+1
        people[person][preferencesInd]=preferences[:a]

def mirror():
    '''do a mirror removal'''
    for p in people:
        for person in people:
            if p not in people[person][preferencesInd] and person in people[p][preferencesInd]:
                people[p][preferencesInd].remove(person)

def match_request():
    '''match people who have explicitly requested each other'''
    nPairs = 0
    for p in people:
        request = people[p][requestInd]
        if request:
            if people[request][requestInd]== p and people[p][isFreeInd]:
                match(p, request)
                nPairs += 1
                people[p][acceptInd] = request
                people[p][proposedInd] = request
                people[request][proposedInd] = p
                people[request][acceptInd] = p
    return nPairs

def send_mail(seekerName, seekerEmail, roommateName, roommateEmail, message):
    '''This method sends an email to two people who are paired as roommates,
    including a message they have for their roommate'''

    content = "Hello "+seekerName+",\n \nYou have been matched with "+roommateName+\
              " ("+roommateEmail+")"+" for the following academic year of 2018-2019.\n"+roommateName+\
              ' has a message that they would like to share with you, which you may find below. We have also provided you with their email address, so go ahead and get to know each other!\n\n"'\
              +message+'"\n\nBest, \nSmith University <3'
    email = "SmithUniversityResLife@gmail.com"
    password = "sophiasmith"
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    mail.sendmail(email, seekerEmail, content)
    mail.close()

def send_single(person, personEmail):
    '''Sends an email to the person who got a single'''
    content = "Hello "+person+",\n \nYou have been assign a single for the following academic year of 2018-2019.\n\nBest,\nSmith University"
    email = "SmithUniversityResLife@gmail.com"
    password = "sophiasmith"
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    mail.sendmail(email, personEmail, content)
    mail.close()

def main():
    import csv
    file = open('OKRoomie.csv',"r") #open and read the csv file
    reader = csv.reader(file)
    extractInfo(reader) #call method that reads in and stores info from csv
    file.close()
    computeCompatibility() #create sums based on compatibility
   #count to keep track of matches
    count = 0
    #first person in list
    index = next(iter(people))
    #number of people
    nPairs = math.floor(len(people)/2)
    #match people who requested each other
    count += match_request()
    #if odd find least desired and give them a single
    if len(people)%2 != 0:
        solo = least_desired()
        single(solo)
    #propose
    for p in people:
        if people[p][isFreeInd]:
            propose(p,0)
    #clear preference list after accepted index
    clear_pref_list()
    #do removal to mirror the one above
    mirror()
    while count != nPairs:
        for p in people:
            #if only one in preference, match them
            if len(people[p][preferencesInd]) == 1 and people[p][isFreeInd]:
                match(p,people[p][preferencesInd][0])
                clear(people[p][preferencesInd][0])
                clear(p)
                count +=1

            #if there are more people find a preference cycle to eliminate pairs
            elif len(people[p][preferencesInd]) > 1:
                pref_cycle(p,[p])               

def result():
    print("Stable matched roommates:\n")
    for p in people:
        roommate1 = p
        roommate2 = people[p][matchInd]

        print("{} <---> {}".format(roommate1, roommate2))
        if roommate1 != roommate2:
            send_mail(roommate1, dictionary[roommate1][2][0], roommate2, dictionary[roommate2][2][0], dictionary[roommate1][2][1])
        else:
            send_single(roommate1, dictionary[roommate1][2][0])
main()
result()

            
            
    
