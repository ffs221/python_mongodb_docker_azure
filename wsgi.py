from app import create_app
import os

env_name = os.getenv("BOILERPLATE_ENV") or "dev"
app = create_app(env_name)
if __name__ == "__main__":
    app.run()
