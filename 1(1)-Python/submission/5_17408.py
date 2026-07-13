from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable, cast


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    def __init__(
        self,
        data: list[T],
        identity: T,
        merge: Callable[[T, T], T],
    ) -> None:
        """
        data: 초기 배열
        identity: merge의 항등원 (합이면 0)
        merge: 두 값을 합치는 함수
        """
        self.n: int = len(data)
        self.identity: T = identity
        self.merge: Callable[[T, T], T] = merge
        self.tree: list[T] = [identity] * (2 * self.n)
        self.build(data)

    def build(self, data: list[T]) -> None:
        """리프 노드를 데이터로 채우고 내부 노드를 병합 결과로 채운다."""
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, left: int, right: int) -> T:
        """[left, right] 구간을 병합한 결과를 반환한다."""
        left += self.n
        right += self.n
        result = self.identity

        while left <= right:
            if left % 2 == 1:
                result = self.merge(result, self.tree[left])
                left += 1
            if right % 2 == 0:
                result = self.merge(result, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        return result

    def update(self, pos: int, value: T) -> None:
        """특정 위치의 값을 바꾸고 부모 노드들을 갱신한다."""
        pos += self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.merge(self.tree[2 * pos], self.tree[2 * pos + 1])


    def find_kth(self, k: int) -> int:
        """구간 합 기준으로 k번째 원소의 인덱스를 찾는다 (1-indexed)."""
        node = 1
        while node < self.n:
            left_child = 2 * node
            left_val = cast(int, self.tree[left_child])
            if k <= left_val:
                node = left_child
            else:
                k -= left_val
                node = left_child + 1
        return node - self.n


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