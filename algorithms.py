from time import time

# functions for just sorting a list with different algorithms
# can be used to collect meta data

def simple_bubble_sort_time(*sortable_list):
    start = time()

    sortable_list = list(sortable_list)
    # when using the threading library passing a list causes it to pass as *args
    # as such the *args need to be repacked and then turned into a list

    while True:

        # find and select a value with a smaller neighbor to the right
        for index, value in enumerate(sortable_list):
            if index + 1 != len(sortable_list):  # end of list
                if value > sortable_list[index + 1]:  # next number is smaller
                    current_value = value
                    current_index = index
                    break
            else:  # no smaller value can be found
                return round((time() - start)*1000, 4)  # convert to ms and round to 4 decimals

        while current_index + 1 != len(sortable_list):  # not at the end of list
            if current_value > sortable_list[current_index + 1]:

                # remove element and insert it at the position after
                # also update affected elemets' properties

                current_index += 1  # move value to the right
                # move the value to the new index
                sortable_list.remove(current_value)
                sortable_list.insert(current_index, current_value)
            else:
                break


def simple_selection_sort_time(*sortable_list):
    start = time()

    sortable_list = list(sortable_list)
    # when using the threading library passing a list causes it to pass as *args
    # as such the *args need to be repacked and then turned into a list

    for i in range(len(sortable_list)):
        # select the smallest value of the segment and find a column with the same value
        # then place it at the front of the searched part of the list

        selected = min([value for value in sortable_list[i:]])  # select the smallest value
        for value in sortable_list[i:]:
            if value == selected:
                current_value = value
                break

        if current_value:
            sortable_list.remove(current_value)
            sortable_list.insert(i, current_value)

    else:
        return round((time() - start)*1000, 4)


def simple_merge_sort_time(*sortable_list):
    start = time()

    sortable_list = list(sortable_list)
    # when using the threading library passing a list causes it to pass as *args
    # as such the *args need to be repacked and then turned into a list

    def merge(first_sublist, second_sublist):
        final  = []

        # take the smallest value of the sublists and append them to the final
        for i in range(len(first_sublist + second_sublist)):
            if not len(first_sublist) and len(second_sublist):
                val = second_sublist[0]
                second_sublist.remove(val)
            elif not len(second_sublist) and len(first_sublist):
                val = first_sublist[0]
                first_sublist.remove(val)
            else:
                if first_sublist[0] < second_sublist[0]:
                    val = first_sublist[0]
                    first_sublist.remove(val)
                elif second_sublist[0] < first_sublist[0]:
                    val = second_sublist[0]
                    second_sublist.remove(val)
                elif first_sublist[0] == second_sublist[0]:
                    val = first_sublist[0]
                    first_sublist.remove(val)

            final.append(val)

        return final

    def split(split_list):

        # return the lists with elements ordered from smallest -> largest
        if len(split_list) == 1:
            return split_list

        if len(split_list) == 2:
            if split_list[0] > split_list[1]:
                return split_list[::-1]

            else:
                return split_list

        # find the middle index
        split_index = len(split_list) // 2 + (1 if len(split_list)%2 else 0)
        return merge(split(split_list[:split_index]), split(split_list[split_index:]))

    sortable_list = split(sortable_list)  # start recurssion
    return round((time() - start)*1000, 4)
