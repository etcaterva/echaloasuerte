/**
 * Function that given a chat entry generates
 *  and returns the html code necessarry to be
 *  rendered in the chat
**/
function formatChatEntry(chat_entry){
    var user = chat_entry.user;
    var content = chat_entry.content;
    var time = chat_entry.creation_time;


    return '<li class="right clearfix"><span class="chat-img pull-right">' +
        '    <img src="http://placehold.it/50/FA6F57/fff&text=' + user.toUpperCase().charAt(0) + '" alt="User Avatar" class="img-circle" />' +
        '</span>' +
        '    <div class="chat-body clearfix">' +
        '        <div class="header">' +
        '            <small class=" text-muted"><i class="fa fa-clock-o"></i> ' + time + '</small>' +
        '            <strong class="pull-right primary-font">' + user + '</strong>' +
        '        </div>' +
        '        <p>' + content + '</p>' +
        '    </div>' +
        '</li>';
}

