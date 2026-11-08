import subprocess

vbs_path = r"C:\Users\Bryan\Desktop\Bryan's App\bryan-to-do-list\to_do_list.vbs"

subprocess.Popen(
    ["wscript.exe", vbs_path],
    creationflags=subprocess.CREATE_NO_WINDOW
)