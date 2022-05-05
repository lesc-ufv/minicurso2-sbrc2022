# Prática do Minicurso 2 - SBRC 2022
Repositório contendo os arquivos da prática do Minicurso 2, do evento SBRC 2022.

## Requisitos
* [Python 3.x](https://www.python.org/downloads/);
* [Remix IDE](http://remix.ethereum.org/);
* [IPFS Desktop](https://docs.ipfs.io/install/ipfs-desktop/);
* [Ganache](https://trufflesuite.com/docs/ganache/);

## Bibliotecas necessárias
Execute o comando abaixo na pasta do repositório para instalar as dependências:
```bash
pip install -r requirements.txt
```

## Configuração das variáveis de ambiente
Preencha os arquivos `vendedor.env` e `locatario.env` com os dados gerados pelo Remix e o Ganache.
As chaves públicas e privadas das duas entidades ficam a escolha das contas disponíveis no Ganache.
Os outros dados podem ser obtidos no Remix.

## Execução
Na pasta do repositório, basta executar os comandos abaixo para exemplificar o vendedor e locatário, respectivamente:
```bash
python scripts/vendedor.py
```
```bash
python scripts/locatario.py
```

O arquivo `base_cids.txt` pode ser utilizado como teste para colar os CIDs das imagens, porém é recomendada a utilização do próprio IPFS.

## Referências
- [Documentação Solidity](https://docs.soliditylang.org/en/v0.8.9/)
- [Documentação Web3.py](https://web3py.readthedocs.io/en/stable/)
- [NFT Rental Marketplace](https://github.com/ShivaShanmuganathan/NFT-Rental-Marketplace)