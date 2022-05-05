from dapp.Connection import Connection
from web3.logs import DISCARD
from web3 import Web3

class MarketplaceAluguel:
    '''
        Cria um novo objeto MarketplaceAluguel. Contém os métodos do contrato MarketplaceAluguel.

        Parâmetros
        ----------
            - pubk (str): Chave pública da conta
            - pk (str): Chave privada da conta
            - connection (Connection): Instância da conexão do web3 e do contrato
            - contractNFT (str): Endereço do contrato de NFTs
        
        Atributos
        ----------
            - public_key (str): Chave pública da conta
            - private_key (str): Chave privada da conta
            - web3 (Web3): Instância Web3
            - contract (Contract): Instância do contrato inteligente
            - contract_nft (str): Endereço do contrato de NFTs
    '''

    def __init__(self, pubk : str, pk : str, connection : Connection, contractNFT : str):
        self.public_key = pubk
        self.private_key = pk
        self.web3 = connection.getWeb3Connection()
        self.contract = connection.getContractConnection()
        self.contract_nft = contractNFT
    
    def criaItemAlugavel(self, tokenId : int, preco : int, tempoExpira : int, descricaoAdicional : str, taxa : float):
        '''
            Disponibiliza um NFT para ser alugado.

            Parâmetros
            ----------
                - tokenId (int): ID do NFT.
                - preco (int): Preço do NFT alugável em Wei.
                - tempoExpira (int): Tempo de expiração do item em segundos.
                - descricaoAdicional (str): Descrição do novo item.
                - taxa (float): Taxa cobrada pelo marketplace para criar um novo item.

            Retorno
            -------
                - item_formatado (None | dict): Dicionário contendo os
                dados cadastrados ou None caso ocorra algum erro.
        '''
        try:
            # Resgata o nonce da conta
            nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
            # Cria a transação
            tx = self.contract.functions.criaItemAlugavel(
                self.contract_nft,
                tokenId,
                Web3.toWei(preco, 'ether'),
                tempoExpira,
                descricaoAdicional.encode('utf-8')
            ).buildTransaction({
                "nonce": nonce,
                "from": self.public_key,
                'value': self.web3.toWei(taxa, 'ether'),
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei')
            })
            # Assina a transação com a chave privada da conta
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            # Resgata o hash da transação
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Aguarda o término da transação para resgatar os dados do novo item
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            logs = self.contract.events.ItemCriado().processReceipt(receipt, DISCARD)
            print("NFT disponibilizado para aluguel com sucesso!")
            item_formatado = self.formataItemCriado(dict(logs[0]['args']))
            return item_formatado
        except Exception as e:
            print(e)
            return None
    
    def alugarItem(self, itemId: int, valor : float):
        '''
            Aluga um NFT.

            Parâmetros
            ----------
                - itemId (int): ID do item alugável.
                - valor (float): Valor a ser pago pelo aluguel.

            Retorno
            -------
                - status (bool): Indica o sucesso ou falha do aluguel.
        '''
        try:
            # Resgata o nonce da conta
            nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
            # Cria a transação
            tx = self.contract.functions.alugarItem(
                self.contract_nft,
                itemId
            ).buildTransaction({
                "nonce": nonce,
                "from": self.public_key,
                'value': self.web3.toWei(valor, 'ether'),
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei')
            })
            # Assina a transação com a chave privada da conta
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            # Resgata o hash da transação
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Aguarda o término da transação para resgatar os dados do novo item
            retorno = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        except Exception as e:
            print(e)
            return False
    
    def finalizaAluguel(self, itemId: int):
        '''
            Finaliza um aluguel.

            Parâmetros
            ----------
                - itemId (int): ID do item alugado.

            Retorno
            -------
                - status (bool): Indica o sucesso ou falha da finalização do aluguel.
        '''
        try:
            # Resgata o nonce da conta
            nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
            # Cria a transação
            tx = self.contract.functions.finalizaAluguel(
                itemId
            ).buildTransaction({
                "nonce": nonce,
                "from": self.public_key
            })
            # Assina a transação com a chave privada da conta
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            # Resgata o hash da transação
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Aguarda o término da transação para resgatar os dados do novo item
            retorno = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        except Exception as e:
            print(e)
            return False

    def getNFTsAlugaveis(self):
        '''
            Resgata os NFTs disponíveis para alugar.

            Retorno
            -------
                - nfts_disponiveis (None | list): Lista contendo os NFTs.
        '''
        try:
            nfts_disponiveis = self.contract.functions.getNFTsAlugaveis().call({'from': self.public_key})
            lista_final = []
            for item in list(nfts_disponiveis):
                lista_final.append(self.formataItem(item))
            return lista_final
        except Exception as e:
            print(e)
            return None
    
    def getNFTsPorVendedor(self):
        '''
            Resgata os NFTs de um vendedor.

            Retorno
            -------
                - nfts_disponiveis (None | list): Lista contendo os NFTs.
        '''
        try:
            nfts_disponiveis = self.contract.functions.getNFTsPorVendedor().call({'from': self.public_key})
            lista_final = []
            for item in list(nfts_disponiveis):
                lista_final.append(self.formataItem(item))
            return lista_final
        except Exception as e:
            print(e)
            return None
    
    def getNFTsPorLocatario(self):
        '''
            Resgata os NFTs de um locatário.

            Retorno
            -------
                - nfts_disponiveis (None | list): Lista contendo os NFTs.
        '''
        try:
            nfts_disponiveis = self.contract.functions.getNFTsPorLocatario().call({'from': self.public_key})
            lista_final = []
            for item in list(nfts_disponiveis):
                lista_final.append(self.formataItem(item))
            return lista_final
        except Exception as e:
            print(e)
            return None
    
    def getNFTsExpiradosEAlugados(self):
        '''
            Resgata os NFTs expirados e que ainda estão alugados.

            Retorno
            -------
                - nfts_disponiveis (None | list): Lista contendo os NFTs.
        '''
        try:
            nfts_disponiveis = self.contract.functions.getNFTsExpiradosEAlugados().call({'from': self.public_key})
            lista_final = []
            for item in list(nfts_disponiveis):
                lista_final.append(self.formataItem(item))
            return lista_final
        except Exception as e:
            print(e)
            return None
    
    def getTaxaMarketplace(self):
        '''
            Resgata a taxa cobrada pelo marketplace para criar um novo item.

            Retorno
            -------
                - taxa (None | float) - Taxa cobrada pelo marketplace.
        '''
        try:
            taxa = self.contract.functions.getTaxaMarketplace().call({'from': self.public_key})
            taxa = float(Web3.fromWei(taxa, 'ether'))
            return taxa
        except Exception as e:
            print(e)
            return None
    
    def formataItemCriado(self, item_criado : dict):
        '''
            Formata um item vindo da blockchain.

            Parâmetros
            ----------
                - item_criado (dict) - Item não formatado.

            Retorno
            -------
                - item_formatado (None | dict) - Item formatado.
        '''
        return {
            'itemId': item_criado['itemId'],
            'tokenId': item_criado['tokenId'],
            'statusAlugado': "Sim" if item_criado['statusAlugado'] else "Não",
            'vendedor': item_criado['vendedor'],
            'preco': Web3.fromWei(item_criado['preco'], 'ether'),
            'expiraEm': item_criado['expiraEm'],
            'descricao': Web3.toText(item_criado['descricao'])
        }
    
    def formataItem(self, item : tuple):
        '''
            Formata um item vindo da blockchain.

            Parâmetros
            ----------
                - item (tuple) - Item não formatado.

            Retorno
            -------
                - item_formatado (None | dict) - Item formatado.
        '''
        return {
            'itemId': item[0],
            'statusAlugado': "Sim" if item[1] else "Não",
            'enderecoContratoNFT': item[2],
            'tokenId': item[3],
            'vendedor': item[4],
            'locatario': item[5] if item[1] else "-",
            'preco': Web3.fromWei(item[6], 'ether'),
            'expiraEm': item[7],
            'descricao': Web3.toText(item[8])
        }
