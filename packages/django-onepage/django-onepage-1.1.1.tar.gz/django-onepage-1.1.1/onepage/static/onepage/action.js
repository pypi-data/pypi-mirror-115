$(document).ready(function() {
    var elements = document.getElementsByClassName("ajax-four-act-handler");
    var sessionModelKw = {};

    let sessionElement = null;
    let currentElement = {};

    $('.ajax-four-act-handler').each(function(){
        sessionElement = $(this);
        currentElement = {
            "model-props": sessionElement.data("props"),
            "r_kwargs": sessionElement.data("r-kwargs"),
            "data-keys": sessionElement.data("keys"),
            "data-post-url": sessionElement.data("post-url")
        }
        sessionModelKw[sessionElement[0].id] = currentElement
    });

    $.ajax({
        url: "/onepage/set-session/",
        method: "GET",
        data: {
            body: JSON.stringify(sessionModelKw)
        },
        success: function(data){
//            console.log(data)
        },
        error: function(data){
            swal("Error", "Something wrong, some functionalities might not work!", "error");
        }
    })
});
