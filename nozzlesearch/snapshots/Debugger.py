from collections import Counter, defaultdict

def count_lanes_modules_in_dict(layered_dict):
    # Create a new dictionary to store the results
    result = defaultdict(lambda: defaultdict(list))

    for head_type, nozzle_dict in layered_dict.items():
        for nozzle_size, triplets in nozzle_dict.items():
            # Extract [lane, module] pairs from [lane, module, slot] triplets
            pairs = [(lane, module) for lane, module, slot in triplets]
            # Count occurrences of each [lane, module] pair
            counter = Counter(pairs)
            # Convert counts into the desired format
            result[head_type][nozzle_size] = [[lane, module, count] for (lane, module), count in counter.items()]

    # Convert defaultdict to a regular dict before returning
    return {head_type: dict(nozzle_dict) for head_type, nozzle_dict in result.items()}

# Example usage
layered_dict = {
    'head1': {
        'nozzle1': [[1, 2, 3], [1, 2, 4], [1, 2, 5], [2, 3, 6], [2, 3, 7], [2, 3, 8], [2, 3, 8], [2, 3, 9], [2, 3, 10], [2, 3, 11], [2, 3, 12]],
        'nozzle2': [[3, 4, 5], [3, 4, 6], [4, 5, 7]]
    },
    'head2': {
        'nozzle1': [[7, 8, 9], [7, 8, 10], [7, 9, 11], [10, 11, 12]],
        'nozzle2': [[13, 14, 15], [13, 14, 16], [14, 15, 17], [14, 15, 18]]
    }
}

new_layered_dict = count_lanes_modules_in_dict(layered_dict)
print(new_layered_dict)

input()