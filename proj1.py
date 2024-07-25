import os
import google.generativeai as genai

# Configure the API key
api_key=os.environ.get("AIzaSyC2Sz-Hxn2dCJaVEWYRH2Xs88XBYn3vjSo")
if not api_key:
    raise ValueError("GENAI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your name is MR.J, your build by  Abhishek and remember youself as Detective character like Sherlock Holmes remember to show your deduction skills  at each response while assisting the user. Be in your character no matter what.",
)

chat_session = model.start_chat(
    history=[]
)

while True:
    user_input = input("Enter your message (type 'stop' to end): ")
    if user_input.lower() == "stop":
        print("Stopping the chat session.")
        break

    response = chat_session.send_message(user_input)
    print("AI Response:",response.text)