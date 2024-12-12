from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    print("app created successfully")
    app.run(host="0.0.0.0", port=5000)