from datetime import datetime
import os
import hashlib


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

def Gestao_Usuario(nome: str, email: str, senha: str, tipo: str):
    """Função para gestão de usuários"""
    try:
        while not validar_tipo_usuario(tipo):
            print("Tipo inválido! Deve ser: admin, inspector ou técnico")
            tipo = input("Digite o tipo novamente: ")
        
        dados = f"{nome}|{email}|{senha}|{tipo.lower()}"
        return salvar_registro('usuarios.txt', dados)
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        return False

def login():
    """Função para realizar login no sistema"""
    print("\n=== Login do Sistema ===")
    try:
        email = input("Email: ")
        senha = input("Senha: ")
        
        arquivo_path = get_file_path('usuarios.txt')
        
        if not os.path.exists(arquivo_path):
            print("Nenhum usuário cadastrado no sistema.")
            return None
            
        with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                dados = linha.strip().split('|')
                if dados[1] == email and dados[2] == senha:
                    return {'nome': dados[0], 'tipo': dados[3]}
        
        print("Email ou senha incorretos.")
        return None
        
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None

def menu_admin():
    """Menu para usuários admin"""
    while True:
        print("\n=== Menu Administrador ===")
        print("1. Ver todos os dados")
        print("2. Gerenciar usuários")
        print("3. Gerenciar equipamentos")
        print("4. Gerenciar chamados")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_todos_dados()
        elif opcao == "2":
            gerenciar_usuarios()
        elif opcao == "3":
            gerenciar_equipamentos()
        elif opcao == "4":
            gerenciar_chamados()

def menu_tecnico(usuario):
    """Menu para usuários técnicos"""
    while True:
        print("\n=== Menu Técnico ===")
        print("1. Ver equipamentos")
        print("2. Cadastrar equipamento")
        print("3. Registrar ação")
        print("4. Ver meus chamados")
        print("5. Ver meu perfil")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_equipamentos()
        elif opcao == "2":
            cadastrar_equipamento()
        elif opcao == "3":
            registrar_acao(usuario)
        elif opcao == "4":
            ver_meus_chamados(usuario)
        elif opcao == "5":
            ver_perfil(usuario)

def menu_inspetor():
    """Menu para usuários inspetores"""
    while True:
        print("\n=== Menu Inspetor ===")
        print("1. Ver todos os dados")
        print("2. Gerenciar equipamentos")
        print("3. Gerenciar chamados")
        print("4. Ver usuários")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_todos_dados()
        elif opcao == "2":
            gerenciar_equipamentos()
        elif opcao == "3":
            gerenciar_chamados()
        elif opcao == "4":
            ver_usuarios()

def ver_todos_dados():
    """Função para visualizar todos os dados do sistema"""
    arquivos = ['usuarios.txt', 'equipamentos.txt', 'chamado.txt', 'acao.txt']
    
    for arquivo in arquivos:
        arquivo_path = get_file_path(arquivo)
        print(f"\n=== Conteúdo de {arquivo} ===")
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print(f"Arquivo {arquivo} não encontrado.")

def ver_equipamentos():
    """Visualiza todos os equipamentos cadastrados"""
    arquivo_path = get_file_path('equipamentos.txt')
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Equipamentos Cadastrados ===")
            print(f.read())
    else:
        print("Nenhum equipamento cadastrado.")

def ver_meus_chamados(usuario):
    """Visualiza chamados atribuídos ao usuário"""
    arquivo_path = get_file_path('chamado.txt')
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Meus Chamados ===")
            for linha in f:
                if usuario in linha:
                    print(linha.strip())
    else:
        print("Nenhum chamado encontrado.")

def ver_perfil(usuario):
    """Visualiza informações do próprio perfil"""
    arquivo_path = get_file_path('usuarios.txt')
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            for linha in f:
                if usuario in linha:
                    dados = linha.strip().split('|')
                    print("\n=== Meu Perfil ===")
                    print(f"Nome: {dados[0]}")
                    print(f"Email: {dados[1]}")
                    print(f"Tipo: {dados[2]}")
                    break
    else:
        print("Perfil não encontrado.")

def criar_admin_padrao():
    """Cria um usuário admin padrão se não existir nenhum"""
    arquivo_path = get_file_path('usuarios.txt')
    
    try:
        # Verifica se já existe algum admin
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if 'admin' in linha:
                        return
        
        # Cria usuário admin padrão
        nome = "admin"
        email = "admin@sistema.com"
        senha = "admin123"
        tipo = "admin"
        
        # Formata a linha do usuário
        linha = f"{nome}|{email}|{senha}|{tipo}"
        
        with open(arquivo_path, 'a', encoding='utf-8') as f:
            f.write(linha + '\n')
            
        print("\nUsuário admin padrão criado:")
        print("Email: admin@sistema.com")
        print("Senha: admin123")
        
    except Exception as e:
        print(f"Erro ao criar admin padrão: {e}")

def main_loop():
    """Loop principal que integra todas as funções"""
    # Cria usuário admin padrão se necessário
    criar_admin_padrao()
    
    while True:
        usuario = login()
        if not usuario:
            continue
        
        print(f"\nBem-vindo, {usuario['nome']}!")
        
        if usuario['tipo'] == 'admin':
            menu_admin()
        elif usuario['tipo'] == 'tecnico':
            menu_tecnico(usuario['nome'])
        elif usuario['tipo'] == 'inspector':
            menu_inspetor()
        else:
            print("Tipo de usuário inválido!")

def gerenciar_usuarios():
    """Função para gerenciar usuários (apenas admin)"""
    while True:
        print("\n=== Gerenciamento de Usuários ===")
        print("1. Ver todos os usuários")
        print("2. Cadastrar novo usuário")
        print("3. Editar usuário")
        print("4. Excluir usuário")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_usuarios()
        elif opcao == "2":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            tipo = input("Tipo (admin/inspector/tecnico): ")
            if Gestao_Usuario(nome, email, senha, tipo):
                print("Usuário cadastrado com sucesso!")
        elif opcao == "3":
            nome = input("Nome do usuário a ser editado: ")
            if verificar_usuario(nome):
                email = input("Novo email: ")
                senha = input("Nova senha: ")
                tipo = input("Novo tipo (admin/inspector/tecnico): ")
                editar_usuario(nome, email, senha, tipo)
            else:
                print("Usuário não encontrado!")
        elif opcao == "4":
            nome = input("Nome do usuário a ser excluído: ")
            if excluir_usuario(nome):
                print("Usuário excluído com sucesso!")

def gerenciar_equipamentos():
    """Função para gerenciar equipamentos"""
    while True:
        print("\n=== Gerenciamento de Equipamentos ===")
        print("1. Ver todos os equipamentos")
        print("2. Cadastrar novo equipamento")
        print("3. Editar equipamento")
        print("4. Excluir equipamento")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_equipamentos()
        elif opcao == "2":
            cadastrar_equipamento()
        elif opcao == "3":
            nome = input("Nome do equipamento a ser editado: ")
            if verificar_equipamento(nome):
                editar_equipamento(nome)
            else:
                print("Equipamento não encontrado!")
        elif opcao == "4":
            nome = input("Nome do equipamento a ser excluído: ")
            if excluir_equipamento(nome):
                print("Equipamento excluído com sucesso!")

def gerenciar_chamados():
    """Função para gerenciar chamados"""
    while True:
        print("\n=== Gerenciamento de Chamados ===")
        print("1. Ver todos os chamados")
        print("2. Registrar novo chamado")
        print("3. Atualizar status do chamado")
        print("4. Excluir chamado")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            ver_todos_chamados()
        elif opcao == "2":
            descricao = input("Descrição do chamado: ")
            prioridade = input("Prioridade (baixa/media/alta): ")
            equipamento = input("Equipamento: ")
            atribuir_para = input("Atribuir para: ")
            if Chamado(descricao, prioridade, equipamento, atribuir_para):
                print("Chamado registrado com sucesso!")
        elif opcao == "3":
            id_chamado = input("ID do chamado: ")
            atualizar_status_chamado(id_chamado)
        elif opcao == "4":
            id_chamado = input("ID do chamado: ")
            if excluir_chamado(id_chamado):
                print("Chamado excluído com sucesso!")

def registrar_acao(usuario):
    """Função para registrar ação de um técnico"""
    print("\n=== Registrar Ação ===")
    try:
        equipamento = input("Equipamento: ")
        if not verificar_equipamento(equipamento):
            return False
            
        descobertas = input("Descobertas: ")
        while True:
            status = input("Status (aberta/fechada/pendente): ").lower()
            if status in ['aberta', 'fechada', 'pendente']:
                break
            print("Status inválido!")
            
        dados = f"{equipamento}|{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}|{usuario}|{descobertas}|{status}"
        if salvar_registro('acao.txt', dados):
            print("Ação registrada com sucesso!")
            return True
        return False
        
    except Exception as e:
        print(f"Erro ao registrar ação: {e}")
        return False

def ver_usuarios():
    """Função para visualizar usuários"""
    arquivo_path = get_file_path('usuarios.txt')
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Usuários Cadastrados ===")
            for linha in f:
                dados = linha.strip().split('|')
                print(f"Nome: {dados[0]}")
                print(f"Email: {dados[1]}")
                print(f"Tipo: {dados[2]}")
                print("-" * 30)
    else:
        print("Nenhum usuário cadastrado.")

# Funções auxiliares
def editar_usuario(nome, email, senha, tipo):
    """Função para editar usuário"""
    arquivo_path = get_file_path('usuarios.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                if nome in linha:
                    f_out.write(f"{nome}|{email}|{senha}|{tipo}\n")
                else:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Usuário editado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")
        return False

def excluir_usuario(nome):
    """Função para excluir usuário"""
    arquivo_path = get_file_path('usuarios.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                if nome not in linha:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        return True
        
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return False

def editar_equipamento(nome):
    """Função para editar equipamento"""
    arquivo_path = get_file_path('equipamentos.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        # Coleta os novos dados
        serie = input("Novo número de série: ")
        while True:
            try:
                quantidade = int(input("Nova quantidade: "))
                break
            except ValueError:
                print("Por favor, digite um número válido para quantidade.")
        descricao = input("Nova descrição: ")
        foto = input("Novo nome do arquivo de foto: ")
        local = input("Novo local: ")
        
        # Atualiza o arquivo
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                if nome in linha:
                    f_out.write(f"{serie}|{nome}|{quantidade}|{descricao}|{foto}|{local}\n")
                else:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Equipamento editado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao editar equipamento: {e}")
        return False

def excluir_equipamento(nome):
    """Função para excluir equipamento"""
    arquivo_path = get_file_path('equipamentos.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        # Verifica se há chamados abertos para este equipamento
        chamados_path = get_file_path('chamado.txt')
        if os.path.exists(chamados_path):
            with open(chamados_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    if nome in linha and 'aberta' in linha.lower():
                        print("Não é possível excluir equipamento com chamados abertos!")
                        return False
        
        # Exclui o equipamento
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                if nome not in linha:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Equipamento excluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao excluir equipamento: {e}")
        return False

def ver_todos_chamados():
    """Função para visualizar todos os chamados"""
    arquivo_path = get_file_path('chamado.txt')
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Chamados Registrados ===")
            for linha in f:
                dados = linha.strip().split('|')
                print(f"Descrição: {dados[0]}")
                print(f"Prioridade: {dados[1]}")
                print(f"Data: {dados[2]}")
                print(f"Equipamento: {dados[3]}")
                print(f"Responsável: {dados[4]}")
                print("-" * 30)
    else:
        print("Nenhum chamado registrado.")

def atualizar_status_chamado(id_chamado):
    """Função para atualizar o status de um chamado"""
    arquivo_path = get_file_path('chamado.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        chamado_encontrado = False
        
        # Mostra o status atual
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            for linha in f:
                dados = linha.strip().split('|')
                if dados[0] == id_chamado:
                    chamado_encontrado = True
                    print(f"\nChamado encontrado:")
                    print(f"Descrição: {dados[0]}")
                    print(f"Status atual: {dados[1]}")
                    break
        
        if not chamado_encontrado:
            print("Chamado não encontrado!")
            return False
        
        # Solicita o novo status
        while True:
            novo_status = input("Novo status (aberto/em_andamento/fechado): ").lower()
            if novo_status in ['aberto', 'em_andamento', 'fechado']:
                break
            print("Status inválido!")
        
        # Atualiza o arquivo
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f:
                dados = linha.strip().split('|')
                if dados[0] == id_chamado:
                    dados[1] = novo_status
                    f_out.write('|'.join(dados) + '\n')
                else:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Status do chamado atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao atualizar status do chamado: {e}")
        return False

def excluir_chamado(id_chamado):
    """Função para excluir um chamado"""
    arquivo_path = get_file_path('chamado.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        chamado_encontrado = False
        
        # Verifica se o chamado existe e não está em andamento
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            for linha in f:
                dados = linha.strip().split('|')
                if dados[0] == id_chamado:
                    chamado_encontrado = True
                    if dados[1] == 'em_andamento':
                        print("Não é possível excluir um chamado em andamento!")
                        return False
                    break
        
        if not chamado_encontrado:
            print("Chamado não encontrado!")
            return False
        
        # Exclui o chamado
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f:
                dados = linha.strip().split('|')
                if dados[0] != id_chamado:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Chamado excluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao excluir chamado: {e}")
        return False

if __name__ == "__main__":
    main_loop()