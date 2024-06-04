# from numpy import random

# random.seed(44)
# rand_list=[]
# n=22
# rand_list = random.choice(['x', 'w', 'r', 'h','c'], p=[0.2, 0.2, 0.2, 0.2,0.2], size=(n))

# print(rand_list)


# import random as random1
import random

N = 22
R = 1
 
random.seed(44)

generate_tuples = lambda N, R: [(random.randint(0, R), random.randint(0, R)) for _ in range(N)]

output = generate_tuples(N, R)
print(output)
# random1.seed(44)
# print(generate_tuples(N,R))