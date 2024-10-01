def hit_rate(relevance_total: list[list[bool]]) -> float:
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)


def mrr(relevance_total: list[list[bool]]) -> float:
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank]:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)
