# Protein Pow(d)er, minor Programming UvA, june 2022
#### By Fons van de Hare, Sunita Rijs and Lotte Notenboom

## Case Description
Proteins are large, complex strings of amino acids that play many important roles in all living organisms. They do most of the work in cells and are required for the structure, function, and regulation of the body’s tissues and organs. The amino acids are arranged in a certain way, 'folding' the protein. The way this folding is executed, is crucial for the correct functioning of the protein, making the protein 'stable' or low in energy. If a protein is folded incorrectly, it can cause malfunctions such as diseases.

Understanding how this folding comes about and attempting to recreate the folding proces, has been one of the most important topics studied in science and biology. Computational scientists have also been trying to recreate this proces using varying computer algorithms.

For our project we've studied this using The hydrophobic-polar protein folding model. This is a highly simplified model for examining protein folds in space. Even though this model abstracts away many of the details of protein folding, it is still an NP-hard problem on both 2D and 3D square lattices.
The amino acid types are limited to hydrophobic (H), polar (P) and Cystein (C). Interactions between H-amino's, C-amino's and between H- and C-amino's contribute to the stability of proteins. The goal is to fold the proteins in such a way that produces the lowest stability (or score) possible.

Below is a 2D-example of a protein folding of the protein 'HPPPPHHHPCHCCPH'. The '|' represents the line combining the amino acids in one long protein string. If amino's of type 'C' and 'H' are placed next to each other (one place apart, but NOT connected), it leads to a better stability. Each '*' represents generated points. H\*H = -1 point, C\*H = -1 point, C\*C = -5 points.

     P-P
     | |
     P H   H-C*H
     | *   | | |
     P-H-H C*C-P
         | |
         H-P

Limitations: amino acids each need their own place in the grid and the path the amino's follow must be self-avoiding.

Using the guidelines above, we've implemented nine different constructive and iterative algorithm, to try and find the best possible (lowest) scores for a selection of protein strings.

## Algorithms
### Constructive algorithms

#### Randomize
This algorithm generates a 3D-folded self-avoiding protein by choosing a random move for each amino acid. There are six move options, corresponding with the directions within a 3D-grid. The amino acids are placed on the grid one at a time, starting at the beginning of the protein-string. For each amino, a random move is chosen from the list of possible moves. The coordinates of the amino acid being placed on the grid, are determined by adding a move eg. (1, 0, 0) to the coordinates of the previous amino acid eg. (2, 0, 1), thus placing the new amino acid at (3, 0, 1) on the grid. Next, these coordinates are checked against a list with coordinates currently occupied by amino acids, to prevent overlap of aminos. If the coordinates are already occupied, a new random move is chosen until this results in a free spot. If a free spot is found, the coordinates are assigned to the protein model and the algorithm moves on to the next amino acid.

#### Greedy
This algorithm bases it's moves on what move gets the highest score at that time. It's a depth-first approach without look-ahead.

#### Depth First
This algorithm checks every possible way a protein can be folded. This works as follows: there are five (three in 2D) possible options to place the next amino acid. The depth-first algorithm chooses a space to put the amino acid and then moves on to place the next amino acid. This depth first way of searching is created because the algorithm uses a stack, so the last conformation added, is the first to get re-evaluated at the next step. The algorithm keeps running until all possible conformations have been placed at the grid, thus covering the entire state-space. The running-time of this algorithm increases exponentially with the length of the protein.  

#### Breadth First
This algorithm inherites a lot of functions from the depth first algorithm and also goes through the entire state-space. Instead of placing one amino and then moving on to the next in the chain (depth-first), this algorithm places an amino acid on the grid and then creates a new partial conformation that places the same amino on another spot in the grid. So after two aminos are placed on the grid, it will create all new possible states  from that partial conformation with the third amino. After all possible conformations from the third are created, it moves on to the fourth and so on. The running-time of this algorithm also increases exponentially with the length of the protein.  

#### Beam Breadth
This algorithm is based on a breadth first algorithm. It uses a 'beam' to keep a steady number of states that are evaluated to build further upon. This prevents branching and the exponential increase in running time with longer strings. So if a beam of 30 is chosen, ONLY the thirty conformations with the best scores are being kept, at each stage of the algorithm. The other states are discarded. This results in a running-time that is lower than the branch and bound algorithm, while resulting in better scores. Because our research showed that not even all states with a score equal to the highest need to be evaluated to reach the best score in the end, conformations with a score equal to best have a 50 percent chance of being kept. Using a bigger number for beam_size results in a longer running-time, but also increases the chance of reaching the best score, because more states are evaluated.

#### Branch And Bound
This algorithm inherites functionalties from the BeamBreadth algorithm. It uses a different pruning strategy than the beam breadth algorithm. It compares scores of partial conformations that have the same length. If a score is worse than average, it has a very low chance of being kept. If the score is between average and the best score, this chance is slightly higher. Conformations with the best score have a fifty percent chance of being kept. Because this strategy generates increasingly more states with longer strings, the running-time is longer than that of the beam-breadth algorithm. This implementation was inspired by [this paper](https://www.brown.edu/Research/Istrail_Lab/_proFolding/papers/2005/bran-06.pdf).

### Iterative algorithms

#### Hill Climber

#### Random Hill Climber
This algorithm starts of by executing the randomize algorithm once to place a protein on the grid. After this, at each iteration it chooses two random amino acids and reassigns the coordinates of the amino acids in between, creating a new path that fits between the two amino acids, by calculating the Manhattan distances. The rest of the protein remains untouched. If a new path is not valid (eg. amino's are placed on the same space), the new path is discarded and new next mutation is performed on the old conformation. If the new conformation is valid, the score of the new conformation is compared to that of the old conformation. Conformations with a score of 1 of 2 worse than the old conformation have a 50% chance of being kept, because we found that this will generally generate a higher result in the end. Conformations that have the same score or a better score are being kept per definition.

#### Simulated Annealing with Pull Move

#### Random Simulated Annealing
This algorithm inherites from the random hillclimber algorithm. It uses a temperature to determine a chance that a conformation with a score that is sub-optimal is being kept. This is to avoid getting stuck in a local optimum and reaching a global optimum by exploring options that have a worse score than best at the time, because there is a chance that those will lead to a better score in the end. The temperature decreases over the number of iterations. So nearer to the end, it will gradually stop accepting conformations that have a worse score.

## Getting started
1. Install requirements via
```
pip3 install -r requirements.txt
```
<br>

## Protein folding competition
[Here](protein.quinner.nl) you can see the results of our BeamBreadth algorithm (Pikachurine) on the folding of different proteins, varying in dimension en length. Scores can be compared to other people's algorithms.
