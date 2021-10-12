def remove_duplicates(seq):
    """
    | Fastest order preserving way to make a list unique
    | http://www.peterbe.com/plog/uniqifiers-benchmark
    | Specific method by: ``Dave Kirby``

    :param seq: Input sequence
    :type seq: list
    :return: Unique sequence
    :rtype: list
    """
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]
