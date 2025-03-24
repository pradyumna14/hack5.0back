import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=openai_api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get JSON data from the request
        data = request.get_json()
        user_message = data.get("message", "")
        
        # Validate user message
        if not user_message:
            return jsonify({"error": "Message is required."}), 400

        # Generate response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are an AI doctor. Provide medical advice, but always recommend consulting a real doctor."},
                {"role": "user", "content": user_message}
            ]
        )

        # Return response as JSON
        return jsonify({"response": response.choices[0].message.content})

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
