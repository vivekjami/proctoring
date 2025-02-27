from flask import Flask, jsonify
import threading
import detection  # Ensure this is correctly importing your detection module
import head_pose
import audio
import os

PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

@app.route('/cheat_data', methods=['GET'])
def get_cheat_data():
    return jsonify({
        "cheat_percent": detection.PERCENTAGE_CHEAT,
        "cheat_detected": detection.CHEAT_COUNTER  # Fetch the latest cheat counter
    })

def start_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    head_pose_thread = threading.Thread(target=head_pose.pose, daemon=True)
    audio_thread = threading.Thread(target=audio.sound, daemon=True)
    detection_thread = threading.Thread(target=detection.run_detection, daemon=True)

    head_pose_thread.start()
    audio_thread.start()
    detection_thread.start()

    head_pose_thread.join()
    audio_thread.join()
    detection_thread.join()
