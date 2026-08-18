# Calculator Rendering Explanation

## How the Calculator Renders Results to Console

The calculator follows a structured process to render evaluation results to the console:

### 1. Input Processing (main.py)
- Accepts mathematical expressions as command-line arguments
- Validates input format and handles errors
- Creates Calculator instance for evaluation

### 2. Expression Evaluation (pkg/calculator.py)
- Parses mathematical expressions using operator precedence rules
- Implements proper tokenization and stack-based evaluation
- Handles operators: +, -, *, / with correct precedence
- Returns computed numerical results or appropriate errors

### 3. Result Formatting (pkg/render.py)
- Formats results as structured JSON objects
- Converts float results to integers when they are whole numbers
- Includes both original expression and computed result
- Uses JSON formatting with indentation for readability

### 4. Console Output
- Prints the formatted JSON to the console
- Provides clear, structured output showing:
  - The original expression entered
  - The computed result
  - Error messages for invalid inputs

## Example Output
For input: `python main.py "3 + 5"`
Output: 
```json
{
  "expression": "3 + 5",
  "result": 8
}
```

This modular approach ensures proper error handling, consistent formatting, and clear user feedback through a structured console output.