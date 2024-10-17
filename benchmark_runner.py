
import os, json
from tqdm import tqdm
from my_utils import *
from algorithm_metrics import *
from tsp_utils import *
from dataset_generator import *

def save_results(results, output_file):
    """
    Salva il dizionario dei risultati in un file JSON.
    
    Parametri:
    - results (dict): Dizionario con i risultati da salvare.
    - output_file (str): Percorso del file JSON dove salvare i risultati.
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

def insert_results(results, num_vertices, max_coord, path_distance, execution_time, average_execution_time):
    """
    Inserts the results of a TSP benchmark into the results dictionary.
    Parameters:
    results (dict): The dictionary to store the results. The keys are tuples of (num_vertices, max_coord),
                    and the values are lists of tuples containing (path_distance, execution_time, average_execution_time).
    num_vertices (int): The number of vertices in the TSP instance.     -->  These are the
    max_coord (int): The maximum coordinate value for the vertices.     -->  keys of the dictionary
    path_distance (float): The total distance of the path found.
    execution_time (float): The time taken to find the path.
    average_execution_time (float): The average time taken over multiple runs to find the path.
    Returns:
    None
    """
    key = (num_vertices, max_coord)
    
    # Crea una nuova lista se la chiave non esiste
    if key not in results:
        results[key] = []
    
    # Aggiungi i nuovi risultati alla lista
    results[key].append((path_distance, execution_time, average_execution_time))

def print_results(results):
    """
    Stampa in maniera chiara e leggibile i risultati contenuti nel dizionario.
    Il dizionario ha chiavi come tuple (num_vertices, max_coord) e valori come liste di tuple
    (path_distance, execution_time, average_execution_time).
    
    Parametri:
    results (dict): Dizionario che contiene i risultati delle istanze TSP.
    """
    for key, values in results.items():
        num_vertices, max_coord = key
        print(f"Numero Vertici: {num_vertices}, Max Coordinata: {max_coord}")
        print("--------------------------------------------------------")
        print(f"{'Path Distance':<20} {'Execution Time (s)':<20} {'Avg Execution Time (s)':<25}")
        print("-" * 65)
        
        for path_distance, execution_time, avg_execution_time in values:
            print(f"{path_distance:<20.5f} {execution_time:} {avg_execution_time:}")
        
        print("\n")  # Stampa una riga vuota tra le diverse combinazioni

def generate_statistics(num_vertices_list, max_coords_list, num_instances, input_dir, function):
    total_files = len(num_vertices_list) * len(max_coords_list) * num_instances
    results = {}

    with tqdm(total=total_files, desc="Esecuzione benchmark TSP") as pbar:
            for num_vertices in num_vertices_list: # For each number of vertices
                    for max_coord in max_coords_list:  # For each maximum coordinate value     --> this create all the possible combinations
                        
                        with tqdm(total=num_instances, desc=f"Vertici: {num_vertices}, Max Coord: {max_coord}", leave=False) as instance_bar:
                            for instance_num in (range(1, num_instances + 1)):
                                # Create the path of the file
                                instance_path = os.path.join(input_dir, f"NumVertices_{num_vertices}", f"MaxVal_{max_coord}", f"instance_{instance_num}.csv")
                                # Load the graph graph
                                points, dist = load_graph_data(instance_path)
                                # Run the algorithm
                                path= function(points, dist) # oppure la funzione passata come parametro 
                                # Compute the metrics
                                path_distance = path_length(dist, path)
                                execution_time = research_path_time(points, dist, function)
                                average_execution_time = average_research_path_time(points, dist, function, num_runs=1000)
                                
                                insert_results(results, num_vertices, max_coord, path_distance, execution_time, average_execution_time)
                                
                                instance_bar.update(1)
                                pbar.update(1)  
            save_results(results, "better_name.json")   
            return results
                # La struttura dati per memorizzare queste info sarà fatta così:
                # dizionario chaive = coppia (num_vertices, max_coord) e valore = lista di tuple (path_distance, execution_time, average_execution_time)
                # Ci sarà un dizionario per ogni algoritmo
                # Visivamente:
                # results = {
                #             (num_vertices, max_coord): [
                #                 (path_distance_1, execution_time_1, average_execution_time_1),
                #                 (path_distance_2, execution_time_2, average_execution_time_2),
                #                 ...
                #             ],
                #             ...
                #         }
                # results = {
                #             (10, 10): [
                #                 (123.4, 0.0012, 0.0011),  # Prima istanza per 10 vertici, max coord 10
                #                 (134.6, 0.0014, 0.0012)   # Seconda istanza per 10 vertici, max coord 10
                #             ],
                #             (10, 100): [
                #                 (543.7, 0.0023, 0.0020),  # Prima istanza per 10 vertici, max coord 100
                #                 (567.1, 0.0025, 0.0021)   # Seconda istanza per 10 vertici, max coord 100
                #             ],
                #             (50, 10): [
                #                 (1523.6, 0.0121, 0.0117), # Prima istanza per 50 vertici, max coord 10
                #                 (1601.3, 0.0128, 0.0119)  # Seconda istanza per 50 vertici, max coord 10
                #             ],
                #             (50, 1000): [
                #                 (6543.2, 0.0456, 0.0440), # Prima istanza per 50 vertici, max coord 1000
                #                 (6600.1, 0.0462, 0.0445)  # Seconda istanza per 50 vertici, max coord 1000
                #             ]
                #         }
                
# Allora adesso ho salvato tutti i grafi in file csv che faranno parte del mio benchmarks. Adesso ho bisogno di chiamare il mio algoritmo nearest_neighbor_first su ogni istanza. E in seguito ottenere i dati statistici dell'algoritmo.
num_vertices_list= [10, 50, 100, 500, 1000]
max_coords_list = [50, 100, 1000]
num_instances = 20
input_dir = "./data/euclidean"
function = nearest_neighbor_first
dictionary = generate_statistics(num_vertices_list, max_coords_list, num_instances, input_dir, function)
print_results(dictionary)