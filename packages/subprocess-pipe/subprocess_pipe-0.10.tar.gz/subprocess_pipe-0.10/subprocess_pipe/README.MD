# Pipe commands with subprocess

```python
$pip install subprocess-pipe
from subprocess_pipe import pipe_commands
pa = pipe_commands(["ls"], ["grep", r".*py$"], ["grep", r"^w"])
print(pa.stdout.decode('utf-8'))

#output:
win_debugger.py
windowcapture.py

```