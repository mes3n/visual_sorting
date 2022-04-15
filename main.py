import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from random import randint
from time import sleep

# run sorting algorithm separatly from main thread
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
async_result = pool.apply_async(lambda: 0)

# impor the basic algorithms
from algorithms import *

pygame.init()

WIDTH, HEIGHT = 700, 600

ARRAY_SIZE = WIDTH  # must be 0 <= x <= WIDTH

pause = True  # if visual pauses are enabled

app = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
pygame.display.set_caption("Sorting")
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# constant colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# values for each column
class ColumnEntity():
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.color = black

# class for the comlete list of columns
class ClassColumns():
    def __init__(self, values):
        self._list = [ColumnEntity(val, i) for i, val in enumerate(values)]  # each passed number becomes a colum
        self.value_list = values

    # functions to sort the list while showing graphics
    # slower and irrelevant for meta data

    def bubble_sort(self):  # sort based of bubble sort algorithm
        while True:
            if check_events() == 'stop': return  # exit if list is reset

            # find a colum which is larger than the one next to it
            for index, entity in enumerate(self._list):
                if index+1 != len(self._list):  # end of list
                    if entity.value > self._list[index+1].value:  # next number is smaller
                        current_entity = entity
                        current_index = index
                        break

            if current_entity:
                current_entity.color = red  # color selected column

                if pause: sleep(0.03)  # visual

                # move colum by one step until it is smaller than the column next to it
                while current_index+1 != len(self._list):  # stay within list
                    if check_events() == 'stop': return
                    # move colum until it is smaller than the one next to it
                    if current_entity.value > self._list[current_index+1].value:

                        # remove element and insert it at the position after
                        # also update affected elemets' properties

                        # insert colum at selcted spot

                        current_index += 1  # move one step to the right
                        self._list.remove(current_entity)
                        self._list.insert(current_index, current_entity)

                        # if pause: sleep(0.01)  # much more illustrative

                    else:  # it is
                        update()
                        break

                current_entity.color = blue

            else:
                # color all finished entities green
                for entity in self._list:
                    entity.color = green
                    update()

                    if pause: sleep(0.01)  # just for effect
                return
        return

    def selection_sort(self):  # sort based of the selection sort algorithm
        for i in range(len(self._list)):
            if check_events() == 'stop': return

            # select the smallest value of the segment and find a column with the same value
            # then place it at the front of the searched part of the list

            selected = min([entity.value for entity in self._list[i:]])  # find smallest value
            # select the entity
            for entity in self._list[i:]:
                if entity.value == selected:
                    current_entity = entity
                    break

            current_entity.color = red
            update()

            if pause: sleep(0.03)  # can see what is happening

            # move the selected entity to the start of the working list
            if current_entity:
                self._list.remove(current_entity)
                self._list.insert(i, current_entity)
                update()

                current_entity.color = blue
                update()

        else:  # when done color them green
            for entity in self._list:
                entity.color = green
                update()

                if pause: sleep(0.01)  # just for effect
            return

    def merge_sort(self):
        def merge(first_sublist, second_sublist):
            if check_events() == 'stop': main()  # exit merge_sort if r is pressed

            final  = []
            joined_list = first_sublist + second_sublist

            # color active elements red
            for entity in joined_list:
                entity.color = red
            update()

            for entity in joined_list:  # select the smallest number from sublist
                # only one of the sublists holds a value
                if not len(first_sublist) and len(second_sublist):
                    val = second_sublist[0]  # select the smallest value
                    second_sublist.remove(val)  # remove from list
                elif not len(second_sublist) and len(first_sublist):
                    val = first_sublist[0]
                    first_sublist.remove(val)
                # both sublists hold values
                else:
                    if first_sublist[0].value <= second_sublist[0].value:
                        val = first_sublist[0]  #
                        first_sublist.remove(val)
                    elif second_sublist[0].value < first_sublist[0].value:
                        val = second_sublist[0]
                        second_sublist.remove(val)

                final.append(val)  # append the smallest value of sublist to final

            # lower and upper indexes for the sublists in correlation to the source list
            lower = min([self._list.index(entity) for entity in joined_list])
            upper = lower + len(final)

            if pause: sleep(len(final)/100)  # sleep more as active lists get larger

            self._list[lower:upper] = final
            for entity in final:
                entity.color = blue
            update()

            if pause: sleep(0.01)

            return final

        def split(split_list):
            if check_events() == 'stop': main()

            # simply return list
            if len(split_list) == 1:
                return split_list

            # return list in order of small -> large
            if len(split_list) == 2:
                if split_list[0].value > split_list[1].value:
                    return split_list[::-1]

                else:
                    return split_list

            # find middle of list then merge the first and second half
            split_index = len(split_list) // 2 + (1 if len(split_list)%2 else 0)
            return merge(split(split_list[:split_index]), split(split_list[split_index:]))

        split(self._list)  # split list in half

        # color final result green
        for entity in self._list:
            entity.color = green
            update()

            if pause: sleep(0.01)  # just for effect

        return # [t.value for t in self._list]

def update():
    app.fill(white)

    # draw each colum
    for index, column in enumerate(columns._list):
        pygame.draw.rect(app, column.color, [blocksizex*index,
                         HEIGHT-blocksizey*column.value, blocksizex, HEIGHT])  # create the values as columns

    if async_result.ready():  # see if function is done
        # draw the return value of the function
        app.blit(font.render(str(async_result.get()) + " ms", True, black), (3, 3))


    pygame.display.update()

def check_events(from_main=False):
    global async_result, pause

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # closing window
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC to quit
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                pause = False if pause else True  # toggle pause
            if event.key == pygame.K_r:
                columns.__init__([randint(0, 100) for i in range(ARRAY_SIZE)])  # passes random list of integers
                return 'stop'  # exit merge sort function since its recursive
            if from_main:
                if event.key == pygame.K_b:
                    # get time of function by running it in a seperate thread
                    async_result = pool.apply_async(simple_bubble_sort_time, (columns.value_list))  # get time needed
                    columns.bubble_sort()  # sort list visually
                if event.key == pygame.K_s:
                    # get time of function by running it in a seperate thread
                    async_result = pool.apply_async(simple_selection_sort_time, (columns.value_list))
                    columns.selection_sort()  # sort list visually
                if event.key == pygame.K_m:
                    # get time of function by running it in a seperate thread
                    async_result = pool.apply_async(simple_merge_sort_time, (columns.value_list))
                    columns.merge_sort()  # sort list visually


def main():
    while True:
        check_events(from_main=True)
        update()

if __name__ == '__main__':
    columns = ClassColumns([randint(0, 100) for i in range(ARRAY_SIZE)])  # create a starting list of random integers

    blocksizex = WIDTH // len(columns._list)  # one colum is blocksizex wide
    blocksizey = HEIGHT // max(columns.value_list)  # highest value reaches top of window

    main()
