This code implements an AI to answer questions.

Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. 

We perform two tasks:

1. document retrieval- we use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. 
2. passage retrieval- we’ll use a combination of inverse document frequency and a query term density measure.

The code can be seen in action here: https://youtu.be/lN4zI4O3JT8