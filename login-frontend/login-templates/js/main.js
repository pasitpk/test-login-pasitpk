
(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);

function makeid(length) {
    var result           = '';
    var characters       = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}

async function loginLine() {
     
    const endpoint = "https://access.line.me/oauth2/v2.1/authorize";
    const state = makeid(10);
    const params = [
            "response_type=code",
            "client_id=1656952085",
            "redirect_uri=https://test.pasitpk.app/login-frontend/verify-line-token",
            "state=" + state, //this should be randomly generated
            "scope=profile%20openid%20email"
        ].join("&");

    const url = endpoint + "?" + params;
          
    location.replace(url);
};

async function verifyLine() {
    const 
        endpoint = "https://access.line.me/oauth2/v2.1/authorize",  
        params = [
            "response_type=code",
            "client_id=1656952085",
            "redirect_uri=https://test.pasitpk.app/login-frontend/verify-line-token",
            "state=12345abcde", //this should be randomly generated
            "scope=profile%20openid"
        ].join("&")

    const url = endpoint + "?" + params
          
    try {
        var res = await fetch(url);
        if (res.status == 200) {
            line_info = await res.json();
            console.log(line_info)
        }
    }
    catch (err) {
        console.log(err);
    }
};

async function sendOTP() {
    const 
        endpoint = "https://access.line.me/oauth2/v2.1/authorize",
        params = [
            "response_type=code",
            "client_id=1656952085",
            "redirect_uri=https://test.pasitpk.app/login-frontend/verify-line-token",
            "state=12345abcde", //this should be randomly generated
            "scope=profile%20openid"
        ].join("&")

    const url = endpoint + "?" + params
          
    try {
        var res = await fetch(url);
        if (res.status == 200) {
            line_info = await res.json();
            console.log(line_info)
        }
    }
    catch (err) {
        console.log(err);
    }
};