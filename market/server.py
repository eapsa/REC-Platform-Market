import grpc
from concurrent import futures
from authenticated_market_service import AuthenticatedMarketService
from market_service import MarketService
from proto_files import market_pb2_grpc
import logging
import os


def serve():
    server1 = grpc.server(futures.ThreadPoolExecutor())
    server2 = grpc.server(futures.ThreadPoolExecutor())
    market_pb2_grpc.add_MarketServiceServicer_to_server(MarketService(), server1)
    market_pb2_grpc.add_AuthenticatedMarketServiceServicer_to_server(AuthenticatedMarketService(), server2)
    server1.add_insecure_port('[::]:50050')  # Choose the appropriate port for your service
    logging.info("Server started. Listening on port 50050.")
    # private_key = open(os.path.join(os.getcwd(), "market/secrets/market_key.pem"), 'rb').read()
    # certificate_chain = open(os.path.join(os.getcwd(), "market/secrets/market_crt.pem"), 'rb').read()
    # private_key = open("/market-microservice/market/secrets/market_key.pem", 'rb').read()
    # certificate_chain = open("/market-microservice/market/secrets/market_crt.pem", 'rb').read()
    private_key = open("/run/secrets/market_key.pem", 'rb').read()
    certificate_chain = open("/run/secrets/market_crt.pem", 'rb').read()
    credentials = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=[(private_key, certificate_chain)],
    )

    server2.add_secure_port('[::]:50051', credentials)
    server1.start()
    server2.start()
    logging.info("Server started. Listening on port 50051.")
    server1.wait_for_termination()
    server2.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Configure logging level
    serve()
