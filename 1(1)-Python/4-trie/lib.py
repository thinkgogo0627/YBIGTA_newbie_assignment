from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    ## 문자열 삽입
    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        # 루트 인덱스
        cur_idx = 0

        for char in seq:
            # 현재 노드의 자식들 중 body == char인 노드 찾기
            next_idx: Optional[int] = None
            for child_idx in self[cur_idx].children:
                if self[child_idx].body == char:
                    next_idx = child_idx
                    break

            # 없음? -> 새로 제작 후 Trie(list)에 추가
            if next_idx is None:
                new_node = TrieNode(body=char)
                self.append(new_node)
                next_idx = len(self) - 1
                self[cur_idx].children.append(next_idx)

            cur_idx = next_idx

        self[cur_idx].is_end = True