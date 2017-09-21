function addProduct(productName, quantity, price){
    var nb = parseInt($("#product_"+productName+"_nb").text());
    ping();
    if(nb<quantity){
        //get old price
        $("#product_"+productName+"_nb").html(nb+1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));

        //set new price
        $("#total").html((total+priceDot).toFixed(2).replace('.',',') + " €");
        sessionStorage.setItem("product_"+productName+'_nb', nb+1);
        sessionStorage.setItem('total', $('#total').text());
    }
}

function removeProduct(productName, price){
    var nb = parseInt($("#product_"+productName+"_nb").text());
    ping();
    if(nb>0){
        //get old price
        $("#product_"+productName+"_nb").html(nb-1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));

        //set new price
        $("#total").html((total-priceDot).toFixed(2).replace('.',',') + " €");
        if (nb-1 == 0){
            sessionStorage.removeItem("product_"+productName+'_nb');
        } else {
            sessionStorage.setItem("product_"+productName+'_nb', nb-1);
        }
        sessionStorage.setItem('total', $('#total').text());
    }
}
