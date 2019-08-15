// export module{}

//config NODE,init trollllllllllln Object
//var request = require("request");
const TronWeb = require('tronweb');
const HttpProvider = TronWeb.providers.HttpProvider;
const blankKey='141d58c8d053849675b780eec17f813fb6116be222188c2dbe8b8cfc43d9ff55'; //very important key for security

//main
// const fullNode = new HttpProvider('https://api.trongrid.io');
// const solidityNode = new HttpProvider('https://api.trongrid.io');
// const eventServer = 'https://api.trongrid.io';

//shasta
const fullNode = new HttpProvider('https://api.shasta.trongrid.io');
const solidityNode = new HttpProvider('https://api.shasta.trongrid.io');
const eventServer = 'https://api.shasta.trongrid.io';

// var privateKey;
// var userAddress;
// var toAddress;



const tronWeb = new TronWeb(
    fullNode,
    solidityNode,
    eventServer,
);


const tronController={

//toolkits part
async isConnected(){
   return connStatus=await tronWeb.isConnected();
},//statusChecker

setPrivateKey(privateKey){
    setKey=tronWeb.setPrivateKey(privateKey);
},//setKey


toSun(value){
    return result=tronWeb.toSun(value);
},//trasfrom unit of value in TRX-Sun pair

fromSun(value){
return result=tronWeb.fromSun(value);
},//trasfrom unit of value in TRX-Sun pair

toHex(address){
    return result=tronWeb.toHex(address);
},

async getContract(contractAddress){
    result=await tronWeb.trx.getContract(contractAddress);
    // console.log(result);
    return result
},


//useful methods
async getBalance(userAddress){
    const userBalance = await tronWeb.trx.getBalance(userAddress);
    
    return userBalance
},

async getAccount(userAddress){
    const accountInfo=tronWeb.trx.getAccount("TEEXEWrkMFKapSMJ6mErg39ELFKDqEs6w3");
    return accountInfo
},

async transfer(to,value,privateKey)  {

 const transaction= await tronWeb.trx.sendTransaction(to, value, privateKey);

 return transaction
},

 async createAccount() {
    const account =await tronWeb.createAccount();
    return account
  
  
},

async transferTRC10(to,value,tokenId,privateKey)  {

    const tokenTransaction= await tronWeb.trx.sendToken(to, value, tokenId,privateKey);
   
    return tokenTransaction
   },


async transferTRC20(to,value,contractAddress,privateKey)  {
    
    this.setPrivateKey(privateKey)
    let abi=[{inputs:[{name: "_to", type: "address"},{name: "_value", type: "uint256"}] , name: "transfer", stateMutability: "Nonpayable", type: "Function"}];
    let contractInstance = await tronWeb.contract().at(contractAddress);
    const txID = await contractInstance.transfer(to, value).send();
    this.setPrivateKey(blankKey);
    return txID
   },

   async scanLastestBlock(startHeight,endHeight){

    var blockInfo = await tronWeb.trx.getBlockRange(startHeight,endHeight);
    console.log(blockInfo);
    return blockInfo
},

async getTransactionInfo(txID){
 result=await tronWeb.trx.getTransactionInfo(txID);
 return result
},

async CtoTRC20Listener(contractAddress){
    contractInstance=await tronWeb.contract().at(contractAddress);
    contractInstance.Transfer().watch((err, event) => {
      if (err) return console.error('Error with "Transfer" event:', err);
      if (event) { 
        console.log(event);  
        return event
      }
    })
}//现成的WATCHER

}

//toolkits SM开发测试用工具

//isConnected()
//setPrivateKey(privateKey)
//toSun(value)
//fromSun(value)
//toHex(value)
//getContract(contractAddress)


//methods 用得到的方法
// getAccount (userAddress)
// getBalance(userAddress)
//transfer(to,value,privateKey)  //TRX transfer
// createAccount()
// transferTRC10(to,value,tokenId,privateKey) 
//transferTRC20(to,value,contractAddress,privateKey)
//scanLastestBlock(startHeight,endHeight)
//getTransactionInfo(txID)
//CtoTRC20Listener(contractAddress)

module.exports=tronController