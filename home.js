function callAPI() {
  console.log("asdf")

  $.ajax({
    url: 'http://localhost:5000',
    dataType: 'jsonp',
    success: function(data) {
       console.log('data is ' + JSON.stringify(data))
       $('#result').html(JSON.stringify(data))
    },
    type: 'GET',
    crossDomain: true,
    // The name of the callback parameter, as specified by the YQL service
    jsonp: "callback",
  });
}
