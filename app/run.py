import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
print(sys.path)

from myapp import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
