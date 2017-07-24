function addProduct(productName, quantity, price){
    var nb = parseInt($("#"+productName+"_nb").text());
    if(nb<quantity){
        $("#"+productName+"_nb").html(nb+1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));
        $("#total").html((total+priceDot).toFixed(2).replace('.',',') + " €");
    }
}

function removeProduct(productName, price){
    var nb = parseInt($("#"+productName+"_nb").text());
    if(nb>0){
        $("#"+productName+"_nb").html(nb-1);
        var total = parseFloat($("#total").text().replace(',','.'));
        var priceDot = parseFloat(price.replace(',','.'));
        $("#total").html((total-priceDot).toFixed(2).replace('.',',') + " €");
    }
}

function change_theme_view(name_theme){
    $.ajax({
        type: "POST",
        url: "/change_theme/",
        dataType: "json",
        traditional: true,
        data: {"color": JSON.stringify(name_theme)},
        success: function(data) {}
    });
}
