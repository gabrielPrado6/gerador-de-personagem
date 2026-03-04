import random
import time
import json

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
            "projecao": random.choice(self.caracteristicas["nariz"]["projeção"]),
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
        print(f"Gênero: {genero['nome']}")
        print(f"Raça: {especie['nome']}")
        print(f"Classe: {classe['classe']} - {subclasse['nome'] if subclasse else 'sem subclasse'}")
        print(f"Idade: {idade} anos")
        
        print("=" * 70)
        print(f"{{especie: {especie}, genero: {genero}, idade: {idade}, etinia: {etinia}, rosto: {rosto}, olhos: {olhos}, nariz: {nariz}, boca: {boca}, cabelo: {cabelo}, pele: {pele}, corpo: {corpo}}}")
        print("=" * 70)
        
        print(f"\n {especie['descricao']}, de corpo inteiro, visto em ângulo de três quartos, em pé, sobre {fundo}, do {genero['descricao']}, aparenta {idade} anos, de etnia {etinia}, com expressão facial serena e observadora.\nO rosto é bem definido e de traços suaves, {rosto['formato']['descricao']}{', '+rosto['detalhes'] if rosto['detalhes'] else ''}, olhos amendoados na cor {olhos['cor']}{'-'+olhos['insencidades_cor'] if olhos['insencidades_cor'] else ''}{' '+olhos['efeito'] if olhos['efeito'] else ''}, sobrancelhas {olhos['sobrancelhas']}, nariz {nariz['formato']} {nariz['largura']} {nariz['altura']} e {nariz['projecao']}, ponta do nariz {nariz['ponta_formato']} {nariz['ponta_direcao']}, narinas {nariz['narinas_tamanho']} {nariz['narinas_formato']}, lábios {boca['labios_superior']} e {boca['labios_inferior']}, cabelo {cabelo['estilo']} {cabelo['comprimento']} na cor {cabelo['cor']}, penteado {cabelo['penteado']}. A pele {pele['tom']} possui textura {pele['textura']}{', '+pele['marcas'] if pele['marcas'] else ''}{', '+pele['condicoes_temporarias'] if pele['condicoes_temporarias'] else ''}.\nO vestuário é complexo e combina elementos de fantasia medieval e era industrial, adequado a uma classe comum de RPG, como artífice. {subclasse['descricao']}, {subclasse['vestimenta']}, {subclasse['itens_marcantes']}.\nA iluminação é suave e difusa, proveniente de uma fonte frontal levemente superior, criando sombras suaves que modelam o corpo e o rosto. As cores são terrosas com toques de azul-acinzentado e metálicos, com alto contraste e saturação moderada. Estilo de ilustração digital com traços nítidos e texturas realistas.\nO universo de Kreat é sugerido de forma abstrata por meio de padrões sutis no fundo ou na roupa, como runas estilizadas, engrenagens decorativas, ou motivos que mesclam orgânico e mecânico, sem representações explícitas de cenários.")

class CYOA_Kreat:
    def __init__(self):
        self.gerarPersonagem = GeradorPersonagem()
    
    def executar(self):
        # fluxo central
        print("=" * 70)
        print("CYOA - CRIADOR DE PERSONAGENS DE KREAT")
        print("=" * 70)
        
        while True:
            print("MENU PRINCIPAL")
            print("=" * 70)
            print("1. Gerar Novo Personagem Aleatório")
            
            opcao = input("\nEscolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                self.gerar_novo_personagem()
            # elif opcao == "2":
            #     self.mostrar_personagem()
            # elif opcao == "3":
            #     self.gerar_prompt_flux()
            # elif opcao == "4":
            #     self.salvar_personagem()
            elif opcao == "5":
                print("\nAté a próxima aventura em Kreat!")
                break
            else:
                print("Opção inválida! Tente novamente.")
                
    def gerar_novo_personagem(self):
        # Gera um novo personagem aleatório
        print("\n" + "=" * 70)
        print("GERANDO NOVO PERSONAGEM...")
        
        self.personagem_atual = self.gerarPersonagem.gerar()
        
            
if __name__ == "__main__":
    print("iniciando a criação de personagens para Kreat")
    time.sleep(1)
    
    cyoa = CYOA_Kreat()
    cyoa.executar()