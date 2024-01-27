from flask import Flask, render_template, request, jsonify
import json
import os
import requests

app = Flask(__name__)

# Function to get the list of books
def get_books():
    books_dir = 'books'
    # List comprehension to exclude non-json files
    return [book.replace('.json', '') for book in os.listdir(books_dir) if book.endswith('.json')]

# Function to get hamdb information for a given callsign
def get_hamdb_info(call_sign):
    api_url = f'https://api.hamdb.org/v1/{call_sign}/json/redirect'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        try:
            data = response.json()
        except ValueError:
            print("Error: Invalid JSON in the response.")
            return None

        hamdb_info = data.get('hamdb', {}).get('callsign', {})

        if hamdb_info:
            return hamdb_info
        else:
            print(f"Error: No information available for call sign {call_sign}")
            return None

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

# Route for the home page (index.html)
@app.route('/index.html')
def home():
    return render_template('index.html')

# Route for the contact display page
@app.route('/contactdisplay.html')
def contactdisplay():
    return render_template('contactdisplay.html')

# Route for the settings page
@app.route('/settings.html')
def settings():
    return render_template('settings.html')

# Route for the info log page
@app.route('/logform.html')
def infolog():
    return render_template('logform.html')

# Route for the search page (search.html)
@app.route('/search.html')
def search():
    return render_template('search.html')

# Route for the map page
@app.route('/map.html')
def map():
    return render_template('map.html')

# Route for saving contacts
@app.route('/saveContacts', methods=['POST'])
def save_contacts():
    try:
        contacts = request.json['contacts']

        # Save the contacts to ham_logbook.json
        with open('public/ham_logbook.json', 'w') as file:
            json.dump(contacts, file, indent=2)

        return jsonify({'success': True}), 200

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Route to get the list of books
@app.route('/getBooks')
def get_books_route():
    return jsonify({'books': get_books()})

# Route to get hamdb information for a given callsign
@app.route('/getHamdbInfo/<callsign>')
def get_hamdb_info_route(callsign):
    hamdb_info = get_hamdb_info(callsign)
    return jsonify({'hamdb_info': hamdb_info})

if __name__ == '__main__':
    app.run(port=3000)
    print("Running on http://127.0.0.1:3000/index.html")
