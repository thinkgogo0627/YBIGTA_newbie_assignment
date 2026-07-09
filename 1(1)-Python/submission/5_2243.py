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