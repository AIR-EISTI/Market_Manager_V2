function addProduct(productName, quantity, price){
    var nb = parseInt($("#"+productName+"_nb").text());
    if(nb<quantity){
        $("#"+productName+"_nb").html(nb+1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));
        $("#total").html((total+priceDot).toFixed(2).replace('.',',') + " €");
        Cookies.set(productName+'_nb', nb+1);
        Cookies.set('total', $("#total").text());
    }
}

function removeProduct(productName, price){
    var nb = parseInt($("#"+productName+"_nb").text());
    if(nb>0){
        $("#"+productName+"_nb").html(nb-1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));
        $("#total").html((total-priceDot).toFixed(2).replace('.',',') + " €");

        if (nb-1 == 0){
            Cookies.remove(productName+'_nb');
        } else {
            Cookies.set(productName+'_nb', nb-1);
        }
        Cookies.set('total', $("#total").text());
    }
}
