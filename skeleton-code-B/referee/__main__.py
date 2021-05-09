from referee.main import main
import time

i = 0
t = []
while i < 10:
    start = time.time()
    main()
    end = time.time()
    t.append(end - start)
    i += 1


print(t)

