def max_length_from_choices(choices_dict):
    max_length = 0
    for choice in choices_dict.keys():
        max_length = max(max_length, len(choice))
    return max_length
