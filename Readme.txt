This program determines how many “degrees of separation” is present between two actors.
Here, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. It is based on the six degrees of Kevin Bacon game.
Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.
The distribution code contains two sets of CSV data files: one set in the large directory and one set in the small directory. Each contains files with the same names, and the same structure, but small is a much smaller dataset for ease of testing and experimentation.
The program can be seen in action here:
https://youtu.be/sVccq_kHTQ8 (for small dataset)
https://youtu.be/WzxQ_U4TIW8 (for large dataset)