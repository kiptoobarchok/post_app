from application import app, db

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=1, port=5001)
