
import sys
import os

# from app import NvidiaFanControl
from nvidia_fan_control import app


def main():
    app.NvidiaFanControl().run(sys.argv)


if __name__ == '__main__':
    main()
