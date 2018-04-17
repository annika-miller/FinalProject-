#Final Project
#Annika Miller, Matty Kulke, Alonda Robichaud, Rachel Cooke
#April 24 2018
#flask

from collections import Counter

dictionary = {} #stores names and survey answers
respondents = [] #indexed list of names
matrix = {} #stores sorted compatibility

def main():
    import csv
    file = open('RoommateDataTest.csv',"r")
    #print(file)
    reader = csv.reader(file)
    #print(reader)
    result = [[item for item in row if item != ''] for row in reader]
    result = [x for x in result if x]
    #for row in result:
        #print(row)
    print(" ")
    for row in result:
        if row != result[0]:
            respondents.append(row[0])
            responses = [row[i] for i in range(1,len(row), 2)] #responses go in one array
            weights = [row[i] for i in range(2, len(row), 2)] #weights to responses go in another array
            #self = [row[i] for i in range(1,int((len(row)-1)/2 + 1, 2))] #self-responses go in one array
            #other = [row[i] for i in range(int((len(row)-1)/2 + 1), len(row),2)] #others responses go in other array
            dictionary[row[0]] = [responses, weights] #add a dictionary entry with name as key and value as double array with self, others answers
    file.close()

    #create sums based on compatibility
    for person in respondents:
        array1 = dictionary[person]
        sums = Counter({})
        for respondent in respondents:
            if respondent != person:
                array2 = dictionary[respondent]
                sums[respondent] = 0
                for i in range(0, len(array1[0])):
                    own_answer = array1[0][i]
                    response = array2[0][i]
                    if own_answer == response:
                        sums[respondent] += int(array1[1][i])
        compatibilitylist = [key[0] for key in sums.most_common()]
        matrix[person] = compatibilitylist
    print(matrix)
            
main()
    
