import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
ALGOLIA_APP_ID = os.getenv("VITE_ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("VITE_ALGOLIA_SEARCH_API_KEY")
ALGOLIA_INDEX_NAME = os.getenv("VITE_ALGOLIA_INDEX_NAME")

ALGOLIA_URL = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{ALGOLIA_INDEX_NAME}/query"

HEADERS = {
    "X-Algolia-Application-Id": ALGOLIA_APP_ID,
    "X-Algolia-API-Key": ALGOLIA_API_KEY,
    "Content-Type": "application/json"
}

# --- Local Knowledge Base ---
PORTFOLIO_DATA = {
    "name": "Hala Kabir",
    "title": "Youngest Certified Professional AI, Blockchain & Chatbot Developer",
    "tagline": "Building AI-powered applications, teaching Python globally, and innovating with cloud and blockchain",
    "about": "I am Hala Kabir, the youngest certified professional AI, blockchain, and chatbot developer. I have completed advanced certifications and fellowship programs in AI and blockchain with top positions. Alongside building real-world AI applications, I am now teaching Python to millions of children and beginners around the world through social media platforms such as YouTube and Facebook.",
    "skills": [
        "Artificial Intelligence", "Generative AI", "Machine Learning", "Large Language Models (LLMs)",
        "Blockchain Development", "Chatbot Development", "Python Programming", "Web & App Development",
        "Google Cloud & Cloud Run", "Teaching & Technical Content Creation", "Hackathon Development", "Startup & Product Building"
    ],
    "experience": [
        "Participated in 5–7 national and international hackathons during 2025",
        "Participated in MUX Hackathon 2026",
        "Built and shipped multiple AI-powered applications",
        "Actively teaching Python through live sessions and tutorial series"
    ],
    "links": {
        "github": "https://github.com/halakabir234-hub",
        "linkedin": "https://www.linkedin.com/in/afia-mother-of-a-young-coder-48519138b/",
        "youtube": "https://www.youtube.com/@LearnwithHala-r2v",
        "facebook": "https://www.facebook.com/profile.php?id=61562563944122",
        "instagram": "https://www.instagram.com/halalearns/",
        "website": "https://halakabir.dev",
        "x": "https://x.com/AfiaOld58450",
        "tiktok": "https://www.tiktok.com/@your-username",
        "devto": "https://dev.to/halakabir234-hub",
        "devpost": "https://devpost.com/halakabir234-hub",
        "discord": "https://discord.gg/8VBnGjyh"
    }
}

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask_diary():
    user_question = request.json.get("question", "").lower()

    # 1. NEW: Check for Link/Social Media requests
    social_keywords = ["link", "social", "github", "youtube", "facebook", "instagram", "twitter", " x ", "tiktok", "discord", "dev.to", "devpost"]
    if any(key in user_question for key in social_keywords):
        response_text = "Sure! Here are Hala's official links:\n"
        for platform, url in PORTFOLIO_DATA["links"].items():
            # If they asked for a specific platform, we could filter, 
            # but usually, it's better to show all links when asked.
            response_text += f"• {platform}: {url}\n"
        return jsonify({"answer": response_text})

    # 2. Existing Keyword Checks
    if "skill" in user_question:
        return jsonify({"answer": f"Hala's skills include: {', '.join(PORTFOLIO_DATA['skills'])}."})
    
    if "about" in user_question or "who is" in user_question:
        return jsonify({"answer": PORTFOLIO_DATA['about']})
    
    if "experience" in user_question or "hackathon" in user_question:
        return jsonify({"answer": f"Hala has: {'. '.join(PORTFOLIO_DATA['experience'])}."})

    # 3. External Search (Algolia)
    payload = {"query": user_question, "hitsPerPage": 5}
    try:
        response = requests.post(ALGOLIA_URL, headers=HEADERS, json=payload)
        data = response.json()
        hits = data.get("hits", [])
        if not hits:
            return jsonify({"answer": "My diary couldn’t find any specific notes on that, but Hala is an expert in AI and Blockchain! 📖"})
        combined_answer = " ".join(hit.get("content", "") for hit in hits if "content" in hit)
        return jsonify({"answer": combined_answer})
    except Exception as e:
        return jsonify({"answer": f"Error searching diary: {str(e)}"}), 500

if __name__ == "__main__":
    print("📖 Diary chatbot running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)