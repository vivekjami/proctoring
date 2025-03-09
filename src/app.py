from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import threading
import detection  # Ensure correct import
import head_pose  # Ensure correct import
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Global event to signal threads to stop
stop_event = threading.Event()
head_pose_thread = None
detection_thread = None

@app.route('/cheat_data', methods=['GET'])
def get_cheat_data():
    return jsonify({
        "cheat_percent": detection.PERCENTAGE_CHEAT,
        "cheat_detected": detection.CHEAT_COUNTER
    })

@app.route('/start', methods=['GET'])
def start_program():
    global head_pose_thread, detection_thread, stop_event
    
    if head_pose_thread is None or not head_pose_thread.is_alive():
        stop_event.clear()  # Ensure the stop flag is cleared

        # Start head_pose and detection in new threads
        head_pose_thread = threading.Thread(target=head_pose_runner, daemon=True)
        detection_thread = threading.Thread(target=detection_runner, daemon=True)
        
        head_pose_thread.start()
        detection_thread.start()
        
        return "Program started", 200
    else:
        return "Program already running", 200

@app.route('/end', methods=['GET'])
def end_program():
    global stop_event
    stop_event.set()  # Signal the threads to stop
    return "Program stopping", 200

def head_pose_runner():
    """Runs head_pose.pose() in a loop until stop_event is set."""
    while not stop_event.is_set():
        head_pose.pose()

def detection_runner():
    """Runs detection.run_detection() in a loop until stop_event is set."""
    while not stop_event.is_set():
        detection.run_detection()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
