import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

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
    # def proof_of_work(self, block):
    #     """
        
    #     """
    #     block_string = json.dumps(block)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1
    #     return proof
    @staticmethod
    def valid_proof(block_string, proof):
        """
        Change `valid_proof` to require *6[ ] leading zeroes.
        """
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"
        

# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()
@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    required = ['proof', 'id']
    if not all(k in data for k in required):
        error = {'message': 'Missing a required key'}
        return jsonify(error), 400
    
    last_block = blockchain.last_block
    last_block_string =json.dumps(last_block, sort_keys=True)

    if blockchain.valid_proof(last_block_string, data['proof']):
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(data['proof'], previous_hash)        

        response = {
            'message': 'New Block Forged',
            'new_block': block
        }
    else:
        response = {
            'message': 'Proof is invalid or already submitted'
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

@app.route('/last_block', methods=['GET'])
# Add an endpoint called `last_block` that returns the last block in the chain
def last_block():
    last_blockchain = blockchain.last_block
    response = {
        'last_blockchain': last_blockchain
    }
    return jsonify(response), 200
# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
