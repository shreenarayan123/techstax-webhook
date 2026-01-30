from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

# Vercel requires the app to be named 'app'
if __name__ == '__main__':
    app.run(debug=True)
