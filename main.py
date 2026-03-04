import random
import time
import json
import os
import msvcrt

def seletor(opcoes, formatar_opcao, apresentacao="Use as setas para cima/baixo e Enter para selecionar:\n"):
    indice_atual = 0
    filtro = ""
    while True:
        # Limpa a tela (funciona no Windows)
        os.system('cls')
        print(apresentacao)
        
        if filtro and len(filtro) > 0:
            opcoes_filtradas = [obj for obj in opcoes if filtro.lower() in formatar_opcao(obj).lower()]
        else:
            opcoes_filtradas = opcoes
        
        # Exibe todas as opções, destacando a atual com '>'
        for i, obj in enumerate(opcoes_filtradas):
            linha = formatar_opcao(obj)
            if i == indice_atual:
                print(f"{linha}")
                print("\nUse as setas ↑↓ para navegar, Enter para selecionar")

        # Captura a tecla pressionada
        tecla = msvcrt.getch()
        
        if tecla == b'\r':  # Enter
            return opcoes[indice_atual]
        elif tecla == b'\xe0':  # Tecla especial (setas)
            tecla2 = msvcrt.getch()
            if tecla2 == b'H':  # Seta para cima
                indice_atual = (indice_atual - 1) % len(opcoes_filtradas)
            elif tecla2 == b'P':  # Seta para baixo
                indice_atual = (indice_atual + 1) % len(opcoes_filtradas)
        elif tecla == b'\x1b':  # Esc para sair
            filtro = ""
            indice_atual = 0
        elif tecla == b'\x08':  # Backspace para apagar o filtro
            filtro = filtro[:-1]
            indice_atual = 0
        elif 32 <= tecla[0] <= 126:  # Caracteres imprimíveis
            filtro += tecla.decode('ascii', errors='ignore')
            indice_atual = 0
    
class GeradorPersonagem:
    def __init__(self):
        with open('./base_dados/especie.json', 'r', encoding='utf-8') as f:
            self.especies = json.load(f)
            print(f"Carregadas {len(self.especies)} espécies do arquivo JSON.")
        with open('./base_dados/genero.json', 'r', encoding='utf-8') as f:
            self.generos = json.load(f)
            self.generos_binarios =  self.generos["genero_binarios"]
            self.generos_nao_binarios = self.generos["genero_nao_binarios"]
            print(f"Carregados {len(self.generos_binarios)+len(self.generos_nao_binarios)} gêneros do arquivo JSON.")
        with open('./base_dados/caracteristicas_fisicas.json', 'r', encoding='utf-8') as f:
            self.caracteristicas = json.load(f)
            print(f"Carregadas {len(self.caracteristicas['etnia'])} etnias do arquivo JSON.")
        with open('./base_dados/classe.json', 'r', encoding='utf-8') as f:
            self.classes = json.load(f)
            print(f"Carregadas {len(self.classes['classes'])} classes do arquivo JSON.")
    
    def calcular_chance_barba(self, genero):
        """Calcula a chance de ter barba com base no gênero"""
        if genero and genero["nome"]:
            nome_genero = genero["nome"].lower()
            if "masculino" in nome_genero or "genderqueer" in nome_genero or "bigénero" in nome_genero:
                return random.random() < 0.3  # 30% de chance
        return False  # para outros gêneros, não tem barba
    
    def avaliar_barba(self, rosto):
        """Avalia se o personagem tem barba com base no gênero e retorna a descrição apropriada"""
        tem_barba = rosto["barba"]["tem"]
        if tem_barba:
            return f"Barba: {rosto['barba']['presenca']}, estilo {rosto['barba']['estilos']}, textura {rosto['barba']['textura']}, cor {rosto['barba']['cor']}."
        else:
            return "(Sem barba.)"
    
    def avaliar_bigode(self, rosto):
        """Avalia se o personagem tem bigode com base no gênero e retorna a descrição apropriada"""
        tem_bigode = rosto["barba"]["tem"]
        if tem_bigode:
            return f"Bigode: {rosto['bigode']['presenca']}, estilo {rosto['bigode']['estilos']}, textura {rosto['bigode']['textura']}, cor {rosto['bigode']['cor']}."
        else:
            return "(Sem bigode.)"
       
    def avl_caract(self, caracteristica, template="{}"):
        """ Retorna o template formatado com a característica se ela for válida (não None),
        caso contrário retorna string vazia. """
        if caracteristica:
            return template.format(caracteristica)
        return ""

    def selecionar_com_nulo(self, opcoes, formatar_opcao, apresentacao="Use as setas para cima/baixo e Enter para selecionar:\n", label="Nulo"):
        isString = False
        if opcoes and isinstance(opcoes[0], str):
            placeholder = label
            isString = True
        else:
            placeholder = {"__none__": True, "nome": label, "descricao": ""}
        opcoes_com_nulo = [placeholder] + opcoes
        
        escolha = self.selecionar_com_aleatorio(opcoes_com_nulo, formatar_opcao, apresentacao)
        
        if isinstance(escolha, dict) and escolha.get("__none__"):
            return None
        if isString and escolha == label:
            return None
        
        return escolha
        
    def selecionar_com_aleatorio(self, opcoes, formatar_opcao, apresentacao="Use as setas para cima/baixo e Enter para selecionar:\n", label="Aleatório"):
        isString = False
        if opcoes and isinstance(opcoes[0], str):
            placeholder = label
            isString = True
        else:
            placeholder = {"__aleatorio__": True, "nome": label, "descricao": ""}

        opcoes_com = [placeholder] + opcoes

        def safe_format(obj):
            try:
                return formatar_opcao(obj)
            except Exception:
                if isinstance(obj, dict) and obj.get("__aleatorio__"):
                    return label
                return str(obj)

        escolha = seletor(opcoes_com, safe_format, apresentacao)

        if isinstance(escolha, dict) and escolha.get("__aleatorio__"):
            return random.choice(opcoes)
        if isString and escolha == label:
            return random.choice(opcoes)
        
        return escolha

    def formatar_descricao_personagem(self, genero, especie, classe, subclasse, idade, etinia, rosto, olhos, nariz, boca, cabelo, pele, corpo, fundo):
        """Retorna a string de descrição completa de um personagem. Pode ser reutilizada em qualquer  lugar desde que os campos sejam fornecidos. """
        texto = []
        texto.append(f"Gênero: {genero['nome']}")
        texto.append(f"Raça: {especie['nome']}")
        texto.append(f"Classe: {classe['classe']} - {subclasse['nome'] if subclasse else 'sem subclasse'}")
        texto.append(f"Idade: {idade} anos")
        texto.append("" + "=" * 70)
        texto.append(f"\nPersonagem de corpo inteiro, visto em ângulo de três quartos, em pé, sobre {fundo}.\nA iluminação é suave e difusa, proveniente de uma fonte frontal levemente superior, criando sombras suaves que modelam o corpo e o rosto.\nCores terrosas com toques de azul-acinzentado e metálicos, alto contraste e saturação moderada.\nEstilo de ilustração digital com traços nítidos e texturas realistas.\nO universo de Kreat é sugerido de forma abstrata por meio de padrões sutis no fundo ou na roupa, como runas estilizadas, engrenagens decorativas, ou motivos que mesclam orgânico e mecânico, sem representações explícitas de cenários.\n--- CARACTERÍSTICAS DA ESPÉCIE (PRIORIDADE MÁXIMA) ---\nEspécie: {especie['nome']}- {especie['descricao']}.\n(As características da espécie se sobrepõem a quaisquer traços humanos conflitantes.)\n--- DETALHES GERAIS ---\nGênero: {genero['nome']} ({genero['descricao']}).\nIdade: {idade} anos.\nEtnia: {etinia}.\n--- ROSTO ---\nFormato do rosto: {rosto['formato']['nome']} ({rosto['formato']['descricao']}).\n{self.avaliar_barba(rosto)}{self.avaliar_bigode(rosto)}\nDetalhes do rosto: {rosto['detalhes']}.\n--- OLHOS ---\nOlhos: formato {olhos['formato']}, cor {olhos['cor']}{self.avl_caract(olhos['insencidades_cor'], '-{}')}{self.avl_caract(olhos['efeito'], ' efeito: {}')}{self.avl_caract(olhos['condicoes'], ', concição: {}')}.\nCaracterísticas: {self.avl_caract(olhos['caracteristicas']['heterocromia'], 'heterocromia {},')} {self.avl_caract(olhos['caracteristicas']['anel_limbal'],'anel limbal {},')}{self.avl_caract(olhos['caracteristicas']['sardas_na_iris'],' sardas na íris {},')} {self.avl_caract(olhos['caracteristicas']['pupila'], 'pupila {}.')}\nCílios: {olhos['cilios']}.\nSobrancelhas: {olhos['sobrancelhas']}.\n--- NARIZ ---\nNariz: formato {nariz['formato']}, largura {nariz['largura']}, altura {nariz['altura']}, projeção {nariz['projecao']}.\nPonta: formato {nariz['ponta_formato']}, direção {nariz['ponta_direcao']}.\nlateral do nariz: largura {nariz['asas_largura']}, formato {nariz['asas_formato']}.\nNarinas: tamanho {nariz['narinas_tamanho']}, formato {nariz['narinas_formato']}, visibilidade {nariz['narinas_visibilidade']}.\n{self.avl_caract(nariz['detalhes_adicionais'],'Detalhes adicionais: {}.')}\n--- BOCA ---\nBoca: lábio superior {boca['labios_superior']}, lábio inferior {boca['labios_inferior']}, tamanho {boca['tamanho']}.\nArco do cupido: {boca['arco_cupido']}, comissuras {boca['comissuras']}.\nTextura: {boca['textura']}, {self.avl_caract(boca['cor'],' cor {},')}{self.avl_caract(boca['detalhes_especiais'],'detalhes especiais{}.')}\n--- CABELO ---\nCabelo: tipo{cabelo['tipo']}, comprimento{cabelo['comprimento']}, estilo{cabelo['estilo']}, penteado{cabelo ['penteado']}.\nTextura: {cabelo ['textura']}, cor{cabelo ['cor']},{self.avl_caract(cabelo ['acessorio'], ' acessórios{}.')}\n--- PELE ---\nPele: tom{pele ['tom']}, textura{pele ['textura']}, 	{self.avl_caract(pele ['marcas'],'marcas {}.')}\n{self.avl_caract(pele ['caracteristicas_especiais'],'Características especiais: {}.')}\n{self.avl_caract(pele ['condicoes_temporarias'],'Condições temporárias:{}.')}\n--- CORPO ---\nCorpo: altura{corpo ['altura']}, peso{corpo ['peso']}, biotipo{corpo ['somatotipo']}, forma{corpo ['forma']}.\nMusculatura:{corpo ['musculatura']}, gordura{corpo ['gordura']}.\nEstrutura óssea:{corpo ['estrutura_ossea']}, proporções{corpo ['proporcoes']}.\nTipo híbrido:{corpo ['tipos_hibridos']}.\n{self.avl_caract(corpo ['caracteristicas_especiais'], 'Características especiais: {}.')}\n{self.avl_caract(corpo ['condicoes_temporarias'], ' Condições temporárias:{}.')}\n--- CLASSE E EQUIPAMENTOS ---\nClasse:{subclasse ['nome']} . \nDescrição:{subclasse ['descricao']} . \nVestimenta:{subclasse ['vestimenta']} . \nItens marcantes:{subclasse ['itens_marcantes']} . \n--ar 2 : 3")

        return "\n".join(texto)
      
    def selecionar_e_registrar(self, opcoes, formatar_opcao, pergunta, mensagem, permite_nulo=False):
        global apresentacao
        if permite_nulo:
            valor = self.selecionar_com_nulo(opcoes, formatar_opcao, apresentacao + pergunta)
        else:
            valor = self.selecionar_com_aleatorio(opcoes, formatar_opcao, apresentacao + pergunta)
        
        apresentacao += mensagem.format(formatar_opcao(valor))
        print(apresentacao)
        return valor
        
    def gerar(self):
        """Gera um personagem completo aleatoriamente"""
        # 1. Raça (para influenciar características)
        especie = random.choice(self.especies)
        # 2. Gênero (para influenciar nome e características)
        genero = random.choice(self.generos_binarios)
        # 3. Idade (para influenciar aparência e vestuário)
        if genero and genero["nome"] and genero["nome"] == "não binário":
            genero = random.choice(self.generos_nao_binarios)
        idade = random.randint(20, 70)
        etinia = random.choice(self.caracteristicas["etnia"])
        classe = random.choice(self.classes["classes"])
        subclasse = random.choice(classe["subclasses"]) if classe["subclasses"] else None
        # se o genero tiver masculino no nome, genderqueer ou bigénero ele deve ter 30% de chance de ter barba, se não, não deve ter
        tem_barba = self.calcular_chance_barba(genero)
        cor_cabelo = random.choice(self.caracteristicas["cabelo"]["cor"])
        cabelo_tipo = random.choice(self.caracteristicas["cabelo"]["tipo"])
        cabelo = {
            "cor": cor_cabelo,
            "tipo": cabelo_tipo["nome"],
            "descricao": cabelo_tipo["descricao"],
            "estilo": random.choice(cabelo_tipo["estilos"]),
            "comprimento": random.choice(self.caracteristicas["cabelo"]["comprimento"]),
            "penteado": random.choice(self.caracteristicas["cabelo"]["penteado"]),
            "textura": random.choice(self.caracteristicas["cabelo"]["textura"]),
            "acessorio": None if random.random() < 0.8 else random.choice(self.caracteristicas["cabelo"]["acessorios"]),
        }
        rosto = {
            "formato": random.choice(self.caracteristicas["rosto"]["formato"]),
            "barba": {
                "tem": tem_barba,
                "presenca": random.choice(self.caracteristicas["rosto"]["barba"]["presenca"]),
                "estilos": random.choice(self.caracteristicas["rosto"]["barba"]["estilos"]),
                "textura": random.choice(self.caracteristicas["rosto"]["barba"]["textura"]),
                "cor": cor_cabelo if random.random() < 0.95 else random.choice(self.caracteristicas["cabelo"]["cor"]), 
            },
            "bigode": {
                "tem": tem_barba,
                "presenca": random.choice(self.caracteristicas["rosto"]["bigode"]["presenca"]),
                "estilos": random.choice(self.caracteristicas["rosto"]["bigode"]["estilos"]),
                "textura": random.choice(self.caracteristicas["rosto"]["bigode"]["textura"]),
                "cor": cor_cabelo if random.random() < 0.95 else random.choice(self.caracteristicas["cabelo"]["cor"]), 
            },
            "detalhes": random.choice(self.caracteristicas["rosto"]["detalhes_adicionais"]),
        }
        olhos = {
            "formato": random.choice(self.caracteristicas["olhos"]["formato"]),
            "cor": random.choice(self.caracteristicas["olhos"]["cor"]),
            "insencidades_cor": None if random.random() < 0.9 else random.choice(self.caracteristicas["olhos"]["insencidades_cor"]),
            "efeito": None if random.random() < 0.9 else random.choice(self.caracteristicas["olhos"]["efeitos"]),
            "caracteristicas": {
                "heterocromia": None if random.random() < 0.999 else random.choice(self.caracteristicas["olhos"]["caracteristicas_especiais"]["heterocromia"]),
                "anel_limbal": None if random.random() < 0.6 else random.choice(self.caracteristicas["olhos"]["caracteristicas_especiais"]["anel_limbal"]),
                "sardas_na_iris": None if random.random() < 0.3 else random.choice(self.caracteristicas["olhos"]["caracteristicas_especiais"]["sardas_na_iris"]),
                "pupila": None if random.random() < 0.5 else random.choice(self.caracteristicas["olhos"]["caracteristicas_especiais"]["pupila"]),
            },
            "condicoes": None if random.random() < 0.6 else random.choice(self.caracteristicas["olhos"]["condicoes"]),
            "cilios": random.choice(self.caracteristicas["olhos"]["detalhes_adicionais"]["cilios"]),
            "sobrancelhas": random.choice(self.caracteristicas["olhos"]["detalhes_adicionais"]["sobrancelhas"]["formato"]),
        }
        nariz = {
            "formato": random.choice(self.caracteristicas["nariz"]["formato"]),
            "largura": random.choice(self.caracteristicas["nariz"]["largura"]),
            "altura": random.choice(self.caracteristicas["nariz"]["altura"]),
            "projecao": random.choice(self.caracteristicas["nariz"]["projecao"]),
            "ponta_formato": random.choice(self.caracteristicas["nariz"]["ponta"]["formato"]),
            "ponta_direcao": random.choice(self.caracteristicas["nariz"]["ponta"]["direcao"]),
            "asas_largura": random.choice(self.caracteristicas["nariz"]["asas"]["largura"]),
            "asas_formato": random.choice(self.caracteristicas["nariz"]["asas"]["formato"]),
            "narinas_tamanho": random.choice(self.caracteristicas["nariz"]["narinas"]["tamanho"]),
            "narinas_formato": random.choice(self.caracteristicas["nariz"]["narinas"]["formato"]),
            "narinas_visibilidade": random.choice(self.caracteristicas["nariz"]["narinas"]["visibilidade"]),
            "detalhes_adicionais": None if random.random() < 0.3 else random.choice(self.caracteristicas["nariz"]["detalhes_adicionais"]),
        }
        boca = {
            "labios_superior": random.choice(self.caracteristicas["boca"]["labios"]["superior"]),
            "labios_inferior": random.choice(self.caracteristicas["boca"]["labios"]["inferior"]),
            "tamanho": "média" if random.random() < 0.5 else random.choice(self.caracteristicas["boca"]["tamanho"]),
            "arco_cupido": random.choice(self.caracteristicas["boca"]["arco_cupido"]),
            "comissuras": "neutras" if random.random() < 0.5 else random.choice(self.caracteristicas["boca"]["comissuras"]),
            "textura": random.choice(self.caracteristicas["boca"]["textura"]),
            "cor": None if random.random() < 0.5 else random.choice(self.caracteristicas["boca"]["cor"]),
            "detalhes_especiais": None if random.random() < 0.8 else random.choice(self.caracteristicas["boca"]["detalhes_especiais"]),
        }
        pele = {
            "tom": random.choice(self.caracteristicas["pele"]["tom"]),
            "textura": random.choice(self.caracteristicas["pele"]["textura"]),
            "marcas": None if random.random() < 0.6 else random.choice(self.caracteristicas["pele"]["marcas"]),
            "caracteristicas_especiais": None if random.random() < 0.8 else random.choice(self.caracteristicas["pele"]["caracteristicas_especiais"]),
            "condicoes_temporarias": None if random.random() < 0.8 else random.choice(self.caracteristicas["pele"]["condicoes_temporarias"]),
            
        }
        corpo = {
            "altura": random.choice(self.caracteristicas["corpo"]["altura"]),
            "peso": random.choice(self.caracteristicas["corpo"]["peso"]),
            "somatotipo": random.choice(self.caracteristicas["corpo"]["somatotipo"]),
            "forma": random.choice(self.caracteristicas["corpo"]["forma"]),
            "musculatura": random.choice(self.caracteristicas["corpo"]["musculatura"]),
            "gordura": random.choice(self.caracteristicas["corpo"]["gordura"]),
            "estrutura_ossea": random.choice(self.caracteristicas["corpo"]["estrutura_ossea"]),
            "proporcoes": random.choice(self.caracteristicas["corpo"]["proporcoes"]),
            "tipos_hibridos": random.choice(self.caracteristicas["corpo"]["tipos_hibridos"]),
            "caracteristicas_especiais": None if random.random() < 0.8 else random.choice(self.caracteristicas["corpo"]["caracteristicas_especiais"]),
            "condicoes_temporarias": None if random.random() < 0.99 else random.choice(self.caracteristicas["corpo"]["condicoes_temporarias"]),
        }
        fundo = "fundo branco infinito"
        # uso do método reutilizável para gerar todo o texto de descrição
        
        descricaoPersonagem = self.formatar_descricao_personagem( genero, especie, classe, subclasse, idade, etinia, rosto, olhos, nariz, boca, cabelo, pele, corpo, fundo )
        print(descricaoPersonagem)
    
    def montar(self):
        global apresentacao
        """Permite ao usuário personalizar um personagem escolhendo características específicas"""
        # 1. Raça (para influenciar características)
        def formato(obj):
            return f"{obj['nome']}"
        def formatoString(obj):            
            return f"{obj}"
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "ESPÉCIE\n\n"
        # Seleciona espécie (com opção 'Aleatório' na primeira posição)
        especie = self.selecionar_e_registrar(self.especies, formato, "Selecione uma opção para Raça:\n", "Raça selecionada: {}\n")
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "GÊNERO\n\n"
        # 2. Gênero (para influenciar nome e características)
        todos_generos = [g for g in self.generos_binarios + self.generos_nao_binarios if not ( g['nome'] == "não binário" and g['descricao'] == "")]  
        # Exclui o gênero "não binário" específico para a seleção personalizada
        genero = self.selecionar_e_registrar(todos_generos, formato, "Selecione uma opção para Gênero:\n", "Gênero selecionado: {}\n")
        tem_barba = self.calcular_chance_barba(genero)
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "IDADE\n\n"
        # 3. Idade (para influenciar aparência e vestuário)
        idades = [{"nome": f"{i} anos", "valor": i} for i in range(20, 71, 5)]
        idade = self.selecionar_e_registrar(idades, formato, "Selecione uma opção para Idade:\n", "Idade selecionada: {} anos\n")
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "ETNIA\n\n"
        #4. Etnia
        etinia = self.selecionar_e_registrar(self.caracteristicas["etnia"], formatoString, "Selecione uma opção para Etnia:\n", "Etnia selecionada: {}\n")
        #5. Classe e subclasse
        classe = self.selecionar_e_registrar(self.classes["classes"], lambda obj: obj["classe"], "Selecione uma opção para Classe:\n", "Classe selecionada: {}\n")
        subclasse = self.selecionar_e_registrar(classe["subclasses"], lambda obj: obj["nome"], "Selecione uma opção para Subclasse:\n", "Subclasse selecionada: {}\n") if classe["subclasses"] else None
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "ROSTO\n\n"
        #6. Rosto
        rosto = {
            "formato": "",
            "barba": { "tem": False, "presenca": "", "estilos": "", "textura": "", "cor": "" },
            "bigode": { "tem": False, "presenca": "", "estilos": "", "textura": "", "cor": "" },
            "detalhes": ""
        }
        rosto["formato"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["formato"], lambda obj: obj["nome"], "Selecione uma opção para Formato do Rosto:\n", "Rosto formato selecionado: {}\n")
        cor_cabelo = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["cor"], lambda obj: obj, "Selecione uma opção para Cor do Cabelo:\n", "Cor cabelo selecionada: {}\n")
        """Pergunta se o usuário quer barba/bigode (se o gênero permite)
        Oferece opção de escolher se quer barba/bigode ou não"""
        opcoes_barba = [
            {"nome": "Sim, com barba/bigode", "valor": True},
            {"nome": "Não, sem barba/bigode", "valor": False}
        ]
        
        escolha_barba = self.selecionar_e_registrar(opcoes_barba, lambda obj: obj["nome"], "Este gênero pode ter barba/bigode. Deseja incluir?\n", "Barba/bigode:{}\n")
        
        tem_barba = escolha_barba["valor"]
        apresentacao += f"Barba/bigode: {'Sim' if tem_barba else 'Não'}\n"
        if tem_barba:
            rosto["barba"]["tem"] = True
            rosto["barba"]["presenca"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["barba"]["presenca"], lambda obj: obj, "Selecione uma opção para Presença da Barba:\n", "Barba presença: {}\n")
            rosto["barba"]["estilos"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["barba"]["estilos"], lambda obj: obj, "Selecione uma opção para Estilo da Barba:\n", "Barba estilo: {}\n")
            rosto["barba"]["textura"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["barba"]["textura"], lambda obj: obj, "Selecione uma opção para Textura da Barba:\n", "Barba textura: {}\n")
            rosto["barba"]["cor"] = self.selecionar_e_registrar([cor_cabelo] + self.caracteristicas["cabelo"]["cor"], lambda obj: obj, "Selecione uma opção para Cor da Barba:\n", "Cor da barba: {}\n")
            rosto["bigode"]["tem"] = True
            rosto["bigode"]["presenca"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["bigode"]["presenca"], lambda obj: obj, "Selecione uma opção para Presença do Bigode:\n", "Presença do Bigode: {}\n")
            rosto["bigode"]["estilos"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["bigode"]["estilos"], lambda obj: obj, "Selecione uma opção para Estilo do Bigode:\n", "Estilo do Bigode: {}\n")
            rosto["bigode"]["textura"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["bigode"]["textura"], lambda obj: obj, "Selecione uma opção para Textura do Bigode:\n", "Textura do Bigode: {}\n")
            rosto["bigode"]["cor"] = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["cor"], lambda obj: obj, "Selecione uma opção para Cor do Bigode:\n", "Cor do Bigode: {}\n")
        rosto["detalhes"] = self.selecionar_e_registrar(self.caracteristicas["rosto"]["detalhes_adicionais"], lambda obj: obj, "Selecione uma opção para Detalhes do Rosto:\n", "Detalhes do Rosto: {}\n")
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "OLHOS\n\n"
        #7. Olhos
        olhos = {
            "formato": None,
            "cor": None,
            "insencidades_cor": None,
            "efeito": None,
            "caracteristicas": {
                "heterocromia": None,
                "anel_limbal": None,
                "sardas_na_iris": None,
                "pupila": None
            },
            "condicoes": None,
            "cilios": None,
            "sobrancelhas": None, 
        }
        olhos["formato"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["formato"], lambda obj: obj, "Selecione uma opção para o Formato do Olhos:\n", "Olhos formato selecionado: {}\n")
        olhos["cor"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["cor"], lambda obj: obj, "Selecione uma opção para o Cor do Olhos:\n", "Olhos cor selecionado: {}\n")
        olhos["insencidades_cor"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["insencidades_cor"], lambda obj: obj, "Selecione uma opção para a insencidade da cor do Olhos:\n", "Olhos insencidades da cor selecionado: {}\n", True)
        olhos["efeito"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["efeitos"], lambda obj: obj, "Selecione uma opção para a efeito do Olhos:\n", "Olhos efeito selecionado: {}\n", True)
        olhos["caracteristicas"]["heterocromia"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["caracteristicas_especiais"]["heterocromia"], lambda obj: obj, "Selecione uma opção para a caracteristica de Heterocromia:\n", "Olhos caracteristicas heterocromia selecionado: {}\n", True)
        olhos["caracteristicas"]["anel_limbal"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["caracteristicas_especiais"]["anel_limbal"], lambda obj: obj, "Selecione uma opção para a caracteristica de anel limbal:\n", "Olhos caracteristicas anel limbal selecionado: {}\n", True)
        olhos["caracteristicas"]["sardas_na_iris"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["caracteristicas_especiais"]["sardas_na_iris"], lambda obj: obj, "Selecione uma opção para a caracteristica de sardas na iris:\n", "Olhos caracteristicas sardas na iris selecionado: {}\n", True)
        olhos["caracteristicas"]["pupila"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["caracteristicas_especiais"]["pupila"], lambda obj: obj, "Selecione uma opção para a caracteristica de pupila:\n", "Olhos caracteristicas pupila selecionado: {}\n", True)
        olhos["condicoes"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["condicoes"], lambda obj: obj, "Selecione uma opção condição no olho:\n", "Olhos condição selecionado: {}\n", True)
        olhos["cilios"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["detalhes_adicionais"]["cilios"], lambda obj: obj, "Selecione uma opção de cilios:\n", "Olhos cilios selecionado: {}\n", True)
        olhos["sobrancelhas"] = self.selecionar_e_registrar(self.caracteristicas["olhos"]["detalhes_adicionais"]["sobrancelhas"]["formato"], lambda obj: obj, "Selecione uma opção de sobrancelhas:\n", "Olhos sobrancelhas selecionadas: {}\n", True)
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "NARIZ\n\n"
        #8. Nariz
        nariz = {
            "formato" : None,
            "largura" : None,
            "altura" : None,
            "projecao" : None,
            "ponta_formato" : None,
            "ponta_direcao" : None,
            "asas_largura" : None,
            "asas_formato" : None,
            "narinas_tamanho" : None,
            "narinas_formato" : None,
            "narinas_visibilidade" : None,
            "detalhes_adicionais" : None
        }
        nariz['formato'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["formato"], lambda obj: obj, "Selecione uma opção para o formato do nariz:\n", "Nariz formato selecionado: {}\n")
        nariz['largura'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["largura"], lambda obj: obj, "Selecione uma opção para o largura do nariz:\n", "Nariz largura selecionado: {}\n")
        nariz['altura'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["altura"], lambda obj: obj, "Selecione uma opção para o altura do nariz:\n", "Nariz altura selecionado: {}\n")
        nariz['projecao'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["projecao"], lambda obj: obj, "Selecione uma opção para o projecao do nariz:\n", "Nariz projecao selecionado: {}\n")
        nariz['ponta_formato'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["ponta"]["formato"], lambda obj: obj, "Selecione uma opção para o ponta formato do nariz:\n", "Nariz ponta formato selecionado: {}\n")
        nariz['ponta_direcao'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["ponta"]["direcao"], lambda obj: obj, "Selecione uma opção para o ponta direção do nariz:\n", "Nariz ponta direção selecionado: {}\n")
        nariz['asas_largura'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["asas"]["largura"], lambda obj: obj, "Selecione uma opção para o asas largura do nariz:\n", "Nariz asas largura selecionado: {}\n")
        nariz['asas_formato'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["asas"]["formato"], lambda obj: obj, "Selecione uma opção para o asas formato do nariz:\n", "Nariz asas formato selecionado: {}\n")
        nariz['narinas_tamanho'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["narinas"]["tamanho"], lambda obj: obj, "Selecione uma opção para o narinas tamanho do nariz:\n", "Nariz narinas tamanho selecionado: {}\n")
        nariz['narinas_formato'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["narinas"]["formato"], lambda obj: obj, "Selecione uma opção para o narinas formato do nariz:\n", "Nariz narinas formato selecionado: {}\n")
        nariz['narinas_visibilidade'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["narinas"]["visibilidade"], lambda obj: obj, "Selecione uma opção para o narinas visibilidade do nariz:\n", "Nariz narinas visibilidade selecionado: {}\n")
        nariz['narinas_adicionais'] = self.selecionar_e_registrar(self.caracteristicas["nariz"]["detalhes_adicionais"], lambda obj: obj, "Selecione uma opção para o detalhes adicionais do nariz:\n", "Nariz detalhes adicionais selecionado: {}\n")
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "BOCA\n\n"
        #9. Boca
        boca = {
            "labios_superior": None,
            "labios_inferior": None,
            "tamanho": None,
            "arco_cupido": None,
            "comissuras": None,
            "textura": None,
            "cor": None,
            "detalhes_especiais": None
        }
        boca['labios_superior'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["labios"]["superior"], lambda obj: obj, "Selecione uma opção para o labio superior da boca:\n", "Boca labio superior selecionado: {}\n")
        boca['labios_inferior'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["labios"]["inferior"], lambda obj: obj, "Selecione uma opção para o labio inferior da boca:\n", "Boca labio inferior selecionado: {}\n")
        boca['arco_cupido'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["arco_cupido"], lambda obj: obj, "Selecione uma opção para o arco do cupido na boca:\n", "Boca arco do cupido selecionado: {}\n")
        boca['comissuras'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["comissuras"], lambda obj: obj, "Selecione uma opção para o comissuras na boca:\n", "Boca comissuras selecionado: {}\n")
        boca['textura'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["textura"], lambda obj: obj, "Selecione uma opção para o textura na boca:\n", "Boca textura selecionado: {}\n")
        boca['cor'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["cor"], lambda obj: obj, "Selecione uma opção para o cor na boca:\n", "Boca cor selecionado: {}\n")
        boca['detalhes_especiais'] = self.selecionar_e_registrar(self.caracteristicas["boca"]["detalhes_especiais"], lambda obj: obj, "Selecione uma opção para o detalhes especiais na boca:\n", "Boca detalhes especiais selecionado: {}\n")
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "CABELO\n\n"
        #10. Cabelo
        cabelo_tipo = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["tipo"], lambda obj: obj["nome"], "Selecione um tipo para o cabelo:\n", "Tipo de cabelo selecionado: {}\n")
        cabelo = {
            "cor": cor_cabelo,
            "tipo": cabelo_tipo["nome"],
            "descricao": cabelo_tipo["descricao"],
            "estilo": None,
            "comprimento": None,
            "penteado": None,
            "textura": None,
            "acessorio": None
        }
        cabelo['estilo'] = self.selecionar_e_registrar(cabelo_tipo["estilos"], lambda obj: obj, "Selecione uma opção o estilo do cabelo:\n", "Cabelo estilo selecionado: {}\n")
        cabelo['comprimento'] = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["comprimento"], lambda obj: obj, "Selecione uma opção de cabelo comprimento:\n", "Cabelo comprimento selecionado: {}\n")
        cabelo['penteado'] = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["penteado"], lambda obj: obj, "Selecione uma opção de cabelo penteado:\n", "Cabelo penteado selecionado: {}\n")
        cabelo['textura'] = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["textura"], lambda obj: obj, "Selecione uma opção de cabelo textura:\n", "Cabelo textura selecionado: {}\n")
        cabelo['acessorio'] = self.selecionar_e_registrar(self.caracteristicas["cabelo"]["acessorios"], lambda obj: obj, "Selecione uma opção de cabelo acessorio:\n", "Cabelo acessorio selecionado: {}\n", True)
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "PELE\n\n"
        #11. Pele
        pele = {
            "tom": random.choice(self.caracteristicas["pele"]["tom"]),
            "textura": random.choice(self.caracteristicas["pele"]["textura"]),
            "marcas": None if random.random() < 0.6 else random.choice(self.caracteristicas["pele"]["marcas"]),
            "caracteristicas_especiais": None if random.random() < 0.8 else random.choice(self.caracteristicas["pele"]["caracteristicas_especiais"]),
            "condicoes_temporarias": None if random.random() < 0.8 else random.choice(self.caracteristicas["pele"]["condicoes_temporarias"]),
            
        }
        pele['tom'] = self.selecionar_e_registrar(self.caracteristicas["pele"]["tom"], lambda obj: obj, "Selecione uma opção de pele tom:\n", "Pele tom selecionado: {}\n")
        pele['textura'] = self.selecionar_e_registrar(self.caracteristicas["pele"]["textura"], lambda obj: obj, "Selecione uma opção de pele textura:\n", "Pele textura selecionado: {}\n")
        pele['caracteristicas_especiais'] = self.selecionar_e_registrar(self.caracteristicas["pele"]["caracteristicas_especiais"], lambda obj: obj, "Selecione uma opção de pele caracteristicas especiais:\n", "Pele caracteristicas especiais selecionado: {}\n", True)
        pele['condicoes_temporarias'] = self.selecionar_e_registrar(self.caracteristicas["pele"]["condicoes_temporarias"], lambda obj: obj, "Selecione uma opção de pele condicoes temporarias:\n", "Pele condicoes temporarias selecionado: {}\n", True)
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "CORPO\n\n"
        #12. Corpo
        corpo = {
            "altura": None,
            "peso": None,
            "somatotipo": None,
            "forma": None,
            "musculatura":None,
            "gordura": None,
            "estrutura_ossea": None,
            "proporcoes": None,
            "tipos_hibridos": random.choice(self.caracteristicas["corpo"]["tipos_hibridos"]),
            "caracteristicas_especiais": None if random.random() < 0.8 else random.choice(self.caracteristicas["corpo"]["caracteristicas_especiais"]),
            "condicoes_temporarias": None if random.random() < 0.99 else random.choice(self.caracteristicas["corpo"]["condicoes_temporarias"]),
        }
        corpo['altura'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["altura"], lambda obj: obj, "Selecione uma opção de corpo altura:\n", "Corpo altura selecionado: {}\n", True)
        corpo['peso'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["peso"], lambda obj: obj, "Selecione uma opção de corpo peso:\n", "Corpo peso selecionado: {}\n", True)
        corpo['somatotipo'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["somatotipo"], lambda obj: obj, "Selecione uma opção de corpo somatotipo:\n", "Corpo somatotipo selecionado: {}\n", True)
        corpo['forma'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["forma"], lambda obj: obj, "Selecione uma opção de corpo forma:\n", "Corpo forma selecionado: {}\n", True)
        corpo['musculatura'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["musculatura"], lambda obj: obj, "Selecione uma opção de corpo musculatura:\n", "Corpo musculatura selecionado: {}\n", True)
        corpo['gordura'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["gordura"], lambda obj: obj, "Selecione uma opção de corpo gordura:\n", "Corpo gordura selecionado: {}\n", True)
        corpo['estrutura_ossea'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["estrutura_ossea"], lambda obj: obj, "Selecione uma opção de corpo estrutura ossea:\n", "Corpo estrutura ossea selecionado: {}\n")
        corpo['proporcoes'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["proporcoes"], lambda obj: obj, "Selecione uma opção de corpo proporções:\n", "Corpo proporções selecionado: {}\n")
        corpo['tipos_hibridos'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["tipos_hibridos"], lambda obj: obj, "Selecione uma opção de corpo tipos_hibridos:\n", "Corpo tipos_hibridos selecionado: {}\n")
        corpo['caracteristicas_especiais'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["caracteristicas_especiais"], lambda obj: obj, "Selecione uma opção de corpo caracteristicas_especiais:\n", "Corpo caracteristicas_especiais selecionado: {}\n")
        corpo['condicoes_temporarias'] = self.selecionar_e_registrar(self.caracteristicas["corpo"]["condicoes_temporarias"], lambda obj: obj, "Selecione uma opção de corpo condicoes_temporarias:\n", "Corpo condicoes_temporarias selecionado: {}\n")
        
        fundo = "fundo branco infinito"
        
        
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "PROMPT\n\n"
        # uso do método reutilizável para gerar todo o texto de descrição
        descricaoPersonagem = self.formatar_descricao_personagem( genero, especie, classe, subclasse, idade['valor'], etinia, rosto, olhos, nariz, boca, cabelo, pele, corpo, fundo)
        apresentacao += descricaoPersonagem
        
        os.system('cls')
        print(apresentacao)
        
class CYOA_Kreat:
    def __init__(self):
        global apresentacao
        self.gerarPersonagem = GeradorPersonagem()
    
    def executar(self):
        # fluxo central
        global apresentacao
        cabecalho = "Bem-vindo ao CYOA - Criador de Personagens de Kreat!\n"
        cabecalho += "=" * 70 + "\n"
        cabecalho += "CYAO - CRIADOR DE PERSONAGENS DE KREAT\n"
        cabecalho += "=" * 70 + "\n"
        cabecalho += "MENU PRINCIPAL\n"
        cabecalho += "=" * 70 + "\n"
        
        while True:
            apresentacao = cabecalho
            os.system('cls')
            print(apresentacao)
            
            dados = [
                {"ação": "Gerar Novo Personagem Aleatório", "valor": "1"},
                {"ação": "Personalizar Personagem", "valor": "2"},
                {"ação": "Sair", "valor": "5"}
            ]
            
            # Função que define como cada objeto será exibido
            def formato(obj):
                return f"{obj['ação']}"
            opcao = seletor(dados, formato, apresentacao + "Selecione uma opção:\n")
            if opcao['valor'] == "1":
                self.gerar_novo_personagem()
            elif opcao['valor'] == "2":
                self.montar_novo_personagem()
            # elif opcao == "3":
            #     self.gerar_prompt_flux()
            # elif opcao == "4":
            #     self.salvar_personagem()
            elif opcao['valor'] == "5":
                print("\nAté a próxima aventura em Kreat!")
                break
            else:
                print("Opção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")
                
    def gerar_novo_personagem(self):
        # Gera um novo personagem aleatório
        global apresentacao
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "GERANDO NOVO PERSONAGEM...\n"
        
        self.personagem_atual = self.gerarPersonagem.gerar()

    def montar_novo_personagem(self):
        # Permite ao usuário personalizar um personagem
        global apresentacao
        apresentacao += "\n" + "=" * 70 + "\n"
        apresentacao += "PERSONALIZANDO PERSONAGEM...\n"
        
        self.personagem_atual = self.gerarPersonagem.montar()
        
apresentacao = ""
 
if __name__ == "__main__":
    apresentacao = ""
    apresentacao += "Bem-vindo ao CYOA - Criador de Personagens de Kreat!\n"
    apresentacao += "Neste programa, você pode criar personagens únicos\n"
    apresentacao += "iniciando a criação de personagens\n\n\n"
    print(apresentacao)
    time.sleep(1)
    
    cyoa = CYOA_Kreat()
    cyoa.executar()