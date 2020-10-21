#!/usr/bin/env python3

import connexion


def main():
    app = connexion.AioHttpApp(__name__, specification_dir='./swagger/')
    #app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'auth-service'})
    app.run(port=8080)


if __name__ == '__main__':
    main()