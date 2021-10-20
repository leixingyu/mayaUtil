def remove_duplicates(seq):
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
    import collections
    dups = [item
            for item, count in collections.Counter(seq).items()
            if count > 1]
    return dups


def get_percentages(sample_count):
    if sample_count <= 1:
        return

    outputs = list()
    gap = 1.00 / (sample_count-1)
    for index in range(sample_count):
        outputs.append(index * gap)

    return outputs
