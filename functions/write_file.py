import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # CREATING PATH AND VALIDATION
        absPath = os.path.abspath(working_directory)
        fullPath = os.path.join(absPath, file_path)
        targetFile = os.path.normpath(fullPath)
        validTargetFile = os.path.commonpath([absPath, targetFile]) == absPath
        if not validTargetFile:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if  os.path.isdir(targetFile):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(targetFile), exist_ok=True)
        ####
        with open(targetFile, "w") as f:
            result = f.write(content)
        return f'Successfully wrote to "{file_path}" ({result} characters written)'
    except Exception as e:
        message = str(e)
        return f'Error: Internal Server Error {message}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites the content of a specified file with the new content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to the file whose content will be overwritten, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "the content which will be written to the file",
                },
            },
        },
    },
}
