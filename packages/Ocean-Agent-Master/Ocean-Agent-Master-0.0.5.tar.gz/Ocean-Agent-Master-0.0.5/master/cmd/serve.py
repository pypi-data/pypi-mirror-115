from master.server import server


HOST = "0.0.0.0"
PORT = "8080"


def serve():
    server.run(host=HOST, port=PORT)