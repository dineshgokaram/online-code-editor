from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
from fastapi.responses import JSONResponse
import shutil
import logging
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Take environment variables from .env.

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")
APP_ENV = os.getenv("APP_ENV", "development")
EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", 5))
MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_SIZE", 1000))
# -------------------
# Setup logger
logger = logging.getLogger("code_runner")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# -------------------
app = FastAPI()

# Enable CORS for all origins (Frontend compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url} from {request.client.host}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Completed in {process_time:.3f}s with status code {response.status_code}")
    return response

# Supported language configs
LANGUAGES = {
    "python": {
        "extension": ".py",
        "docker_image": "code-runner-python",
        "cmd": ["python3", "Main.py"],
    },
    "cpp": {
        "extension": ".cpp",
        "docker_image": "code-runner-cpp",
        "compile_cmd": ["g++", "Main.cpp", "-o", "MainExec"],
        "cmd": ["./MainExec"],
    },
    "javascript": {
        "extension": ".js",
        "docker_image": "code-runner-node",
        "cmd": ["node", "Main.js"],
    },
    "java": {
        "extension": ".java",
        "docker_image": "code-runner-java",
        "compile_cmd": ["javac", "Main.java"],
        "cmd": ["java", "Main"],
    },
}

class CodeRequest(BaseModel):
    code: str
    language: str
    input: Optional[str] = ""

@app.get("/")
async def read_root():
    return {"message": "Code Runner API is live!"}

def run_in_docker(tmpdir: str, lang_cfg: dict, input_data: str):
    base_cmd = [
        "docker", "run", "--rm",
        "-m", "256m",
        "--cpus", "0.5",
        "-v", f"{tmpdir}:/app",
        "-w", "/app",
    ]

    if "compile_cmd" in lang_cfg:
        compile_cmd = lang_cfg["compile_cmd"]
        try:
            compile_proc = subprocess.run(
                base_cmd + compile_cmd,
                capture_output=True, text=True, timeout=10
            )
            if compile_proc.returncode != 0:
                return "", compile_proc.stderr.strip()
        except subprocess.TimeoutExpired:
            return "", "⏱️ Compilation timed out."

    try:
        run_proc = subprocess.run(
            base_cmd + lang_cfg["cmd"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return run_proc.stdout.strip(), run_proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "⏱️ Code execution timed out."
    except Exception as e:
        return "", str(e)

def run_java_locally(tmpdir: str, code: str, input_data: str):
    classname = "Main"
    java_file = os.path.join(tmpdir, f"{classname}.java")
    with open(java_file, "w") as f:
        f.write(code)

    try:
        compile_proc = subprocess.run(
            ["javac", java_file],
            capture_output=True, text=True, cwd=tmpdir, timeout=10
        )
        if compile_proc.returncode != 0:
            return "", compile_proc.stderr.strip()

        run_proc = subprocess.run(
            ["java", classname],
            input=input_data,
            capture_output=True,
            text=True,
            cwd=tmpdir,
            timeout=10
        )
        return run_proc.stdout.strip(), run_proc.stderr.strip()

    except subprocess.TimeoutExpired:
        return "", "⏱️ Local Java execution timed out."
    except Exception as e:
        return "", f"Java exec error: {str(e)}"

@app.post("/run")
async def run_code(req: CodeRequest):
    logger.info(f"Code execution request for language={req.language}, input_length={len(req.input or '')}, code_size={len(req.code)}")

    code = req.code
    language = req.language.lower()
    input_data = req.input or ""

    output = ""
    error = ""

    if language not in LANGUAGES:
        error = "Unsupported language."
        logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
        return {"output": output, "error": error}

    lang_cfg = LANGUAGES[language]
    tmpdir = tempfile.mkdtemp()

    try:
        filename = os.path.join(tmpdir, f"Main{lang_cfg['extension']}")
        with open(filename, "w") as f:
            f.write(code)

        # Check if Docker is available
        docker_ok = shutil.which("docker") is not None
        if docker_ok:
            try:
                ping = subprocess.run(["docker", "info"], capture_output=True)
                docker_ok = (ping.returncode == 0)
            except Exception:
                docker_ok = False

        if docker_ok:
            output, error = run_in_docker(tmpdir, lang_cfg, input_data)
            logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
            return {"output": output, "error": error}

        # Local fallback for Python
        if language == "python":
            try:
                result = subprocess.run(
                    ["python3", filename],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout.strip()
                error = result.stderr.strip()
            except subprocess.TimeoutExpired:
                error = "⏱️ Local Python execution timed out."
            except Exception as e:
                error = f"Local Python exec error: {str(e)}"
            logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
            return {"output": output, "error": error}

        # Local fallback for Java
        if language == "java":
            output, error = run_java_locally(tmpdir, code, input_data)
            logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
            return {"output": output, "error": error}

        # Local fallback for JavaScript
        if language == "javascript":
            try:
                result = subprocess.run(
                    ["node", filename],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout.strip()
                error = result.stderr.strip()
            except subprocess.TimeoutExpired:
                error = "⏱️ Local JavaScript execution timed out."
            except Exception as e:
                error = f"Local JavaScript exec error: {str(e)}"
            logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
            return {"output": output, "error": error}

        # Local fallback for C++
        if language == "cpp":
            exec_path = os.path.join(tmpdir, "MainExec")
            try:
                compile_proc = subprocess.run(
                    ["g++", filename, "-o", exec_path],
                    capture_output=True, text=True, timeout=10
                )
                if compile_proc.returncode != 0:
                    error = compile_proc.stderr.strip()
                else:
                    run_proc = subprocess.run(
                        [exec_path],
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    output = run_proc.stdout.strip()
                    error = run_proc.stderr.strip()
            except subprocess.TimeoutExpired:
                error = "⏱️ Local C++ execution timed out."
            except Exception as e:
                error = f"Local C++ exec error: {str(e)}"
            logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
            return {"output": output, "error": error}

        error = "Docker is not available and local execution only supports Python, Java, JavaScript, and C++."
        logger.info(f"Execution completed with output_length={len(output)}, error_length={len(error)}")
        return {"output": output, "error": error}

    finally:
        shutil.rmtree(tmpdir)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error."}
    )

# --------------------------------
# Test code (put this in separate test file normally)
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

@pytest.mark.parametrize("language, code, expected_output", [
    ("python", "print('hello')", "hello"),
    ("javascript", "console.log('hello')", "hello"),
    ("cpp", "#include <iostream>\nint main() { std::cout << \"hello\"; return 0; }", "hello"),
    ("java", "public class Main { public static void main(String[] args) { System.out.println(\"hello\"); } }", "hello"),
])
def test_run_code_success(language, code, expected_output):
    response = client.post("/run", json={"code": code, "language": language})
    assert response.status_code == 200
    data = response.json()
    assert data["output"] == expected_output
    assert data["error"] == ""

def test_unsupported_language():
    response = client.post("/run", json={"code": "print('hi')", "language": "ruby"})
    assert response.status_code == 200
    data = response.json()
    assert "Unsupported language" in data["error"]

def test_timeout_behavior():
    # Infinite loop code snippet in Python to trigger timeout
    infinite_loop_code = "while True: pass"
    response = client.post("/run", json={"code": infinite_loop_code, "language": "python"})
    data = response.json()
    assert "timed out" in data["error"].lower()
