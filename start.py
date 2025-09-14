import re

def carregar_dados(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    blocos = re.split(r'BY: @OSyncRobot\n🔍 CONSULTA DE CPF 🔍\n', conteudo)
    registros = []
    
    for bloco in blocos:
        if not bloco.strip():
            continue
            
        dados = {}
        linhas = bloco.strip().split('\n')
        
        for linha in linhas:
            if '•' in linha:
                partes = linha.split(':', 1)
                if len(partes) == 2:
                    chave = partes[0].replace('•', '').strip()
                    valor = partes[1].strip()
                    dados[chave] = valor
        
        if dados:
            registros.append(dados)
    
    return registros

def buscar_dados(registros, campo, valor):
    resultados = []
    for registro in registros:
        if campo in registro:
            if valor.lower() in registro[campo].lower():
                resultados.append(registro)
    return resultados

def main():
    registros = carregar_dados('dados.txt')
    
    while True:
        print("\n--- MENU DE BUSCA ---")
        print("1. Buscar por CPF")
        print("2. Buscar por Nome")
        print("3. Buscar por CNS")
        print("4. Buscar por Cidade")
        print("5. Sair")
        
        opcao = input("Escolha uma opção (1-5): ")
        
        if opcao == '5':
            break
            
        campo = ''
        if opcao == '1':
            campo = 'CPF'
        elif opcao == '2':
            campo = 'NOME'
        elif opcao == '3':
            campo = 'CNS'
        elif opcao == '4':
            campo = 'CIDADE'
        else:
            print("Opção inválida!")
            continue
            
        valor = input(f"Digite o {campo} para buscar: ").strip()
        resultados = buscar_dados(registros, campo, valor)
        
        if resultados:
            print(f"\n{len(resultados)} registro(s) encontrado(s):")
            for i, resultado in enumerate(resultados, 1):
                print(f"\nResultado {i}:")
                for chave, valor in resultado.items():
                    print(f"{chave}: {valor}")
        else:
            print("Nenhum registro encontrado.")

if __name__ == "__main__":
    main()
