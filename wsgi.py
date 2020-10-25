from cs235A2 import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=8000, threaded=False)

