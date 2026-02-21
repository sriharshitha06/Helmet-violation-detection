import os
import sys
import subprocess

def main():
    """
    Entry point for the Smart Helmet Violation Detection System.
    Sets up the environment and launches the Flask app.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src')
    
    # Ensure src is in python path
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    print(f"Starting Smart Helmet System...")
    print(f"Project Root: {project_root}")
    print(f"Please open http://localhost:5000 in your browser.")
    
    # Run the Flask app
    app_path = os.path.join(src_path, 'web', 'app.py')
    
    # We use subprocess to run it to ensure clean environment or just import it?
    # Importing is better for keeping the same process context usually, 
    # but subprocess is safer for avoiding path issues if not handled carefully.
    # Let's import to keep it simple and cross-platform compatible without relying on 'python' vs 'python3' aliases.
    
    # However, Flask's app.run() blocks. 
    # We need to make sure sys.path is set correctly for app.py imports to work.
    
    # Alternative: direct import
    from src.web.app import app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
