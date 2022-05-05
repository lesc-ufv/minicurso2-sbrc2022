from utils.run import init
from utils.menu import menu_locatario
from datetime import datetime

_, marketplace = init("locatario.env")
if marketplace != None:
    menu_locatario()
    print("=======================================================")
    opcao = int(input("Selecione uma opção: "))
    print("=======================================================")
    if opcao == 1:
        print("=======================================================")
        nfts = marketplace.getNFTsAlugaveis()
        if len(nfts) > 0:
            print("NFTs disponíveis para alugar:\n")
            for nft in nfts:
                print("ID do item alugável: {}".format(nft['itemId']))
                print("ID do NFT: {}".format(nft['tokenId']))
                print("Endereço do contrato do NFT: {}".format(nft['enderecoContratoNFT']))
                print("Alugado? {}".format(nft['statusAlugado']))
                print("Vendedor: {}".format(nft['vendedor']))
                print("Locatário: {}".format(nft['locatario']))
                print("Valor do aluguel: {} ETH".format(nft['preco']))
                print("Prazo do aluguel em segundos: {}".format(nft['expiraEm']))
                print("Descrição adicional: {}".format(nft['descricao']))
                print("=======================================================")
        else:
            print("Nenhum NFT disponível!")
            print("=======================================================")
    elif opcao == 2:
        print("=======================================================")
        item_id = int(input("Digite o ID de um item para alugar: "))
        pgto = float(input("Digite o valor deste item para pagamento: "))
        print("=======================================================")
        if marketplace.alugarItem(item_id, pgto):
            print("Item alugado com sucesso!")
            print("=======================================================")
    elif opcao == 3:
        print("=======================================================")
        nfts = marketplace.getNFTsPorLocatario()
        if len(nfts) > 0:
            print("NFTs alugados por esta conta:\n")
            for nft in nfts:
                print("ID do item alugável: {}".format(nft['itemId']))
                print("ID do NFT: {}".format(nft['tokenId']))
                print("Endereço do contrato do NFT: {}".format(nft['enderecoContratoNFT']))
                print("Alugado? {}".format(nft['statusAlugado']))
                print("Vendedor: {}".format(nft['vendedor']))
                print("Locatário: {}".format(nft['locatario']))
                print("Valor do aluguel: {} ETH".format(nft['preco']))
                print("Prazo do aluguel: {}".format(datetime.fromtimestamp(nft['expiraEm'])))
                print("Descrição adicional: {}".format(nft['descricao']))
                print("=======================================================")
        else:
            print("Nenhum NFT alugado por esta conta!")
            print("=======================================================")
    elif opcao == 4:
        print("=======================================================")
        item_id = int(input("Digite o ID de um item para finalizar o aluguel: "))
        print("=======================================================")
        if marketplace.finalizaAluguel(item_id):
            print("Aluguel finalizado com sucesso!")
            print("=======================================================")
        
