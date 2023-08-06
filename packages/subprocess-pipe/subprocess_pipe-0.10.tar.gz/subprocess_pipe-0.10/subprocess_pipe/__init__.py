import subprocess


def pipe_commands(*args, **kwargs):
    ps = subprocess.run(args[0], capture_output=True)

    for _ in args[1:]:
        ps = subprocess.run(_, input=ps.stdout, capture_output=True)
    return ps


