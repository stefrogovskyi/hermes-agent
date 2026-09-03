import subprocess

res = subprocess.run(["pip", "show", "duckduckgo_search"], capture_output=True, text=True)
print(res.stdout)
