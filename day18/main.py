from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from copy import deepcopy

from dataclasses import dataclass, field
from functools import reduce
from typing import Union

import operator


class Node(ABC):
    def __init__(self, left, right, depth, parent):
        self.left = left
        self.right = right
        self.depth = depth
        self.parent = parent

    def get_left_adjacent_cousin(self):
        current = self
        predecessor = self.left
        while current.left == predecessor:
            # Root node has no left adjacent cousins
            if not current.parent:
                return None

            predecessor = current
            current = current.parent

        current = current.left

        # Go as right and down as we can
        while current.right:
            current = current.right

        return current

    def get_right_adjacent_cousin(self):
        current = self
        predecessor = self.right
        while current.right == predecessor:
            # Root node has no right adjacent cousins
            if not current.parent:
                return None

            predecessor = current
            current = current.parent

        current = current.right

        # Go as left and down as we can
        while current.left:
            current = current.left

        return current

    def children(self):
        queue = deque([self.right, self.left])

        while queue:
            current = queue.pop()
            yield current

            if current.right:
                queue.append(current.right)
            if current.left:
                queue.append(current.left)

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @abstractmethod
    def can_explode(self):
        ...

    @abstractmethod
    def can_split(self):
        ...

    def split(self):
        raise Exception('Cannot split this type of node.')


class NumberNode(Node):
    def __init__(self, value, depth, parent):
        self.value = value

        super().__init__(None, None, depth, parent)

    def magnitude(self):
        return self.value

    def can_explode(self):
        return False

    def can_split(self):
        return self.value >= 10

    def split(self):
        new_child_depth = self.depth + 1
        left_value = self.value // 2
        right_value = self.value // 2 + (self.value % 2 > 0)
        replacement_node = PairNode(
            left=NumberNode(value=left_value, depth=new_child_depth, parent=None),
            right=NumberNode(value=right_value, depth=new_child_depth, parent=None),
            depth=self.depth,
            parent=self.parent,
        )
        replacement_node.left.parent = replacement_node
        replacement_node.right.parent = replacement_node
        return replacement_node


class PairNode(Node):
    def __init__(self, left, right, depth, parent):
        self.left = left
        self.right = right
        self.depth = depth
        self.parent = parent

    def __add__(self, other):
        left = deepcopy(self)
        right = deepcopy(other)
        sum_node = PairNode(left=left, right=right, depth=0, parent=None)

        # Bump the depths of all other nodes
        sum_node.left.depth += 1
        for child in sum_node.left.children():
            child.depth += 1

        sum_node.right.depth += 1
        for child in sum_node.right.children():
            child.depth += 1

        # Fix up parental linkages
        sum_node.left.parent = sum_node
        sum_node.right.parent = sum_node

        # Reduce before continuing
        sum_node.reduce()
        return sum_node

    def _find_explodable_child(self):
        for child in self.children():
            if child.can_explode():
                return child

        return None

    def _find_splittable_child(self):
        for child in self.children():
            if child.can_split():
                return child

        return None

    def reduce(self):
        child_to_explode = self._find_explodable_child()
        child_to_split_asunder = self._find_splittable_child()

        while child_to_explode or child_to_split_asunder:
            if child_to_explode:
                left = child_to_explode.get_left_adjacent_cousin()
                if left:
                    left.value += child_to_explode.left.value

                right = child_to_explode.get_right_adjacent_cousin()
                if right:
                    right.value += child_to_explode.right.value

                parent = child_to_explode.parent  # Exploding nodes are guaranteed to have a parent
                replacement_node = NumberNode(
                    value=0,
                    depth=child_to_explode.depth,
                    parent=parent,
                )
                if parent.left == child_to_explode:
                    parent.left = replacement_node
                elif parent.right == child_to_explode:
                    parent.right = replacement_node
            elif child_to_split_asunder:
                parent = child_to_split_asunder.parent  # Exploding nodes are guaranteed to have a parent
                replacement_node = child_to_split_asunder.split()
                if parent.left == child_to_split_asunder:
                    parent.left = replacement_node
                elif parent.right == child_to_split_asunder:
                    parent.right = replacement_node

            child_to_explode = self._find_explodable_child()
            child_to_split_asunder = self._find_splittable_child()

    def can_explode(self):
        return self.depth >= 4

    def can_split(self):
        return False


def parse_line_as_snailfish_num(line):
    op_stack = list()
    value_stack = list()

    for c in line:
        if c == '[':
            op_stack.append(c)
        elif c.isdigit():
            num = NumberNode(depth=len(op_stack), value=int(c), parent=None)
            value_stack.append(num)
        elif c == ']':
            right = value_stack.pop()
            left = value_stack.pop()
            op_stack.pop()
            parent = PairNode(left=left, right=right, depth=len(op_stack), parent=None)
            left.parent = parent
            right.parent = parent
            value_stack.append(parent)

    assert len(value_stack) == 1
    return value_stack.pop()


with open('input') as f:
    lines = [l.strip() for l in f.readlines()]

snailfish_nums = [parse_line_as_snailfish_num(l) for l in lines]
print(f'Part 1 solution: {reduce(operator.add, snailfish_nums).magnitude()}')

sums = set()
for n in range(len(snailfish_nums)):
    for m in range(len(snailfish_nums)):
        if n == m:
            continue

        sums.add((snailfish_nums[n] + snailfish_nums[m]).magnitude())
print(f'Part 2 solution: {max(sums)}')