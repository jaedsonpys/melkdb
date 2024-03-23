# **MelkDB**: Um banco de dados veloz e otimizado

MelkDB é um banco de dados modelo `key-value` em desenvolvimento. Com **velocidade** em adicionar e obter dados, o MelkDB também possui ótima *otimização no consumo de memória* ao manipular os dados.

> Este projeto está em desenvolvimento, novas funcionalidades e correções serão feitas a cada nova versão lançada. Por favor, informe-nos sobre qualquer tipo de erro encontrado ao utilizar este projeto.

## ⚡ Faça um teste de velocidade

Teste a velocidade e desempenho do banco de dados usando o script `speedtest.py`, desenvolvido para exibir o *tempo de execução* em operações de adicionar e obter dados.

Em testes realizados utilizando um computador com processador **Intel Celeron Dual Core de 2.16GHz** e um SSD, obtemos seguintes dados:

| Criptografia?| N° de dados   | Tempo para adicionar | Tempo para obter |
| ------------ | ------------- | -------------------- | ---------------- |
| Não          | 10.000        | 2.6 segundos         | 1 segundo        |
| Sim          | 10.000        | 6.6 segundos         | 5.5 segundos     |