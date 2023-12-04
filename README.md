# Microsoft-Hackathon-2023

## Quickcards
Quickcards was a project I built for the 2023 Microsoft AI Classroom Hackathon. It allows users to dynamically generate flashcards based off of a YouTube video of their choice.

## How to run
You'll need to get API keys for the following...
- Azure Language Studio
  - If you're a student, you can recieve a free account for Azure, and follow their guide to set up an key for this specific service.
  - You will also need an endpoint. You can create a Language Studio resource, and it will create a key and endpoint for you that you can simply copy and paste. 
- OpenAI
  - OpenAI allows anybody with a valid phone number to get an API key, with $5 worth of free credit (roughly 5,000,000 tokens) a month.

Once you've secured the two API keys, clone this repository to your IDE of chocie (I used VSCode, so it will likely run the best there).
- Use the pip installer in your terminal to install the dependencies...
  
  -pip install openai
  
  -pip install youtube-transcript-api
  
  -pip install azure-ai-textanalytics
  
  -pip install azure-identity

- Open the TranscriptCall.py file, and find the first three variables - they should be labeled "endpoint", "credential", "OpenAI_key".
- Copy and paste your associated endpoint (from Azure Language Studio), and your keys into the associated variables.

Finally, you can run the program and you should recieve a text prompt asking for a YouTube vide URL. Find a video that is 10 minutes or less, and copy and paste the full URL into the terminal.
For example: https://www.youtube.com/watch?v=c-I5S_zTwAc

# How it works
Quickcards uses three seperate API's:
- YouTube transcript API
  - Get the videos transcript
- Azure Language Studio
  - Extract keywords and an abstract summary of the transcript
- OpenAI
  - Use the keywords and the abstract summary to define each keyword in the context of the schema of the summary.

The results are printed into a txt file called "OpenAI.txt".
  


