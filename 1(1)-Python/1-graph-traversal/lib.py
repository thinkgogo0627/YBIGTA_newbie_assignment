from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n = n
        # {0: [1, 2, .. ] , 1: [0, 3, 4, ...]}
        self.graph: dict[int, list[int]] = {i: [] for i in range(1, self.n + 1)}

        

    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        self.graph[u].append(v)
        self.graph[v].append(u)

        ## 방문가능 노드 여러개? -> 노드번호 작은것 먼저 방문
        ## 노드 오름차순 정렬 필요..
        self.graph[u].sort()
        self.graph[v].sort()
        pass
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        구현 방법 선택:
        1. 재귀 방식: 함수 내부에서 재귀 함수 정의하여 구현
        2. 스택 방식: 명시적 스택을 사용하여 반복문으로 구현
        """
        self.visited: list[int] = [] # 방문 노드 기록할 리스트

        def dfs_recur(node):
            self.visited.append(node)

            # 현재 노드와 연결된 다른 노드 순회
            for neighbor in self.graph[node]:
                # 아직 방문 안했으면? -> 재귀호출하며 방문
                if neighbor not in self.visited:
                    dfs_recur(neighbor)
        
        dfs_recur(start)
        return self.visited
        
    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현
        """
        self.visited =  []
        self.queue = deque([start])
        self.visited.append(start)

        # 큐 빌때까지 반복
        while self.queue:
            current_node = self.queue.popleft()

            # 현재 노드와 연결된 다른 노드 순회
            for neighbor in self.graph[current_node]:
                # 아직 방문 안했으면? -> 방문처리 후 큐에 추가
                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    self.queue.append(neighbor)

        
        return self.visited

    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))
