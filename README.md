# stacksync-safe-python-execution

This is a secure Python script execution service built using **Flask**, **Docker**, and **nsjail**. The service executes user-submitted Python code inside a sandboxed environment and returns the result of the `main()` function.

---

## Features

- Secure sandboxing with `nsjail`
- Dockerized for easy deployment
- Accepts and executes user-defined Python scripts via REST API
- Only returns `main()` output in JSON format
- Captures standard output (`print`) separately

---

## Project Structure

```
.
├── app.py                  # Flask API server
├── Dockerfile              # Docker build instructions
├── nsjail.cfg              # nsjail config file for sandboxing
├── requirements.txt        # Python dependencies
└── README.md               # You're reading it!
```

---

## Requirements

- Docker
- PowerShell (for the provided curl example)
- Internet (to build and pull dependencies)

---

## Setup & Usage

### 1. Clone the Repository

```bash
git clone <your_repo_url>
cd <your_repo_folder>
```

### 2. Build the Docker Image

```bash
docker build -t safe-python-api .
```

### 3. Run the Container

```bash
docker run -p 8080:8080 safe-python-api
```

---

## API Usage

### Endpoint

```
POST http://localhost:8080/execute
```

### Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "script": "import json\n\ndef main():\n    return {\"message\": \"It works!\"}\n\nprint(\"Inside nsjail\")\nprint(json.dumps(main()))"
}
```

---

### Example (PowerShell)

```powershell
curl -Method POST http://localhost:8080/execute `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{ "script": "import json\n\ndef main():\n    return {\"message\": \"It works!\"}\n\nprint(\"Inside nsjail\")\nprint(json.dumps(main()))" }'
```

---

### Successful Response

```json
{
  "result": {
    "message": "It works!"
  },
  "stdout": "Inside nsjail\n{\"message\": \"It works!\"}\n"
}
```

## Cloud Run Deployment

You can deploy this API to Google Cloud Run without using `nsjail` by setting an environment variable.

### Build and Push Docker Image

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/safe-python-api
```

### Deploy to Cloud Run (no nsjail)

```bash
gcloud run deploy safe-python-api ^
  --image gcr.io/YOUR_PROJECT_ID/safe-python-api ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars USE_NSJAIL=false
```

Replace `YOUR_PROJECT_ID` with your actual GCP project ID.

## API Usage

### Endpoint

```
POST /execute
```

### Headers

```
Content-Type: application/json
```

### Request Body

```json
{
  "script": "import json\n\ndef main():\n    return {\"message\": \"It works!\"}\n\nprint(\"Inside nsjail\")\nprint(json.dumps(main()))"
}
```

### Example (PowerShell)

```powershell
curl -Method POST https://safe-python-api-xxxxxx.run.app/execute `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{ "script": "import json\n\ndef main():\n    return {\"message\": \"It works!\"}\n\nprint(\"Inside nsjail\")\nprint(json.dumps(main()))" }'
```

### Successful Response

```json
{
  "result": {
    "message": "It works!"
  },
  "stdout": "Inside nsjail\n{\"message\": \"It works!\"}\n"
}
```

