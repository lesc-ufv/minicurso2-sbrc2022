from web3 import Web3
from web3.eth import Contract

class Connection:
    '''
        Create a new Connection object instance. Contains all methods to
        connect with the network and with the contract.

        Parameters
        ----------
            - provider (str): Network Provider URL (e.g. Ganache)
            - address (str): Contract address
            - abi (dict): Contract ABI
        
        Attributes
        ----------
            - provider (str): Network Provider URL (e.g. Ganache)
            - contract_address (str): Contract address
            - contract_abi (dict): Contract ABI
            - web3 (Web3): Web3 instance
            - contract (Contract): Smart Contract instance
    '''
    provider : str
    contract_address : str
    contract_abi : dict
    web3 : Web3
    contract : Contract

    def __init__(self, provider : str, address : str, abi : dict):
        self.provider = provider
        self.contract_address = address
        self.contract_abi = abi
    
    def executeConnection(self):
        '''
            Call others functions about connection.

            Returns
            -------
                - status (bool): True if the connection was well-success or False is not.
        '''
        try:
            status_web3 = self.connectNetwork()
            status_contract = self.connectContract()
            return (status_web3 and status_contract)
        except Exception as e:
            print(e)
            return False
    
    def connectNetwork(self):
        '''
            Connects the provider and returns the status of the connection.

            Returns
            -------
                - status (bool): True if the connection was well-success or False is not.
        '''
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.provider))
            return self.web3.is_connected()
        except Exception as e:
            print(e)
            return False
    
    def connectContract(self):
        '''
            Connects the contract through of your address and your ABI.

            Returns
            -------
                - status (bool): True if the connection was well-success or False is not.
        '''
        try:
            self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
            return True
        except Exception as e:
            print(e)
            return False
    
    def getWeb3Connection(self):
        '''
            Returns the Web3 connection.

            Returns
            -------
                - web3 (Web3): Web3 connection.
        '''
        return self.web3
    
    def getContractConnection(self):
        '''
            Returns the contract connection.

            Returns
            -------
                - contract (Contract): Contract connection.
        '''
        return self.contract