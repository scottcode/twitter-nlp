var numMessages;
var messageJSON;

$(document).ready(
    function() {
//        tweetJSON = JSON.parse(curTweet);
//        console.log(1);
//        document.getElementById("displayedTweet").innerHTML = tweetJSON.text;
        getNextTweet();
    }
);

function wrapLabel(label, object) {
    return {
        "label": label,
        "object": object,
        "label_time": Date()
    }
};

function getNextTweet() {
    $.ajax({
      url: '/next_tweet_to_label',
      success: function(data) {
            tweetJSON = data.tweet;
            document.getElementById("displayedTweet").innerHTML = tweetJSON.text;
      },
    });
};

function applyLabel(label, object) {
    $.ajax({
        url: '/collect_tweet',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify(wrapLabel(label, object)),
        processData: false,
        success: function( data, textStatus, jQxhr ){
            $('#response pre').html( JSON.stringify( data ) );
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log( errorThrown );
        }
    });
    getNextTweet()
};



