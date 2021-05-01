
/* adapted from/Credit: open source https://codepen.io/thebeloved88/pen/zvrzoE */
/*Title: Cool Modal Popup Sign In/Out Form*/


    //defining all needed variables
    var overlay = document.getElementsByClassName('overlay');
    var mainPopUp = document.getElementsByClassName('SignUpModal')
    var signIn = document.getElementById('sign-in');
    var SignUp = document.getElementById('SignUp');
    var formSignIn = document.getElementsByClassName('sign-in');
    var formSignUp = document.getElementsByClassName('SignUp');
    
   
   
    
    document.getElementById('modalButton').on('click', function(){
      overlay.addClass('visible');
      mainPopUp.addClass('visible');
      signIn.addClass('active');
      SignUp.removeClass('active');
      formSignUp.removeClass('move-left');
      formSignIn.removeClass('move-left');
    });
    overlay.on('click', function(){
      (this).removeClass('visible');
      mainPopUp.removeClass('visible');
    });
    document.getElementsById('popup-close-button').on('click', function(e){
      e.preventDefault();
      overlay.removeClass('visible');
      mainPopUp.removeClass('visible');
    });
    
    signIn.on('click', function(){
      signIn.addClass('active');
      SignUp.removeClass('active');
      formSignIn.removeClass('move-left');
      formSignUp.removeClass('move-left');
    });
    
    SignUp.on('click', function(){
      signIn.removeClass('active');
      SignUp.addClass('active');
      formSignIn.addClass('move-left');
      formSignUp.addClass('move-left');
    });
    
    
 