from cjdb_api.app import make_app
from cjdb_api.app.resources.querying import type_mapping
from cjdb_api.app.vars import PORT

def main():
    app = make_app()

    @app.before_first_request
    def before_first_request():
        type_mapping()

    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()

