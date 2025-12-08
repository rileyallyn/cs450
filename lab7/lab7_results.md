# Names: Riley Smith, Joseph Nguyen

# Lab: lab7 (RAG for Code with UniXcoder)

# Date: December 4th 2025

1. Look at the "discrimination" scores - what do they tell you?

   - UniXcoder is better at understanding if code snippet functionalities are the same or different.

2. Does UniXcoder recognize functionally similar code despite variable name changes and type hints?

   - It is able to recognize functionally similar code and it gives a higher similarity score for the ones closer to the original code snippet.

3. Does UniXcoder recognize increasingly numerous changes?

   - Yes it is able to recognize increasingly numerous changes.

4. How does it handle the "cosmetic" change? Does it think it's important, and if so, why?

   - It takes the change as if it was a massively different change. This is strange since contrasted with the other changes, the cosmetic change does not alter functionality.

5. Do different phrasings of the same question retrieve the same functions

   - Yes, but the distance value can fluctuate depending on different phrasing of the question

6. Which query types work best with UniXcoder?

   - Natural Language questions like "I want to create a user account"

7. How does UniXcoder handle vague vs specific queries?
