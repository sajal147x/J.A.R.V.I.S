import os
import subprocess
from sys import stderr, stdout


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        result =""
        # CREATING PATH AND VALIDATION
        absPath = os.path.abspath(working_directory)
        fullPath = os.path.join(absPath, file_path)
        targetFile = os.path.normpath(fullPath)
        validTargetFile = os.path.commonpath([absPath, targetFile]) == absPath
        if not validTargetFile:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(targetFile):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        ####
        command = ["python3", targetFile]
        if args != None:
            for arg in args:
                command.extend(arg)
        completedProcess = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if completedProcess.returncode != 0:
            result = f"Process exited with code {completedProcess.returncode}"
            return result
        if len(completedProcess.stderr) <= 0 and len(completedProcess.stdout) <= 0:
            result = result + "No output produced"
        if len(completedProcess.stderr) > 0:
            result = result + f"STDERR: {completedProcess.stderr}"
        if len(completedProcess.stdout) > 0:
            result = result + f"STDOUT: {completedProcess.stdout}"
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
