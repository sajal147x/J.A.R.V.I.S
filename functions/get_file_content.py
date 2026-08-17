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
            return f'Error: File not found or is not a regular file: "{file_path}"'
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

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the content of a given file, if the file is more than 10,000 characters then it returns the first 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to get the content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
