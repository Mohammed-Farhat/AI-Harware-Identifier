import os
import google.generativeai as genai
from dotenv import load_dotenv
import mimetypes

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Ensure you have a .env file with GEMINI_API_KEY set.")

genai.configure(api_key=api_key)

def upload_to_gemini(file_path):
    """Uploads the given file to Gemini AI and returns the uploaded file object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default if MIME type can't be determined

    file = genai.upload_file(file_path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Get user input for image path
image_path = input("Enter the path to the PC hardware image: ").strip()

# Upload the image
file = upload_to_gemini(image_path)

# Configure the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Generate response
response = model.generate_content([
    "What object is this? Describe how it might be used",
    "Object: The input is a PC hardware Image (any component related to computers)",
    "Description: only state the name of the hardware and its type (e.g., Intel i7 10th Gen for a CPU, or RTX 3080 for a GPU). If the input is not related to PC hardware, respond with 'I can't help you with that.'",
    "Object: ",
    file,
    "​",
    "Description: ",
])

print("\nGenerated Description:")
print(response.text)
