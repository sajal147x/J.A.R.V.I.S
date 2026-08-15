import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        absPath = os.path.abspath(working_directory)
        fullPath = os.path.join(absPath, directory)
        targetDir = os.path.normpath(fullPath)
        validTargetDir = os.path.commonpath([absPath, targetDir]) == absPath
        if not validTargetDir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(targetDir):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        message = str(e)
        return f'Error: Internal Server Error {message}'
