// Event handling
document.addEventListener("DOMContentLoaded",
  function (event) {
    
    // Unobtrusive event binding
    document.querySelector("button")
      .addEventListener("click", function () {
        
        // Call server to get the name
        var myurl = document.getElementById('url').value;
        

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "Predictor.py?text=" + myurl, true);
        xhr.send();

        console.log("hi "+myurl);

        $ajaxUtils
          .sendGetRequest("Predictor.py"+myurl, 
            function (request) {
              console.log("Success");
            });

        
      });

        $ajaxUtils
          .sendGetRequest("data/answer.txt", 
            function (request) {
              var name = request.responseText;

              document.querySelector("#content")
                .innerHTML = "<h2>Hello " + name + "!</h2>";
            });

        
});





