from website import create_app

app = create_app()

if __name__ == '__main__': #only if we run this file
    app.run(debug=True)