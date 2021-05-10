from referee.main import main
import time

i = 0
t = []
while i < 3:
    start = time.time()
    pivot = main()
    end = time.time()
    t.append(end - start - 2)
    i += 1


print(t)
print(sum(t) / i)

