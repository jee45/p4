$(window).on('load', function() {
	console.log('the page is loaded');


    $('.followButton').on('click', function() {
        console.log('follow was clicked');

        //set state to what ever is there
        var state = $(this).attr('data-state');

        //is the state 'following'?
        var follow = state ==='not-following';

        //the next state is the opposite of whatever this is.
        var nextState = follow ? 'not-following' : 'following';

        var elt = $(this);

        //console.log(elt.attr('data-answer-id'));


        $.ajax('/api/update-check', {
            method: 'POST',
            data: {

                followee_id: elt.attr('data-other-user-id'),
                want_to_follow: !follow,
                state: nextState,
                _csrf_token: csrfToken
            },

            success: function(data){
                console.log('post succeeded with result %s', data.result);
                //elt.attr('data-state', nextState);
                //elt.text('un follow');

                window.location.reload()

            },
            error: function(){
                console.error('post failed');
                elt.attr('data-state', state);
            }
        });


    });

});




