from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import json
import uuid

USE_NSJAIL = os.environ.get("USE_NSJAIL", "true").lower() == "true"
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    if not data or 'script' not in data:
        return jsonify({'error': 'Missing script field'}), 400

    script = data['script']

    if 'def main()' not in script:
        return jsonify({'error': 'main() function not defined'}), 400

    if not USE_NSJAIL:
        try:
            result = subprocess.run(
                ["python3", "-c", script],
                capture_output=True,
                timeout=10,
                text=True
            )
            stdout = result.stdout
            stderr = result.stderr

            if result.returncode != 0:
                raise Exception(stderr)

            main_result = None
            try:
                main_result = json.loads(stdout.strip().split('\n')[-1])
            except Exception:
                return jsonify({'error': 'main() must return a JSON serializable object', 'stdout': stdout}), 400

            return jsonify({'result': main_result, 'stdout': stdout})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Fallback to nsjail for local/dev environments
    script_filename = f"/app/script_{uuid.uuid4().hex}.py"
    with open(script_filename, "w") as f:
        f.write(script)

    nsjail_cmd = [
        'nsjail',
        '--quiet',
        '--config', '/app/nsjail.cfg',
        '--',
        '/usr/bin/python3', script_filename
    ]

    try:
        result = subprocess.run(
            nsjail_cmd,
            capture_output=True,
            timeout=10,
            text=True
        )
        stdout = result.stdout
        stderr = result.stderr

        if result.returncode != 0:
            raise Exception(stderr)

        main_result = None
        try:
            main_result = json.loads(stdout.strip().split('\n')[-1])
        except Exception:
            return jsonify({'error': 'main() must return a JSON serializable object', 'stdout': stdout}), 400

        return jsonify({'result': main_result, 'stdout': stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(script_filename)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
