var ExampleApplication = React.createClass({
  render: function() {
    var listItems = this.props.data.suggestions.map(function(item){
      return(
        <li key={item.id}>{item.topic}</li>
      )
    });
    return <ul style={{"marginLeft":"0.5in"}}>{listItems}</ul>
  }
});

// Call React.createFactory instead of directly call ExampleApplication({...}) in React.render
var ExampleApplicationFactory = React.createFactory(ExampleApplication);

var start = new Date().getTime();
var update = setInterval(function() {
  $.ajax({
    url: "suggestions",
    success: function(data) {
      //console.log(data);
      ReactDOM.render(
        ExampleApplicationFactory({data: data}),
        document.getElementById('suggested'));
    }
  })
}, 500);
