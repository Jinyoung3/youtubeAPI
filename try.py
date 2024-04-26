from metadata import generate_title, extract_keywords, extract_one_keyword, description, generate_image_from_keyword
# Example script text
script_text = "This video is about lee kang in a very famous south korean football player"

# Generate a title for the script
title = generate_title(script_text)
print(f"Generated Title: {title}")

# # Extract keywords from the script
# keywords = extract_keywords(script_text)
# print(f"Extracted Keywords: {keywords}")

# # Extract one keyword from the list
# selected_keyword = extract_one_keyword(keywords)
# print(f"Selected Keyword: {selected_keyword}")

# # Generate a description for the script
# description_text = description(script_text)
# print(f"Generated Description: {description_text}")

# # Assuming the corrections for DALL-E image generation are applied
# # Generate an image from the selected keyword
# # Note: You will need to implement a corrected version of the image generation function
# image_url = generate_image_from_keyword(selected_keyword)
# print(f"Generated Image URL: {image_url}")

