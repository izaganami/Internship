'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;


var ModelSchema = new Schema({
  name: {
    type: String,
    required: 'Kindly enter the name'
  }
});

module.exports = mongoose.model('Videos', ModelSchema);