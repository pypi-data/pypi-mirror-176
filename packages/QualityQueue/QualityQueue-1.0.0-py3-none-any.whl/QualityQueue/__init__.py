class QueueError(BaseException):
  def __init__(self,m='An unspecifeid error occurred'):
    self.msg = m
  def __str__(self):
    return self.msg
  def __repr____(self):
    return self.msg  

class queue:
  def __init__(self):
    self.qlist = [ ]
  def push(self,val):
    self.qlist.append(val)
  def pop(self):
    try:
      re = self.qlist[0]
    except IndexError:
      raise QueueError("can't pop from empty stack") 
    self.qlist.remove(re)
    return re
  def isempty(self):
    if self.qlist == []:return 1 
    else: return 0
      
  def get_first(self):
    try: 
      return self.qlist[0]
    except IndexError:
      return QueueError("can't get from empty stack") 
  def printall(self):
    print(self.qlist)
  def __str__(self):
    return f"{self.qlist}"
  def __repr__(self):
    return f"{self.qlist}"
   
