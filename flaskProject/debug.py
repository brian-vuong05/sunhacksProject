import sys

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import pymongo

    print(f"PyMongo version: {pymongo.__version__}")
    print("PyMongo successfully imported")
except ImportError as e:
    print(f"Error importing pymongo: {e}")

try:
    from pymongo import MongoClient

    print("MongoClient successfully imported")
except ImportError as e:
    print(f"Error importing MongoClient: {e}")