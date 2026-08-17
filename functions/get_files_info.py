import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    result = []
    try:
        absPath = os.path.abspath(working_directory)
        fullPath = os.path.join(absPath, directory)
        targetDir = os.path.normpath(fullPath)
        validTargetDir = os.path.commonpath([absPath, targetDir]) == absPath
        if not validTargetDir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(targetDir):
            return f'Error: "{directory}" is not a directory'

        ls = os.listdir(targetDir)
        for output in ls:
            name = output
            entry_path = os.path.join(targetDir, output)
            size = os.path.getsize(entry_path)
            isDir = os.path.isdir(entry_path)
            output = f'- {name}: file_size={size} bytes, is_dir={isDir} '
            result.append(output)
        return "\n".join(result)

    except Exception as e:
        message = str(e)
        return f'Error: Internal Server Error {message}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
