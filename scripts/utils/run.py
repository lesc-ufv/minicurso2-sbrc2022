import os, json
from environs import Env
from dapp.Connection import Connection
from dapp.NFTAlugavel import NFTAlugavel
from dapp.MarketplaceAluguel import MarketplaceAluguel

def init(env_name : str):
    '''
        Inicializa as conexões dos contratos na blockchain e
        cria os objetos das classes que mapeiam os contratos em solidity.

        Parâmetros
        ----------
            - env_name (str): Nome do arquivo .env contendo os dados para conexão.

        Retorno
        -------
            - data (None | tuple): Tupla contendo os objetos das classes
            que mapeiam os contratos em solidity.
    '''

    # Resgata variáveis de ambiente
    env = Env()
    path_to_env = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\{}".format(env_name)
    env.read_env(path_to_env)
    # Inicializa constantes
    PUBLIC_KEY = env.str("PUBLIC_KEY")
    PRIVATE_KEY = env.str("PRIVATE_KEY")
    CHAIN_URL = env.str("CHAIN_URL")
    CONTRACT_ADDRESS_NFT = env.str("CONTRACT_ADDRESS_NFT")
    CONTRACT_ABI_NFT = json.loads(env.str("CONTRACT_ABI_NFT"))
    CONTRACT_ADDRESS_MARKET = env.str("CONTRACT_ADDRESS_MARKET")
    CONTRACT_ABI_MARKET = json.loads(env.str("CONTRACT_ABI_MARKET"))

    # Cria conexões e instancia os objetos dos contratos
    nft_instance = None
    marketplace_instance = None
    conn_nft = Connection(CHAIN_URL, CONTRACT_ADDRESS_NFT, CONTRACT_ABI_NFT)
    conn_marketplace = Connection(CHAIN_URL, CONTRACT_ADDRESS_MARKET, CONTRACT_ABI_MARKET)
    status_nft = conn_nft.executeConnection()
    status_mrktplc = conn_marketplace.executeConnection()
    if status_nft and status_mrktplc:
        nft_instance = NFTAlugavel(PUBLIC_KEY, PRIVATE_KEY, conn_nft)
        marketplace_instance = MarketplaceAluguel(PUBLIC_KEY, PRIVATE_KEY, conn_marketplace, CONTRACT_ADDRESS_NFT)
    else:
        print("Ocorreu um erro! Cheque as conexões com a rede e contratos.")
    return nft_instance, marketplace_instance