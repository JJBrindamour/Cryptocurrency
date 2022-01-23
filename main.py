import rsa, hashlib

class Chain:
	def __init__(self):
		self.validatedBlocks = [Block(self, 'Genisis Block')]
		self.validatedBlocks[0].hash = hashlib.sha256('Genisis Block')
		self.pendingBlocks = []
		self.transactionBlock = Block(self, hashlib.sha256('Genisis Block'))
		self.accounts = {}
		self.validators = []

class Block:
	def __init__(self, chain, prevBlockHash):
		self.transactions = []
		self.chain = chain
		self.capacity = 3
		self.previousHash = prevBlockHash
		self.hash = None
		self.data = ''
		self.votes = []
	
	def addTransaction(self, transaction):
		self.transactions.append(transaction)
		if len(self.transactions) >= self.capacity:
			self.data = ' | '.join([' - '.join((transaction.sender, transaction.amount, transaction.reciver)) \
				for transaction in self.transactions] + ' || ' + self.previousHash).encode('ascii')
			self.hash = hashlib.sha256(self.data)
			self.chain.pendingBlocks.append(self)

	def vote(self, vote, blockSignature, publicKey):
		if publicKey in self.chain.validators and rsa.decrypt(blockSignature, publicKey) == self.data:
			self.votes.append((vote, blockSignature, publicKey))

class Transaction:
	def __init__(self, amount, senderPubKey, senderPrivKey, reciver):
		self.amount = amount
		self.sender = senderPubKey
		self.reciver = reciver
		self.signature = self.sign(senderPrivKey)

	def sign(self, key):
		data = f'{self.sender} sending {self.amount} to {self.reciver}'
		return rsa.encrypt(data.encode('ascii'), key)

class Wallet:
	def __init__(self, chain):
		self.balance = 0
		self.publicKey, self.privateKey = rsa.newkeys(4096)
		chain.accounts[self.publicKey] = 0

	def send(self, amount, reciver):
		transaction = Transaction(amount, self.publicKey, self.privateKey, reciver)

class Validator:
	def __init__(self, chain, wallet):
		self.chain = chain
		self.wallet = wallet
		self.chain.validators.append(self.wallet.publickKey)

	def validateBlock(self):
		block = self.chain.pendingBlocks[0]
		for transaction in block.transactions:
			if rsa.decrypt(transaction.signature, transaction.sender) == \
			f'{transaction.sender} sending {transaction.amount} to {transaction.reciver}' and \
			self.chain.accounts[transaction.sender] >= transaction.amount:
				block.vote(True, rsa.encrypt(block.data.encode('ascii'), self.wallet.privateKey), self.wallet.publicKey)