from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dataclasses import dataclass
from typing import List, Dict
import re

app = Flask(__name__)
CORS(app)

@dataclass
class Song:
    id: int
    title: str
    lyrics: List[str]
    difficulty: str
    category: str

songs = [
    Song(
        id=1,
        title="Amazing Grace",
        lyrics=[
            "Amazing grace, how sweet the sound",
            "That saved a wretch like me",
            "I once was lost, but now am found",
            "Was blind, but now I see"
        ],
        difficulty="easy",
        category="hymn"
    ),
    Song(
        id=2,
        title="This Little Light of Mine",
        lyrics=[
            "This little light of mine",
            "I'm gonna let it shine",
            "This little light of mine",
            "I'm gonna let it shine, let it shine, let it shine, let it shine"
        ],
        difficulty="easy",
        category="children"
    )
]

@app.route('/')
def index():
    return send_file('static/index.html')

@app.route('/api/songs', methods=['GET'])
def get_songs():
    return jsonify([vars(song) for song in songs])

@app.route('/api/songs/<int:song_id>', methods=['GET'])
def get_song(song_id: int):
    song = next((song for song in songs if song.id == song_id), None)
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(vars(song))

@app.route('/api/hint/<int:song_id>/<int:line_index>', methods=['GET'])
def get_hint(song_id: int, line_index: int):
    song = next((song for song in songs if song.id == song_id), None)
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    
    if line_index >= len(song.lyrics):
        return jsonify({"error": "Invalid line index"}), 400
    
    line = song.lyrics[line_index]
    words = line.split()
    hint = ' '.join([word[0] + '_' * (len(word)-1) for word in words])
    
    return jsonify({
        "hint": hint,
        "firstLetter": line[0],
        "wordCount": len(words),
        "letterCount": len(line)
    })

@app.route('/api/check-lyrics', methods=['POST'])
def check_lyrics():
    data = request.get_json()
    song_id = data.get('songId')
    user_lyrics = data.get('lyrics', '')
    line_index = data.get('lineIndex', 0)
    
    song = next((song for song in songs if song.id == song_id), None)
    if song is None:
        return jsonify({"error": "Song not found"}), 404
        
    correct_lyrics = song.lyrics[line_index]
    is_correct = user_lyrics.lower().strip() == correct_lyrics.lower().strip()
    
    return jsonify({
        "correct": is_correct,
        "correctLyrics": correct_lyrics
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)