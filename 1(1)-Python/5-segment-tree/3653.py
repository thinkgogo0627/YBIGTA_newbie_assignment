from lib import SegmentTree
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