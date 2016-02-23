;(function ($) {

    // Set the defaults
    var pluginName = 'EASchat',
        defaults = {
            is_enabled: true,
            url_send_message: false,
            draw_id: false,
            user_alias: false,
            user_id: false,
            msg_type_your_message: 'Type your message here...',
            msg_type_your_alias: 'Type your alias',
            msg_chat: "Chat",
            msg_login_first: "To use the chat you should <a href='#'>login</a> or <a href='#'>register</a>",
            msg_alias: "If not, simply type an Alias that allows others to recognize you",
            msg_error_alias: "The alias must have between 2 and 20 characters",
            msg_access_chat: "Access chat",
            msg_send: "Send",
            default_avatar: false,
            message_sent_callback: function(){}
        };

    /*********************************
     *     CHAT CLASS DEFINITION
     ********************************/
    var Chat = function (element, options){
        this.init(element, options);
    };

    Chat.prototype = {

        constructor: Chat,

        init: function (element, options){
            var that = this;
            this.$element = $(element)
            this.options = $.extend( {}, defaults, options) ;

            this.$element.removeClass("hidden");
            this.enable(this.options.is_enabled);

            this.renderChat();

            // Toggle chat when click on it header
            this.$element.find('.panel-heading').click(function (){
                that.$element.find(".panel-body").toggle(150);
            });


            // Submit message when click on "Send" button
            this.$element.find('#chat-send').click(function () {
                    var message = that.get_message_and_clean();
                    that.submit_message(message);
                }
            );

            // If the user is not logged in and does not have an alias, setup the button
            if (!this.options.user_alias) {
                this.$element.find('#access-chat').click(function () {
                    var valid_alias = that.check_alias_and_enable_chat();
                    console.log(valid_alias)
                    if (!valid_alias){
                        var $form_alias = that.$element.find('.login-for-chat .form-group');
                        $form_alias.addClass('has-error');
                        $form_alias.find('.control-label').removeClass('hidden');
                    }
                });
            }

            // Submit message when the "enter" key is pressed
            this.$element.find("#chat-message-box").keyup(function (e) {
               if(e.keyCode == 13) {
                   var message = that.get_message_and_clean();
                   that.submit_message(message);
               }
            });

        },

        // Return the message from the chat input box and clean it
        get_message_and_clean: function (){
            var $message_input = this.$element.find("#chat-message-box");
            var message = $message_input.val();
            $message_input.val("");
            return message;
        },

        // Submit the parameter "message" to the server
        submit_message: function (message) {
            // Check empty string
            if(!message || /^\s*$/.test(message)){
                return;
            }

            var message_object = {
                message : message
            };
            // Send the alias if the user is not authenticated
            if (this.options.user_id == null){
                message_object["anonymous_alias"] = this.options.user_alias;
            }
            var data = JSON.stringify(message_object);
            var that = this;

            $.ajax({
                url : this.options.url_send_message,
                method : "POST",
                contentType: 'application/json',
                data: data
            }).done(function(){
                that.options.message_sent_callback(message);
            }).fail(function(e){
                alert("The message was not sent");
            });
        },

        set messages(messages) {
            var $chat = this.$element.find("#chat-board");
            $chat.html("");
            for (var i = 0, length = messages.length; i < length; i++) {
                var element = messages[i];
                var entry = this.formatChatEntry(element);
                $chat.prepend(entry);
            }
            var $chat_body = this.$element.find('.panel-body');
            $chat_body.scrollTop($chat.height());
        },

        enable: function (enabled) {
            if(enabled) {
                this.$element.removeClass("chat-disabled");
            } else {
                this.$element.addClass("chat-disabled");
            }
        },

        // Given a chat entry generates and returns the html code necessarry to be rendered
        formatChatEntry: function (chat_entry){
            var user = (chat_entry.user != null) ? chat_entry.user_alias : chat_entry.anonymous_alias;
            var avatar = chat_entry.avatar || this.options.default_avatar;
            var content = chat_entry.content;
            var time = moment.utc(chat_entry.creation_time).fromNow();
            var html = '<li class="clearfix">' +
                        '    <p class="chatline-details text-muted small">' + user + '<span class="chatline-datetime"><i class="fa fa-clock-o"></i> ' + time + '</span></p>' +
                        '	<span class="chat-img pull-left">' +
                        '		<img width="10px" src="' + avatar + '" alt="User Avatar" class="img-circle chat-avatar">' +
                        '	</span>' +
                        '	<div class="chatline-content">' + content +
                        '	</div>' +
                        '</li>';

            return html    ;
        },

        check_alias_and_enable_chat: function (){
            var alias = this.$element.find('.alias-chat').val();
            if (alias.length > 1 && alias.length < 20 ){
                $('.login-for-chat').remove();
                setCookie("user_alias", alias);
                this.options.user_alias = alias;
                return true;
            }
            return false;

        },

        renderChat: function (){
            var html_input = '<input id="chat-message-box" type="text" class="form-control input-sm" placeholder="'+this.options.msg_type_your_message+'"/>';

            var html_button = '<button class="btn btn-success btn-sm" id="chat-send">'+this.options.msg_send+'</button>';

            var html = "";
            if (!this.options.user_alias){
                // Add grayed out layer to "disable" chat until an alias is given
                html =  '<div class="login-for-chat text-center"><p>' + this.options.msg_login_first + '</p>' +
                        '   <p>' + this.options.msg_alias + '</p>' +
                        '   <div class="form-group">' +
                        '       <label class="control-label hidden" for="inputError">' + this.options.msg_error_alias + '</label>' +
                        '       <input type="text" class="alias-chat form-control" placeholder="'+this.options.msg_type_your_alias+'">' +
                        '   </div>' +
                        '   <a id="access-chat" class="btn btn-primary" href="javascript:void(0)" role="button">' + this.options.msg_access_chat + '</a>' +
                        '</div>';
            }

            html += '    <div class="panel panel-success panel-chat">' +
                    '        <div class="panel-heading">' +
                    '            <span class="fa fa-comment"></span>'+this.options.msg_chat +
                    '        </div>' +
                    '        <div class="panel-body">' +
                    '            <ul id="chat-board">' +
                    '            </ul>' +
                    '        </div>' +
                    '        <div class="panel-footer">' +
                    '            <div class="input-group">' +
                    '                '+ html_input +
                    '                <span class="input-group-btn">' +
                    '                    '+ html_button +
                    '                </span>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>';
            this.$element.append(html);
        }
    };

    /*********************************
     *     CHAT PLUGIN DEFINITION
     ********************************/
    $.fn.chat = function(options) {
        var chats = []
        this.each(function() {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName,
                chats.push(new Chat( this, options )));
            }
        });
        return chats;
    };
})(window.jQuery, window, document );




