# import redis
from .dataCtrl import *
from .BLWecc import *
from .gate import *
from .plusU import *
from .configure import *
import ujson as json
import hashlib
from peewee import fn
import peewee
import sqlite3
import os
import logging
import uuid
import pickle
import redis
import time
import base64
from functools import wraps


logging.basicConfig(filename='seaQlord.log',format='%(asctime)s %(message)s', level=logging.WARNING)


r=redis.StrictRedis(host=redisHost.split(':')[0], port=int(redisHost.split(':')[1]), decode_responses=True,db=0)
#redis for pending tx

def useRedis(ex=5):
	def rDec(func):
		if LAYER2!='redis':
			return func
		@wraps(func)
		def wrapped_function(*args, **kwargs):
			rk=func.__name__
			for i in args:
				rk+=('/'+str(i))
			rv=r.get(rk)
			if rv is None:
				rv=func(*args, **kwargs)
				r.setex(rk,ex,rv)
			return rv
		return wrapped_function
	return rDec

def pushTx(tx):
	tx['from']='0x'+hex(int(tx['from'],16))[2:].zfill(23) 
	tx['to']='0x'+hex(int(tx['to'],16))[2:].zfill(23) 
	assert('asset' in tx)
	tx['asset'].replace('/','')
	tx['amount']=int(tx['amount'])
	tx['type']=tx.get('type',0)
	tx['time']=int(time.time())
	assert(type(tx['amount'])==int)
	assert(tx['amount']>=0)
	assert('uuid' in tx)
	if MhasRecord(tx['uuid']):
		return False
	if LAYER2=='redis':
		r.lpush('pending',json.dumps(tx))
		r.set('uuid'+str(tx.get('uuid')),-1)
		#only stored locally
	if LAYER2=='stagnum':
		txPool.append(tx)

def isFromBellchet(pub):
	sirLaifuSgn='0x335e57b017c638c2306d051ea240a39cfc0d56637915a561332e'
	+'2aefxbelewx0x3b11a29aa91ef8de50c3bb0896e1baeb3aec18b366fc87c119f4ab1b'
	sirLaifuMsg='seaQlord+UtestServer'
	return verifyTx(sirLaifuMsg,sirLaifuSgn,pub)

def getTx(n_max):
	if LAYER2=='redis':
		n = r.llen('pending')
		if n > n_max:
			n = n_max
		txs=[]
		for i in range(n):
			tx=json.loads(r.brpop('pending',1)[1])
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
		logging.info(json.dumps(txs))
		return txs

def isPending(uuid):
	if LAYER2=='redis':
		b=r.get('uuid'+uuid)
		if b is None:
			return False
		else:
			return True
	if LAYER2=='stagnum':
		for tx in txPool:
			if tx['uuid'] == uuid:
				return True
		return False

def backupPool():
	pass

def loadPool():
	pass


@useRedis(2592000) #holding 30 days 
def MgetBlock(block):
	b = uGetBlock(u,block)
	if b:
		block_content = json.loads(b)
	else:
		block_content = []
	if 'txs' in block_content:
		tx_list = block_content['txs']
		block_content['txs']=[]
		for tx_id in tx_list:
			if type(tx_id) is str:
				block_content['txs'].append(json.loads(MtxByHash(tx_id)))
	block_data = base64.b64encode(uGetUlog(u,block).encode()).decode()
	return json.dumps({'number':block, 'content': block_content, 'raw_data': block_data, 'hash': hex(abs(hash(block_data)))})

@useRedis(max(5,block_time))
def Mview(limit,offset):
	b=int(MblockNum())-offset
	s=b-limit
	if b<0:
		b=0
	if s<0:
		s=0
	res={'success':True,'limit':limit,'offset':offset,'data':[]}
	for i in range(s,b):
		a = json.loads(MgetBlock(i))
		if 'raw_data' in a:
			del a['raw_data']
		res['data'].append(a)
	return json.dumps(res)

@useRedis(max(5,block_time))
def MassetByAdd(add):
	wallet=uGetTracker(u,add)
	res={'success':True,'data':[]}
	for asset in wallet:
		res['data'].append({'asset':asset,'amount':uGetAccount(u,add,asset)})
	return json.dumps(res)

#@useRedis(block_time)
def MgetAccount(add,asset):
	return uGetAccount(u,add,asset)


def MblockNum():
	return uGetBlockNumber(u)


#@useRedis(max(10,block_time))
def MlistAllHolder(coin,page=0):
	assert(type(coin)==str)
	page=int(page)
	holders=uGetAllCoinHolder(u,coin)
	res={'success':True,'data':[]}
	for holder in holders:
		res['data'].append({'address':holder,'balance':MgetAccount(holder,coin)})
	return json.dumps(res)


#@useRedis(max(3,block_time))
def MlistAllCoin():
	res={'success':True,'data':[]}
	res['data']=uGetAllCoin(u)
	return json.dumps(res)

#@useRedis(max(3,block_time))
def MtotalOf(coin):
	assert(type(coin)==str)
	return uGetCoin(u,coin)


def MtxByBlock(block):
	block=int(block)
	res={'success':True,'data':[]}
	res['data'] = json.loads(MgetBlock(block))
	return json.dumps(res)

#@useRedis(max(10,block_time))
def MtxByAdd(address,from_block=0,to_block=-1,rev=False,limit=20):
	if to_block == -1:
		to_block = int(MblockNum())-1
	res={'success':True,'data':[]}
	for txid in uGetAddressHistroy(u,address,from_block,to_block,rev,limit):
		res['data'].append(json.loads(_MtxByHash(txid)))
	return json.dumps(res)


def MtxByHash(tx_hash):
	return _MtxByHash(tx_hash)



#@useRedis(259200) #holding three days to save memory
def _MtxByHash(tx_hash): #no pending version
	d=r.get('_Mtx'+tx_hash)
	if d:
		return d
	else:
		res={'tx':[]}
		(b,tx)=uGetId(u,tx_hash)
		res['block']=b
		res['tx'] = tx if type(tx) is dict else json.loads(tx)
		if b==-99:
			res['status']='notExist'
			d=json.dumps(res)
		#-1:pending
		elif b<-1:
			res['status']='failed'
			d=json.dumps(res)
			r.setex('_Mtx'+tx_hash,259200,d)
		elif b==-1:
			res['status']='pending'
		else:#b>=0
			res['status']='success'
			d=json.dumps(res)
			r.setex('_Mtx'+tx_hash,259200,d)
		
		return d

#@useRedis(max(10,block_time))
def MtxByCoin(coin,from_block=0,to_block=-1,rev=True,limit=20):
#too much cost for large coin! TO BE optimized <-fixed
#19.6.1:force to limit to 20 results <-unlimited now
#19.6.3: optimized
	if to_block == -1:
		to_block = int(MblockNum())-1
	res={'success':True,'data':[]}
	for txid in uGetCoinHistroy(u,coin,from_block,to_block,rev,limit):
		res['data'].append(json.loads(_MtxByHash(txid)))
	return json.dumps(res)


def MisCoin(coin):
	try:
		res = int( (u.Get( ('coin/'+coin).encode() )).decode() )
	except:
		return False
	else:
		return True

def MhasRecord(uuid):
	if json.loads(MtxByHash(uuid)).get('block')!=-99:
		return True
	else:
		return False



def initDb():
	pass

def Mtest():
	code=uuid.uuid1().hex
	pvt=getPrivateKey(code)
	add=getAddress(code)
	sign('test',pvt)
	testTx={'from':'0x0',
		'to':add,
		'asset':code,
		'amount':int(code[:8],16),
		'uuid':uuid.uuid1().hex
	}
	pushTx(testTx)
	Mview()
	return 'test'
