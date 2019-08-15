# import redis
from dataCtrl import *
from BLWecc import *
from plusU import *
import json
import hashlib
from py_ecc import bls
from peewee import fn
import peewee
import sqlite3
import os
import logging
import uuid
import pickle
import redis
logging.basicConfig(filename='seaQlord.log',format='%(asctime)s %(message)s', level=logging.INFO)

LAYER2='redis'
FailTracer=False

redisHost='localhost:6379'
r=redis.StrictRedis(host=redisHost.split(':')[0], port=int(redisHost.split(':')[1]), decode_responses=True,db=0)
#redis for pending tx


def pushTx(tx):
	assert('from' in tx)
	assert('to' in tx)
	assert('asset' in tx)
	assert('amount' in tx)
	assert('uuid' in tx)
	if LAYER2=='redis':
		r.lpush('pending',json.dumps(tx))
		r.set('uuid'+str(tx.get('uuid')),-1)
	if LAYER2=='stagnum':
		txPool.append(tx)


def getTx(n_max):
	if LAYER2=='redis':
		n = r.llen('pending')
		if n > n_max:
			n = n_max
		txs=[]
		for i in range(n):
			tx=json.loads(r.blpop('pending',1)[1])
			txs.append(tx)
			r.delete('uuid'+str(tx.get('uuid')))
		return txs
	if LAYER2=='stagnum':
		n = len(txPool)
		#print(n)
		if n > n_max:
			n = n_max
		txs=[]
		for i in range(n):
			txs.append(txPool.popleft())
		#print(txs)
		return txs

def isPending(uuid):
	if LAYER2=='redis':
		return False
	if LAYER2=='stagnum':
		for tx in txPool:
			if tx['uuid'] == uuid:
				return True
		return False

def backupPool():
	pass

def loadPool():
	pass

def gateKeeper(tx,_publicKey, _signature):
	assert(type(tx) is dict)
	assert(tx['amount'] > 0)
	#assert(tx['asset'].isalpha())
	int(tx['from'],16)
	int(tx['to'],16)
	if tx['from'] == pub2add(_publicKey):
		return True
	if int(tx['from'],16) == 0:
		if MisCoin(tx['asset']):
			print('same asset found')
			#return False
		if not _issuePermit(tx['to']):
			print('not permitted to issue')
			return False
		if int(tx['amount']) > 10**18 or int(tx['amount']) < 0:
			print('value error')
			return False
		return True
	if verifyTx(json.dumps(tx), _signature,_publicKey):
		return True
	return False

def _issuePermit(address):
	if address!= '0x0':
		return True
	else: 
		return False

def MgetBlock(block):
	return uGetBlock(u,block)

def Mview():
	b=MblockNum()
	if b>10:
		s=b-10
	else:
		s=0
	res={'success':True,'data':[]}
	for i in range(s,b):
		res['data'].append(MgetBlock(i))
	return json.dumps(res)

def MassetByAdd(add):
	wallet=uGetTracker(u,add)
	res={'success':True,'data':[]}
	for asset in wallet:
		res['data'].append({'asset':asset,'amount':uGetAccount(u,add,asset)})
	return json.dumps(res)

def MblockNum():
	return uGetBlockNumber(u)

def MlistAllHolder(coin,page=0):
	assert(type(coin)==str)
	page=int(page)
	res={'success':True,'data':uGetCoinHolder(u,coin,page)}
	return json.dumps(res)

def MlistAllCoin():
	res={'success':True,'data':[]}
	res['data']=uGetAllCoin(u)
	return json.dumps(res)

def MtotalOf(coin):
	assert(type(coin)==str)
	return uGetCoin(u,coin)


def MtxByBlock(block):
	block=int(block)
	res={'success':True,'data':[]}
	res['data'] = uGetBlock(u,block)
	return json.dumps(res)

def MtxByAdd(address,from_block=0,to_block=-1,rev=False):
	if to_block == -1:
		to_block = MblockNum()-1
	res={'success':True,'data':[]}
	for txid in uGetAddressHistroy(u,address,from_block,to_block,rev):
		res['data'].append(MtxByHash(txid))
	return json.dumps(res)

def MtxByHash(tx_hash):
	# if isPending(tx_hash):
	# 	res={'success':True,'status':'pending'}
	# 	return json.dumps(res)

	res={'success':True,'tx':[]}
	(b,tx)=uGetId(u,tx_hash)
	res['block']=b
	if b==-99:
		res['status']='notExist'
	#-1:pending
	elif b<-1:
		res['status']='failed'
	elif b==-1:
		res['status']='success'
	else:
		res['status']='pending'
	res['tx'] = tx
	return json.dumps(res)

def MtxByCoin(coin,from_block=-1,to_block=-1):#too much cost for large coin! TO BE optimized
#now:force to limit to 20 results
	if to_block == -1:
		to_block=MblockNum()-1
	if from_block == -1:
		from_block=max(0,to_block-20)
	data=[]
	for k,v in u.RangeIter(key_from=b'block'+str(from_block).encode(),key_to=b'block'+str(to_block).encode(),reverse=True,):
		for tx in json.loads(v.decode()).get('txs'):
			if(tx.get('asset')==coin):
				data.append({'block':int(k.decode()[5:]),'tx':tx})
		if len(data)>=20:
			break
	res={'success':True,'data':data}
	return json.dumps(res)


def MisCoin(coin):
	try:
		res = int( (u.Get( ('coin/'+coin).encode() )).decode() )
	except:
		return False
	else:
		return True

def MhasRecord(uuid):
	if uGetId(u,uuid)[0]==-99:
		return False
	else:
		return True



def initDb():
	pass