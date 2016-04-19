

function checkFormComponents(e){
    console.log('preventing submission');

    //stop default submission function
    e.preventDefault();

    // if the image field does not have content
    if($('#image').val()){
        console.log('something uploading');
        console.log('continuing with regular post submission');

        $(this).unbind('submit').submit()



    }else {

        console.log('nothing uploading');

        var form = $(this);
        var entry = $('#entry')
        var url = $('#url')
        console.log(form);


        //make ajax request.

        //update timeline.


        //else
        //normal form submission function


        $.ajax('/api/newPost', {
            method: 'POST',
            data: {

                entry: entry.val(),
                url: url.val(),
                _csrf_token: csrfToken
            },

            success: function (data) {
                console.log('post succeeded with result %s', data.result);
                window.location.reload()

            },

            error: function () {
                console.error('post failed');

            }
        });

    }


}







// set up the socket handler
$(window).load(function() {
    // handle the click event of a reply button in a message
    //$('.newPost').on('click', checkFormComponents );
    $('form').on('submit', checkFormComponents );



});

