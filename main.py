
from ts_load_balancer import ServidorVirtual, Aplicacao, LoadBalancer

# Função principal para executar o exemplo
def main():
    #fatores de ajuste
    max_iteracoes=100 
    tamanho_tabu=10
    max_movimentos=20

    # Criar servidores
    servidores = [
        ServidorVirtual(1, 100),
        ServidorVirtual(2, 120),
        ServidorVirtual(3, 80),
        ServidorVirtual(4, 150),
        ServidorVirtual(5, 90)
    ]
    
    # Criar aplicações
    aplicacoes = [
        Aplicacao(1, 30),
        Aplicacao(2, 50),
        Aplicacao(3, 25),
        Aplicacao(4, 40),
        Aplicacao(5, 35),
        Aplicacao(6, 60),
        Aplicacao(7, 20),
        Aplicacao(8, 45),
        Aplicacao(9, 15),
        Aplicacao(10, 55),
        Aplicacao(11, 30),
        Aplicacao(12, 25),
        Aplicacao(13, 40),
        Aplicacao(14, 30),
        Aplicacao(15, 20)
    ]
    
    # Criar balanceador de carga
    balanceador = LoadBalancer(servidores, aplicacoes)
    
    print("Distribuição inicial aleatória:")
    solucao_inicial = balanceador.gerar_solucao_inicial()
    balanceador.aplicar_solucao(solucao_inicial)
    for servidor in balanceador.servidores:
        print(servidor)
    print(f"Valor da função objetivo inicial: {balanceador.calcular_funcao_objetivo():.4f}")
    
    # Visualizar distribuição inicial
    print("\nVisualizando distribuição inicial:")
    balanceador.visualizar_balanceamento()
    
    # Executar busca tabu
    print("\nExecutando busca tabu:")
    historico = balanceador.busca_tabu(max_iteracoes,tamanho_tabu,max_movimentos)
    
    print("\nMelhor distribuição encontrada:")
    for servidor in balanceador.servidores:
        print(servidor)
    print(f"Melhor valor da função objetivo: {balanceador.melhor_valor_global:.4f}")
    
    # Visualizar distribuição final
    print("\nVisualizando distribuição final:")
    balanceador.visualizar_balanceamento()
    
    # Visualizar convergência
    print("\nVisualizando convergência:")
    balanceador.visualizar_convergencia(historico)

if __name__ == "__main__":
    main()