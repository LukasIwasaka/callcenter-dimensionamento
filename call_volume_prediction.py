import random
import numpy as np

# Função de aptidão ajustada


def fitness(predicted, actual):
    return -abs(predicted - actual)

# Função para calcular o volume de chamadas com base nas variáveis ajustadas


def calcular_volume_chamadas(horas_por_dia, tempo_medio_atendimento, dias_uteis_por_mes, agentes_manha, agentes_tarde, satisfacao_cliente):
    # A fórmula de volume agora considera os agentes e a satisfação do cliente
    base_volume = (horas_por_dia * 3600) / tempo_medio_atendimento
    volume_ajustado = base_volume * \
        (agentes_manha + agentes_tarde) * (satisfacao_cliente / 5)
    total_chamadas_por_mes = volume_ajustado * dias_uteis_por_mes
    return total_chamadas_por_mes

# Geração inicial da população


def generate_population(size, n_features=6):
    population = []
    for _ in range(size):
        individual = [
            random.randint(0, 1),  # Hora do dia (0 = manhã, 1 = tarde)
            random.randint(0, 5),   # Dia da semana (0 a 5)
            random.randint(30, 80),  # Volume de chamadas anterior (30 a 80)
            random.randint(1, 5),  # Satisfação do cliente (1 a 5)
            random.randint(3, 3) if random.randint(
                0, 1) == 0 else random.randint(3, 3)  # 3 de manhã e 3 à tarde
        ]
        population.append(individual)
    return population

# Função de seleção (tournament selection)


def select_population(population, actual, num_selected):
    scores = []
    for individual in population:
        hora_dia = individual[0]
        dia_semana = individual[1]
        volume_chamadas = individual[2]
        satisfacao_cliente = individual[3]
        agentes = individual[4]

        predicted = calcular_volume_chamadas(
            10, 300, 26, agentes, agentes, satisfacao_cliente)
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
            individual[i] = random.uniform(0, 1)
    return individual

# Função principal para rodar o algoritmo genético


def genetic_algorithm(actual, population_size=100, num_generations=500, mutation_rate=0.01):
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
            10, 300, 26, best_individual[4], best_individual[4], best_individual[3])
        print(f"Geração {generation + 1}, Melhor previsão: {best_prediction}")

    # Retorna a melhor solução encontrada
    best_individual = select_population(population, actual, 1)[0]
    return best_individual


# Exemplo de execução do algoritmo
if __name__ == "__main__":
    actual_call_volume = 100  # Volume real de chamadas

    # Rodando o algoritmo genético para estimar o volume de chamadas
    best_solution = genetic_algorithm(actual_call_volume)
    predicted_volume = calcular_volume_chamadas(
        10, 300, 26, best_solution[4], best_solution[4], best_solution[3])

    # Arredondando o valor da previsão para o inteiro mais próximo
    rounded_predicted_volume = round(predicted_volume)

    print(f"Melhor solução encontrada: {best_solution}")
    print(f"Previsão final do volume de chamadas (arredondada): {
          rounded_predicted_volume}")
