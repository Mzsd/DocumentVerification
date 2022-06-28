from django.conf import settings
from datetime import datetime
from web3 import Web3

import hashlib
import json
import os


class Verification():


    def __init__(self, request, doc=None, file=None) -> None:
        self.doc = doc
        self.file = file
        self.request = request
        self.query_dict = request.POST
        self.config = self.get_config()
        self.web3 = Web3(Web3.HTTPProvider(self.config['provider']))
        self.contract_addr = self.config['contract_addr']
        
        self.address = self.config['address']
        self.pvt_key = self.config['pvt_key']
        self.contract = self.web3.eth.contract(address=self.contract_addr, abi=self.load_abi())

        self.tx =   {
                        'from': self.address,
                        'to': self.contract_addr,
                        'gas': 250000,
                        'gasPrice': self.web3.toWei('10','gwei'),
                        'chainId': 80001
                    }

    def get_config(self):
        with open(os.path.join(settings.CONFIG_FILE, "config.json")) as fp:
            config = json.load(fp)
        return config

    def load_abi(self):
        with open(os.path.join(settings.CONTRACTS_DATA, self.config['contract_filename'])) as fp:
            abi = json.load(fp)
        return abi

    def hash_data(self):
        
        if self.doc:
            # print(os.path.join(settings.DOCUMENTS_ROOT, str(self.doc.document).split('/')[1]))
            with open(os.path.join(settings.DOCUMENTS_ROOT, str(self.doc.document).split('/')[1]), 'rb') as fp:
                data = fp.read()
        else:
            pass
            data = self.file.read()
            
        data += bytes(self.request.POST['institute_name'].lower(), 'utf-8')
        data += bytes(self.request.POST['holder_name'].lower(), 'utf-8')
        
        sha = hashlib.sha256(data)
        self.digest = sha.digest()
            
    def upload_hash(self):
        self.digest
        
        data = self.contract.encodeABI  (
                                            fn_name="uploadHash", 
                                            args=[self.digest, int(datetime.timestamp(datetime.now()))]
                                        )

        self.tx['nonce'] = self.web3.eth.getTransactionCount(self.address)
        self.tx['data'] = data
        
        signed_tx = self.web3.eth.account.sign_transaction(self.tx, self.pvt_key)
        tx_hash = self.web3.toHex(self.web3.eth.sendRawTransaction(signed_tx.rawTransaction))
        
        print(tx_hash)
        
        return tx_hash
        
    def verify_hash(self):
        
        return self.contract.functions.verify(self.digest).call({"from": self.address})