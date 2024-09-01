import requests
from notion_client import Client
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='docs', static_url_path='')

NOTION_INTEGRATION_TOKEN = "secret_7AoABIpcxMWqy3dr0HhrFQr959oEV7uSDlgmsSyUwXy"
NOTION_DATABASE_ID = "540389a82116480c93d20560a329e995"

notion = Client(auth=NOTION_INTEGRATION_TOKEN)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/search', methods=['GET'])
def search_card():
    query = request.args.get('query')
    response = requests.get(f"https://api.scryfall.com/cards/autocomplete?q={query}")
    if response.status_code == 200:
        suggestions = response.json().get("data", [])
        return jsonify(suggestions)
    return jsonify([])

@app.route('/update_notion', methods=['POST'])
def update_notion_card():
    try:
        data = request.json
        card_name = data.get('card_name')
        print(f"Received card name: {card_name}")  # Debugging line

        if not card_name:
            print("Error: No card name provided")  # Debugging line
            return jsonify({"status": "error", "message": "No card name provided"}), 400

        # Notion API logic
        new_page = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": card_name
                        }
                    }
                ]
            }
        }

        response = notion.pages.create(parent={"database_id": NOTION_DATABASE_ID}, properties=new_page)
        print("Notion update successful", response)  # Debugging line
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Error updating Notion: {e}")  # Debugging line
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
