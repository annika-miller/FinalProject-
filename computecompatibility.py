#Final Project
#Annika Miller, Matty Kulke, Alonda Robichaud, Rachel Cooke
#April 24 2018
#flask

from collections import Counter

dictionary = {} #stores names and survey answers
respondents = [] #indexed list of names
people = {} #stores sorted compatibility

#method to read csv and put relevant information into necessary data structures
def extractInfo(reader):
    
    #print(reader)
    result = [[item for item in row if item != ''] for row in reader]
    result = [x for x in result if x]
    #for row in result:
        #print(row)
    print(" ")
    for row in result:
        if row != result[0]:
            name = row[2]
            respondents.append(name)
            responses = [row[i] for i in range(3,len(row)-1, 2)] #responses go in one array
            weights = [row[i] for i in range(4, len(row)-1, 2)] #weights to responses go in another array
            info = [row[1], row[-1]] #save email and misc. info separately
            #print(info)
            #print(email)
            #self = [row[i] for i in range(1,int((len(row)-1)/2 + 1, 2))] #self-responses go in one array
            #other = [row[i] for i in range(int((len(row)-1)/2 + 1), len(row),2)] #others responses go in other array
            dictionary[name] = [responses, weights, info] #add a dictionary entry with name as key and value as array of arrays with answers, weights, and email



    
#method to compute each person's list of compatible roommates    
def computeCompatibility():
    for person in respondents:
        array1 = dictionary[person] #person's responses and weights
        sums = Counter({})
        for respondent in respondents:
            if respondent != person:
                array2 = dictionary[respondent] #potential roommate's responses
                sums[respondent] = 0
                for i in range(0, len(array2[0])):
                    own_answer = array1[0][i]
                    response = array2[0][i]
                    if own_answer != array1[0][-1]:
                        if own_answer == response: #if person's answer matches potential roommate's, add to their compatibility sum
                            sums[respondent] += int(array1[1][i]) #add the number of importance that the person assigned the question
                    else:
                        if own_answer == respondent:
                            sums[respondent] += 900
        compatibilitylist = [key[0] for key in sums.most_common()] #createan ordered list of potential roommates in order of compatibility sums
        #compatibledict = {"name":person, "is_free":True, "preferences":compatibilitylist, "matched_with": "", "proposed_to":[], "email":array1[2]}
        dictlist = [True, compatibilitylist, "", []]
        people[person] = dictlist


        
def main():
    import csv
    file = open('shortVersion.csv',"r")
    reader = csv.reader(file)
    #print(file)
    extractInfo(reader) #call method that reads in and stores info from csv
    file.close()
    #create sums based on compatibility
    computeCompatibility()
    print(people)
            
main()
    
