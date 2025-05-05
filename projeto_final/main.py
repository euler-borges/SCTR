from init.init import init
from process.process import process


def main():
    client, cameras  = init()
    process(client, cameras)



if __name__ == "__main__":
    main()