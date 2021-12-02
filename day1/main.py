def count_increases(l):
    increases = 0
    previous = l[0]

    for num in l[1:]:
        if num > previous:
            increases += 1
        previous = num
        
    return increases


with open('input') as input_file:
    measurements = [int(l.strip()) for l in input_file.readlines()]

print(count_increases(measurements))

# Part 2 is the same as Part 1, just using sums of 3 elements at a time
print(count_increases([sum(measurements[i:i+3]) for i in range(len(measurements) - 2)]))