function cast_vote(vote) {

    name_of_winner = document.getElementById("champion_" + vote + "_name").innerHTML

    if (vote == 1) {
        name_of_loser = document.getElementById("champion_2_name").innerHTML
    } else {
        name_of_loser = document.getElementById("champion_1_name").innerHTML
    }

    // send the ajax request
    $.post("/champion_vote", {winner: name_of_winner, loser: name_of_loser});

}