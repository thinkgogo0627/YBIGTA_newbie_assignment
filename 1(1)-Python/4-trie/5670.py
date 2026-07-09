from lib import Trie
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