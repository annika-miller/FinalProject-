# FinalProject-
Annika Miller, Alonda Robichaud, Rachel Cooke, Matty Kulke
OKRoomie generates a list of ideal roommate matches given a CSV of survey responses from a roommate matching survey. In order to run, the CSV must be specified in the main method. The survey is a google form that automatically updates a CSV with new responses. Currently, the program does not recognize certain accented letters in names. The program can be run successfully in terminal (the accented letter will just be represented as an odd string of characters), but cannot run in idle.

The program generates ideal matches taking into account if potential roommates have matching responses to survey questions, and how each respondent has ranked the importance of their roommates reponses for a given question. Once a ranked list of roommates is developed for each person, OKRoomie implement Irving’s algorithm which efficiently ensures that each person has the best possible match (there are no two people that prefer each other the most and are not matched). 

The code is somewhat flexible for changes in the survey, with a few exceptions. The index of the participant's name must be the  first question, the “what do you want your roommate to know about you?” short answer question must be second to last, and the specific roommate request short answer must be last. The number of survey questions can be changed, but the weighting of reponses works such that the question ranking scale must be every other question. If questions are added, they will appear on the updated CSV as the last columns, even if they were inserted into the middle of the survey. The CSV columns will have to be manually shifted in this case. 


Contents in github repo: OKroomie file containing code, CSV of survey responses, Link to survey 

Link to survey: https://docs.google.com/forms/d/e/1FAIpQLSe0B7P87diTNIqmW0yDcnvb-PFuXtfX8DIpQ3WY_r55SZ9rag/viewform

Right now, the part where we consider the specific roommate requests isn't working. We're not sure what the problem is, but it just seems to ignore the roommate request entry. Although when we tested it with a different file it worked but it doesn't work everytime. It seems to not work with certain people.
