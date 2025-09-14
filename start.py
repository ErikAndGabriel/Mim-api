import re
import os
from datetime import datetime
from colorama import init, Fore, Back, Style

# Inicializa colorama
init(autoreset=True)

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados(arquivo):
    """Carrega os dados do arquivo de forma robusta"""
    try:
        print(f"{Fore.YELLOW}📂 Carregando dados do arquivo...{Style.RESET_ALL}")
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        registros = []
        # Usa uma expressão regular mais precisa para dividir os registros
        blocos = re.split(r'(?=• CPF: \d)', conteudo)
        
        for bloco in blocos:
            if not bloco.strip() or len(bloco.strip()) < 10:
                continue
                
            dados = {}
            linhas = bloco.strip().split('\n')
            
            for linha in linhas:
                if '•' in linha and ':' in linha:
                    # Remove o • e divide em chave:valor
                    linha_limpa = linha.replace('•', '').strip()
                    partes = linha_limpa.split(':', 1)
                    if len(partes) == 2:
                        chave = partes[0].strip()
                        valor = partes[1].strip()
                        dados[chave] = valor
            
            if dados and 'CPF' in dados:  # Só adiciona se tiver CPF (registro válido)
                registros.append(dados)
        
        return registros
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Erro: Arquivo 'dados.txt' não encontrado!{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}❌ Erro ao ler arquivo: {e}{Style.RESET_ALL}")
        return []

def buscar_dados(registros, campo, valor):
    """Busca dados nos registros"""
    resultados = []
    for registro in registros:
        if campo in registro:
            if valor.lower() in registro[campo].lower():
                resultados.append(registro)
    return resultados

def mostrar_cabecalho():
    """Mostra o cabeçalho bonito do sistema"""
    limpar_tela()
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print(f"║{Fore.MAGENTA}            SISTEMA DE CONSULTA DE DADOS PESSOAIS           {Fore.CYAN}        ║")
    print("║" + " " * 68 + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║ {Fore.WHITE}📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{' ' * 38}{Fore.CYAN} ║")
    print("╚" + "═" * 68 + "╝")
    print(Style.RESET_ALL)

def mostrar_menu():
    """Mostra o menu de opções"""
    print(f"\n{Fore.BLUE}📋 {Style.BRIGHT}MENU PRINCIPAL - OPÇÕES DE BUSCA{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX}┌────────────────────────────────────────────────────┐")
    print(f"│ {Fore.YELLOW}1.  🔍  Buscar por CPF{Fore.LIGHTBLUE_EX}{' ' * 28} │")
    print(f"│ {Fore.YELLOW}2.  👤  Buscar por Nome{Fore.LIGHTBLUE_EX}{' ' * 27} │")
    print(f"│ {Fore.YELLOW}3.  🆔  Buscar por CNS{Fore.LIGHTBLUE_EX}{' ' * 28} │")
    print(f"│ {Fore.YELLOW}4.  🏙️  Buscar por Cidade{Fore.LIGHTBLUE_EX}{' ' * 24}   │")
    print(f"│ {Fore.YELLOW}5.  📞  Buscar por Telefone{Fore.LIGHTBLUE_EX}{' ' * 22}  │")
    print(f"│ {Fore.YELLOW}6.  👩  Buscar por Mãe{Fore.LIGHTBLUE_EX}{' ' * 27}  │")
    print(f"│ {Fore.YELLOW}7.  👨  Buscar por Pai{Fore.LIGHTBLUE_EX}{' ' * 28} │")
    print(f"│ {Fore.YELLOW}8.  🏘️  Buscar por Bairro{Fore.LIGHTBLUE_EX}{' ' * 24}   │")
    print(f"│ {Fore.YELLOW}9.  📋  Listar campos disponíveis{Fore.LIGHTBLUE_EX}{' ' * 17} │")
    print(f"│ {Fore.YELLOW}10. 🏠  Buscar por Endereço{Fore.LIGHTBLUE_EX}{' ' * 22}  │")
    print(f"│ {Fore.YELLOW}11. 📧  Buscar por Email{Fore.LIGHTBLUE_EX}{' ' * 25}  │")
    print(f"│ {Fore.RED}12. ❌  Sair do sistema{Fore.LIGHTBLUE_EX}{' ' * 26}  │")
    print(f"└────────────────────────────────────────────────────┘{Style.RESET_ALL}")

def mostrar_resultados(resultados):
    """Mostra os resultados de forma organizada"""
    if not resultados:
        print(f"\n{Fore.RED}❌ Nenhum registro encontrado!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}✅ {len(resultados)} registro(s) encontrado(s){Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}──────────────────────────────────────────────────────────────{Style.RESET_ALL}")
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{Fore.CYAN}📄 REGISTRO {i}:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}──────────────────────────────────────────────────────────────{Style.RESET_ALL}")
        
        # Agrupa os dados por categorias
        categorias = {
            'Dados Pessoais': ['CPF', 'NOME', 'NASCIMENTO', 'IDADE', 'SEXO', 'SIGNO', 'COR', 'TIPO SANGUÍNEO'],
            'Documentos': ['RG', 'DATA DE EXPEDIÇÃO', 'ORGÃO EXPEDIDOR', 'UF - RG', 'CNS'],
            'Filiação': ['MÃE', 'PAI'],
            'Nascimento': ['PAÍS DE NASCIMENTO', 'CIDADE DE NASCIMENTO', 'ESTADO DE NASCIMENTO'],
            'Certidão': ['TIPO DE CERTIDÃO', 'NOME DO CARTORIO', 'LIVRO', 'FOLHA', 'TERMO', 'DATA DE EMISSÃO'],
            'Endereço': ['TIPO DE LOGRADOURO', 'LOGRADOURO', 'NÚMERO', 'COMPLEMENTO', 'BAIRRO', 'CIDADE', 'ESTADO', 'PAÍS', 'CEP'],
            'Contato': ['E-MAIL', 'TELEFONE', 'TIPO']
        }
        
        for categoria, campos in categorias.items():
            dados_categoria = []
            for campo in campos:
                if campo in resultado and resultado[campo] and resultado[campo] != "SEM INFORMAÇÃO":
                    dados_categoria.append(f"{Fore.LIGHTBLACK_EX}  • {Fore.WHITE}{campo}: {Fore.GREEN}{resultado[campo]}")
            
            if dados_categoria:
                print(f"\n{Fore.MAGENTA}📁 {categoria}:{Style.RESET_ALL}")
                for dado in dados_categoria:
                    print(dado)
        
        print(f"{Fore.LIGHTBLACK_EX}──────────────────────────────────────────────────────────────{Style.RESET_ALL}")
        if i < len(resultados):
            input(f"\n{Fore.YELLOW}⏎ Pressione Enter para ver o próximo registro... {Style.RESET_ALL}")
            limpar_tela()
            mostrar_cabecalho()

def listar_campos(registros):
    """Lista todos os campos disponíveis"""
    if registros:
        print(f"\n{Fore.BLUE}📋 CAMPOS DISPONÍVEIS PARA BUSCA:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}──────────────────────────────────────────────────────────────{Style.RESET_ALL}")
        campos = list(registros[0].keys())
        campos.sort()
        
        for i, campo in enumerate(campos, 1):
            print(f"{Fore.CYAN}{i:2d}. {Fore.WHITE}{campo}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Nenhum campo disponível!{Style.RESET_ALL}")

def main():
    """Função principal do sistema"""
    mostrar_cabecalho()
    print(f"{Fore.YELLOW}📂 Carregando dados...{Style.RESET_ALL}")
    registros = carregar_dados('dados.txt')
    
    if not registros:
        print(f"{Fore.RED}❌ Nenhum dado foi carregado. Verifique o arquivo 'dados.txt'{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}⏎ Pressione Enter para sair... {Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✅ Dados carregados: {len(registros):,} registros encontrados!{Style.RESET_ALL}")
    input(f"{Fore.YELLOW}⏎ Pressione Enter para continuar... {Style.RESET_ALL}")
    
    while True:
        mostrar_cabecalho()
        mostrar_menu()
        
        try:
            opcao = input(f"\n{Fore.CYAN}🎯 Escolha uma opção (1-12): {Style.RESET_ALL}").strip()
            
            if opcao == '12':
                print(f"\n{Fore.GREEN}👋 Obrigado por usar o sistema! Até logo! 👋{Style.RESET_ALL}")
                break
                
            campos_busca = {
                '1': 'CPF',
                '2': 'NOME', 
                '3': 'CNS',
                '4': 'CIDADE',
                '5': 'TELEFONE',
                '6': 'MÃE',
                '7': 'PAI',
                '8': 'BAIRRO',
                '9': 'listar',
                '10': 'LOGRADOURO',
                '11': 'E-MAIL'
            }
            
            if opcao == '9':
                mostrar_cabecalho()
                listar_campos(registros)
                input(f"\n{Fore.YELLOW}⏎ Pressione Enter para voltar ao menu... {Style.RESET_ALL}")
                continue
                
            if opcao not in campos_busca:
                print(f"{Fore.RED}❌ Opção inválida! Tente novamente.{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}⏎ Pressione Enter para continuar... {Style.RESET_ALL}")
                continue
            
            campo = campos_busca[opcao]
            mostrar_cabecalho()
            print(f"{Fore.BLUE}🔍 BUSCA POR: {campo}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}──────────────────────────────────────────────────────────────{Style.RESET_ALL}")
            
            valor = input(f"{Fore.WHITE}Digite o {campo} para buscar: {Style.RESET_ALL}").strip()
            
            if not valor:
                print(f"{Fore.RED}❌ Valor de busca não pode estar vazio!{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}⏎ Pressione Enter para continuar... {Style.RESET_ALL}")
                continue
                
            print(f"\n{Fore.YELLOW}⏳ Buscando por '{valor}'...{Style.RESET_ALL}")
            resultados = buscar_dados(registros, campo, valor)
            
            mostrar_cabecalho()
            mostrar_resultados(resultados)
            
            input(f"\n{Fore.YELLOW}⏎ Pressione Enter para voltar ao menu... {Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 Operação cancelada pelo usuário. Até logo!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}⏎ Pressione Enter para continuar... {Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 Programa interrompido pelo usuário. Até logo!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro fatal: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}⏎ Pressione Enter para sair... {Style.RESET_ALL}")
