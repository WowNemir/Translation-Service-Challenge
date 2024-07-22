import subprocess
import json

class NodeScriptError(Exception):
    pass

class TranslateClient:
    def __init__(self, script_path='translate.js'):
        self.script_path = script_path

    def translate(self, word, language, target):
        try:
            result = subprocess.run(
                ['node', self.script_path, word, language, target], 
                capture_output=True, 
                text=True, 
                check=True
            )
            data = json.loads(result.stdout)
            return data
        except subprocess.CalledProcessError as e:
            raise NodeScriptError(f"Error running Node.js script:\n{e.stderr}")
        except json.JSONDecodeError as e:
            raise NodeScriptError(f"Error parsing JSON output:\n{str(e)}")
