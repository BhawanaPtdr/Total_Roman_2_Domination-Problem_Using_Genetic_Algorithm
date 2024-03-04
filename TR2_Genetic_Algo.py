import random
import math

def make_adjacency_list():
    adjacency_list = {}
    num_vertices, num_edges = map(int,input("Enter the number of vertices and edges : ").split())
    
    for i in range(num_edges):
        node1, node2 = map(int, input().split())
        if node1 != node2 and node2 not in adjacency_list.get(node1, []):
            adjacency_list.setdefault(node1,[]).append(node2)
            adjacency_list.setdefault(node2,[]).append(node1)
    
    # for node,neighbor in adjacency_list.items():
    #     print(f"{node} : {', '.join(map(str, neighbor))}")
    
    return adjacency_list
        

#Heuristic-  1
# first you have to choose one unlabed vertex and choose that vertex neighbor randomly (one of them) and give both vertex
# to label 1 and that both vertex common neighbor give label 0  but in case if u choose vertex which has no unlabeled vertex then 
# you have to check three condition 
# 1 . if that selected vertex neighbor has sum of label is greater or than or equal to 2 then give that selected vertex to label 0
# 2. if first condition is not means neigbor sum is <2 then make that neighbor label 1 and that selected vertex label is also 
# assign to 1

def Heuristic_1(adjacency_list):
    labels = {vertex: -1 for vertex in adjacency_list.keys()}

    def get_neighbors_with_label(vertex, label):
        return [neighbor for neighbor in adjacency_list[vertex] if labels[neighbor] == label]

    def get_unlabeled_vertices():
        return [vertex for vertex, label in labels.items() if label == -1]

    def label_vertex_and_neighbors(vertex):
        labels[vertex] = 1
        neighbors = adjacency_list[vertex]
        random_neighbor = random.choice(neighbors)
        labels[random_neighbor] = 1

        common_neighbors = set(neighbors).intersection(adjacency_list[random_neighbor])
        for common_neighbor in common_neighbors:
            labels[common_neighbor] = 0

    def has_two_labeled_neighbors(vertex):
        labeled_neighbors = get_neighbors_with_label(vertex, 1)
        return len(labeled_neighbors) >= 2

    def sum_labels_of_neighbors(vertex):
        return sum(labels[neighbor] for neighbor in adjacency_list[vertex])

    while -1 in labels.values():
        unlabeled_vertices = get_unlabeled_vertices()
        start_vertex = random.choice(unlabeled_vertices)

        if any(labels[neighbor] == -1 for neighbor in adjacency_list[start_vertex]):
            label_vertex_and_neighbors(start_vertex)
        else:
            neighbor_sum = sum_labels_of_neighbors(start_vertex)
            if neighbor_sum >= 2:
                labels[start_vertex] = 0
            else:
                for neighbor in adjacency_list[start_vertex]:
                    # if labels[neighbor] == -1:
                    labels[neighbor] = 1
                    break
                labels[start_vertex] = 1

    return labels
    


#Heuristic-  2
# select a random vertex and give that vertex to label 2 and give label 1 to one neighbor of that selected vertex
# and give 0 to all other remaining vertex and in case if you select a vertex which has no unlabeled vertex then
# give that vertex to label 1 and one of that neighbor give label 1 

def Heuristic_2(adjacency_list):
    labels = {vertex: -1 for vertex in adjacency_list.keys()}

    def get_unlabeled_vertices():
        return [vertex for vertex, label in labels.items() if label == -1]

    def label_vertex_and_neighbors(vertex):
        labels[vertex] = 2
        neighbors = adjacency_list[vertex]
        if any(labels[neighbor] == -1 for neighbor in neighbors):
            unlabeled_neighbors = [neighbor for neighbor in neighbors if labels[neighbor] == -1]
            chosen_neighbor = random.choice(unlabeled_neighbors)
            labels[chosen_neighbor] = 1
            for neighbor in neighbors:
                if neighbor != chosen_neighbor:
                    labels[neighbor] = 0
        else:
            # If all neighbors are labeled, assign label 1 to the vertex and one neighbor
            labels[vertex] = 1
            chosen_neighbor = random.choice(neighbors)
            labels[chosen_neighbor] = 1

    while -1 in labels.values():
        unlabeled_vertices = get_unlabeled_vertices()
        start_vertex = random.choice(unlabeled_vertices)
        label_vertex_and_neighbors(start_vertex)

    return labels




#Heuristic-  3

def Heuristic_3(adjacency_list):
    labels = {vertex: -1 for vertex in adjacency_list.keys()}

    def get_unlabeled_vertices():
        return [vertex for vertex, label in labels.items() if label == -1]

    def find_max_degree_vertex(unlabeled_vertices):
        max_degree_vertex = None
        max_degree = -1
        for vertex in unlabeled_vertices:
            degree =0
            for neigh in adjacency_list[vertex]:
                if labels[neigh] == -1:
                    degree = degree+1
            # degree = len(adjacency_list[vertex])
            if degree > max_degree:
                max_degree = degree
                max_degree_vertex = vertex
        return max_degree_vertex

    def label_vertex_and_neighbors(vertex):
        labels[vertex] = 2
        neighbors = adjacency_list[vertex]
        if any(labels[neighbor] == -1 for neighbor in neighbors):
            unlabeled_neighbors = [neighbor for neighbor in neighbors if labels[neighbor] == -1]
            chosen_neighbor = random.choice(unlabeled_neighbors)
            labels[chosen_neighbor] = 1
            print("chosen_neighbor: ", chosen_neighbor)
            for neighbor in unlabeled_neighbors:
                if neighbor != chosen_neighbor:
                    if labels[neighbor] == -1:
                        #  print(labels[neighbor])
                         labels[neighbor] = 0
        else:
            # If all neighbors are labeled, assign label 1 to the vertex and one neighbor
            labels[vertex] = 1
            chosen_neighbor = random.choice(neighbors)
            print("chosen_neighbor: ", chosen_neighbor)
            labels[chosen_neighbor] = 1

    while -1 in labels.values():
        unlabeled_vertices = get_unlabeled_vertices()
        # Find maximum degree vertex among the unlabeled vertices
        max_degree_vertex = find_max_degree_vertex(unlabeled_vertices)
        print(max_degree_vertex)
        label_vertex_and_neighbors(max_degree_vertex)

    return labels




    print("Before Modification:", vertex_labels)
    
    labels = dict(vertex_labels)
    for vertex, label in labels.items():
        if label == 0:
            neighbor_sum = sum(labels[neighbor] for neighbor in adjacency_list[vertex])
            if neighbor_sum >= 2:
                continue
            elif neighbor_sum == 1:
                # Find the neighbor labeled 1 and change it to 2
                for neighbor in adjacency_list[vertex]:
                    if labels[neighbor] == 1:
                        labels[neighbor] = 2
                        # print("**")
                        break
            elif neighbor_sum == 0:
                # If neighbor_sum is 0, make any two neighbors label 1
                count = 0
                if len(adjacency_list[vertex]) >= 2:
                    for neighbor in adjacency_list[vertex]:
                        if count < 2:
                            labels[neighbor] = 1
                            count += 1
                else:
                    for neighbor in adjacency_list[vertex]:
                        labels[neighbor] = 2

        else:
            neighbor_sum = sum(labels[neighbor] for neighbor in adjacency_list[vertex])
            if neighbor_sum >= 1:
                continue
            else:
                for neighbor in adjacency_list[vertex]:
                    labels[neighbor] = 1
                    # print("**")
                    break
        
    print("After Modification:", labels)
    return labels


def check_feasible(vertex_labels, adjacency_list):
    # print("check")
    for vertex, label in vertex_labels.items():
        # print(vertex, "->", label)
        if label == 0:
            neighbor_sum = sum(vertex_labels[neighbor] for neighbor in adjacency_list[vertex])
            # print(neighbor_sum)
            if neighbor_sum < 2:
                return False
        elif label == 1:
            neighbor_sum = sum(vertex_labels[neighbor] for neighbor in adjacency_list[vertex])
            if neighbor_sum < 1:
                return False
        elif label == 2:
            neighbor_sum = sum(vertex_labels[neighbor] for neighbor in adjacency_list[vertex])
            if neighbor_sum < 1:
                return False
                
    return True
    
    

def make_feasible(vertex_labels, adjacency_list):

    
    # print("Before Modification:", vertex_labels)
    
    labels = dict(vertex_labels)
    for vertex, label in labels.items():
        if label == 0:
            neighbor_sum = sum(labels[neighbor] for neighbor in adjacency_list[vertex])
            # print("ns: ",neighbor_sum)
            if neighbor_sum >= 2:
                continue
            elif neighbor_sum == 1:
                # Find the neighbor labeled 1 and change it to 2
                for neighbor in adjacency_list[vertex]:
                    if labels[neighbor] == 1:
                        labels[neighbor] = 2
                        # print("**")
                        break
            elif neighbor_sum == 0:
                # If neighbor_sum is 0, make any two neighbors label 1
                count = 0
                if len(adjacency_list[vertex]) >= 2:
                    for neighbor in adjacency_list[vertex]:
                        if count < 2:
                            labels[neighbor] = 1
                            count += 1
                else:
                    for neighbor in adjacency_list[vertex]:
                        labels[neighbor] = 2

        else:
            neighbor_sum = sum(labels[neighbor] for neighbor in adjacency_list[vertex])
            if neighbor_sum >= 1:
                continue
            else:
                for neighbor in adjacency_list[vertex]:
                    labels[neighbor] = 1
                    # print("**")
                    break
    # print("After Modification:", labels)
    return labels


def cost_function(labels):
    return sum(labels.values())


POPULATION_SIZE = 10
MUTATION_RATE = 0.1
NUM_GENERATIONS = 1



# def crossover(parent1, parent2, adjacency_matrix):
#     parent1 = list(parent1)  # Convert tuple to list
#     parent2 = list(parent2)  # Convert tuple to list

#     # Generate random crossover points
#     r1 = random.randint(0, len(parent1) - 1)
#     r2 = random.randint(0, len(parent1) - 1)

#     # Ensure r1 and r2 are different
#     while r2 == r1:
#         r2 = random.randint(0, len(parent1) - 1)

#     # Get the labels between the crossover points for both parents
#     labels_parent1 = parent1[min(r1, r2):max(r1, r2)]
#     labels_parent2 = parent2[min(r1, r2):max(r1, r2)]

#     # Swap the labels between the parents
#     parent1[min(r1, r2):max(r1, r2)] = labels_parent2
#     parent2[min(r1, r2):max(r1, r2)] = labels_parent1

#     return tuple(parent1), tuple(parent2)


# def genetic_algorithm(num_nodes, adjacency_matrix):
#     # Initialize population
#     population = []
#     for i in range(POPULATION_SIZE):
#         current_labels = Heuristic_1(adjacency_list)
#         current_cost = cost_function(current_labels)
#         population.append((current_labels))

#     # Main loop
#     for generation in range(NUM_GENERATIONS):
#         # Select parents for crossover
#         parent1 = random.choice(population)
#         parent2 = random.choice(population)

#         # Perform crossover and mutation to create new generation
#         child1, child2 = crossover(tuple(parent1), tuple(parent2), adjacency_list)
#         # child1 = mutate(child1)
#         # child2 = mutate(child2)

#         # Replace parents with children
#         population.append(child1)
#         population.append(child2)

#         population = sorted(population, key=lambda x: cost_function(x))[:POPULATION_SIZE]

#     # Return the best solution found
#     best_solution = min(population, key=lambda x: cost_function(x, adjacency_matrix))
#     best_cost = cost_function(best_solution)
#     return best_solution, best_cost

#         # Select the top solutions for the next generation
#     #     population = sorted(population, key=lambda x: cost(x, adjacency_matrix))[:POPULATION_SIZE]

#     # # Return the best solution found
#     # best_solution = min(population, key=lambda x: cost(x, adjacency_matrix))
#     # return best_solution, cost(best_solution, adjacency_matrix)







def crossover(parent1, parent2, adjacency_matrix):
    # print(parent1)
    # print(parent2)
    # print()

    # Generate random crossover points
    r1 = random.randint(0, len(parent1) - 1)
    r2 = random.randint(0, len(parent1) - 1)

    # Ensure r1 and r2 are different
    while r2 - r1 > 1:
        r2 = random.randint(0, len(parent1) - 1)
    
    # print(r1, r2)
    
    # Get the labels between the crossover points for both parents
    labels_parent1 = {k: parent1[k] for k in range(min(r1, r2), max(r1, r2))}
    labels_parent2 = {k: parent2[k] for k in range(min(r1, r2), max(r1, r2))}


    # Swap the labels between the parents
    for key in labels_parent1:
        parent1[key] = labels_parent2[key]
    for key in labels_parent2:
        parent2[key] = labels_parent1[key]

    # print(parent1)
    # print(parent2)
    # print()

    if(not(check_feasible(parent1, adjacency_matrix))):
       parent1 = make_feasible(parent1, adjacency_matrix)

    if(not(check_feasible(parent2, adjacency_matrix))):
       parent2 = make_feasible(parent2, adjacency_matrix)
    
    # print(parent1)
    # print(parent2)
    return parent1, parent2


def genetic_algorithm(num_nodes, adjacency_matrix):
    # Initialize population
    population = []
    for _ in range(POPULATION_SIZE):
        current_labels = Heuristic_1(adjacency_matrix)
        current_cost = cost_function(current_labels)
        population.append(current_labels)

    # print(population)

    # Main loop
    for _ in range(NUM_GENERATIONS):
        # Select parents for crossover
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        while parent1 == parent2:
            parent1 = random.choice(population)
            parent2 = random.choice(population)


        # print(parent1)
        # print(parent2)

        # Perform crossover and mutation to create new generation
        child1, child2 = crossover(parent1, parent2, adjacency_matrix)
        # child1 = mutate(child1)
        # child2 = mutate(child2)

        # print(child1)
        # print(child2)

        # Replace parents with children
        population.append(child1)
        population.append(child2)

        population = sorted(population, key=lambda x: cost_function(x))[:POPULATION_SIZE]

    # Return the best solution found
    best_solution = min(population, key=lambda x: cost_function(x))
    best_cost = cost_function(best_solution)
    return best_solution, best_cost


if __name__ == "__main__":
    adjacency_matrix = make_adjacency_list()  
    num_nodes = len(adjacency_matrix)
    best_solution, best_cost = genetic_algorithm(num_nodes, adjacency_matrix)
    print("Best solution:", best_solution)
    print("Cost:", best_cost)



# adjacency_list = make_adjacency_list()
# vertex_labels = Heuristic_2(adjacency_list)
# print("Vertex Labels:", vertex_labels)
# print("Cost: ", sum(vertex_labels.values()))
# print(check_feasibility(vertex_labels, adjacency_list))







