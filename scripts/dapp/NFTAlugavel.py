from dapp.Connection import Connection
from web3 import Web3

class NFTAlugavel:
    '''
        Cria um novo objeto NFTAlugavel. Contém os métodos do contrato NFTAlugavel.

        Parâmetros
        ----------
            - pubk (str): Chave pública da conta
            - pk (str): Chave privada da conta
            - connection (Connection): Instância da conexão do web3 e do contrato
        
        Atributos
        ----------
            - public_key (str): Chave pública da conta
            - private_key (str): Chave privada da conta
            - web3 (Web3): Instância Web3
            - contract (Contract): Instância do contrato inteligente
    '''

    def __init__(self, pubk : str, pk : str, connection : Connection):
        self.public_key = pubk
        self.private_key = pk
        self.web3 = connection.getWeb3Connection()
        self.contract = connection.getContractConnection()

    def criarNovoToken(self, tokenCID : str):
        '''
            Salva um NFT na blockchain.

            Parâmetros
            ----------
                - tokenCID (str): CID do novo NFT.

            Retorno
            -------
                - token_id (None | int): ID do novo Token ou None caso ocorra algum erro.
        '''
        try:
            # Resgata o nonce da conta
            nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
            # Cria a transação
            tx = self.contract.functions.criarNovoToken(
                tokenCID
            ).build_transaction({
                "nonce": nonce,
                "from": self.public_key
            })
            # Assina a transação com a chave privada da conta
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            # Resgata o hash da transação realizada
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Aguarda o término da transação para resgatar o ID do Token
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            token_id = Web3.to_int(receipt['logs'][0]['topics'][3])
            print("NFT criado com sucesso!")
            return token_id
        except Exception as e:
            print(e)
            return None
