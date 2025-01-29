import subprocess

print("Running paint.py...")
subprocess.run(["python", "paint.py"])

print("Running hsv_modifier.py...")
subprocess.run(["python", "hsv_modifier.py"])

print("Running inpaint.py...")
subprocess.run(["python", "inpaint.py"])

print("All scripts executed successfully!")
