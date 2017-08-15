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
