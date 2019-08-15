tronController=require('./tronController');


toAddress='TCtz5X4x2HMhx5Cu9jGXnZhj9JFNfzp5s8';
contractAddress='TVwXxvyYawS21PT1B7XZxBZCMbQZLUENoE';//ATTAddress at Mainnet
pk='b22d5d606bee10f4c67f8bd942f63a26de7778a757da94ce4ad87c21d0958ae2';


//使用这个函数注释掉测试网，并且启用主网

watcherForATT=tronController.CtoTRC20Listener(contractAddress);

