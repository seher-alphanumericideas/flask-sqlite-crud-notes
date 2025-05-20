from flask import Flask, request, jsonify, render_template
import sqlite3

#Initialize Flask app
app = Flask(__name__)

def init_db():
    #Initialize the SQLite database and create the "notes" table if it does not exist
    #This ensures the backend has the required table structure on the first run
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#Run database initialization on app startup 
init_db()

@app.route('/')
def index():
    #Render the main frontend HTML page located in the templates folder
    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    #Retrieve all notes from the database
    #Returns: JSON: a list of all notes with their id, title, and content
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return jsonify([{'id': n[0], 'title': n[1], 'content': n[2]} for n in notes])

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    #Retrieve a single note by its ID
    #Args: note_id(int): The ID of the note to retrieve
    #Returns: JSON: A note object if found, otherwise an error message
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    if note:
        return jsonify({'id': note[0], 'title': note[1], 'content': note[2]})
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes', methods=['POST'])
def create_note():
    #Create a new note using the JSON body of the request
    #Expects: {"title": "Note Title", "content": "Note Content"}
    #Returns: JSON: Success message with status code 201
    data = request.json
    title = data.get('title')
    content = data.get('content')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note created'}), 201

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    #Updating an existing note using its ID and data from the request body
    #Expects: {"title": "Updated Title", "content": "Updated Content"}
    #Returns: JSON: Success message after update
    data = request.json
    title = data.get('title')
    content = data.get('content')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note updated'})

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    #Delete a note from the database using its ID
    #Args: note_id(int): The ID of the note to delete
    #Returns: JSON: Success message after deletion
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note deleted'})

if __name__ == '__main__':
    #Start the Flask development server
    app.run(debug=True)
