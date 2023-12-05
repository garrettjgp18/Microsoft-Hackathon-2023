# Import block
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import Formatter
from youtube_transcript_api.formatters import TextFormatter
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import AbstractiveSummaryAction

endpoint = "YOUR_AZURE_ENDPOINT_HERE"

credential = AzureKeyCredential("YOUR_AZURE_KEY_HERE")

openAI_key = "YOUR_OPENAI_KEY_HERE"

# Variables for Azure AI (KEEP IT SECRET, KEEP IT SAFE)
credential = credential
endpoint = endpoint
text_analytics_client = TextAnalyticsClient(endpoint, credential)

print("\n\nWelcome to the prototype of Quickcards!\n")
video_URL = input("\nEnter the YouTube video URL: \n")



"""
Purpose: Retrieve video's transcript from YouTube
Input: Video URL ()
Output: Formatted video transcript
"""
def youtubeTranscriptExtract(videoURL):
    # Split the URL to only capture the video's unique ID
    videoID = videoURL.split("=", 1)[1]

    # Ensure the videoID parsed correctly
    print(f"{videoID}\n")


    # Gets the transcript of the video according to its ID
    srt = YouTubeTranscriptApi.get_transcript(videoID)

    # Format the transcript to how it would look like in paragraph form for easier reading
    formatter = TextFormatter()
    formattedTranscript = formatter.format_transcript(srt)

    try:
        # Azure Language Studio requires documents to be under 5200 characters, this will split the transcript into two seperate documents. As of right now (for token purposes), videos
        # can only be up to 10 minutes long.
        documentArray = []
        limit = 5000
        halfLimit = 2500
        if len(formattedTranscript) > limit:
            # Splits the formatted transcript into two seperate parts (part A and part B), and appends them to an array to act as documents for Azure.
            partA = formattedTranscript[:halfLimit]
            partB = formattedTranscript[halfLimit:]
            documentArray.append(partA)
            documentArray.append(partB)
            print(f"Transcript succesfully found\n")
        else:
            # If video's transcript doesn't need to be split into two documents, just append it to the array anyway to act as a single document.
            documentArray.append(formattedTranscript)
            print(f"Transcript succesfully found\n")
    except Exception as e:
        print(f"An error occured with the YouTube transcript: {e}")
        documentArray = [formattedTranscript]

    return documentArray


# Stores return value of youtubeTranscriptExtract for other methods to use
document = youtubeTranscriptExtract(video_URL)


"""
Purpose: Shorten transcirpt to create a "schema" to more accurantly define keywords
Input: Formatted transcript (document)
Output: Summarized transcript
"""
def summaryExtract(document):
    poller = text_analytics_client.begin_abstract_summary(document)
    abstract_summary = poller.result()
    print(f"Summary extract succesfully\n")

    # for result in abstract_summary:
    #     print("\nSummary Extracted:")
    #     [print(f"{summary.text}\n") for summary in result.summaries]
    return abstract_summary


"""
Purpose: Extract keywords from the formatted document for flashcards
Input: Formatted transcript (document)
Output: list of keywords / keyphrases
"""
keywordArray = []


def keynameExtract(document):
    # Mumbo Jumbo -----------------
    response = text_analytics_client.extract_key_phrases(document, language="en")
    result = [doc.key_phrases for doc in response if not doc.is_error]
    print(f"Keywords succesfully extracted\n")
    for phrases in result:
        keywordArray.append(phrases)
    return result


# Run method to store keynames and summary of transcript
keywords = keynameExtract(document)
summary = summaryExtract(document)

"""
Purpose: Create defenitions for each keyname present from the transcript
Input: Transcript and Summarized transcript
Output: Dictionary of "key" : "Defenition"
"""
openai.api_key = openAI_key
def compileDefs(keywordArray, summary):
    print(f"Plesae wait a moment while the flashcards are defined, this may take a while")
    # Construct a single prompt containing all keywords
    prompt = "\n".join(
        [
            f"Define the keyword '{keyword}' in the context of the schema: {summary}. Definitions cannot be more than 10 words"
            for keyword in keywordArray
        ]
    )

    # Add system and user messages to the prompt
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that creates Flashcards",
        },
        {"role": "user", "content": prompt},
    ]

    # Add assistant messages for each keyword
    for keyword in keywordArray:
        messages.append({"role": "assistant", "content": f"Define {keyword}"})

    # Make a single API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1500
        # 1000 tokens gets roughly 50 flashcards
    )

    # Extract and print definitions for each keyword

    for keyword, choice in zip(keywordArray, response["choices"]):
        definition = choice["message"]["content"]
        f = open("OpenAI.txt", "w")
        f.write(f"{definition}")
        print("Flashcards written in OpenAI.txt")
        f.close()


compileDefs(keywordArray, summary)
