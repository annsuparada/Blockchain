import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

"""
Server*
Modify the server we created to:
* Remove the `proof_of_work` function from the server.
* Change `valid_proof` to require *6* leading zeroes.
* Add an endpoint called `last_block` that returns the last block in the chain
* Modify the `mine` endpoint to instead receive and validate or reject a new proof sent by a client.
    * It should accept a POST
    * Use `data = request.get_json()` to pull the data out of the POST
        * Note that `request` and `requests` both exist in this project
    * Check that 'proof', and 'id' are present
        * return a 400 error using `jsonify(response)` with a 'message'
* Return a message indicating success or failure.  Remember, a valid proof should fail for all senders except the first.

"""
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
    def new_block(self, proof, previous_hash=None):
       
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block
    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """
  
        string_object = json.dumps(block, sort_keys=True).encode()
        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(string_object)
        hex_hash = raw_hash.hexdigest()
        
        return hex_hash
    @property
    def last_block(self):
        return self.chain[-1]
    def proof_of_work(self, block):
        """
        
        """
        block_string = json.dumps(block)
        proof = 0
        while self.valid_proof(block_string, proof) is False:
            proof += 1
        return proof
    @staticmethod
    def valid_proof(block_string, proof):
        """
        
        """
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == "000"
        

# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()
@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algorithm to get the next proof
    proof = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'new_block': block
    }
    return jsonify(response), 200
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200
# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
