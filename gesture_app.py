from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Route to render the start viewer page
@app.route('/')
def start_viewer():
    return render_template('start_viewer.html')

# Route to update gesture configuration
@app.route('/update_gesture_config', methods=['POST'])
def update_gesture_config():
    # Get the form data
    gesture_config = {
        "left_slide": json.loads(request.form['left_slide']),
        "right_slide": json.loads(request.form['right_slide']),
        "show_pointer": json.loads(request.form['show_pointer']),
        "draw": json.loads(request.form['draw']),
        "erase_last_annotation": json.loads(request.form['erase_last_annotation']),
        "exit": json.loads(request.form['exit'])
    }

    # Save the updated gestures to the JSON file
    config_path = "gesture_config.json"
    with open(config_path, "w") as file:
        json.dump(gesture_config, file, indent=4)

    # Redirect back to the start viewer page
    return redirect(url_for('start_viewer'))

# Route to run the viewer logic
@app.route('/run_viewer_route')
def run_viewer_route():
    # Here you can call the viewer.py script
    # For example, using subprocess to run the script
    import subprocess
    subprocess.Popen(['python', 'viewer.py'])
    return "Viewer logic is running!"

if __name__ == '__main__':
    app.run(debug=True)