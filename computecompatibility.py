#Final Project
#Annika Miller, Matty Kulke, Alonda Robichaud, Rachel Cooke
#April 24 2018



def main():
    import csv
    file = open('fakelahoma.csv',"r")
    reader = csv.reader(file)
    file.close()
    for row in reader:
        print(row)

main()
    
