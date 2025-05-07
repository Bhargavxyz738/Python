# Python Code Execution API

This Flask-based REST API allows clients to submit and execute Python code in a restricted, sandboxed environment. The service enforces safety checks on imports and disallows dangerous operations.

**Live API endpoint:**  
https://python-4b0j.onrender.com

---

## Features

- Accepts Python code via HTTP POST and returns execution results (stdout, stderr, exit code, execution time).
- Enforces a maximum execution time (default: 5 seconds) to prevent long-running or infinite loops.
- Validates imports against a strict whitelist.
- Blocks file-writing operations and shell execution.
- Automatically cleans up temporary script files.
- CORS enabled for cross-origin requests.

---

## Allowed Imports

Only the following modules (and their submodules) may be imported. Any other import will result in a “Disallowed import” error.

- `math`
- `random`
- `datetime`
- `numpy`
- `requests`
- `json`
- `string`
- `os`
- `sys`
- `collections`
- `re`
- `time`
- `subprocess`
- `itertools`
- `functools`
- `typing`
- `statistics`
- `decimal`
- `hashlib`
- `uuid`
- `copy`
- `heapq`
- `bisect`
- `operator`
- `shlex`
- `dataclasses`
- `textwrap`

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/python-execution-api.git
   cd python-execution-api
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt`**:

   ```
   Flask>=2.0
   flask-cors>=3.0
   numpy>=1.20
   requests>=2.25
   ```

---

## Configuration

* **`TEMP_DIR`** (in `app.py`)
  Directory where temporary scripts are saved. Default: `temp_scripts/`.
* **`MAX_EXECUTION_TIME`** (in `app.py`)
  Maximum number of seconds a script is allowed to run. Default: `5`.

No additional environment variables are required.

---

## Running the Service

```bash
python app.py
```

The API will listen on `http://0.0.0.0:5000/`. You can also deploy it to any WSGI-compatible host—this service is already live at:

```
https://python-4b0j.onrender.com
```

---

## API Endpoints

### `POST /execute`

Execute a Python script.

* **Request Headers**
  `Content-Type: application/json`

* **Request Body**

  ```json
  {
    "code": "print('Hello, world!')"
  }
  ```

* **Success Response (HTTP 200)**

  ```json
  {
    "output": "Hello, world!\n",
    "error": "",
    "returncode": 0,
    "execution_time": "0.0023 seconds"
  }
  ```

* **Client Error (HTTP 400)**

  * Missing `"code"` field
  * Disallowed import or operation

  ```json
  {
    "error": "Code is not safe: Disallowed import: subprocess"
  }
  ```

* **Server Error (HTTP 500)**
  Unexpected exceptions:

  ```json
  {
    "error": "An unexpected error occurred: <error details>"
  }
  ```

---

## Security Measures

1. **Import Whitelist**
   Only modules listed in “Allowed Imports” may be imported.

2. **Forbidden Operations**

   * `os.system()`
   * File-opening in write, append, or update modes (`open(..., 'w')`, `'a'`, or `'+'`)
   * `subprocess.run(..., shell=True)`

3. **Execution Timeout**
   Scripts running longer than `MAX_EXECUTION_TIME` seconds are terminated.

4. **Temporary File Cleanup**
   Scripts are written to `TEMP_DIR` with a UUID filename and deleted immediately after execution.

---

## Project Structure

```
.
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── temp_scripts/        # Auto-generated scripts (ignored by VCS)
└── README.md            # This documentation
```

---

## Example Usage

```bash
curl -X POST https://python-4b0j.onrender.com/execute \
     -H "Content-Type: application/json" \
     -d '{"code": "import math\nprint(math.sqrt(16))"}'
```

Response:

```json
{
  "output": "4.0\n",
  "error": "",
  "returncode": 0,
  "execution_time": "0.0031 seconds"
}
```

---

## License

This project is licensed under the MIT License.

```

Let me know if you need any further adjustments or additional sections!
