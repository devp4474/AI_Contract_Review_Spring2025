import google.generativeai as genai

# Set your API key
genai.configure(api_key="AIzaSyAAhPrdCte0KGIHCWH3q8d4gsKoy9rBk-c")

# Create a model instance (Don't overwrite 'model' from the loop above)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Test with a prompt
response = model.generate_content("Explain how AI works")
print(response.text)
