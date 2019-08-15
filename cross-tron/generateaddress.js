
const https = require('https');
const options = {
   
      host:'api.trongrid.io',
      path:'/wallet/generateaddress',
      //port: 443,
      method:'GET',
      //auth:'api:key-442199e5d02324bc7d1ff2a2f675882e',
      //agent:false,
     // rejectUnauthorized : false,
     headers:{
      'Content-Type' : 'application/x-www-form-urlencoded',
      accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'cache-control': 'no-cache',
      pragma: 'no-cache',
      'upgrade-insecure-requests': 1,
      'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    //
     },

    
  }

  //const options = getAddress;
  
  const getAddressReq = https.request(options, (res) => {
    console.log('状态码:', res.statusCode);
  console.log('请求头:', res.headers);
 // res.on('data', (d) => {
//    process.stdout.write(d);
 // });
  });

 // req.on('error', (e) => {
//    console.error(e);
 // });
 // req.end();
  //getAddressReq.write(content);
 // getAddressReq.end();
