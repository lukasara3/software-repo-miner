from dotenv import load_dotenv
load_dotenv()

from pr_profiler.cli import app

if __name__ == "__main__":
    app()