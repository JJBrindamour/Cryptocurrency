class Chain:
	def __init__(self):
		self.validatedBlocks = []
		self.pendingBlocks = []
		self.transactionBlock = None
		self.accounts = []

	def validateBlock():
		pass

class Block:
	def __init__(self, chain):
		self.transactions = []
		self.chain = chain
		self.capacity = 3
	
	def addTransaction(self, transaction):
		self.transactions.append(transaction)
		if len(self.transactions) >= self.capacity:
			self.chain.pendingBlocks.append(self)

class Transaction:
	def __init__(self, amount, sender, reciver):
		self.amount = amount
		self.sender = sender
		self.reciver = reciver

class Wallet:
	def __init__(self, publicKey, privateKey):
		self.publicKey = publicKey
		self.privateKey = privateKey
		self.balance = 0

	def send(self, amount, reciver):
		pass
