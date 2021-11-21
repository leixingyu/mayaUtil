import collections


def get_list_unique(seq):
    """
    | Fastest order preserving way to make a list unique
    | http://www.peterbe.com/plog/uniqifiers-benchmark
    | Specific method by: ``Dave Kirby``

    :param seq: list. Input sequence
    :return: list. Unique sequence
    """
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def get_duplicates(seq):
    """
    Get duplicate in a list

    :param seq: list. original list of items
    :return: list. duplicated items
    """
    dups = [item
            for item, count in collections.Counter(seq).items()
            if count > 1]
    return dups


def get_percentages(sample_count):
    """
    Get normalized percent for each sample

    :param sample_count: int. number of sample point
    :return: list. normalized percents
    """
    if sample_count <= 1:
        return

    outputs = list()
    gap = 1.00 / (sample_count-1)
    for index in range(sample_count):
        outputs.append(index * gap)

    return outputs


def is_list_intersect(sub, sequence):
    """
    Find if any element in the subset belongs to a master sequence
    https://stackoverflow.com/questions/62115746/can-i-check-if-a-list-contains-any-item-from-another-list

    :return: bool. whether if the sequence contains any item from the subset
    """
    return any(item in sequence for item in sub)


def is_list_contained(sub, sequence):
    """
    Find if all elements in the subset belongs to a master sequence
    https://stackoverflow.com/questions/6159313/how-to-test-the-membership-of-multiple-values-in-a-list

    :return: bool. whether if the sequence contains all items of the subset
    """
    return all(item in sequence for item in sub)
