tronController=require('./tronController');



// var start=393902; //起始块
// var end=394000;   //结束块


scan=tronController.scanLastestBlock(start,end)
scan.then(result=>{
    for (i of result){
        for(j of i.transactions){
           for (k of j.raw_data.contract)
            isTransfer=k.type;
            if (isTransfer=='TransferContract'){
               trxTransfer=k.parameter.value
                console.log(trxTransfer)
                return trxTransfer
            }
        }   
    }
})