import google.generativeai as genai

genai.configure(api_key="AIzaSyDGfK8y5mdOoYRJ1Ncm3lSfbKHmYBQ0Ro4")

models = genai.list_models()
for model in models:
    print(model.name)
