//function addMedicine(id,name,unit   ){
//    event.preventDefault()
//
//    fetch('/api/add-medicine',{
//        method: 'post',
//        body :JSON.stringify( {
//            'id':id,
//            'name':name,
//            'unit' :unit,
//            'price':price
//
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//
//    }).then(function(res){
//         console.info(res)
//         return res.json()
//    }).then(function(data){
//     console.info(data)
//     let counter = document.getElementById('counter')
//     counter.innerText = data.total_quantity
//    }).catch(function(err){
//             console.error(err)
//
//    })
//}


function addMedicine(id, name, unit) {
//    alert("alo")
    fetch('/api/add-medicine', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "unit": unit
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
//        let d = document.getElementsByClassName('cart-counter')
//        for (let i = 0; i < d.length; i++)
//            d[i].innerText = data.total_quantity
    }) // promise
}


