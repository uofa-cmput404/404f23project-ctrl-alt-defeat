import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';

function Register(props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    // Add the class to the body when the component mounts
    document.body.classList.add('body-no-padding');

    // Remove the class when the component unmounts
    return () => {
      document.body.classList.remove('body-no-padding');
    };
  }, []);


  const styles = {
    container: {
      height: '100vh',            
      background: 'linear-gradient(to right, #348ac7, #7474bf)', // Adjust the gradient colors
    },
    registerContainer: {
        margin: "auto",
        width: "500px",
      top: "50%",
      transform: "translate(0, 50%)",
      padding:" 10px"  
    },
    input: {
      margin: '10px',
      padding: '10px',
      fontSize: '16px',
      width: '500px',
    },

  };

  const handleRegistration = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      toast.error('Empty Fields!', {
        position: 'top-right',
        autoClose: 3000,
      });
      return;
    }

    const registrationData = {
      username: username.toLowerCase(),
      password: password.toLowerCase(),
    };
    
    try {
      const response = await fetch('http://localhost:5000/api/requestors/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.error === 'Username already exists') {
          toast.error('Username already exists');
        } else {
          toast.success('Awaiting Approval!');
        }
      } else {
        console.error('Registration failed');
        toast.error('Registration failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={styles.container}>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <div style={styles.registerContainer}>
            <center class="card" style={{padding: 50, boxShadow: "rgba(0, 0, 0, 0.35) 0px 5px 15px;"}}>
                <h1>Registration</h1>          
                <form>
                    <div class="form-group">
                    <label for="exampleInputUsername1">Username</label>
                    <input type="username" class="form-control" value={username} id="exampleInputUsername1" placeholder="Username"  onChange={(e) => setUsername(e.target.value)}/>              
                    </div>
                    <div class="form-group" style={{marginTop: 10}}>
                    <label for="exampleInputPassword1">Password</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" onChange={(e) => setPassword(e.target.value)}/>
                    </div>            
                    <button type="submit"  style={{width: "100%", marginTop: 10}} class="btn btn-primary" onClick={(e) => handleRegistration(e)}>Submit</button>
                </form>
                <small style={{marginTop: 10}} class="form-text text-muted">Have an account already? <a style={{textDecoration: "none"}} href='http://localhost:3000/'>Login</a></small>        
            </center>     
        </div>
    </div>
  );
}

export default Register;
