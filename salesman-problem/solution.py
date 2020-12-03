class Solution:
  def __init__(self, num):
    self.index = num
    self.solution = []
    self.value = 0
    self.iterations = []

  def set(self, solution, value, iterations):
    self.solution = solution
    self.value = value
    self.iterations = iterations
  
  def get(self):
    return self.solution, self.value, self.iterations