from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    # 원본 값을 Pair로 변환해서 세그트리 초기화
    data = [Pair.f_conv(w) for w in arr]
    seg: SegmentTree[Pair, int] = SegmentTree(
        data=data,
        identity=Pair.default(),
        merge=Pair.f_merge,
    )

    m = int(input())
    results = []
    for _ in range(m):
        q = list(map(int, input().split()))
        if q[0] == 1:
            # 1 i v: i번째(1-indexed)를 v로 변경
            i, v = q[1], q[2]
            seg.update(i - 1, Pair.f_conv(v))   # 0-indexed로 변환
        else:
            # 2 l r: [l, r] 구간의 최대 두 값 합
            l, r = q[1], q[2]
            result = seg.query(l - 1, r - 1)    # 0-indexed
            results.append(result.sum())

    print('\n'.join(map(str, results)))
    


if __name__ == "__main__":
    main()