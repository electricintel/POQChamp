# Most of the credit for this goes to aunyks who coded the Snakecoin that I'm using as the base. <3

import hashlib as hasher
import datetime as date
import projectq
from projectq.ops import H, Measure
from projectq import MainEngine

# Define what a POQChamp block is
class Block:
   
  def __init__(self, index, timestamp, data, previous_hash, random_number):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
    self.random_number = self.random_number()
  
  def random_number(quantum_engine): 
    quantum_engine = MainEngine()
    qubit = quantum_engine.allocate_qubit()
    H | qubit
    Measure | qubit
    random_number = int(qubit)
    return random_number


  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8') + str(self.random_number).encode('utf-8')) 
    return sha.hexdigest()

# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", "0", 0)

# Generate all later blocks in the blockchain
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = str(this_index)
  this_hash = last_block.hash
  this_random_number = last_block.random_number
  return Block(this_index, this_timestamp, this_data, this_hash, this_random_number)

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  block_to_add = next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  print ("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print ("Hash: {}\n".format(block_to_add.hash)) 

