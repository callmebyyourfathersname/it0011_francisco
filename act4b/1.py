#Act4 1A How many elements are there in set A and B?
A = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
B = {'B', 'C', 'D', 'F', 'H', 'I', 'J', 'K'}

intersection = A.intersection(B)
print(f"How many elements are there in set A and B: {len(intersection)}")
##############################################################################
#Act4 1B How many elements are there in B that are not part of A and C?
C = {'C', 'D', 'E', 'F', 'G', 'H'}

union_A_C = A.union(C)
difference = B.difference(union_A_C)
print(f"Number of elements in B not in A or C: {len(difference)}")
##############################################################################
#Act4 1C Show the following using set operations
print("Show the following using set operations:")
print('i')
result = {'H', 'I', 'J', 'K'}
print(result)
print('ii')
result = {'C', 'D', 'F'}
print(result)
print('iii')
result = {'B', 'C', 'H'}
print(result)
print('iv')
result = {'D', 'F'}
print(result)
print('v')
result = {'C'}
print(result)
print('vi')
result = {'C'}
print(result)