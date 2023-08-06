import os

def Settings(**kwargs):
	if not os.path.exists("venv"):
		raise Exception("Run tools/create_venv.sh first")

	return {
		"interpreter_path": "./venv/bin/python"
	}
