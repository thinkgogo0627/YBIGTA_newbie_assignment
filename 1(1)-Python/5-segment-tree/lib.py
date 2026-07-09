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