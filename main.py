import window
import db_maker

if __name__ == "__main__":
    db_maker.create_db()
    window.create_app()

