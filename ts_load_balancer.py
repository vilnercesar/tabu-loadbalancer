import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ServidorVirtual:
    """Representa um servidor virtual com capacidade e carga atual."""
    def __init__(self, id, capacidade):
        self.id = id
        self.capacidade = capacidade
        self.carga_atual = 0
        self.aplicacoes = []  # Lista de aplicações hospedadas
    
    def utilization(self):
        """Retorna a taxa de utilização do servidor (carga/capacidade)."""
        if self.capacidade == 0:
            return 0
        return self.carga_atual / self.capacidade
    
    def __repr__(self):
        return f"Servidor {self.id}: {self.carga_atual}/{self.capacidade} ({self.utilization()*100:.1f}%) - Apps: {self.aplicacoes}"

class Aplicacao:
    """Representa uma aplicação com um requisito de recursos."""
    def __init__(self, id, recursos_necessarios):
        self.id = id
        self.recursos_necessarios = recursos_necessarios
    
    def __repr__(self):
        return f"App-{self.id}({self.recursos_necessarios})"

class LoadBalancer:
    """Sistema de balanceamento de carga usando Busca Tabu."""
    def __init__(self, servidores, aplicacoes):
        self.servidores = servidores
        self.aplicacoes = aplicacoes
        self.melhor_solucao_global = None
        self.melhor_valor_global = float('inf')
        
    def gerar_solucao_inicial(self):
        """Gera uma solução inicial aleatória distribuindo as aplicações entre os servidores."""
        # Limpar todas as alocações atuais
        for servidor in self.servidores:
            servidor.carga_atual = 0
            servidor.aplicacoes = []
        
        # Alocar aplicações aleatoriamente
        for app in self.aplicacoes:
            servidor = random.choice(self.servidores)
            servidor.aplicacoes.append(app)
            servidor.carga_atual += app.recursos_necessarios
            
        return self.clonar_solucao()
    
    def clonar_solucao(self):
        """Clona a solução atual para não alterar diretamente os objetos originais."""
        clone = []
        for servidor in self.servidores:
            apps_ids = [app.id for app in servidor.aplicacoes]
            clone.append((servidor.id, apps_ids))
        return clone
    
    def aplicar_solucao(self, solucao):
        """Aplica uma solução ao estado atual dos servidores."""
        # Limpar todas as alocações atuais
        for servidor in self.servidores:
            servidor.carga_atual = 0
            servidor.aplicacoes = []
        
        # Aplicar a solução
        for servidor_id, app_ids in solucao:
            servidor = next(s for s in self.servidores if s.id == servidor_id)
            for app_id in app_ids:
                app = next(a for a in self.aplicacoes if a.id == app_id)
                servidor.aplicacoes.append(app)
                servidor.carga_atual += app.recursos_necessarios
    
    def calcular_funcao_objetivo(self):
        """
        Calcula o valor da função objetivo.
        
        Neste caso, queremos minimizar o desvio padrão da utilização dos servidores
        e penalizar servidores sobrecarregados.
        """
        utilizacoes = [s.utilization() for s in self.servidores]
        desvio_padrao = np.std(utilizacoes)
        
        # Penalidade para servidores sobrecarregados
        penalidade = sum(max(0, s.carga_atual - s.capacidade) * 10 for s in self.servidores)
        
        return desvio_padrao + penalidade
    
    def gerar_movimentos(self,max_movimentos=None):
        """
        Gera uma lista de movimentos possíveis.
        
        Um movimento consiste em mover uma aplicação de um servidor para outro.
        """
        movimentos = []
        
        for i, servidor_origem in enumerate(self.servidores):
            if not servidor_origem.aplicacoes:
                continue
                
            for app in servidor_origem.aplicacoes:
                for j, servidor_destino in enumerate(self.servidores):
                    if i != j:  # Não mover para o mesmo servidor
                        movimentos.append((servidor_origem.id, servidor_destino.id, app.id))
        
        random.shuffle(movimentos)  # Randomizar a ordem dos movimentos
        if max_movimentos is None:
            # Heurística: limitar baseado no tamanho do problema
            max_movimentos = min(len(movimentos), 20 + len(self.servidores) * 2)
    
        return movimentos[:min(len(movimentos), max_movimentos)] # Limitar a quantidade de movimentos
       
    
    
    def aplicar_movimento(self, movimento):
        """
        Aplica um único movimento à solução atual.
        
        Movimento: (id_servidor_origem, id_servidor_destino, id_app)
        """
        origem_id, destino_id, app_id = movimento
        
        servidor_origem = next(s for s in self.servidores if s.id == origem_id)
        servidor_destino = next(s for s in self.servidores if s.id == destino_id)
        app = next(a for a in servidor_origem.aplicacoes if a.id == app_id)
        
        # Remover a aplicação do servidor de origem
        servidor_origem.aplicacoes.remove(app)
        servidor_origem.carga_atual -= app.recursos_necessarios
        
        # Adicionar a aplicação ao servidor de destino
        servidor_destino.aplicacoes.append(app)
        servidor_destino.carga_atual += app.recursos_necessarios
        
        return self.clonar_solucao()
    
    def busca_tabu(self, max_iteracoes=100, tamanho_tabu=10,max_movimentos=None):
       
        """
        Implementa a Busca Tabu para balanceamento de carga.
        
        Args:
            max_iteracoes: Número máximo de iterações
            tamanho_tabu: Número de iterações que cada movimento permanece tabu
        """
        # Gerar solução inicial
        solucao_atual = self.gerar_solucao_inicial()
        self.aplicar_solucao(solucao_atual)
        valor_atual = self.calcular_funcao_objetivo()
        
        self.melhor_solucao_global = solucao_atual
        self.melhor_valor_global = valor_atual
        
        # Inicializar lista tabu
        lista_tabu = defaultdict(int)
        
        # Histórico para gráfico
        historico_valores = [valor_atual]
        
        iteracao_atual = 0
        while iteracao_atual < max_iteracoes:
            iteracao_atual += 1
            
            movimentos = self.gerar_movimentos(max_movimentos)
            melhor_solucao_vizinha = None
            melhor_valor_vizinho = float('inf')
            movimento_escolhido = None
            
            for movimento in movimentos:
                # Aplicar movimento
                solucao_candidata = self.aplicar_movimento(movimento)
                valor_candidato = self.calcular_funcao_objetivo()
                
                # Verificar se é o melhor movimento vizinho
                if movimento not in lista_tabu and valor_candidato < melhor_valor_vizinho:
                    melhor_solucao_vizinha = solucao_candidata
                    melhor_valor_vizinho = valor_candidato
                    movimento_escolhido = movimento
                # Critério de aspiração: aceitar movimento tabu se for melhor que a solução global
                elif valor_candidato < self.melhor_valor_global:
                    melhor_solucao_vizinha = solucao_candidata
                    melhor_valor_vizinho = valor_candidato
                    movimento_escolhido = movimento
                
                # Reverter o movimento para testar o próximo
                self.aplicar_solucao(solucao_atual)
            
            # Se não encontrou nenhum movimento válido
            if melhor_solucao_vizinha is None:
                break
                
            # Atualizar solução atual
            solucao_atual = melhor_solucao_vizinha
            self.aplicar_solucao(solucao_atual)
            valor_atual = melhor_valor_vizinho
            
            # Atualizar a melhor solução global
            if valor_atual < self.melhor_valor_global:
                self.melhor_solucao_global = solucao_atual
                self.melhor_valor_global = valor_atual
            
            # Marcar movimento como tabu
            if movimento_escolhido:
                lista_tabu[movimento_escolhido] = tamanho_tabu
            
            # Decrementar todos os valores na lista tabu
            for mov in list(lista_tabu.keys()):
                lista_tabu[mov] -= 1
                if lista_tabu[mov] <= 0:
                    del lista_tabu[mov]
            
            historico_valores.append(valor_atual)
            
            print(f"Iteração {iteracao_atual}: Valor = {valor_atual:.4f}, Melhor Global = {self.melhor_valor_global:.4f}")
        
        # Aplicar a melhor solução encontrada
        self.aplicar_solucao(self.melhor_solucao_global)
        return historico_valores
    
    def visualizar_balanceamento(self):
        """Visualiza o balanceamento de carga atual."""
        utilizacoes = [s.utilization() * 100 for s in self.servidores]
        cargas = [s.carga_atual for s in self.servidores]
        capacidades = [s.capacidade for s in self.servidores]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Gráfico de barras para utilização
        servidores_ids = [f"S{s.id}" for s in self.servidores]
        ax1.bar(servidores_ids, utilizacoes)
        ax1.axhline(y=100, color='r', linestyle='-', alpha=0.3)
        ax1.set_ylim(0, max(utilizacoes) * 1.1 if max(utilizacoes) > 100 else 120)
        ax1.set_ylabel('Utilização (%)')
        ax1.set_title('Utilização dos Servidores')
        
        # Colocar valores nas barras
        for i, v in enumerate(utilizacoes):
            ax1.text(i, v + 1, f"{v:.1f}%", ha='center')
        
        # Gráfico de barras para carga vs capacidade
        x = np.arange(len(servidores_ids))
        width = 0.35
        
        ax2.bar(x - width/2, cargas, width, label='Carga Atual')
        ax2.bar(x + width/2, capacidades, width, label='Capacidade')
        ax2.set_xticks(x)
        ax2.set_xticklabels(servidores_ids)
        ax2.set_ylabel('Recursos')
        ax2.set_title('Carga vs Capacidade dos Servidores')
        ax2.legend()
        
        # Adicionar detalhes
        detalhes = []
        for s in self.servidores:
            apps_info = ", ".join([str(app) for app in s.aplicacoes])
            detalhes.append(f"Servidor {s.id}: {s.carga_atual}/{s.capacidade} - {apps_info}")
        
        plt.figtext(0.1, 0.01, "\n".join(detalhes), fontsize=10)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        plt.show()
    
    def visualizar_convergencia(self, historico_valores):
        """Visualiza a convergência da busca tabu."""
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(historico_valores)), historico_valores)
        plt.xlabel('Iteração')
        plt.ylabel('Valor da Função Objetivo')
        plt.title('Convergência da Busca Tabu')
        plt.grid(True)
        plt.show()


