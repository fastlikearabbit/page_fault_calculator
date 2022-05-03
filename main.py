from collections import deque


def init_table(table, reference_string, memory_capacity):
    table[0][0] = ''.join(' ' * 8)
    for i in range(1, len(reference_string) + 1):
        table[0][i] = ''.join(reference_string[i - 1])

    for frame in range(1, int(memory_capacity) + 1):
        table[frame][0] = ''.join('Frame_' + str(frame) + ' ')

    table[int(memory_capacity) + 1][0] = ''.join("Page Fault")


def print_table(table, reference_string, memory_capacity):
    for i in range(int(memory_capacity) + 2):
        for j in range(len(reference_string) + 1):
            print(table[i][j], end='\t')
        print()


def show_page_faults(reference_string, memory_capacity, alg):
    table = [['_'] * (len(reference_string) + 1) for _ in range(int(memory_capacity) + 2)]
    init_table(table, reference_string, memory_capacity)
    queue = deque()
    lru_cache = []
    page_faults = 0

    for page_idx in range(int(memory_capacity)):
        # table[row][page_idx + 1], 1 <= row <= page_idx + 1

        if alg == "FIFO":
            queue.append(reference_string[page_idx])
        elif alg == "LRU":
            lru_cache.append(reference_string[page_idx])
        page_faults += 1
        table[int(memory_capacity) + 1][page_idx + 1] = ''.join("!")
        for row in range(1, page_idx + 2):
            table[row][page_idx + 1] = ''.join(reference_string[row - 1])

    current_col = int(memory_capacity) + 1

    for page in reference_string[int(memory_capacity):]:
        is_present = False
        for row in range(1, int(memory_capacity) + 1):
            if table[row][current_col - 1] == page:
                is_present = True

        if is_present:
            for row in range(1, int(memory_capacity) + 1):
                table[row][current_col] = ''.join(table[row][current_col - 1])

            if alg == "LRU":
                lru_cache.remove(page)
                lru_cache.append(page)

        else:
            page_to_remove = None
            if alg == "FIFO":
                page_to_remove = queue.popleft()
                queue.append(page)
            elif alg == "LRU":
                page_to_remove = lru_cache.pop(0)
                lru_cache.append(page)

            table[int(memory_capacity) + 1][current_col] = ''.join("!")
            for row in range(1, int(memory_capacity) + 1):
                if table[row][current_col - 1] == page_to_remove:
                    table[row][current_col] = ''.join(page)
                else:
                    table[row][current_col] = ''.join(table[row][current_col - 1])

            page_faults += 1

        current_col += 1

    print_table(table, reference_string, memory_capacity)

    print(f"The total number of page faults is {page_faults}")


def main():
    reference_string = input("Enter the pages the process should access, without spaces: ")
    reference_string = reference_string.upper()

    memory_capacity = input("Enter the total number of pages assigned to this process: ")

    alg = input("Enter the algorithm you want to use: ")
    alg = alg.upper()

    show_page_faults(reference_string, memory_capacity, alg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
