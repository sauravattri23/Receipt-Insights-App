import subprocess
import os

if __name__ == "__main__":
    # Run Streamlit app located in frontend/app.py
    app_path = os.path.join("frontend", "app.py")
    subprocess.run(["streamlit", "run", app_path])
