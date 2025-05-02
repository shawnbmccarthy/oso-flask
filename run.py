from oso_demo import create_app
from dotenv import load_dotenv

# not needed just in case right now
load_dotenv(".env")
app = create_app()