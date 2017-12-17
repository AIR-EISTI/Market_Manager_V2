//send request to update session 
function ping()
{
    $.ajax({
        
        url : '/heartbeat/',
        type : 'GET',
        dataType : 'html', // On désire recevoir du HTML
        success : function(code_html, statut){}

    });

    clearTimeout(timeoutSession)
    clearTimeout(timeoutLogout)
    timeoutSession = setTimeout(session_expire,100000);
    timeoutLogout = setTimeout(logout,120000);
}