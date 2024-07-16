import subprocess
import json

class NodeScriptError(Exception):
    pass

def run_and_parse_js(word, language, target):
    try:
        # Run the Node.js script with arguments
        result = subprocess.run(['node', 'translate.js', word, language, target], capture_output=True, text=True, check=True)
        
        # Check if the script ran successfully
        if result.returncode == 0:
            # Parse the JSON output
            data = json.loads(result.stdout)
            return data
        else:
            # Raise a custom exception if Node.js script returned an error
            raise NodeScriptError(f"Error running Node.js script:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        # Raise a custom exception if subprocess run failed
        raise NodeScriptError(f"Error running subprocess:\n{str(e)}")
    except json.JSONDecodeError as e:
        # Raise a custom exception if JSON decoding failed
        raise NodeScriptError(f"Error parsing JSON output:\n{str(e)}")