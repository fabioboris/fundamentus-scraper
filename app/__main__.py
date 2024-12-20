import sys

from .fundamentus import Fundamentus

if __name__ == "__main__":
    file_path = None

    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    fundamentus = Fundamentus(file_path=file_path)
    fundamentus.etl()
