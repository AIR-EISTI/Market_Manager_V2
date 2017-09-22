function addProduct(e){
    

    if(! ($(e.target).parents('.remove').length > 0 || e.target.classList.contains("remove")))
    { 
        //get values
        var productId = this.getAttribute("data-id");
        var productName = this.getAttribute("data-name");
        var quantity = this.getAttribute("data-quantity");
        var price = this.getAttribute("data-price");
        var nb = parseInt($("#product_"+productId+"_nb").text());
        
        ping();
        
        if(nb<quantity){
            //get old price
            $("#product_"+productId+"_nb").html(nb+1);
            var total = parseFloat($("#total").text().replace(',','.'));
            var priceDot = parseFloat(price.replace(',','.'));

            //set new price
            $("#total").html((total+priceDot).toFixed(2).replace('.',',') + " €");
            sessionStorage.setItem("product_"+productId+'_nb', nb+1);
            saveAmountProduct(productName,nb+1)
            sessionStorage.setItem('total', $('#total').text());
        }
    }
}

function removeProduct(productId,productName, price){
    var nb = parseInt($("#product_"+productId+"_nb").text());
    ping();
    if(nb>0){
        //get old price
        $("#product_"+productId+"_nb").html(nb-1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));

        //set new price
        $("#total").html((total-priceDot).toFixed(2).replace('.',',') + " €");
        console.log("yop");
        if (nb-1 == 0){
            sessionStorage.removeItem("product_"+productId+'_nb');
            saveAmountProduct(productName,0);
        } else {
            sessionStorage.setItem("product_"+productId+'_nb', nb-1);
            saveAmountProduct(productName,nb-1);
        }
        sessionStorage.setItem('total', $('#total').text());
    }
}


function saveAmountProduct(productName,nb)
{
    if(sessionStorage.amountProduct != null)
    {
        amountProduct = JSON.parse(sessionStorage.amountProduct);
        console.log(amountProduct)
    }
    else
    {
        console.log("titi")
        amountProduct = {};
    }
    amountProduct[productName] = nb;
    console.log(amountProduct);
    console.log(JSON.stringify(amountProduct));
    sessionStorage.setItem("amountProduct", JSON.stringify(amountProduct));
}