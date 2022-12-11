function addMedicine(id,name,unit,price   ){
    event.preventDefault()

    fetch('/api/add-medicine',{
        method: 'post',
        body :JSON.stringify( {
            'id':id,
            'name':name,
            'unit' :unit,
            'price':price

        }),
        headers: {
            'Content-Type': 'application/json'
        }

    }).then(function(res){
         console.info(res)
         return res.json()
    }).then(function(data){
     console.info(data)
    }).catch(function(err){
             console.error(err)

    })
}


