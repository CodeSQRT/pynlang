class TabManager:
	def __init__(self):
		self.tabs = dict()
		self.last_index = 0
		self.next_state = True
		self.count = 0

	def __getitem__(self, name):
		return self.tabs[name]

	def push(self, count, status):
		self.tabs[count] = status
		self.last_index = count