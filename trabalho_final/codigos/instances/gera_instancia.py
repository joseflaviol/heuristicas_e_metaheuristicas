import random 

def main():
    n_v = int(input())
    
    added = {}

    i = 0
    
    while i < (n_v):
        x = random.randint(0, 1000)
        y = x
        
        while y == x:
            y = random.randint(0, 1000)

        if (x, y) in added:
            continue

        added[(x, y)] = True

        i += 1

    with open('%dg.txt' % (n_v), 'w') as f:
        for (x, y) in added:
            f.write('%d %d\n' % (x, y))

main()    
