// after the page and table has loaded, begin loading images, to avoid the annoyingness of the data not loading until images do.
function get_images() {
    

    console.log("getting images");

    // get the tbody element, which is a child of the table
    table = document.getElementsByClassName("dataframe").item(0).children[1];

    console.log(table);

    // iterate through the table and request images
    for (i = 0; true; i++) {

        try {
            // get the image and src from the id of the img element
            let image = table.rows[i].cells[6].children[0];
            src = image.id;

            //console.log("requesting image for " + src);

            // request the image
            $.ajax({
                url: "/get_image",
                type: "GET",
                data: {src: src}
            }).done(function (data) {
                //console.log("got image for " + src + ": with data " + data);
                image.src = "data:image/png;base64," + data
            })
        }
        catch (e) {
            //console.log(e);
            break;
        }
        
    }


}