const TronWeb = require('tronweb');
tronController=require('./tronController');
var privateKey='cab4178e66e0398ea7756bb83380905fe930b8bb0ca91f7df57bc6ba03849ad0';//数据库里检索查询
var userAddress='TNmPRNCVF57286xPo3im81GkQrhLaTzgm4';//数据库里检索查询
var warehouseAddress='TPzR3u5MbPqzvF2HeScDjoErzXGvWoTYXg';


tronController.getBalance(userAddress).then(result=>{

    if (result>0) {
    amonut=result;
    tronController.transfer(warehouseAddress,amonut,privateKey);}
    return amonut
}
).then((amonut)=>{
//生成新地址入库 //todo 回调java后端接口update info
    newAddress=tronController.createAccount()
    return  newAddress
})


// console.log(b);