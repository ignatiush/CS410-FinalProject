function display_topics(topics) {
    if(topics.length !== 0) {
        $('#temp').text("Recommended Results");
        for (i = 0; i < topics.length; i++) {
            let $li = $("<li>", {"class": "list-group-item"});
            let $link = "https://www.reddit.com/r/" + topics[i];
            let $a = $("<a>", {href: $link, target: "_blank"});
            let $h = $("<span>", {text: topics[i], class: "lead"});

            $a.append($h);
            $li.append($a);
            $(".list-group").append($li);
        }
        return;
    }

    $('#temp').text("Subreddit does not exist");
}


function finished_loading() {
    let $spinner = $(".loader");
    if($spinner.length > 0){
        $spinner.remove()
    }
}


function loading() {
    $('#temp').text("loading");
    let $div = $("<div>", {"class":"loader"});
    $(".results").append($div)
}


function get_data(subreddit){
    $.ajax({
        type: "GET",
        url: '/topics',
        data: {'subreddit':subreddit},
        success: function (response) {
            finished_loading();
            console.log(response);
            display_topics(JSON.parse(response));
        },
        error: function (error) {
            finished_loading();
            console.log(error);
            $('#temp').text("Something went wrong. Maybe try another subreddit?");
        }
    });
}


$('#topics-btn').click(function () {
    $('.list-group').empty();

    let sub = $('#subreddit').val();
    if(sub === ""){
        alert("Empty Search Field");
        return;
    }

    loading();
    console.log("Fetching data with subreddit " + subreddit);
    get_data(sub);
});
