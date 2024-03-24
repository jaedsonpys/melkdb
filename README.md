# **MelkDB**: Um banco de dados veloz e otimizado

MelkDB é um banco de dados modelo key-value desenvolvido totalmente em Python. Com seu funcionamento bem documentado, O MelkDB é fácil de usar e pode ser instalado facilmente em sistemas operacionais baseados em Linux e no Windows.

1. **Obtenha os dados rapidamente**: Desenvolvido para ser extremamente veloz na escrita e leitura de dados, o MelkDB possui um método eficiente para realizar a busca de items, além de ter um código bem otimizado.
2. **Mantenha seus dados seguros**: O MelkDB oferece a opção de criptografia de dados usando AES-256, protegendo seus dados e mantendo a velocidade ao adicionar e obter items.
3. **Baixo consumo de memória**: Apenas os dados solicitados pelo usuário são carregados na memória, evitando o alto consumo de memória ao realizar operações no banco de dados. 

## ⚡ A velocidade do MelkDB

Em testes realizados utilizando um computador com processador **Intel Celeron Dual Core de 2.16GHz** e um SSD, obtemos seguintes dados sobre a velocidade de escrita e leitura:

| Criptografia?| N° de dados   | Tempo para adicionar | Tempo para obter |
| ------------ | ------------- | -------------------- | ---------------- |
| Não          | 10.000        | 2.6 segundos         | 1 segundo        |
| Sim          | 10.000        | 6.6 segundos         | 5.5 segundos     |

> Você pode realizar o seu próprio teste de velocidade utilizando o script [speedtest.py](https://github.com/jaedsonpys/melkdb/blob/master/speedtest.py)

## Começando

Para começar a utilizar o MelkDB, você deve possuir a versão `3.6` do Python **ou superior** para conseguir executar o banco de dados sem problemas. Após isso, realiza a instalação utilizando o gerenciador de pacotes PyPI:

```bash
pip install MelkDB
```

Finalizando a instalação, o banco de dados MelkDB já está pronto para ser utilizado. Veja abaixo um simples exemplo de uso:

```python
from melkdb import MelkDB

db = MelkDB('cache')

# adicionando um item
db.add("latest_news", "Conteúdo das últimas notícias")

# atualizando um item
db.update("latest_news", "MelkDB é lançado oficialmente")

# obtendo um item
print(db.get("latest_news"))

# deletando um item
db.delete("latest_news")
```

Veja a [documentação completa](https://github.com/jaedsonpys/melkdb/tree/master/docs) para aprender mais sobre o funcionamento e métodos disponíveis para uso do MelkDB.

## Licença de uso

Este projeto utiliza a **licença MIT**. Por favor, considere [ler o documento LICENSE](https://github.com/jaedsonpys/melkdb/blob/master/LICENSE) para obter mais informações sobre o uso adequado deste projeto!

```
MIT License
Copyright (c) 2024 Jaedson Silva
```