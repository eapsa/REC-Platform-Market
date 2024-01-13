import grpc

from proto_files import market_pb2_grpc, market_pb2


server_port = 50051
server_host = '10.255.33.19'
ca_cert = 'market/secrets/market_crt.pem'
root_certs = open(ca_cert, 'rb').read()
credentials = grpc.ssl_channel_credentials(root_certs)
cert_cn = "market"  # or parse it out of the cert data
options = (('grpc.ssl_target_name_override', cert_cn,),)
channel = grpc.secure_channel(server_host + ':' + str(server_port), credentials, options=options)
stub = market_pb2_grpc.AuthenticatedMarketServiceStub(channel=channel)

# l = market_pb2.MatchesFilter(state=[0])
# print(stub.RetrieveMatches(l))

l = market_pb2.ListUpdateMatch()
l.matches.append(market_pb2.UpdateMatch(matchID="64f84eb150e852c156fde834", state=0))
print(stub.UpdateMatch(l))
