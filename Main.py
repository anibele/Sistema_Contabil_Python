import pandas as pd

# --- CONFIGURAÇÕES ---
BASE_ORIGINAL = "Arquivos Lista de contas.xlsx"
BASE_ATUALIZADA = "BaseAtualizada.xlsx"


#carregar_lista_txt: Essa função lê os arquivos de texto, limpa os caracteres indesejados e retorna uma lista de termos para classificação.
def carregar_lista_txt(caminho_arquivo):
    #Lê os arquivos de texto e limpa o caractere ';' e espaços.
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return [linha.replace(';', '').strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"⚠️ Erro: Arquivo {caminho_arquivo} não encontrado.")
        return []

#definir_tipo: Essa função classifica cada operação como "Ativo", "Passivo" ou "" (vazio) com base nas listas carregadas. 
#Ela prioriza a classificação de passivos para evitar conflitos de nomes.
def definir_tipo(nome_operacao, lista_ativos, lista_passivos):
    """Classifica a conta. Prioriza passivos para evitar conflitos de nomes."""
    if pd.isna(nome_operacao) or not isinstance(nome_operacao, str):
        return ""

    for item in lista_passivos:
        if item in nome_operacao:
            return "Passivo"
            
    for item in lista_ativos:
        if item in nome_operacao:
            return "Ativo"
    
    return ""

#obter_dados_processados: Essa função lê o Excel original, 
#limpa os dados, classifica as operações e retorna um DataFrame estruturado para as próximas etapas.
def obter_dados_processados():
    """Lê o Excel original, limpa e retorna um DataFrame classificado."""
    # Carregar listas
    ativos = carregar_lista_txt("ativos.txt")
    passivos = carregar_lista_txt("passivos.txt")

    # Ler Excel pulando as linhas de cabeçalho vazias (baseado no seu print anterior)
    df = pd.read_excel(BASE_ORIGINAL, skiprows=3, header=None)
    df = df.dropna(subset=[0]) # Remove linhas onde a operação está vazia
    
    # Renomear e estruturar
    df_limpo = pd.DataFrame()
    df_limpo['Operação'] = df.iloc[:, 0]
    df_limpo['Ativo/Passivo'] = df_limpo['Operação'].apply(lambda x: definir_tipo(x, ativos, passivos))
    df_limpo['Valor'] = df.iloc[:, 2]
    
    return df_limpo

#verificar_equilibrio: Essa função exibe o balanço patrimonial no terminal, mostrando os ativos, passivos, 
#totais e o status de equilíbrio.
def verificar_equilibrio():
    """Opção 1: Mostra o balanço e a verificação no terminal."""
    df = obter_dados_processados()
    
    ativos = df[df['Ativo/Passivo'] == 'Ativo']
    passivos = df[df['Ativo/Passivo'] == 'Passivo']
    
    total_a = ativos['Valor'].sum()
    total_p = passivos['Valor'].sum()
    saldo = total_a - total_p

    print("\n" + "="*45)
    print(f"{'BALANÇO PATRIMONIAL':^45}")
    print("="*45)
    
    print(f"{'--- ATIVOS ---':<30} | {'VALOR':>10}")
    for _, linha in ativos.iterrows():
        print(f"{linha['Operação']:<30} | R$ {linha['Valor']:>10.2f}")
        
    print("\n" + f"{'--- PASSIVOS E PL ---':<30} | {'VALOR':>10}")
    for _, linha in passivos.iterrows():
        print(f"{linha['Operação']:<30} | R$ {linha['Valor']:>10.2f}")
    
    print("="*45)
    print(f"TOTAL ATIVOS: {total_a:>31.2f}")
    print(f"TOTAL PASSIVOS/PL: {total_p:>26.2f}")
    print(f"EQUILÍBRIO (A - P): {saldo:>25.2f}")
    
    if round(saldo, 2) == 0:
        print(f"{'✅ BALANÇO EQUILIBRADO':^45}")
    else:
        print(f"{'❌ BALANÇO DESEQUILIBRADO':^45}")
    print("="*45)

#gerar_novo_arquivo: Essa função gera um novo arquivo Excel com os dados processados e inclui um resumo no final, 
#mostrando os totais de ativos, passivos, o saldo e o status de equilíbrio. 
def gerar_novo_arquivo():
    """Opção 2: Gera o Excel com os dados e o resumo no final."""
    print(f"\n⏳ Gerando {BASE_ATUALIZADA}...")
    df = obter_dados_processados()
    
    total_a = df[df['Ativo/Passivo'] == 'Ativo']['Valor'].sum()
    total_p = df[df['Ativo/Passivo'] == 'Passivo']['Valor'].sum()
    saldo = total_a - total_p
    
    # Criar linhas de resumo para anexar ao final do Excel
    resumo_dados = [
        {"Operação": "", "Ativo/Passivo": "", "Valor": None},
        {"Operação": "TOTAL ATIVOS", "Ativo/Passivo": "", "Valor": total_a},
        {"Operação": "TOTAL PASSIVOS/PL", "Ativo/Passivo": "", "Valor": total_p},
        {"Operação": "EQUILÍBRIO (A - P)", "Ativo/Passivo": "", "Valor": saldo},
        {"Operação": "STATUS", "Ativo/Passivo": "EQUILIBRADO" if round(saldo, 2) == 0 else "DESEQUILIBRADO", "Valor": None}
    ]
    
    df_resumo = pd.DataFrame(resumo_dados)
    df_final = pd.concat([df, df_resumo], ignore_index=True)
    
    # Salvar
    df_final.to_excel(BASE_ATUALIZADA, index=False)
    print(f"✅ Arquivo '{BASE_ATUALIZADA}' gerado com sucesso!")

def menu():
    while True:
        print("\n--- MENU CONTÁBIL ---")
        print("1. Verificar Equilíbrio (Terminal)")
        print("2. Gerar Novo Arquivo Excel")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            verificar_equilibrio()
        elif opcao == "2":
            gerar_novo_arquivo()
        elif opcao == "3":
            print("Encerrando sistema...")
            break
        else:
            print("⚠️ Opção inválida!")

if __name__ == "__main__":
    menu()