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
from typing import Optional

"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: Optional[int] = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break
        
        if new_index is None:
            break

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    lines = sys.stdin.read().split('\n')
    idx = 0
    results = []

    while idx < len(lines) and lines[idx].strip() != '':
        n = int(lines[idx].strip())
        idx += 1

        words = []
        for _ in range(n):
            words.append(lines[idx].strip())
            idx += 1

        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)

        total = sum(count(trie, word) for word in words)
        avg = total / n
        results.append(f"{avg:.2f}")

    print('\n'.join(results))


if __name__ == "__main__":
    main()