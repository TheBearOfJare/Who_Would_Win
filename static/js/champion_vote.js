function cast_vote(vote) {

    // create the form and submit the vote. Redirect back to the vote page to allow the user to vote again on a new matchup.

    var vote_form = document.createElement("form");

    vote_form.method = "POST";
    vote_form.action = "/champion_vote.html";
    vote_form.id = "vote";

    var vote_input = document.createElement("input");

    vote_input.type = "hidden";
    vote_input.display = "none";
    vote_input.name = "vote";
    vote_input.value = vote;

    vote_form.appendChild(vote_input);

    vote_form.submit();


}
