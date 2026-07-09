from lib import Trie
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