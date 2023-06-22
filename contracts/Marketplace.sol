// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

// Padrão ERC721
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.9/contracts/token/ERC721/ERC721.sol";
// Contador para os IDs dos itens alugáveis
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.9/contracts/utils/Counters.sol";


contract Marketplace{
    /*
        Contrato contendo os atributos e métodos
        de um marketplace de NFTs alugáveis.
    */

    // Importando utilização do contador
    using Counters for Counters.Counter;
    // Contador para os IDs dos itens alugáveis
    Counters.Counter private _itemIds;
    // Contador para a quantidade de itens alugados
    Counters.Counter private _countItensAlugados;
    // Contador para a quantidade de itens devolvidos após o aluguel
    Counters.Counter private _countItensDevolvidos;

    // Endereço do dono do contrato
    address payable donoContrato;
    // Taxa cobrada pelo Marketplace para um vendedor
    // colocar o seu item disponível para aluguel
    uint256  private taxaMarketplace;
    
    // Estrutura que mapeia um item alugável
    struct Item{
        uint256 itemId; // Identificador do item
        bool statusAlugado; // Status indicando se o item está alugado (true) ou não (false)
        address contratoNFT; // Endereço do contrato que o NFT pertence
        uint256 tokenId; // Identificador do NFT
        address payable vendedor; // Endereço do vendedor responsável pelo item
        address locatario; // Endereço da pessoa que está alugando o item
        uint256 preco; // Preço do aluguel
        uint256 expiraEm; // Tempo de duração do aluguel
    }

    // Lista dos itens alugáveis do marketplace
    mapping(uint256 => Item) private listaItens;
    
    // Evento que será disparado para retornar um item após sua criação
    event ItemCriado(
        uint256 indexed itemId,
        bool statusAlugado,
        address indexed contratoNFT,
        uint256 indexed tokenId,
        address vendedor,
        address locatario,
        uint256 preco,
        uint256 expiraEm
    );

    // Construtor que inicializa o dono do contrato
    constructor(){
        donoContrato = payable(msg.sender);
        taxaMarketplace = 0.02 ether;
    }

    // Função que retorna a taxa cobrada pelo marketplace
    function getTaxaMarketplace() public view returns (uint256) {
        return taxaMarketplace;
    }

    // Função que altera a taxa cobrada pelo Marketplace
    // (Apenas o dono do contrato pode utilizar esta função)
    function setTaxaMarketplace(uint256 _novaTaxa) external apenasDono{
        taxaMarketplace = _novaTaxa;
    }

    // Função que cria um novo item para ser alugado
    function criaItemAlugavel(
        address contratoNFT, uint256 tokenId,
        uint256 preco, uint256 expiraEm) public payable{
        
        require(preco > 0, "Preco deve ser ao menos de 1 wei!");
        require(msg.value == taxaMarketplace, "Pague exatamente a taxa que o Marketplace exige!");

        _itemIds.increment();
        uint256 itemId = _itemIds.current();

        listaItens[itemId] = Item(
            itemId,
            false,
            address(contratoNFT),
            tokenId,
            payable(msg.sender),
            address(0),
            preco,
            expiraEm
        );

        IERC721(contratoNFT).transferFrom(msg.sender, address(this), tokenId);
        donoContrato.transfer(taxaMarketplace);

        emit ItemCriado(
            itemId,
            false,
            contratoNFT,
            tokenId,
            msg.sender,
            address(0),
            preco,
            expiraEm
        );
    }

    // Função que aluga um item disponível no marketplace
    function alugarItem(address contratoNFT, uint256 itemId) public payable{
        uint256 preco = listaItens[itemId].preco;
        uint256 tokenId = listaItens[itemId].tokenId;

        require(!listaItens[itemId].statusAlugado, "Este token ja esta alugado!");
        require(IERC721(contratoNFT).ownerOf(tokenId) == address(this), "Token nao disponivel!");
        require(msg.value == preco, "Pague exatamente o valor do aluguel!");
        
        listaItens[itemId].vendedor.transfer(msg.value);
        IERC721(contratoNFT).transferFrom(address(this), msg.sender, tokenId);

        listaItens[itemId].expiraEm = listaItens[itemId].expiraEm + block.timestamp;
        listaItens[itemId].locatario = msg.sender;
        listaItens[itemId].statusAlugado = true;
        _countItensAlugados.increment();
    }

    // Função que finaliza um aluguel após o prazo de um item
    // ou caso o locatário desejar finalizar antes do prazo
    function finalizaAluguel(uint256 itemId) external {
        Item storage itemAlugado = listaItens[itemId];

        require(itemAlugado.statusAlugado, "Este token nao esta alugado!");
        require(msg.sender == itemAlugado.locatario || block.timestamp >= itemAlugado.expiraEm,
                "Este token ainda esta no periodo de aluguel!");
        
        itemAlugado.statusAlugado = false;
        
        (bool sucessoTransferencia, ) = (itemAlugado.contratoNFT).call(
            abi.encodeWithSignature(
                "transferirTokenExpirado(address,address,uint256)",
                itemAlugado.locatario,
                itemAlugado.vendedor,
                itemAlugado.tokenId
            )
        );
        require(sucessoTransferencia, "Nao foi possivel transferir o NFT de volta para o vendedor!");

        _countItensDevolvidos.increment();
        delete listaItens[itemId];
    }

    // Função que retorna a lista de NFTs disponíveis para alugar
    function getNFTsAlugaveis() public view returns (Item[] memory) {
        uint256 qtdeItensTotal = _itemIds.current();
        uint256 qtdeItensAlugaveis = 0;
        uint256 indiceAtual = 0;

        // Contabiliza a quantidade de NFTs totais disponíveis
        // para criar a lista de retorno
        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].itemId != 0 && !listaItens[i].statusAlugado) {
                qtdeItensAlugaveis += 1;
            }
        }

        Item[] memory listaItensDisponiveis = new Item[](qtdeItensAlugaveis);

        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].itemId != 0 && !listaItens[i].statusAlugado) {
                listaItensDisponiveis[indiceAtual] = listaItens[i];
                indiceAtual += 1;
            }
        }
        return listaItensDisponiveis;
    }

    // Função que retorna os NFTs alugáveis de um vendedor
    function getNFTsPorVendedor() public view returns (Item[] memory) {
        uint256 qtdeItensTotal = _itemIds.current();
        uint256 countItensVendedor = 0;
        uint256 indiceAtual = 0;

        // Contabiliza a quantidade de NFTs totais do vendedor
        // para criar a lista de retorno
        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].vendedor == msg.sender) {
                countItensVendedor += 1;
            }
        }

        Item[] memory listaItensVendedor = new Item[](countItensVendedor);

        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].vendedor == msg.sender) {
                listaItensVendedor[indiceAtual] = listaItens[i];
                indiceAtual += 1;
            }
        }
        return listaItensVendedor;
    }

    // Função que retorna os NFTs alugados por um locatário
    function getNFTsPorLocatario() public view returns (Item[] memory) {
        uint256 qtdeItensTotal = _itemIds.current();
        uint256 countItensLocatario = 0;
        uint256 indiceAtual = 0;

        // Contabiliza a quantidade de NFTs totais do locatário
        // para criar a lista de retorno
        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].locatario == msg.sender) {
                countItensLocatario += 1;
            }
        }

        Item[] memory listaItensLocatario = new Item[](countItensLocatario);

        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].locatario == msg.sender) {
                listaItensLocatario[indiceAtual] = listaItens[i];
                indiceAtual += 1;
            }
        }
        return listaItensLocatario;
    }

    // Função que retorna os itens expirados, mas ainda alugados até o momento atual da pesquisa
    function getNFTsExpiradosEAlugados() public view returns (Item[] memory) {
        uint256 qtdeItensTotal = _itemIds.current();
        uint256 countItensExpiradosEAlugados = 0;
        uint256 indiceAtual = 0;

        // Contabiliza a quantidade de NFTs totais expirados
        // para criar a lista de retorno
        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].statusAlugado && listaItens[i].expiraEm <= block.timestamp) {
                countItensExpiradosEAlugados += 1;
            }
        }

        Item[] memory listaItensExpirados = new Item[](countItensExpiradosEAlugados);

        for (uint256 i = 1; i <= qtdeItensTotal; i++) {
            if (listaItens[i].statusAlugado && listaItens[i].expiraEm <= block.timestamp) {
                listaItensExpirados[indiceAtual] = listaItens[i];
                indiceAtual += 1;
            }
        }
        return listaItensExpirados;
    }


    // Modificador utilizado para especificar quais funções apenas o dono do marketplace pode chamar
    modifier apenasDono() {
        require(msg.sender == donoContrato, "Apenas o marketplace pode utilizar este metodo!");
        _;
    }
}