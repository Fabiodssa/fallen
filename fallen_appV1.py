from datetime import datetime
import os

"""
Pontos de melhora: quando for um usuario de admin
    - na em editar usuarios deve listar e mostrar uma lista numerada com todos os
    usuarios, então o usuario deve escolher um usuario da lista para fazer a mudança,
    além disso para a cada edição deve ter uma mensagem de confirmação, se for sim ira fazer a mudança,
    se for não, não ira fazer
    - em editar e excluir usuarios deve poder fazer a pesquisa por nome ou por email, alem disso,
    em excluir deve ter uma mensagem de confirmação antes de excluir o usuario
"""

def get_file_path(arquivo):
    """Retorna o caminho completo do arquivo na pasta fallen"""
    pasta_fallen = 'fallen'
    
    # Cria a pasta fallen se não existir
    if not os.path.exists(pasta_fallen):
        os.makedirs(pasta_fallen)
        
    return os.path.join(pasta_fallen, arquivo)

def get_next_id(arquivo):
    """Retorna o próximo ID disponível para o arquivo"""
    arquivo_path = get_file_path(arquivo)
    try:
        if not os.path.exists(arquivo_path):
            return 1
            
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            if not linhas:
                return 1
            return len(linhas) + 1
    except:
        return 1

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
            
        # Se o usuário existe, registra o chamado
        data_abertura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Gera o próximo ID disponível
        id_chamado = get_next_id('chamado.txt')
        
        dados = f"{id_chamado}|{descricao}|{prioridade}|{data_abertura}|{equipamento}|{atribuir_para}"
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
                    print(f"Senha: {dados[2]}")
                    print(f'Tipo: {dados[3]}')
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
            # Lista os usuários disponíveis
            usuarios = listar_usuarios_numerados()
            if not usuarios:
                print("Nenhum usuário cadastrado.")
                continue
                
            try:
                escolha = int(input("\nDigite o número do usuário que deseja editar: ")) - 1
                if escolha < 0 or escolha >= len(usuarios):
                    print("Número inválido!")
                    continue
                
                usuario = usuarios[escolha]
                if editar_usuario(usuario[0], usuario[1], usuario[2], usuario[3]):
                    print("Usuário editado com sucesso!")
            except ValueError:
                print("Por favor, digite um número válido!")
                
        elif opcao == "4":
            # Lista os usuários disponíveis
            usuarios = listar_usuarios_numerados()
            if not usuarios:
                print("Nenhum usuário cadastrado.")
                continue
                
            try:
                escolha = input("\nDigite o número do usuário que deseja excluir: ")
                if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(usuarios):
                    print("Número inválido!")
                    continue
                
                if excluir_usuario(escolha):
                    print("Usuário excluído com sucesso!")
            except ValueError:
                print("Por favor, digite um número válido!")

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
            # Lista os equipamentos disponíveis
            equipamentos = listar_equipamentos_numerados()
            if not equipamentos:
                print("Nenhum equipamento cadastrado.")
                continue
                
            try:
                escolha = input("\nDigite o número do equipamento que deseja editar: ")
                if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(equipamentos):
                    print("Número inválido!")
                    continue
                
                if editar_equipamento(escolha):  # Passa o número escolhido diretamente
                    print("Equipamento editado com sucesso!")
            except ValueError:
                print("Por favor, digite um número válido!")
                
        elif opcao == "4":
            # Lista os equipamentos disponíveis
            equipamentos = listar_equipamentos_numerados()
            if not equipamentos:
                print("Nenhum equipamento cadastrado.")
                continue
                
            try:
                escolha = input("\nDigite o número do equipamento que deseja excluir: ")
                if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(equipamentos):
                    print("Número inválido!")
                    continue
                
                if excluir_equipamento(escolha):
                    print("Equipamento excluído com sucesso!")
            except ValueError:
                print("Por favor, digite um número válido!")

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
            
            # Validação da prioridade
            while True:
                prioridade = input("Prioridade (baixa/media/alta): ").lower()
                if prioridade in ['baixa', 'media', 'alta']:
                    break
                print("Prioridade inválida! Use: baixa, media ou alta")
            
            # Validação do equipamento
            equipamento = None
            while not equipamento:
                nome_equip = input("Equipamento: ")
                arquivo_path = get_file_path('equipamentos.txt')
                
                if os.path.exists(arquivo_path):
                    with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
                        for linha in arquivo:
                            dados = linha.strip().split('|')
                            if dados[1].lower() == nome_equip.lower():
                                equipamento = dados[1]  # Usa o nome exato do equipamento
                                break
                
                if not equipamento:
                    print(f"Equipamento '{nome_equip}' não encontrado.")
                    opcao = input("Deseja cadastrar? (S/N): ").upper()
                    
                    if opcao == 'S':
                        serie = input("Número de série: ")
                        while True:
                            try:
                                quantidade = int(input("Quantidade: "))
                                break
                            except ValueError:
                                print("Por favor, digite um número válido para quantidade.")
                        descricao_equip = input("Descrição: ")
                        foto = input("Nome do arquivo de foto: ")
                        local = input("Local: ")
                        
                        if Equipamento(serie, nome_equip, quantidade, descricao_equip, foto, local):
                            print("Equipamento cadastrado com sucesso!")
                            equipamento = nome_equip
                        else:
                            print("Erro ao cadastrar equipamento.")
                    else:
                        print("Operação cancelada.")
                        return
            
            # Validação do usuário
            while True:
                atribuir_para = input("Atribuir para: ")
                if verificar_usuario(atribuir_para):
                    break
                print("\nUsuário não encontrado!")
                print("Usuários disponíveis:")
                listar_nomes_usuarios()
                print()
            
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
            for i, linha in enumerate(f, 1):
                dados = linha.strip().split('|')
                print(f"{i}. Nome: {dados[0]}")
                print(f"   Email: {dados[1]}")
                print(f"   Tipo: {dados[3]}")
                print("-" * 30)
    else:
        print("Nenhum usuário cadastrado.")

# Funções auxiliares
def listar_usuarios_numerados():
    """Lista todos os usuários com numeração"""
    arquivo_path = get_file_path('usuarios.txt')
    usuarios = []
    
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Usuários Cadastrados ===")
            for i, linha in enumerate(f, 1):
                dados = linha.strip().split('|')
                print(f"{i}. Nome: {dados[0]}")
                print(f"   Email: {dados[1]}")
                print(f"   Tipo: {dados[3]}")
                print("-" * 30)
                usuarios.append(dados)
    else:
        print("Nenhum usuário cadastrado.")
    return usuarios

def buscar_usuario(termo_busca):
    """Busca usuário por nome ou email"""
    arquivo_path = get_file_path('usuarios.txt')
    usuarios = []
    
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            for linha in f:
                dados = linha.strip().split('|')
                if termo_busca.lower() in dados[0].lower() or termo_busca.lower() in dados[1].lower():
                    usuarios.append(dados)
    
    return usuarios

def editar_usuario(nome, email, senha, tipo):
    """Função para editar usuário"""
    arquivo_path = get_file_path('usuarios.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            
            encontrado = False
            for linha in f_in:
                dados = linha.strip().split('|')
                if dados[0] == nome:  # Encontrou o usuário para editar
                    encontrado = True
                    # Mostra dados atuais
                    print("\nDados atuais:")
                    print(f"Nome: {dados[0]}")
                    print(f"Email: {dados[1]}")
                    print(f"Tipo: {dados[3]}")
                    
                    # Solicita novos dados (ou mantém os atuais)
                    novo_nome = input("\nNovo nome (Enter para manter atual): ") or dados[0]
                    novo_email = input("Novo email (Enter para manter atual): ") or dados[1]
                    nova_senha = input("Nova senha (Enter para manter atual): ") or dados[2]
                    novo_tipo = input("Novo tipo (admin/inspector/tecnico) (Enter para manter atual): ") or dados[3]
                    
                    # Confirma alterações
                    print("\nConfirma as alterações?")
                    print(f"Nome: {novo_nome}")
                    print(f"Email: {novo_email}")
                    print(f"Tipo: {novo_tipo}")
                    
                    confirmacao = input("\nConfirmar alterações? (S/N): ").upper()
                    if confirmacao == 'S':
                        # Escreve a linha atualizada
                        f_out.write(f"{novo_nome}|{novo_email}|{nova_senha}|{novo_tipo}\n")
                        print("Alterações salvas com sucesso!")
                    else:
                        # Mantém os dados originais
                        f_out.write(linha)
                        print("Operação cancelada.")
                else:
                    # Mantém as outras linhas inalteradas
                    f_out.write(linha)
            
            if not encontrado:
                print("Usuário não encontrado!")
                return False
        
        # Substitui o arquivo original pelo temporário
        os.replace(temp_path, arquivo_path)
        return True
        
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")
        return False

def excluir_usuario(nome):
    """Função para excluir usuário"""
    arquivo_path = get_file_path('usuarios.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        # Lista todos os usuários numerados
        usuarios = listar_usuarios_numerados()
        
        if not usuarios:
            print("Nenhum usuário encontrado.")
            return False
        
        # Confirma exclusão
        print(f"\nTem certeza que deseja excluir o usuário?")
        print(f"Nome: {usuarios[int(nome)-1][0]}")
        print(f"Email: {usuarios[int(nome)-1][1]}")
        print(f"Tipo: {usuarios[int(nome)-1][3]}")
        
        confirmacao = input("\nConfirmar exclusão? (S/N): ").upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return False
        
        # Exclui o usuário
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for i, linha in enumerate(f_in):
                if i != int(nome)-1:  # Se não for o usuário selecionado, mantém no arquivo
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Usuário excluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return False

def listar_equipamentos_numerados():
    """Lista todos os equipamentos com numeração"""
    arquivo_path = get_file_path('equipamentos.txt')
    equipamentos = []
    
    if os.path.exists(arquivo_path):
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            print("\n=== Equipamentos Cadastrados ===")
            for i, linha in enumerate(f, 1):
                dados = linha.strip().split('|')
                print(f"{i}. Nome: {dados[1]}")
                print(f"   Série: {dados[0]}")
                print(f"   Quantidade: {dados[2]}")
                print(f"   Local: {dados[5]}")
                print("-" * 30)
                equipamentos.append(dados)
    else:
        print("Nenhum equipamento cadastrado.")
    return equipamentos

def excluir_equipamento(nome):
    """Função para excluir equipamento"""
    arquivo_path = get_file_path('equipamentos.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        # Lista todos os equipamentos numerados
        equipamentos = listar_equipamentos_numerados()
        
        if not equipamentos:
            print("Nenhum equipamento encontrado.")
            return False
        
        # Confirma exclusão
        print(f"\nTem certeza que deseja excluir o equipamento?")
        print(f"Nome: {equipamentos[int(nome)-1][1]}")
        print(f"Série: {equipamentos[int(nome)-1][0]}")
        print(f"Quantidade: {equipamentos[int(nome)-1][2]}")
        print(f"Local: {equipamentos[int(nome)-1][5]}")
        
        confirmacao = input("\nConfirmar exclusão? (S/N): ").upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return False
        
        # Exclui o equipamento
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for i, linha in enumerate(f_in):
                if i != int(nome)-1:  # Se não for o equipamento selecionado, mantém no arquivo
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Equipamento excluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao excluir equipamento: {e}")
        return False

def editar_equipamento(nome):
    """Função para editar equipamento"""
    arquivo_path = get_file_path('equipamentos.txt')
    temp_path = get_file_path('temp.txt')
    
    try:
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            
            encontrado = False
            for i, linha in enumerate(f_in):
                dados = linha.strip().split('|')
                if i == int(nome)-1:  # Encontrou o equipamento para editar pelo índice
                    encontrado = True
                    # Mostra dados atuais
                    print("\nDados atuais:")
                    print(f"Nome: {dados[1]}")
                    print(f"Série: {dados[0]}")
                    print(f"Quantidade: {dados[2]}")
                    print(f"Local: {dados[5]}")
                    
                    # Solicita novos dados (ou mantém os atuais)
                    novo_nome = input("\nNovo nome (Enter para manter atual): ") or dados[1]
                    nova_serie = input("Nova série (Enter para manter atual): ") or dados[0]
                    while True:
                        try:
                            nova_qtd = input("Nova quantidade (Enter para manter atual): ")
                            if nova_qtd == "":
                                nova_qtd = dados[2]
                                break
                            nova_qtd = int(nova_qtd)
                            break
                        except ValueError:
                            print("Por favor, digite um número válido para quantidade.")
                    nova_descricao = input("Nova descrição (Enter para manter atual): ") or dados[3]
                    nova_foto = input("Nova foto (Enter para manter atual): ") or dados[4]
                    novo_local = input("Novo local (Enter para manter atual): ") or dados[5]
                    
                    # Confirma alterações
                    print("\nConfirma as alterações?")
                    print(f"Nome: {novo_nome}")
                    print(f"Série: {nova_serie}")
                    print(f"Quantidade: {nova_qtd}")
                    print(f"Local: {novo_local}")
                    
                    confirmacao = input("\nConfirmar alterações? (S/N): ").upper()
                    if confirmacao == 'S':
                        # Escreve a linha atualizada
                        f_out.write(f"{nova_serie}|{novo_nome}|{nova_qtd}|{nova_descricao}|{nova_foto}|{novo_local}\n")
                        print("Alterações salvas com sucesso!")
                    else:
                        # Mantém os dados originais
                        f_out.write(linha)
                        print("Operação cancelada.")
                else:
                    # Mantém as outras linhas inalteradas
                    f_out.write(linha)
            
            if not encontrado:
                print("Equipamento não encontrado!")
                return False
        
        # Substitui o arquivo original pelo temporário
        os.replace(temp_path, arquivo_path)
        return True
        
    except Exception as e:
        print(f"Erro ao editar equipamento: {e}")
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
                    print(f"ID: {dados[0]}")
                    print(f"Descrição: {dados[1]}")
                    print(f"Prioridade: {dados[2]}")
                    print(f"Data: {dados[3]}")
                    print(f"Equipamento: {dados[4]}")
                    print(f"Responsável: {dados[5]}")
                    print(f"Status atual: {dados[2]}")
                    break
        
        if not chamado_encontrado:
            print("Chamado não encontrado!")
            return False
        
        # Solicita o novo status
        while True:
            novo_status = input("\nNovo status (aberto/em_andamento/fechado): ").lower()
            if novo_status in ['aberto', 'em_andamento', 'fechado']:
                break
            print("Status inválido!")
        
        # Confirma a alteração
        print("\nConfirma a alteração do status?")
        confirmacao = input("(S/N): ").upper()
        if confirmacao != 'S':
            print("Operação cancelada.")
            return False
        
        # Atualiza o arquivo com nova data e hora
        nova_data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                dados = linha.strip().split('|')
                if dados[0] == id_chamado:
                    dados[2] = novo_status  # Atualiza o status
                    dados[3] = nova_data    # Atualiza a data
                    f_out.write('|'.join(dados) + '\n')
                else:
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Status do chamado atualizado com sucesso!")
        print(f"Nova data/hora: {nova_data}")
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
                if dados[0] == id_chamado:  # Compara o ID
                    chamado_encontrado = True
                    print(f"\nChamado encontrado:")
                    print(f"ID: {dados[0]}")
                    print(f"Descrição: {dados[1]}")
                    print(f"Prioridade: {dados[2]}")
                    print(f"Data: {dados[3]}")
                    print(f"Equipamento: {dados[4]}")
                    print(f"Responsável: {dados[5]}")
                    
                    confirmacao = input("\nConfirmar exclusão? (S/N): ").upper()
                    if confirmacao != 'S':
                        print("Operação cancelada.")
                        return False
                    break
        
        if not chamado_encontrado:
            print("Chamado não encontrado!")
            return False
        
        # Exclui o chamado
        with open(arquivo_path, 'r', encoding='utf-8') as f_in, \
             open(temp_path, 'w', encoding='utf-8') as f_out:
            for linha in f_in:
                dados = linha.strip().split('|')
                if dados[0] != id_chamado:  # Mantém todos exceto o ID selecionado
                    f_out.write(linha)
        
        os.replace(temp_path, arquivo_path)
        print("Chamado excluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao excluir chamado: {e}")
        return False

def listar_nomes_usuarios():
    """Lista apenas os nomes dos usuários cadastrados"""
    arquivo_path = get_file_path('usuarios.txt')
    if os.path.exists(arquivo_path):
        print("\nUsuários disponíveis:")
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            for linha in f:
                dados = linha.strip().split('|')
                print(f"- {dados[0]}")

if __name__ == "__main__":
    main_loop()