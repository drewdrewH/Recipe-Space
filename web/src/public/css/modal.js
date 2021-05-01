
    var overlay = document.getElementById('overlay');
    var mainPopUp = document.getElementById('SignUpModal');
    var signIn = document.getElementById('sign-in');
    var SignUp = document.getElementById('Sign-Up');
    var formSignIn = document.getElementById('sign');
    var formSignUp = document.getElementById('SignUp');
     
   
   

    
   document.getElementById('modalButton').onclick = function(){
      overlay.className += ' visible';
      mainPopUp.className += ' visible';
      SignUp.className += ' active';
      SignIn.className = 'Sign-Up';
      formSignUp.className = 'SignUp';
      formSignIn.className = 'sign';
      console.log(signIn.classList);
    };
    overlay.onclick = function(){
      overlay.className = 'overlay';
      mainPopUp.className = 'SignUpModal';
    };
    document.getElementById('popup-close-button').onclick = function(e){
      e.preventDefault();
      overlay.className = 'overlay';
      mainPopUp.className = 'SignUpModal';
    };
    
    signIn.onclick = function(){
      signIn.className += ' active';
      SignUp.className = 'SignUp';
      formSignIn.className = 'sign';
      formSignUp.className = 'SignUp';
    }; 
    
    SignUp.onclick =function(){
      signIn.className = 'sign-in';
      SignUp.className += ' active';
      formSignIn.className += ' move-left';
      formSignUp.className += ' move-left';
    };
    
    
 