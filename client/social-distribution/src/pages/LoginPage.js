import React, { useEffect, useState } from 'react';
import Login from '../components/login';
import Register from '../components/register';
import { useNavigate, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { toast } from 'react-toastify';

function LoginPage({ isAuthenticated, updateAuthStatus, updateUserAndAuthorId }) {
  const [currentPage, setCurrentPage] = useState(null); 
  const navigate = useNavigate(); 

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    const loginData = {
      username: username.toLowerCase(), 
      password: password.toLowerCase(), 
    };
  
    fetch('http://localhost:5000/api/authors/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })
      .then(response => response.json())
      .then(data => {
        if (data.message === 'Login successful') {
          localStorage.setItem('isAuthenticated', 'true');
          const newUsername = username.toLowerCase();
          const newAuthorId = data.author_id;
          updateAuthStatus(true);
          updateUserAndAuthorId(newUsername, newAuthorId);
          navigate('/homepage');
        } else if (data.message === 'Wrong Password') {
          toast.error('Wrong Password');
        } else if (data.message === 'User not found') {
          toast.error('User not found');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  useEffect(() => {
    // Add the class to the body when the component mounts
    document.body.classList.add('body-no-padding');

    // Remove the class when the component unmounts
    return () => {
      document.body.classList.remove('body-no-padding');
    };
  }, []);

  const styles = {
    loginContainer: {            
      margin: "auto",
      width: "500px",
      top: "50%",
      transform: "translate(0, 35%)",
      padding:" 10px"            
    },
    buttonSpace: {
      display: "flex",
      width: "100%",
      
      justifyContent: "center",
      height: "100%"
    },
    container: {     
      paddingTop: "-50px",           
      height: "100vh",      
      background: 'linear-gradient(to right, #348ac7, #7474bf)', // Adjust the gradient colors
    },
    buttonContainer: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: "center",            
      gap: '20px',              
    },
    button: {
      padding: '10px 20px',
      fontSize: '18px',
      cursor: 'pointer',
      backgroundColor: '#808080',  // Grey color
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      width: '150px',  // Fixed width for consistency
      textAlign: 'center',
      transition: 'background-color 0.3s',
    },
    buttonHover: {
      backgroundColor: '#666666',  // Slightly darker grey on hover
    }
  };

  if (isAuthenticated) {
    return <Navigate to="/homepage" />;
  }

  return (
    <div style={styles.container}>
       <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
      {currentPage === null && (
       <div style={styles.loginContainer}>
        <center  class="card" style={{padding: 50, boxShadow: "rgba(0, 0, 0, 0.35) 0px 5px 15px;"}}>
          <h1>Social Distribution</h1>
          <form>
            <div class="form-group">
              <label for="exampleInputUsername1">Username</label>
              <input type="username" class="form-control" value={username} id="exampleInputUsername1" placeholder="Username"  onChange={(e) => setUsername(e.target.value)}/>              
            </div>
            <div class="form-group" style={{marginTop: 10}}>
              <label for="exampleInputPassword1">Password</label>
              <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" onChange={(e) => setPassword(e.target.value)}/>
            </div>            
            <button type="submit"  style={{width: "100%", marginTop: 10}} class="btn btn-primary" onClick={(e) => handleLogin(e)}>Submit</button>
          </form>
            <small style={{marginTop: 10}}x class="form-text text-muted">Don't have an account yet? <a style={{textDecoration: "none"}} href='http://localhost:3000/register'>Register</a></small>        
            </center>
        </div>
        
      )}
      
      {currentPage === 'login' && (
        <Login
          setCurrentPage={setCurrentPage}
          navigate={navigate}
          updateAuthStatus={updateAuthStatus}
          updateUserAndAuthorId={updateUserAndAuthorId}
        />
      )}
      {currentPage === 'register' && <Register setCurrentPage={setCurrentPage} />}

      <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
    </div>
  );
}


export default LoginPage;