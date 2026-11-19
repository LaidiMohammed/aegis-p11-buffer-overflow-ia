$py = if (Test-Path .venv/bin/python) { '.venv/bin/python' } else { 'python' }
& $py "src\buffer-overflow-ia_main.py"
