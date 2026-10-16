import subprocess

subprocess.Popen(
    ["cmd", "/c", "start", "", "msedge", "https://www.youtube.com"],
    shell=False
)