import logging

from init.init import init
from process.process import process


def main():
    cameras = init()
    process(cameras)



if __name__ == "__main__":
    main()