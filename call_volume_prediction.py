import random

# Função de aptidão ajustada para penalizar desvios e normalizar a diferença
def fitness(predicted, actual):
    return 1 / (1 + abs(predicted - actual))

# Função para calcular o volume de chamadas com base nas variáveis ajustadas
def calcular_volume_chamadas(horas_por_dia, tempo_medio_atendimento, dias_uteis_por_mes, agentes_manha, agentes_tarde, satisfacao_cliente):
    base_volume = (horas_por_dia * 3600) / tempo_medio_atendimento
    fator_agentes = agentes_manha + agentes_tarde
    fator_satisfacao = satisfacao_cliente / 5
    total_chamadas_por_mes = base_volume * fator_agentes * fator_satisfacao * dias_uteis_por_mes
    return total_chamadas_por_mes

# Geração inicial da população com valores mais realistas
def generate_population(size, n_features=6):
    population = []
    for _ in range(size):
        individual = [
            random.randint(0, 1),    # Hora do dia (0 = manhã, 1 = tarde)
            random.randint(0, 5),    # Dia da semana
            random.randint(50, 100), # Volume inicial estimado
            random.randint(3, 5),    # Satisfação do cliente (mais otimista)
            random.randint(3, 10),   # Agentes disponíveis manhã
            random.randint(3, 10),   # Agentes disponíveis tarde
        ]
        population.append(individual)
    return population

# Função de seleção (tournament selection)
def select_population(population, actual, num_selected):
    scores = []
    for individual in population:
        satisfacao_cliente = individual[3]
        agentes_manha = individual[4]
        agentes_tarde = individual[5]

        predicted = calcular_volume_chamadas(
            10, 300, 26, agentes_manha, agentes_tarde, satisfacao_cliente)
        score = fitness(predicted, actual)
        scores.append((score, individual))

    scores.sort(reverse=True, key=lambda x: x[0])
    selected = [individual for _, individual in scores[:num_selected]]
    return selected

# Função de cruzamento (crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Função de mutação
def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            if i == 0:  # Hora do dia
                individual[i] = random.randint(0, 1)
            elif i == 1:  # Dia da semana
                individual[i] = random.randint(0, 5)
            elif i == 2:  # Volume inicial estimado
                individual[i] = random.randint(50, 100)
            elif i == 3:  # Satisfação do cliente
                individual[i] = random.randint(3, 5)
            elif i == 4 or i == 5:  # Número de agentes
                individual[i] = random.randint(3, 10)
    return individual

# Função principal para rodar o algoritmo genético
def genetic_algorithm(actual, population_size=200, num_generations=1000, mutation_rate=0.01):
    n_features = 6  # Número de características
    population = generate_population(population_size, n_features)

    for generation in range(num_generations):
        selected = select_population(population, actual, population_size // 2)

        # Cruzamento para gerar novos indivíduos
        new_population = []
        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            parent2 = selected[i + 1]
            child1, child2 = crossover(parent1, parent2)
            new_population.append(child1)
            new_population.append(child2)

        # Mutação
        population = [mutate(individual, mutation_rate)
                      for individual in new_population]

        # Avaliar a melhor solução da geração
        best_individual = select_population(population, actual, 1)[0]
        best_prediction = calcular_volume_chamadas(
            10, 300, 26, best_individual[4], best_individual[5], best_individual[3])
        print(f"Geração {generation + 1}, Melhor previsão: {best_prediction}")

    # Retorna a melhor solução encontrada
    best_individual = select_population(population, actual, 1)[0]
    return best_individual

# Execução do algoritmo genético
if __name__ == "__main__":
    actual_call_volume = 18720  # Volume real de chamadas no mês

    # Rodando o algoritmo genético para estimar o volume de chamadas
    best_solution = genetic_algorithm(actual_call_volume)
    predicted_volume = calcular_volume_chamadas(
        10, 300, 26, best_solution[4], best_solution[5], best_solution[3])

    # Arredondando o valor da previsão para o inteiro mais próximo
    rounded_predicted_volume = round(predicted_volume)

    print(f"Melhor solução encontrada: {best_solution}")
    print(f"Previsão final do volume de chamadas (arredondada): {rounded_predicted_volume}")
