from classes.Result import Result
from typing import List

def select_result(results: List[Result]):
    best_result_num_identifieds = -1
    best_result_prob = 0
    best_result = None

    for result in results:
        if (len(result.relevant_infos_json) > best_result_num_identifieds) or (len(result.relevant_infos_json) == best_result_num_identifieds and result.rg_probability > best_result_prob):
            best_result = result
            best_result_num_identifieds = len(result.relevant_infos_json)
            best_result_prob = result.rg_probability
    
    return best_result
