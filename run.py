# create the app
from app import create_app, db
app = create_app()

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == "__main__":
    # create tables (dev only)
    with app.app_context():
        db.create_all()  # 👈 creates tables from models
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    app.run(debug=True, host='0.0.0.0')