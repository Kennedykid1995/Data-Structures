import time
import hashlib

"""
A class representing a single Block in a Blockchain
"""
class Block:
  def __init__(self, index, hash, previous_hash, timestamp, data):
    # The index of this Block in the Chain
    self.index = index
    # The hash of all this Block's data, including the previous Block's hash
    self.hash = hash
    # The hash for the previous Block in the Chain
    self.previous_hash = previous_hash
    # The timestamp of when this Block was created
    self.timestamp = timestamp
    # The data this Block holds
    self.data = data

  """
  Repr method that returns the Block represented as a string
  """
  def __repr__(self):
    return "Block(" + str(self.index) + "," + str(self.hash) + "," + str(self.previous_hash) + "," + str(self.timestamp) + "," + str(self.data)

  """
  Method to validate that this Block has the appropriate structure
  """
  def is_valid_block_structure(self):
    return isinstance(self.index, int) and isinstance(self.hash, str) and isinstance(self.previous_hash, str) and isinstance(self.timestamp, int) and isinstance(self.data, str)


"""
A class representing a Chain of Blocks
"""
class Chain:
  def __init__(self):
    # All the Blocks in the chain are stored in a list
    # The Blocks list is initialized with the genesis Block, which has no `previous_hash`
    self.blocks = [Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1465154705, 'my genesis block!!')]

  """
  Method to get the length of the Chain
  """
  def __len__(self):
    return len(self.blocks)

  """
  Add a Block to the Chain after validating it
  """
  def add_block(self, new_block):
    if self.is_valid_new_block(new_block):
      self.chain.append(new_block)

  """
  Return the last Block in the Chain
  """
  def get_latest_block(self):
    return self.blocks[-1]

  """
  Method to calculate the hash of all a Block's data
  """
  def calculate_hash(self, index, previous_hash, timestamp, block_data):
    # Use the hashlib library to generate a sha256 hash of all the Block's data
    return hashlib.sha256(index + previous_hash + timestamp + block_data)

  """
  Method to calculate the hash of a given Block
  """
  def calculate_hash_for_block(self, new_block):
    return self.calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data)

  """
  Method to generate a new Block given the data the Block is going to store
  """
  def generate_next_block(self, block_data):
    previous_block = self.get_latest_block()
    next_index = previous_block.index + 1
    next_timestamp = int(round(time.time() * 1000))
    next_hash = self.calculate_hash(next_index, previous_block.hash, next_timestamp, block_data)
    return Block(next_index, next_hash, previous_block.hash, next_timestamp, block_data)

  """
  Method to validate a new Block against the latest Block in the Chain
  """
  def is_valid_new_block(self, new_block, previous_block):
    if not new_block.is_valid_block_structure():
      print('invalid block structure')
      return False
    if previous_block.index + 1 != new_block.index:
      print('invalid index')
      return False
    if previous_block.hash != new_block.previous_hash:
      print('invalid previous hash')
      return False
    if self.calculate_hash_for_block(new_block) != new_block.hash:
      print('hashes do not match')
      return False
    return True

  """
  Method to validate each Block in an entire Chain
  """
  def is_valid_chain(self, new_chain):
    # Lambda function to validate just the genesis Block
    is_valid_genesis = lambda block: repr(block) == repr(self.blocks[0])
    if not is_valid_genesis(new_chain[0]):
      print('invalid genesis block')
      return False
    # Validate each Block in the Chain
    for i in range(1, len(new_chain)):
      if not self.is_valid_new_block(new_chain[i], new_chain[i-1]):
        print('block ' + i + ' in new chain is not valid')
        return False
    return True
    
  """
  Method to replace the current Chain with a longer valid Chain
  """
  def replace_chain(self, new_blocks):
    if self.is_valid_chain(new_blocks) and len(new_blocks) > len(self.blocks):
      print('Received blockchain is valid. Replacing current blockchain with received chain.')
      self.blocks = new_blocks
    else:
      print('Received blockchain is invalid')