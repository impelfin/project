#!/usr/bin/env python

n = int(input("how much number input? : "))

building = list(map(int, input().split()))
print("\nbuilding :", building)

min_build = min(building)
print("\nmin(build) :", min_build)

min_build = min(building) * n
print("\nmin(building) * n  :", min_build)

sum_building = sum(building)
print("\nsum_building :", sum_building)

result = sum(building) - min_build
print("\nsum(build) - n :", result)
