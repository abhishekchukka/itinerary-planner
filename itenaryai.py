import google.generativeai as genai
import json
import streamlit as st
st.title("ITIENARY PLANNER")

def generate_recipe(start, destination ,days,budget):
    """Generates a recipe based on given parameters.

    Args:
        food: The type of food.
        profession: The target user's profession.

    Returns:
        A dictionary containing the recipe, or None if an error occurs.
    """

    try:
        # Configure API key
        genai.configure(api_key="AIzaSyCHqUPsZJPk1X6D4nYRlZ9wZ6dWfhwIwSk")

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
            system_instruction="You are an expert tourist guide. Create amazing itenary plans tailored to the user's needs, including travel,stay,food.",
        )

        # Construct the prompt
        prompt = f"Create an itenary for  {days} trip that provides all around experience such as places to visit , food to eat , hotels to stay ,for a place {destination} from {start}. Categorize the plan according to the budget as  {budget} consider trains and busses also for cost cutting. Include a clear list of plan with day with activities of the day includin traveland other commodities  and detailed budget of each day along with the overall trip budget "

        # Generate the recipe
        response = model.generate_content(prompt)
        itinerary_text = response.text

        # Basic recipe formatting (you can enhance this)
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
        print(f"An error occurred: {e}")
        return None

# Example usage
start = st.text_input(label="Enter the place you want to start your journey from:")
destination = st.text_input(label="Enter where you want to go:")
days=st.text_input(label="Enter the number of days of the trip")
budget = st.selectbox(label="Select your budget:", options=["Low", "Medium", "High"])
output = generate_recipe(start, destination,days,budget)
if output:
    for i in output["events"]:
        st.markdown(i)
else:
    print("Failed to generate plan")
# guntur
# if output:
#     print("Ingredients:")
#     for ingredient in output["ingredients"]:
#         print("- " + ingredient)
#     print("\nInstructions:")
#     for step in output["instructions"]:
#         print("- " + step)
# else:
#     print("Failed to generate itenary.")