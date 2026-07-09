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
    '''
    dvd 스택 -> dvd 위치 찾은 다음 pop
    영화 다 본 뒤 가장 위에 놓기

    영화 볼 때마다 그 dvd 위에 몇 개의 dvd 있었는지 구해야 함
    '''
    tcase = int(input())

    results = []

    for _ in range(tcase):
        n, m = map(int, input().split())
        movie_order = list(map(int, input().split()))

        size = 2 * n
        dvd_stack: SegmentTree[int, int] = SegmentTree(
            data=[0] * (size + 1),
            identity=0,
            merge=lambda a, b: a + b,
        )

        pos = [0] * (n + 1)  # pos[영화번호] = 세그트리에서의 위치
        for i in range(1, n + 1):
            pos[i] = n + i
            dvd_stack.update(n + i, 1)

        next_top = n  # 다음에 맨 위로 옮길 때 쓸 위치 (점점 감소)
        answers = []

        for movie in movie_order:
            cur_pos = pos[movie]
            # 이 영화보다 "위"(더 작은 위치)에 있는 DVD 개수
            above = dvd_stack.query(1, cur_pos - 1) if cur_pos > 1 else 0
            answers.append(above)

            # 이 영화를 스택에서 제거
            dvd_stack.update(cur_pos, 0)
            # 맨 위 새 자리에 삽입
            dvd_stack.update(next_top, 1)
            pos[movie] = next_top
            next_top -= 1

        results.append(' '.join(map(str, answers)))

    print('\n'.join(results))




if __name__ == "__main__":
    main()