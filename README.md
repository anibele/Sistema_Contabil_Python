# Sistema de Automação Contábil (Python)
Este projeto é uma aplicação em Python desenvolvida para automatizar a classificação e a verificação de equilíbrio de um Balanço Patrimonial. O sistema processa dados de um arquivo Excel, utiliza listas externas para classificação e gera relatórios tanto no terminal quanto em um novo arquivo .xlsx.

# Funcionalidades
* Processamento Direto de Excel: Lê dados contábeis de arquivos .xlsx.
* Classificação Inteligente: Classifica contas entre Ativo e Passivo/PL utilizando arquivos de texto (ativos.txt e passivos.txt) como base de dados.
* Lógica de Prioridade: Evita erros de classificação em termos ambíguos (ex: "Financiamento de Veículos" é priorizado como Passivo, mesmo contendo a palavra "Veículos").
* Verificação de Equilíbrio: Aplica a Equação Fundamental da Contabilidade: A - P - PL = 0
* Relatório Automatizado: Gera uma versão atualizada do balanço em Excel com um resumo dos totais e status de equilíbrio.

# Pré-requisitos
Para executar este projeto, você precisará do Python instalado e do 'pandas', use:
pip install pandas openpyxl

# Estrutura de Arquivos
Para que o programa funcione corretamente, os arquivos devem estar organizados da seguinte forma:
- main.py: O script principal com o código.
- Arquivos Lista de contas.xlsx: Sua base de dados original.
- ativos.txt: Lista de termos para identificar Ativos (um por linha, finalizado com ;).
- passivos.txt: Lista de termos para identificar Passivos/PL (um por linha, finalizado com ;).

# Lógica de Decomposição Funcional
O projeto foi construído seguindo o princípio da responsabilidade única, onde cada função realiza uma tarefa específica:
carregar_lista_txt: Gerencia a entrada de dados das regras de negócio.
definir_tipo: Contém a lógica de classificação e priorização.
obter_dados_processados: Realiza o tratamento e limpeza de dados (ETL) do Excel original.
verificar_equilibrio e gerar_novo_arquivo: Geram as saídas (outputs) do sistema.

# Menu de Opções
-> Opção 1 (Verificar Equilíbrio): Exibe no terminal o balanço organizado, as somas totais de cada grupo e se a equação fundamental foi satisfeita (Resultado = 0).
-> Opção 2 (Gerar Novo Arquivo): Cria o arquivo BaseAtualizada.xlsx contendo todas as contas classificadas e, nas linhas finais, um resumo com Total de Ativos, Total de Passivos e o status de equilíbrio.
-> Opção 3 (Sair): Encerra a aplicação.

# Imagens do programa em execução

