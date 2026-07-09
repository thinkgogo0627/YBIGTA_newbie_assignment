from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    n = int(input())
    max_taste = 1000000
    '''
    case 1
    A:1 >> 사탕상자에서 사탕 꺼내는 경우
    한 정수만 주어짐, B: 꺼낼 사탕의 순위 주어짐
    
    case 2
    A:2 >> 사탕을 넣는 경우
    두 개의 정수 주어짐, B: 넣을 사탕 맛 나타내는 정수, C는 사탕의 갯수
    C가 양수? -> 사탕 넣는 경우, C가 음수? -> 사탕 빼는 경우
    '''
    candy_box: SegmentTree[int, int] = SegmentTree(
        data=[0] * (max_taste + 1),
        identity=0,
        merge=lambda a, b: a + b,)

    results = []

    for _ in range(n):
        queries = list(map(int, input().split()))

        # case 1
        if len(queries) == 2:
            _, B = queries
            idx = candy_box.find_kth(B)
            results.append(idx)
            current = candy_box.query(idx, idx)
            candy_box.update(idx, current - 1)

        # case 2
        else:
            _, B, C = queries
            current = candy_box.query(B, B)
            candy_box.update(B, current + C)

    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()