from PyQt5.QtWidgets import QFrame


class HLine(QFrame):
  def __init__(self):
    super(HLine, self).__init__()
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)


class VLine(QFrame):
  def __init__(self):
    super(VLine, self).__init__()
    self.setFrameShape(QFrame.VLine)
    self.setFrameShadow(QFrame.Sunken)