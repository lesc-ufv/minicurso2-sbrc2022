// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

// Padrões ERC721
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.9/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.9/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
// Contador para os IDs dos Tokens
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.9/contracts/utils/Counters.sol";


contract NFT is ERC721URIStorage {
    /*
        Contrato contendo os atributos e métodos
        para criar e manipular um Token Não-Fungível.
    */

    // Importando utilização do contador
    using Counters for Counters.Counter;
    // Contador para os IDs dos Tokens
    Counters.Counter private _tokenIds;

    // Endereço do contrato do marketplace de aluguel
    // Usado para verificar se quem chama as funções é de fato o marketplace
    address marketplace;

    // Evento para retornar o ID do Token após sua criação
    event TokenId(uint256 token_id);

    // Construtor inicializa o endereço do contrato de aluguel
    constructor(address enderecoContratoMarketplace) ERC721("NFTAlugavel", "AFT") {
        marketplace = enderecoContratoMarketplace;
    }

    // Função que cria um novo AFT
    function criarNovoToken(string memory tokenURI) public {
        _tokenIds.increment();
        uint256 novoId = _tokenIds.current();

        _mint(msg.sender, novoId);
        _setTokenURI(novoId, tokenURI);
        approve(marketplace, novoId);

        emit TokenId(novoId);
    }

    // Função que transfere um AFT do dono para o comprador
    function transferirTokenExpirado(address de, address para, uint256 tokenId) external apenasMarketplace {
        _transfer(de, para, tokenId);
    }
    
    // Modificador utilizado para indicar quais funções apenas o Marketplace pode chamar
    modifier apenasMarketplace(){
        require(msg.sender == marketplace, "Apenas o marketplace pode utilizar esse metodo!");
        _;
    }
}