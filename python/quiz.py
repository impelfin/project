n = int(input())
buliding = list(map(int, input().split()))
min_build = min(buliding) * n
print(sum(buliding) - min_build)
