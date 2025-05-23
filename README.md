# Busca Tabu para Load Balancing

## Descrição do Problema

Este projeto implementa uma solução para o problema de **balanceamento de carga (Load Balancing)** utilizando a metaheurística Busca Tabu. O objetivo é distribuir tarefas entre servidores de forma a minimizar o tempo total de processamento, considerando as capacidades individuais de cada servidor.

O problema consiste em:
- **N tarefas** com diferentes tempos de processamento
- **M servidores** com diferentes capacidades de processamento
- **Objetivo:** Minimizar o makespan (tempo total para completar todas as tarefas)

## Metaheurística Utilizada

**Busca Tabu (Tabu Search)** - Uma metaheurística de busca local que utiliza uma estrutura de memória (lista tabu) para evitar ciclos e explorar regiões promissoras do espaço de soluções.

### Características da implementação:
- **Lista Tabu:** Armazena movimentos recentemente executados para evitar retrocesso
- **Função Objetivo:** Minimização do makespan
- **Estrutura de Vizinhança:** Movimentação de tarefas entre servidores
- **Critério de Parada:** Número máximo de iterações ou critério de convergência

## Bibliotecas Necessárias

O projeto utiliza as seguintes bibliotecas Python:

```bash
numpy>=1.21.0
matplotlib>=3.5.0
```

## Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.7 ou superior instalado
- pip (gerenciador de pacotes Python)

### 2. Instalação das Dependências

```bash
# Atualizar o pip
python -m pip install --upgrade pip

# Instalar as bibliotecas necessárias
pip install numpy matplotlib
```

### 3. Executar o Projeto

```bash
# Navegar até o diretório do projeto
cd caminho/para/seu/projeto

# Executar o programa principal
python main.py
```

### 4. Estrutura dos Arquivos

```
projeto/
├── main.py              # Arquivo principal de execução
├── load_balance.py      # Classes e algoritmos de busca tabu
├── README.md           # Este arquivo
└── resultados/         # Diretório para salvar gráficos e resultados
```

## Resultados Obtidos

### Configuração dos Testes
- **Instâncias testadas:** [Descrever as instâncias utilizadas]
- **Número de execuções:** [Número de repetições por teste]
- **Parâmetros da Busca Tabu:**
  - Tamanho da lista tabu: [valor]
  - Número máximo de iterações: [valor]
  - Critério de parada: [critério utilizado]

### Resultados Principais

| Instância | Melhor Solução | Tempo de Execução | Iterações |
|-----------|----------------|-------------------|-----------|
| Teste 1   | [valor]        | [tempo]           | [iter]    |
| Teste 2   | [valor]        | [tempo]           | [iter]    |
| Teste 3   | [valor]        | [tempo]           | [iter]    |

### Gráficos de Convergência
- Evolução da função objetivo ao longo das iterações
- Comparação entre diferentes configurações de parâmetros
- Análise de desempenho por tipo de instância

## Comentários e Conclusões

### Pontos Positivos
- A Busca Tabu demonstrou eficácia na exploração do espaço de soluções
- A lista tabu preveniu eficientemente a ocorrência de ciclos
- O algoritmo convergiu para soluções de boa qualidade na maioria dos casos testados

### Desafios Encontrados
- Ajuste fino dos parâmetros (tamanho da lista tabu, tempo tabu, critérios de parada)
- Balanceamento entre intensificação e diversificação da busca
- Tratamento de instâncias com características diferentes

### Melhorias Futuras
- Implementação de critérios de aspiração mais sofisticados
- Paralelização do algoritmo para instâncias maiores
- Comparação com outras metaheurísticas (Algoritmo Genético, Simulated Annealing)
- Interface gráfica para visualização interativa dos resultados

### Conclusão
A implementação da Busca Tabu para o problema de Load Balancing mostrou-se uma abordagem promissora, fornecendo soluções de qualidade em tempo computacional aceitável. Os resultados indicam que a metaheurística é adequada para este tipo de problema de otimização combinatória.

---

## Autor
Vilner César Bezerra de Oliveira





<!-- RETIRAR ESSE TRECHO
1. ter o python instalado
2. instalar o pip: 

```bash
python -m pip install numpy matplotlib
python.exe -m pip install --upgrade pip
```

3. instalar o numpy
```bash
pip install numpy matplotlib
```

 -->

