# a2-2

#Part 1
We implemented minimax initially, it gave us results within few seconds but didnot consider the chance nodes.
We then introduced expectiminimax algorithm with a basic heuristic. It takes time but considers all the chance nodes.
We played the game and understood its working first. Then implemented the algorithm followed by deciding the heuristic function for the same.
Problems faced:
The heuristic makes a significant amount of difference. We implemented the algorithm successfully, but the heuristic can always get better.
Since the children expand exponentially, it was difficult to visualise the game with all the chance nodes.

Nov. 11, 2019
We implemented alpha beta pruning to our algorithm and edited the heuristic to make it work better. 



#Part 2

For the Bayes implementation, we have simply considered that every pixel that has the maxmimum edge strength in the column will be the line representing the ridge.

For the Viterbi implementation, we have normalized the emission probabilities as the pixel strength divided by the sum of pixel strengths in the particular column and then calculated the transition probabilities based on the closeness of the previous pixel with highest probability.

For the human implementation, we have initialized the probability of the input pixel as 1. Also, rather than calculating the transition probabilities in one direction we are traversing in left and right direction from the input column in our viterbi algorithm.

Difficulties Faced -
One of the most prominent challanges was coming up with an appropriate formula to calculate transition probabilities. After trying on several combinations and normalizing the probabilities we decided on the final one which gave better results in comparision for most of the files. We assume that the neighbouring pixels in each column would have uniform distribution.
