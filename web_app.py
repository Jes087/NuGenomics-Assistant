from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
from multi_tool_agent.adk_runner import ADKRunner
# No new imports needed for async Flask routes here

app = Flask(__name__)
adk_runner = ADKRunner()

@app.route('/')
def index():
    return render_template('index.html')

# New route to serve FAQ data
@app.route('/faqs_data', methods=['GET'])
def get_faqs_data():
    """Returns the FAQ data loaded by the FAQAgent."""
    # The FAQAgent loads the data during ADKRunner initialization
    return jsonify(adk_runner.faq_agent.faq_data)


@app.route('/ask', methods=['POST'])
async def ask():
    user_input = request.json.get('question', '')
    response = await adk_runner.route_query(user_input)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)