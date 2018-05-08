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
is_free_ind = 0
#index in the list of their information of their preference list
pref_ind = 1
#index in the list of their information of the person they're matched with
match_ind = 2
#index in the list of their information of the person they proposed to and accept
propose_ind = 3
#index in the list of their information of the person they accepted a proposal from 
accept_in = 4
#index in the list of their information of the count that keeps track of how many people rejected them
reject_ind = 5
#index in the list of their information of the person they requested as a roommate, if any
request_ind = 6
#index in the list of their name before splitting
name_ind = 7

'''method to read csv and put relevant information into necessary data structures'''
def extract_info(reader):
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

'''method to compute each person's list of compatible roommates'''
def compute_compatibility():
    for person in respondents: #deal with one person at a time
        request = "" #everyone starts out assuming they don't have a specific roommate request
        array1 = dictionary[person] #person's responses and weights
        sums = Counter({}) #list of people and their compatibility sum in relation to the primary person
        stripped_name = ''.join(person.split()).lower() #split name and lower case it for comparison purposes
        for respondent in respondents: # compare every other person to the primary person
            if respondent != person:
                array2 = dictionary[respondent] #potential roommate's responses
                sums[respondent] = 0 #compatibility sum starts at 0
                for i in range(0, len(array2[0])): #iterate through every response 
                    own_answer = array1[0][i] #primary person's response to the question
                    response = array2[0][i] #potential roommate's response to same question
                    if own_answer != array1[0][-1]:#if the response is not the last one in the array(not the request)
                        if own_answer == response: #if person's answer matches potential roommate's, add to their compatibility sum
                            sums[respondent] += int(array1[1][i]) #add the number of importance that the person assigned the question
                    else:#if response is last one in array, which is the specific roommate request question
                        if ''.join(own_answer.split()).lower() == ''.join(respondent.split()).lower():#if the primary person requested the responsent
                            sums[respondent] += 900 #add to their compatibility sum so that they will be the first choice
                            request = ''.join(respondent.split()).lower()
        compatibilitylist = [key[0] for key in sums.most_common()] #create an ordered list of potential roommates in order of compatibility sums
        for i in range(len(compatibilitylist)):
            compatibilitylist[i] = ''.join(compatibilitylist[i].split()).lower()
        dictlist = [True, compatibilitylist, "","","", 0,request,person] #list of information needed to find roommate matches
        people[stripped_name] = dictlist #add dictlist to people dict with person as key

def who_is_better(person, roomie1, roomie2):
    '''decides which proposer is a better roomate option'''
    preferences = people[person][pref_ind] #person's preferences
    for person in preferences:
        #the potential roommate that shows up first is more preferred
        if roomie1 == person: 
            return roomie1
        if roomie2 == person:
            return roomie2

def match(roomie1, roomie2):
    '''match 2 people as roommates'''
    #add them to each other's match and make them unavailable
    people[roomie1][match_ind] = roomie2
    people[roomie2][match_ind] = roomie1
    people[roomie1][is_free_ind] = False
    people[roomie2][is_free_ind] = False

def least_desired():
    '''find the least desired person in everyone's list and give them a single'''
    last_ranked = {} #dictionary of people ranked last, with the value being the number of times they are ranked last
    for person in people:
        last_person = people[person][pref_ind][-1]
        if people[last_person][is_free_ind]: #if the last person is free then add them to the dictionary or update their counter
            if last_person not in last_ranked:
                last_ranked[last_person] = 1
            else:
                last_ranked[last_person] += 1
    least_desired = next(iter(last_ranked)) #start with the first person in the dictionary
    for person in last_ranked.keys():
        if last_ranked[person] > last_ranked[least_desired]: #if the person's counter is larger, they are now least desired
            least_desired = person
    return least_desired #return least desired person

def single(person):
    '''assgins the person in the parameter a single'''
    #update all their information so they aren't available and can't be proposed to.
    people[person][is_free_ind] = False 
    people[person][match_ind] = person
    people[person][pref_ind][0] = person #prevent better proposals
    people[person][accept_in] = person
    people[person][propose_ind] = person

def propose(proposer, index):
    '''propose to the best option on their list who would accept'''
    #propose to the first person
    proposeTo = people[proposer][pref_ind][index]
    if people[proposeTo][is_free_ind] and not people[proposeTo][accept_in]:
        #if havent accepted any proposals, accept
        accept(proposeTo, proposer)
    elif people[proposeTo][accept_in] and people[proposeTo][is_free_ind]:
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
    oldProposer = people[proposeTo][accept_in]
    break_tie(proposeTo, oldProposer) #break tie from old proposer and person proposed to
    accept(proposeTo,proposer) #accept proposal from new proposer
    #find new pair for old proposer, starting at next index(kept track by number of rejections)
    propose(oldProposer, people[oldProposer][reject_ind])
                    
def break_tie(acceptor, proposer):
    '''breaks the tie between 2 people'''
    #remove ties/connections between acceptor and proposer, update proposer's rejection count
    people[proposer][propose_ind] = ""
    people[proposer][reject_ind] += 1
    people[acceptor][accept_in] = ""

def is_better(person, potential_match):
    '''check if the potentialMatch is the better option'''
    current_match = people[person][accept_in]
    #if potential match is better return true, else false
    if potential_match == who_is_better(person, potential_match, current_match):
        return True
    else:
        return False
            
def accept(acceptor, proposer):
    '''accept proposal'''
    #update acceptance and proposal information for each person
    people[acceptor][accept_in] = proposer
    people[proposer][propose_ind] = acceptor

def remove(person1, person2):
    '''remove mention of person1 from person2's list and vice versa'''
    #remove people from each other's list if they are present
    if person2 in people[person1][pref_ind]:
        people[person1][pref_ind].remove(person2)
    elif person1 in people[person2][pref_ind]:
        people[person2][pref_ind].remove(person1)

def clear(person):
    '''remove person from everyone's list'''
    #remove person from everyone's list
    for p in people[person][pref_ind]:
        remove(p,person)

def pref_cycle(person,lst):
    '''check for a preference cycle in the ranking to help with match elimination'''
    if people[person][pref_ind]:
        #pick the person's last choice because we want to get rid of them
        last = people[person][pref_ind][-1]
        if last in lst: #if the last person is in the preference cycle list, remove the pairs present in the cycle
            lst.append(last)
            #once cycle is found, remove "diagonal pairs" as possibilities
            for i in range(1, len(lst)-1,2):
                remove(lst[i],lst[i+1])
        else: #add to preference cycle list until repetition is found
            lst.append(last)
            pref_cycle(last,lst)

def clear_pref_list():
    '''after all proposals have been made, clear preference list of anyone ranked lower
        than person currently accepted since you can do worse'''
    for person in people:
        preferences = people[person][pref_ind]
        accepted = people[person][accept_in]
        a = people[person][pref_ind].index(accepted)+1 #index where accepted person is in list
        people[person][pref_ind]=preferences[:a] #remove everyone past the person they accepted a proposal from

def mirror():
    '''do a mirror removal'''
    for p in people:
        for person in people:
            #if person is not in p's list but p is in person's, remove p from person's list and vice versa
            if p not in people[person][pref_ind] and person in people[p][pref_ind]:
                people[p][pref_ind].remove(person)

def match_request():
    '''match people who have explicitly requested each other'''
    n_pairs = 0
    for person in people:
        request = people[person][request_ind]
        #if people requested each other, match them
        if request: 
            if people[request][request_ind]== person and people[person][is_free_ind]: #avoid matching twice by checking if they're free
                match(person, request)
                n_pairs += 1
                people[person][accept_in] = request
                people[person][propose_ind] = request
                people[request][propose_ind] = person
                people[request][accept_in] = person
    return n_pairs #return number of pairs made

def send_mail(seeker_name, seeker_email, roommate_name, roommate_email, message):
    '''This method sends an email to two people who are paired as roommates,
    including a message they have for their roommate'''

    content = "Hello "+seeker_name+",\n \nYou have been matched with "+roommate_name+\
              " ("+roommate_email+")"+" for the following academic year of 2018-2019.\n"+roommate_name+\
              ' has a message that they would like to share with you, which you may find below. We have also provided you with their email address, so go ahead and get to know each other!\n\n"'\
              +message+'"\n\nBest, \nSmith University <3' #inserted message
    email = "SmithUniversityResLife@gmail.com"
    password = "sophiasmith"
    mail = smtplib.SMTP('smtp.gmail.com',587) #opens up smtp session on local machine
    mail.ehlo()
    mail.starttls()
    mail.login(email,password) #remote login to dummy account
    mail.sendmail(email, seeker_email, content)
    mail.close()

def send_single(person, person_email):
    '''Sends an email to the person who got a single'''
    content = "Hello "+person+",\n \nYou have been assign a single for the following academic year of 2018-2019.\n\nBest,\nSmith University"
    email = "SmithUniversityResLife@gmail.com"
    password = "sophiasmith"
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    mail.sendmail(email, person_email, content)
    mail.close()

def main():
    import csv
    file = open('OKRoomie.csv',"r") #open and read the csv file
    reader = csv.reader(file)
    extract_info(reader) #call method that reads in and stores info from csv
    file.close()
    compute_compatibility() #create sums based on compatibility
    count = 0 #count to keep track of matches
    index = next(iter(people))  #first person in list
    n_pairs = math.floor(len(people)/2)  #number of pairs
    count += match_request() #match people who requested each other and update count
    #if odd find least desired and give them a single
    if len(people)%2 != 0:
        solo = least_desired()
        single(solo)
    #propose
    for person in people:
        if people[person][is_free_ind]:
            propose(person,0)
    clear_pref_list() #clear preference list after accepted index
    mirror() #do removal to mirror the one above
    while count != n_pairs:
        for person in people:
            #if only one in preference, match them
            if len(people[person][pref_ind]) == 1 and people[person][is_free_ind]:
                match(person,people[person][pref_ind][0])
                clear(people[person][pref_ind][0])
                clear(person)
                count +=1

            #if there are more people find a preference cycle to eliminate pairs
            elif len(people[person][pref_ind]) > 1:
                pref_cycle(person,[person])               

def result():
    print("Stable matched roommates:\n")
    for person in people:
        roommate1 = people[person][name_ind]
        roommate2 = people[person][match_ind]
        roommate2 = people[roommate2][name_ind]

        print("{} <---> {}".format(roommate1, roommate2))
        #send an email notifying them of their roommate
        if roommate1 != roommate2:
            send_mail(roommate1, dictionary[roommate1][2][0], roommate2, dictionary[roommate2][2][0], dictionary[roommate2][2][1])
        #if they dont have a roommate, let them know they have a single
        else:
            send_single(roommate1, dictionary[roommate1][2][0])
main()
result()

