'use strict';
module.exports = function(app) {
  var todoList = require('../controllers/controller');

  // todoList Routes
  app.route('/videos')
    .get(todoList.list_all_videos)
    .post(todoList.create_a_video);


  app.route('/videos/:videoId')
    .get(todoList.read_a_video)
    .put(todoList.update_a_video)
    .delete(todoList.delete_a_video);
};