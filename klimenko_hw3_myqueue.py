class Stack:
    def __init__(self):
        self.stack = []
          

    def push(self, item): # положить элемент в стек
        self.stack.append(item)

    def pop(self): # удалить элемент из стека и вернуть его значение
        if not self.isEmpty:
            return self.stack.pop()
        return None

    def peek(self): # вернуть значение последнего элемента стека (не удаляя его)
        if not self.isEmpty:
            return self.stack[-1]
        return None

    def isEmpty(self): # вернуть True, если стек пуст, иначе вернуть False
        if self.stack == []:
            return True
        return False

class MyQueue:
    def __init__(self): # !!!Вероятно, ошибка вот здесь, потому что TypeError: enqueue() missing 1 required positional argument: 'item'
        self.stack_in = Stack()
        self.stack_out = Stack()

    def move(self): #перемещает из первого стека во второй
        for i in self.stack_in.stack:
            self.stack_out.push(i)

    def enqueue(self, item):  # положить элемент в очередь
        self.stack_in.push(item)

    def dequeue(self):  # удалить элемент из очереди и вернуть его значение
        if self.stack_out.isEmpty():
            if self.stack_in.isEmpty():
                return None
            self.move()
            return self.stack_out.pop()
        return self.stack_out.pop()

    def peek(self):  # вернуть значение первого элемента очереди (не удаляя его)
        if self.stack_out.isEmpty():
            if self.stack_in.isEmpty():
                return None
            self.move()
            return self.stack_out.peek()
        return self.stack_out.peek()

    def isEmpty(self):  # вернуть True, если стек пуст, иначе вернуть False
        if self.stack_in.isEmpty() and self.stack_out.isEmpty():
            return True
        return False

queue = MyQueue
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.enqueue(4)
queue.peek()