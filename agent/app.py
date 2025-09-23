from flask import Flask, request, jsonify, render_template
from main import Agent
from flask_cors import CORS  # Se o frontend for separado
import logging

logging.getLogger("watchdog").setLevel(logging.WARNING)

app = Flask(__name__, template_folder='/workspaces/IC-2025/agent')
CORS(app)  # Permite requisições do frontend (CORS)

agent = Agent(llm=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'Mensagem vazia'}), 400

    responses = agent.chat(user="local", text=user_message)
    return jsonify({'responses': responses})

if __name__ == '__main__':
    app.run(debug=True)