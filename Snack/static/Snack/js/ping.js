//send request to update session 
function ping()
{
    $.ajax({
        
        url : '/heartbeat/',
        type : 'GET',
        dataType : 'html', // On désire recevoir du HTML
        success : function(code_html, statut){}

    });
}