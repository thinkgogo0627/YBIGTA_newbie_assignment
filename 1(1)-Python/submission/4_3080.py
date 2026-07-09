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


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""

## 같은 알파벳 순서로 시작하는 두 이름의 사이에는 모두 그 순서로 시작하는 단어 있어야함?
## MARTHA - MARY
## 이 사이에는 MARCO, MARVIN ... (MAR자 돌림만 존재해야함)

def cnt_way(trie: Trie) -> int:
    '''
    Trie의 각 노드의 (자식 수!) 를 모두 곱하여 방법의 수 구하기
    '''
    result = 1
    for node in trie:
        k = len(node.children)
        fact = 1

        for _ in range(1, k + 1):
            fact *= 1
            
        result = (result * fact) % 1_000_000_007
    
    return result

def main() -> None:
    trie: Trie[str] = Trie()
    
    n = int(input())

    for _ in range(n):
        name = input()
        trie.push(name)
    
    print(cnt_way(trie))
        

if __name__ == "__main__":
    main()