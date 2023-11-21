import React, { useState } from 'react';
import bootstrap from 'bootstrap' 
import { useNavigate } from 'react-router-dom';

function Navbar({ username, authorId }) {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const navigate = useNavigate();

  const handleSearch = async (event) => {
    try {
        event.preventDefault();
      const response = await fetch(`http://localhost:5000/follow/usersearch?query=${searchQuery}`);
      if (response.ok) {
        const data = await response.json();
        const filteredResults = data.users.filter(user => user.id !== authorId);
        
        // Navigate to the new page with the data in the state
        navigate('/search', { state: filteredResults });
        console.log("here");
        
        // setSearchResults(filteredResults);
      } else {
        console.error('Search failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

 
  return (
    <div>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Social Distribution</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/homepage">Home</a>
                    </li>
                    <li class="nav-item">
                    <a class="nav-link" href="/manageposts">Manage Posts</a>                    
                    </li>                                        
                    <li>
                    <a class="nav-link" href="/edit">Edit Profile</a>
                    </li>
                </ul>
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}/>
                    <button class="btn btn-outline-success" type="submit" onClick={(event) => handleSearch(event)}>Search</button>
                </form>
                    <button style={{marginLeft: 10}} type="button" class="btn btn-dark">Logout</button>
                </div>
            </div>
        </nav>
    </div>
  )
}

export default Navbar