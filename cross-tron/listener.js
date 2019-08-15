this.contract && this.contract.Transfer().watch((err, event) => {
    if(err)
        return console.error('Error with "Message" event:', err);

    console.group('New event received');
    console.log('- Contract Address:', event.contract);
    console.log('- Event Name:', event.name);
    console.log('- Transaction:', event.transaction);
    console.log('- Block number:', event.block);
    console.log('- Result:', event.result, '\n');
    console.groupEnd();
});