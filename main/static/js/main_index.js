$(function() {
    function loadFriends() {
        $("#loading-friends").show();
        $.getJSON(
            FETCH_FRIENDS_URL,
            function(response) {
                if (response["fetched"]) {
                    $("#loading-friends").hide();
                    $("#main-friends").html(response["html"]);
                }
                else {
                    setTimeout(loadFriends, 1000);
                }
            });
    }

    if (LOAD) {
        $("#main-content").load(
            FETCH_ME_URL,
            function() {
                $("#loading").hide();
                loadFriends();
            });
    }
    else if (LOAD_FRIENDS) {
        loadFriends();
    }

});