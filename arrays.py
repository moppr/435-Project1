import random


def get_random_array(n):
    # No constraint for the values of the array was provided, so n*10 being used arbitrarily.
    return random.sample(range(0, n*10), n)


def get_sorted_array(n):
    return list(range(n, 0, -1))


if __name__ == "__main__":
    n = 4
    print(f'random arrays x{n}')
    for _ in range(n):
        print(get_random_array(8))
    print('\nsorted array')
    print(get_sorted_array(8))
