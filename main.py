from flask import Flask, request, jsonify
import subprocess
import sys
import os
import uuid  
import traceback
import shutil
import time

app = Flask(__name__)


TEMP_DIR = "temp_scripts"
MAX_EXECUTION_TIME = 5  
ALLOWED_IMPORTS = [
    "math",
    "random",
    "datetime",
    "numpy",
    "requests",
    "json",
    "string",
    "os",
    "sys",
    "collections",
    "re",
    "time",
    "subprocess",
    "itertools",
    "functools",
    "typing",
    "statistics",
    "decimal",
    "hashlib",
    "uuid",
    "copy",
    "heapq",
    "bisect",
    "operator",
    "shlex",
    "dataclasses",
    "textwrap"
]
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def is_safe_code(code):
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("import") or line.startswith("from"):
            parts = line.split()
            module_name = parts[1] if "import" in parts else parts[1].split(".")[0]
            if module_name not in ALLOWED_IMPORTS:
                return False, f"Disallowed import: {module_name}"

        if "open(" in line and ("w" in line or "a" in line or "+" in line):  # Check for file write/append
            if not (line.startswith("#") or line.startswith("    #") or line.startswith("        #")):
              return False, "File writing is not allowed"
        if "os.system(" in line:  # Block os.system
            if not (line.startswith("#") or line.startswith("    #") or line.startswith("        #")):
              return False, "os.system() is not allowed"
        if "subprocess.run(" in line:
            if not (line.startswith("#") or line.startswith("    #") or line.startswith("        #")):
                if ("shell=True" in line):
                    return False, "Shell execution within subprocess is not allowed."
    return True, ""
def execute_python_code(code, timeout=MAX_EXECUTION_TIME):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"script_{file_id}.py")
    try:
        with open(file_path, "w") as f:
            f.write(code)
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, file_path],  
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False, 
            )
            end_time = time.time()
            output = result.stdout
            error = result.stderr
            returncode = result.returncode
        except subprocess.TimeoutExpired:
            end_time = time.time()
            output = ""
            error = f"Execution timed out after {timeout} seconds."
            returncode = -1  

        return output, error, returncode, end_time - start_time

    finally:
        try:
           os.remove(file_path) 
        except FileNotFoundError:
           pass
        except Exception as e:
          print(f"Error deleting file {file_path}: {e}")

@app.route("/execute", methods=["POST"])
def execute_code():
    try:
        data = request.get_json()

        if not data or "code" not in data:
            return jsonify({"error": "No code provided"}), 400

        code = data["code"]

        is_safe, reason = is_safe_code(code)
        if not is_safe:
            return jsonify({"error": f"Code is not safe: {reason}"}), 400

        output, error, returncode, execution_time = execute_python_code(code)
        response_data = {
            "output": output,
            "error": error,
            "returncode": returncode,
            "execution_time": f"{execution_time:.4f} seconds"
        }
        return jsonify(response_data), 200

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        traceback.print_exc() 
        return jsonify({"error": error_message}), 500

@app.route("/")
def hello():
    return "Hello, this is the python execution service!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Use 0.0.0.0 to make it accessible from outside
