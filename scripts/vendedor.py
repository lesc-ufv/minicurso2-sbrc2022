from utils.run import init
from utils.menu import menu_vendedor

nft, marketplace = init("vendedor.env")
if nft != None and marketplace != None:
    menu_vendedor()
    print("=======================================================")
    opcao = int(input("Selecione uma opção: "))
    print("=======================================================")
    if opcao == 1:
        print("=======================================================")
        token_cid = input("Cole aqui o CID do NFT que deseja criar: ")
        print("=======================================================")
        token_id = nft.criarNovoToken(token_cid)
        if token_id is not None:
            print("ID do NFT gerado: {}".format(token_id))
        print("=======================================================")
    elif opcao == 2:
        print("=======================================================")
        token_id = int(input("Digite o ID do NFT: "))
        preco = float(input("Digite o preço de aluguel do NFT (Em Ether): "))
        tempo = int(input("Digite o tempo do aluguel (Em segundos): "))
        descricao = input("Digite uma descrição adicional do NFT: ")
        taxa = marketplace.getTaxaMarketplace()
        print("Taxa cobrada pelo marketplace: {} ETH".format(taxa))
        print("=======================================================")
        item_criado = marketplace.criaItemAlugavel(token_id, preco, tempo, descricao, taxa)
        if item_criado is not None:
            print("=======================================================")
            print("ID do item alugável: {}".format(item_criado['itemId']))
            print("ID do NFT: {}".format(item_criado['tokenId']))
            print("Alugado? {}".format(item_criado['statusAlugado']))
            print("Vendedor: {}".format(item_criado['vendedor']))
            print("Valor do aluguel: {} ETH".format(item_criado['preco']))
            print("Prazo do aluguel em segundos: {}".format(item_criado['expiraEm']))
            print("Descrição adicional: {}".format(item_criado['descricao']))
            print("=======================================================")
    elif opcao == 3:
        print("=======================================================")
        nfts = marketplace.getNFTsPorVendedor()
        if len(nfts) > 0:
            print("NFTs pertencentes a esta conta:\n")
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
            print("Nenhum NFT pertencente a esta conta!")
            print("=======================================================")
