import sys


def main() -> None:
    try:
        from pnts.app import run
    except ModuleNotFoundError as error:
        if error.name == "PyQt6":
            print("PyQt6 is not installed. Run: python -m pip install -r requirements.txt")
            sys.exit(1)
        raise

    run()


if __name__ == "__main__":
    main()
