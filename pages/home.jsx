/** @jsx React.DOM */
/*NPM includes*/
var _ = require('lodash');
var $ = require('jQuery');

/*React includes*/
var React = require("react/addons");
var cx = React.addons.classSet;

/*Styling*/
require('./home.less');

var UploadForm = React.createClass({
  handleClick : function(e){
    var node = this.getDOMNode();
    onComplete = this.props.onComplete;

    e.preventDefault();
    var formData = new FormData(this.getDOMNode());
    $.ajax({
        type:$(node).attr('method'),
        url: $(node).attr('action'),
        data:formData,
        cache:false,
        contentType: false,
        processData: false,
        success:function(data){
          onComplete(data);
        },
        error: function(data){
          alert('error uploading!');
        }
    });
  },
  render : function(){
    return (
      <form method={this.props.method} action={this.props.action} encType='multipart/form-data' onSubmit={this.handleClick}>
        <input type="file" name="file" />
        <input type="submit" value={this.props.value} />
      </form>
    );
  }
});

var View = React.createClass({
  getInitialState : function(){
    return {
      bank : [],
      related : []
    };
  },
  refreshBank : function(){
    $.getJSON('/bank', function(images){
      if(!images || !images.length){
        return;
      }
      this.setState({
        bank : images
      });
    }.bind(this));
  },
  relatedImagesChanged : function(images){
    if(!images || !images.length){
      return;
    }
    images = JSON.parse(images);
    this.setState({
      related : images
    });
  },
  componentDidMount : function(){
    this.refreshBank();
  },
  render : function(){
    var images = _.map(this.state.bank, function(image){
      return (
        <li key={image}>
          <img src={image} className="thumb-100" />
        </li>
      );
    });
    var related = _.map(this.state.related, function(image){
      return (
        <li key={image.image}>
          <img src={image.image} className="thumb-100" />
          <h5>similarity : {image.similarity}</h5>
        </li>
      );
    });
    return (
      <div>
        <h1>Upload a file to check!</h1>
        <UploadForm action="/lookup" value="Upload" method="POST"  action="/similar" onComplete={ this.relatedImagesChanged }/>
        <h1>Results</h1>
        <p>Please upload a file to get some matches</p>
        <ul className="thumbs">
          {related}
        </ul>
        <h1>Recent Images Uploaded</h1>
        <ul className="thumbs">
          {images}
        </ul>
        <h1>Add a file to the bank!</h1>
        <UploadForm action="/bank" value="Upload to bank" method="POST" action="/bank" onComplete={ this.refreshBank }/>
      </div>
    )
  }
});

React.renderComponent(
  View(),
  document.getElementById('content')
);
