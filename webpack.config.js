module.exports = {
  context: __dirname,
  entry: './pages/home.jsx',
  output: {
    path: __dirname + '/static/js',
    filename: 'all.js'
  },
  module: {
    loaders: [
      {test: /\.jsx$/, loader: 'jsx-loader'},
      {test: /\.less$/, loader: 'style-loader!css-loader!less-loader'},
      {test: /bower_components\.*\.js$/, loader: "script-loader"}
    ]
  }
};
