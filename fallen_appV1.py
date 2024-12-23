from datetime import datetime
import os

def get_file_path(arquivo):
    """Retorna o caminho completo do arquivo na pasta fallen"""
    pasta_fallen = 'fallen'
    
    # Cria a pasta fallen se não existir
    if not os.path.exists(pasta_fallen):
        os.makedirs(pasta_fallen)
        
    return os.path.join(pasta_fallen, arquivo)

def cadastrar_equipamento():
    """Função para abrir tela de cadastro de equipamento"""
    print("\n=== Cadastro de Equipamento ===")
    try:
        serie = input("Número de série: ")
        nome = input("Nome do equipamento: ")
        while True:
            try:
                quantidade = int(input("Quantidade: "))
                break
            except ValueError:
                print("Por favor, digite um número válido para quantidade.")
        descricao = input("Descrição: ")
        foto = input("Nome do arquivo de foto: ")
        local = input("Local: ")
        
        if Equipamento(serie, nome, quantidade, descricao, foto, local):
            print("Equipamento cadastrado com sucesso!")
            return True
        return False
    except Exception as e:
        print(f"Erro ao cadastrar equipamento: {e}")
        return False

def verificar_equipamento(nome_equipamento):
    """Verifica se um equipamento existe no cadastro"""
    try:
        arquivo_path = get_file_path('cadastro_equipamentos.txt')
        if not os.path.exists(arquivo_path):
            return False
            
        with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                if nome_equipamento in linha:
                    return True
        
        # Se chegou aqui, o equipamento não foi encontrado
        print(f"\nEquipamento '{nome_equipamento}' não cadastrado no sistema.")
        opcao = input("Deseja cadastrar? (S/N): ").upper()
        
        if opcao == 'S':
            return cadastrar_equipamento()
        else:
            print("Operação cancelada.")
            return False
            
    except Exception as e:
        print(f"Erro ao verificar equipamento: {e}")
        return False

def verificar_usuario(nome_usuario):
    """Verifica se um usuário existe no cadastro"""
    try:
        arquivo_path = get_file_path('usuarios.txt')
        if not os.path.exists(arquivo_path):
            return False
            
        with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                if nome_usuario in linha:
                    return True
        return False
    except Exception as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

def salvar_registro(arquivo, dados):
    """Função genérica para salvar registros em arquivos"""
    try:
        arquivo_path = get_file_path(arquivo)
        with open(arquivo_path, 'a', encoding='utf-8') as f:
            f.write(dados + '\n')
        return True
    except Exception as e:
        print(f"Erro ao salvar em {arquivo}: {e}")
        return False

def validar_tipo_usuario(tipo):
    """Valida o tipo de usuário"""
    tipos_validos = ['admin', 'inspector', 'tecnico']
    return tipo.lower() in tipos_validos

def Chamado(descricao: str, prioridade: str, equipamento: str, atribuir_para: str):
    """Função para registrar um chamado"""
    try:
        # Primeiro verifica se a prioridade é válida
        if prioridade.lower() not in ['baixa', 'media', 'alta']:
            raise ValueError("Prioridade deve ser: baixa, media ou alta")
        
        # Verifica se o usuário existe antes de prosseguir
        if not verificar_usuario(atribuir_para):
            print("Usuário não existente. O chamado não pode ser registrado.")
            return False
            
        # Se o usuário existe, verifica o equipamento
        data_abertura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        arquivo_path = get_file_path('cadastro_equipamentos.txt')
        equipamento_encontrado = False
        
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    if equipamento in linha:
                        equipamento_encontrado = True
                        break
        
        if not equipamento_encontrado:
            print(f"Equipamento {equipamento} não encontrado.")
            opcao = input("Deseja cadastrar? (S/N): ").upper()
            
            if opcao == 'S':
                if cadastrar_equipamento():
                    print("Continuando com o registro do chamado...")
                else:
                    print("Não foi possível cadastrar o equipamento.")
                    return False
            else:
                print("Voltando para o início...")
                return False
        
        # Se chegou aqui, tanto usuário quanto equipamento são válidos
        dados = f"{descricao}|{prioridade}|{data_abertura}|{equipamento}|{atribuir_para}"
        return salvar_registro('chamado.txt', dados)
        
    except Exception as e:
        print(f"Erro ao registrar chamado: {e}")
        return False

def Instalacao(nome: str, endereco: str, cidade: str, estado: str, cep: str, descricao: str):
    """Função para registrar uma instalação"""
    try:
        dados = f"{nome}|{endereco}|{cidade}|{estado}|{cep}|{descricao}"
        return salvar_registro('instalacao.txt', dados)
    except Exception as e:
        print(f"Erro ao registrar instalação: {e}")
        return False

def Equipamento(serie: str, nome: str, quantidade: int, descricao: str, foto: str, local: str):
    """Função para registrar um equipamento"""
    try:
        dados = f"{serie}|{nome}|{quantidade}|{descricao}|{foto}|{local}"
        return salvar_registro('equipamentos.txt', dados)
    except Exception as e:
        print(f"Erro ao registrar equipamento: {e}")
        return False

def Acao(equipamento: str, responsavel: str, descobertas: str, status: str):
    """Função para registrar uma ação"""
    try:
        if status.lower() not in ['aberta', 'fechada', 'pendente']:
            raise ValueError("Status deve ser: aberta, fechada ou pendente")
            
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        if not verificar_equipamento(equipamento):
            print(f"Equipamento {equipamento} não encontrado. Criando novo cadastro...")
            dados_equip = f"{equipamento}|{data}|{responsavel}|{descobertas}|{status}"
            salvar_registro('cadastro_equipamentos.txt', dados_equip)
        
        if not verificar_usuario(responsavel):
            raise ValueError("Usuário não existente")
            
        dados = f"{equipamento}|{data}|{responsavel}|{descobertas}|{status}"
        return salvar_registro('acao.txt', dados)
        
    except Exception as e:
        print(f"Erro ao registrar ação: {e}")
        return False

def Gestao_Equipamento(id: str, data: str, descricao: str, id_equipamento: str):
    """Função para gestão de equipamento"""
    try:
        dados = f"{id}|{data}|{descricao}|{id_equipamento}"
        return salvar_registro('gestao_equipamento.txt', dados)
    except Exception as e:
        print(f"Erro ao registrar gestão de equipamento: {e}")
        return False

def Gestao_Usuario(nome: str, email: str, tipo: str):
    """Função para gestão de usuários"""
    try:
        while not validar_tipo_usuario(tipo):
            print("Tipo inválido! Deve ser: admin, inspector ou técnico")
            tipo = input("Digite o tipo novamente: ")
            
        dados = f"{nome}|{email}|{tipo.lower()}"
        return salvar_registro('usuarios.txt', dados)
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        return False

def main_loop():
    """Loop principal que integra todas as funções"""
    while True:
        try:
            print("\n=== Sistema de Gestão de Equipamentos ===")
            print("1. Registrar Chamado")
            print("2. Registrar Instalação")
            print("3. Registrar Equipamento")
            print("4. Registrar Ação")
            print("5. Gestão de Equipamento")
            print("6. Gestão de Usuário")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "0":
                print("Encerrando o sistema...")
                break
                
            elif opcao == "1":
                descricao = input("Descrição do chamado: ")
                while True:
                    prioridade = input("Prioridade (baixa/media/alta): ").lower()
                    if prioridade in ['baixa', 'media', 'alta']:
                        break
                    print("Prioridade inválida!")
                equipamento = input("Equipamento: ")
                atribuir_para = input("Atribuir para: ")
                
                if Chamado(descricao, prioridade, equipamento, atribuir_para):
                    print("Chamado registrado com sucesso!")
                
            elif opcao == "2":
                nome = input("Nome: ")
                endereco = input("Endereço: ")
                cidade = input("Cidade: ")
                estado = input("Estado: ")
                cep = input("CEP: ")
                descricao = input("Descrição: ")
                
                Instalacao(nome, endereco, cidade, estado, cep, descricao)
                print("Instalação registrada com sucesso!")
                
            elif opcao == "3":
                serie = input("Número de série: ")
                nome = input("Nome do equipamento: ")
                quantidade = int(input("Quantidade: "))
                descricao = input("Descrição: ")
                foto = input("Nome do arquivo de foto: ")
                local = input("Local: ")
                
                Equipamento(serie, nome, quantidade, descricao, foto, local)
                print("Equipamento registrado com sucesso!")
                
            elif opcao == "4":
                equipamento = input("Equipamento: ")
                responsavel = input("Responsável: ")
                descobertas = input("Descobertas: ")
                status = input("Status (aberta/fechada/pendente): ")
                
                Acao(equipamento, responsavel, descobertas, status)
                print("Ação registrada com sucesso!")
                
            elif opcao == "5":
                id = input("ID: ")
                data = input("Data: ")
                descricao = input("Descrição: ")
                id_equipamento = input("ID do equipamento: ")
                
                Gestao_Equipamento(id, data, descricao, id_equipamento)
                print("Gestão de equipamento registrada com sucesso!")
                
            elif opcao == "6":
                nome = input("Nome: ")
                email = input("Email: ")
                tipo = input("Tipo (admin/inspector/tecnico): ")
                
                Gestao_Usuario(nome, email, tipo)
                print("Usuário registrado com sucesso!")
                
            else:
                print("Opção inválida!")
                
        except ValueError as e:
            print(f"Erro de valor: {e}")
        except Exception as e:
            print(f"Erro: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main_loop()