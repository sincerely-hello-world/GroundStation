import sys
import os



print(f"Python interpreter: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current user: {os.geteuid()}")
print(f"Current directory: {os.getcwd()}")
print(f"PATH: {os.environ.get('PATH', 'NOT SET')}")
print(f"LD_LIBRARY_PATH: {os.environ.get('LD_LIBRARY_PATH', 'NOT SET')}")

# Test import
try:
    import pyrealsense2 as rs
    print(f"pyrealsense2 imported successfully")
    print(f"Location: {rs.__file__}")
    print(f"Version: {rs.__version__}")
    # Test creating pipeline
    pipeline = rs.pipeline()
    print(f"pipeline created successfully")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()