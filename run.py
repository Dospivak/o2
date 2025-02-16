from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    # In production, listen on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=False) 