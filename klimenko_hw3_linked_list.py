class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

    def size(self): # вернуть длину списка
        size = 0
        if not self.empty():
            node = self.head
            while node:
                size += 1
                node = node.next
        return size

    def delete(self, value):  # удалить значение value из списка
        if not self.empty():
            node_d = self.head
            node_p = None
            while node_d:
                if node_d.data == value:
                    if node_p == None and node_d.next == None:
                        self.head = None
                    elif node_p == None and node_d.next != None:
                        self.head = node_d.next
                    elif node_p != None:
                        node_p.next = node_d.next
                    return True
                node_p = node_d
                node_d = node_d.next
        return print('Ошибка: список пуст')

    def insert(self, index, value):# вставить значение value в список в позиции index
        if not self.empty() and index + 1 <= self.size():
            if index != 0:
                node = self.head
                node_p = None
                for i in range(index):
                    node_p = node
                    node = node.next
                node_new = Node(value, next=node)
                node_p.next = node_new
            else:
                node_new = Node(value, next=self.head)
                self.head = node_new
            return True
        return print('Ошибка: индекс слишком большой или список пуст')

    def deleteAtPosition(self, index): # удалить узел из списка в позиции index
        if index+1 <= self.size(): # проверяем есть ли индекс в списке
            i = 0
            prev = self.head
            if index != 0: # если не первый
                for i in range(index-1):
                    prev = prev.next
                position = prev.next
                prev.next = position.next
            else:
                if prev.next:
                    self.head = prev.next
                else:
                    self.head = None
                return True
        return print('Ошибка: индекс слишком большой или список пуст')

    def value_at(self, index):  # вернуть значение узла в позиции index
        if index+1 <= self.size():
            i = 0
            node = self.head
            while i != index:
                node = node.next
                i += 1
            return node.data
        return print('Ошибка: индекс слишком большой или список пуст')

    def pop_front(self):  # удалить узел в начале связного списка и вернуть его значение
        if not self.empty():
            node = self.head
            self.head = node.next
            return node.data
        return print('Ошибка: список пуст')

    def pop_back(self):  # удалить узел в конце связного списка и вернуть его значение
        if not self.empty():
            node = self.head
            node_p = None
            while node.next:
                node_p = node
                node = node.next
            if node_p != None:
                node_p.next = None
            else:
                self.head = None
            return node.data
        return print('Ошибка: список пуст')

    def front(self):  # вернуть значение первого узла списка
        if not self.empty():
            node = self.head
            return node.data
        return print('Ошибка: список пуст')

    def back(self):  # вернуть значение последнего узла списка
        if not self.empty():
            node = self.head
            while node:
                node = node.next
                return node.data
        return print('Ошибка: список пуст')

    def reverse(self):
        if not self.empty():
            node = self.head
            snode = Node(node.data, next = None)
            reverse_self = LinkedList(head=snode)
            if node.next:
                node = node.next
                while node:
                    reverse_self.insert(0, node.data)
                    node = node.next
            return reverse_self
        return print('Ошибка: список пуст')

    def value_n_from_end(self, n):
        if not self.empty():
            reverse_self = self.reverse()
            return reverse_self.value_at(n)
        return print('Ошибка: список пуст')







n3 = Node(3)
n2 = Node(2, next=n3)
n1 = Node(1, next=n2)


l = LinkedList(head=n1)
for i in [1,2,3,4,5,4,5,6,6,6,6,1,1,54,3]:
    l.append(i)
l.printList()