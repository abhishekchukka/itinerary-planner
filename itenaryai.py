import google.generativeai as genai
import json
import streamlit as st

st.title("ITINERARY PLANNER")

def generate_itinerary(start, destination, days, budget):
    try:
        # Retrieve API key from Streamlit secrets
        api_key = st.secrets["api_keys"]["google_generativeai"]
        genai.configure(api_key=api_key)

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert tourist guide. Create amazing itinerary plans tailored to the user's needs, including travel, stay, food.",
        )

        # Construct the prompt
        prompt = f"Create an itinerary for a {days}-day trip that provides an all-around experience, including places to visit, food to eat, hotels to stay, for a place {destination} from {start}. Categorize the plan according to the budget as {budget}. Consider trains and buses for cost-cutting. Include a clear list of plans with day-by-day activities, including travel and other commodities, and a detailed budget of each day along with the overall trip budget."

        # Generate the itinerary
        response = model.generate_content(prompt)
        itinerary_text = response.text

        # Basic itinerary formatting
        itinerary_dict = {"events": [], "notes": []}
        current_section = "events"
        for line in itinerary_text.split("\n"):
            if line.startswith("Schedule:"):
                current_section = "events"
            elif line.startswith("Notes:"):
                current_section = "notes"
            else:
                itinerary_dict[current_section].append(line)

        return itinerary_dict

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Example usage
start = st.text_input(label="Enter the place you want to start your journey from:")
destination = st.text_input(label="Enter where you want to go:")
days = st.text_input(label="Enter the number of days of the trip")
budget = st.selectbox(label="Select your budget:", options=["Low", "Medium", "High"])

if st.button("Generate Itinerary"):
    if start and destination and days and budget:
        output = generate_itinerary(start, destination, days, budget)
        if output:
            st.subheader("Itinerary")
            for event in output["events"]:
                st.markdown(event)
            
            for note in output["notes"]:
                st.markdown(note)
        else:
            st.error("Failed to generate itinerary.")
    else:
        st.error("Please fill in all fields.")
