from app import create_app
import os
from dotenv import load_dotenv  # Add this import

load_dotenv()

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
