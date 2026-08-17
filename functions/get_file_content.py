import os

MAX_CHARS = 10000
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # CREATING PATH AND VALIDATION
        absPath = os.path.abspath(working_directory)
        fullPath = os.path.join(absPath, file_path)
        targetFile = os.path.normpath(fullPath)
        validTargetFile = os.path.commonpath([absPath, targetFile]) == absPath
        if not validTargetFile:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(targetFile):
            f'Error: File not found or is not a regular file: "{file_path}"'
        ####
        content = ""
        with open(targetFile, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content+= f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        message = str(e)
        return f'Error: Internal Server Error {message}'
