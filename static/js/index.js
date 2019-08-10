
function error_cb(error) {
    console.log(error);
}

/*
 *
 *    Likes
 *
 */

function create_like(success_cb, error_cb) {
    // 'this' is the icon we found from html file 
    var post_pk = $(this).siblings('.hidden-data').find('.post-pk').text();
    console.log(post_pk);
    // create like
    // ajax is a function for same page operation
    $.ajax({
        // ajax request a operation -> transfer the request to url
        type: "POST",
        url: '/insta/like',
        data: {
            post_pk : post_pk
        },
        // if success, run function success_cb
        // if error, run error_cb
        success: function(data) { success_cb(data); },
        error: function(error) { error_cb(error); }
    });
}
  
function like_update_view(data) {
    console.log(data);

    // toggle heart
    var $hiddenData = $('.hidden-data.' + data.post_pk);
    // data.result is the returned json from addLike in views.py 
    if (data.result) {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart-o').addClass('fa-heart');
    } else {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart').addClass('fa-heart-o');
    }
  
    // update like count
    // if data.result == 1, difference = 1, if data.result == 0, difference = -1
    var difference = data.result ? 1 : -1;
    // find post
    var $post = $('.view-update.' + data.post_pk);
    // find likes on the post
    var $likes = $post.find('.likes');
    // find the number of likes on this post
    var likes = parseInt($likes.text());
    // update the likes
    likes = likes + difference;
  
    console.log('likes', likes);
    
    if (likes == null || isNaN(likes)) {
      $likes.text('1 like');
    } else if (likes === 0) {
      $likes.text('');
    } else if (likes === 1) {
      $likes.text('1 like');
    } else {
      $likes.text(likes + ' likes');
    }
}

// $ means that find all the sumbit-like from all the html files
// .on means that if click is happened, it will do the following function
$('.submit-like').on('click', function() {
    // 'this' is $('.submit-like')
    create_like.call(this, like_update_view, error_cb);
});

  
/*
*
*    Comments
*
*/
  
function enterPressed(e) {
    if (e.key === "Enter") { return true; }
    return false;
}
   
function validComment(text) {
    if (text == '') return false;
    return true;
}
  
function create_comment(success_cb, error_cb) {
    var comment_text = $(this).val();
    var post_pk = $(this).parent().siblings('.hidden-data').find('.post-pk').text();
  
    console.log(comment_text, post_pk);
  
    $.ajax({
      type: "POST",
      url: '/insta/comment',
      data: {
        comment_text: comment_text,
        post_pk: post_pk
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}

function comment_update_view(data) {
    console.log(data);
    var $post = $('.hidden-data.' + data.post_pk);
    var commentHTML = '<li class="comment-list__comment"><a class="user"> ' + data.commenter_info.username + '</a> <span class="comment">'
                    + data.commenter_info.comment_text +'</span></li>'
  
    $post.closest('.view-update').find('.comment-list').append(commentHTML);
  }
  
  $('.add-comment').on('keyup', function(e) {
    if (enterPressed(e)) {
      if (validComment($(this).val())) {
        create_comment.call(this, comment_update_view, error_cb);
        $(this).val('');
      }
    }
  });
  

/*
 *
 *    Follow/Unfollow
 *
 */

function follow_user(success_cb, error_cb, type) {
    var follow_user_pk = $(this).attr('id');
    console.log(follow_user_pk);
  
    $.ajax({
      type: "POST",
      url: '/togglefollow',
      data: {
        follow_user_pk: follow_user_pk,
        type: type
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}
  
function update_follow_view(data) {
    console.log('calling update_follow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('unfollow-user').removeClass('follow-user');
    $button.text('Unfollow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text + 1);
}

function update_unfollow_view(data) {
    console.log('calling update_unfollow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('follow-user').removeClass('unfollow-user');
    $button.text('Follow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text - 1);
}


// $('.follow-toggle__container').on('click', '.follow-user', function() {
//     follow_user.call(this, update_follow_view, error_cb, 'follow');
// });

// $('.follow-toggle__container').on('click', '.unfollow-user', function() {
//     follow_user.call(this, update_unfollow_view, error_cb, 'unfollow');
// });