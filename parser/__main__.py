import sys

from .main import main


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
