#Final Project
#Annika Miller, Matty Kulke, Alonda Robichaud, Rachel Cooke
#April 24 2018
#flask

#Counter will allow us to order people by their associated Compatibility Sums
from collections import Counter

dictionary = {} #stores names and survey answers
respondents = [] #indexed list of names of all respondents
people = {} #stores sorted compatibility with all necessary info to then find final matches

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
        dictlist = [True, compatibilitylist, "","","", []] #list of information needed to find roommate matches
        people[person] = dictlist #add dictlist to people dict with person as key

        
def main():
    import csv
    file = open('shortVersion.csv',"r") #open and read the csv file
    reader = csv.reader(file)
    extractInfo(reader) #call method that reads in and stores info from csv
    file.close()
    computeCompatibility() #create sums based on compatibility
    print(people)
            
main()
    
