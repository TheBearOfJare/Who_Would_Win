function cast_vote(vote) {

    name_of_winner = document.getElementById("champion_" + vote + "_name").innerHTML

    if (vote == 1) {
        name_of_loser = document.getElementById("champion_2_name").innerHTML
    } else {
        name_of_loser = document.getElementById("champion_1_name").innerHTML
    }

    // send the ajax request and then reload the page once completed
    $.ajax({
        url: "/champion_vote.html",
        type: "POST",
        data: {winner: name_of_winner, loser: name_of_loser}
    }).done(function (data) {
        location.reload(true);
    });

}