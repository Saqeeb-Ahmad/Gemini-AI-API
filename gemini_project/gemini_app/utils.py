import google.generativeai as genai

def configure_api():
    api_key = "AIzaSyBY7eAaKWkXVo0pfsCsoKUtycgzg2am0gI"
    genai.configure(api_key=api_key)