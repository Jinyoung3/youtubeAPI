import openai
import os
import requests
import random
import re
from dotenv import load_dotenv
import openai
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
def generate_title(script):
    try:

        start_sequence = "\nAI:"
        restart_sequence = "\nHuman: "
        session_prompt = f"This is a creative AI. I will provide a title for the given script.\nHuman: Generate one title for the following script:\n{script}\nAI:"

        response = openai.Completion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": session_prompt}
            ]
        )

        # Extracting the title from the response
        title = response['choices'][0]['message']['content'].strip()
        return title

    except Exception as e:
        print(f"Error occurred at title: {e}")
        return None
    
def extract_keywords(script):
    try:
        # Customize this prompt to suit your needs for keyword extraction
        session_prompt = (f"This is a keyword extraction AI. I will list a few key keywords from the following script, "
            f"separated by commas:\n{script}\nAI:")

        response = openai.completions.create(
            model="gpt-3.5-turbo",  # or the model of your choice
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": session_prompt}
            ]
        )

        # Extracting the keywords from the response
        keywords = response['choices'][0]['message']['content'].strip()
        return keywords

    except Exception as e:
        print(f"Error occurred at extracting keywords: {e}")
        return None
def extract_one_keyword(script):
        keyword_list = script.split(',')

        # Trimming any leading/trailing whitespace from each keyword
        keyword_list = [keyword.strip() for keyword in keyword_list]

        # Choosing one keyword randomly from the list
        if keyword_list:
            selected_keyword = random.choice(keyword_list)
        else:
            selected_keyword = None

        return selected_keyword

def description(script):
    try:
        # Customize this prompt for summarizing the script and including a call to action
        session_prompt = (f"This is a summarizing AI. I will provide a brief summary of the following script "
                        f"and include a call to action for the viewers.\nScript:\n{script}\nAI:"
                        "\nInclude at the end: Please remember to like and subscribe to this channel for more interesting content!")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or the model of your choice
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": session_prompt}
            ]
        )

        # Extracting the summary from the response
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except Exception as e:
        print(f"Error occurred at description: {e}")
        return None

def generate_image_from_keyword(keyword):
    try:
        # Formulate the prompt for DALL-E using the keyword
        prompt = f"A creative illustration of {keyword}"

        # Generate the image using DALL-E 3
        response = openai.Dalle.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Check if the response contains information about the generated image
        if response:
            # Extract the URL from the response
            image_url = response['data'][0]['url']  # Adjust based on actual response structure
            return image_url
        else:
            print("Failed to generate image.")
            return None

    except Exception as e:
        print(f"Error occurred at img: {e}")
        return None


