import React, { useContext, useState } from 'react';
import bootstrap from 'bootstrap' 
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../App';

function Navbar() {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const navigate = useNavigate();
    const {username, authorId, updateAuthStatus, updateUserAndAuthorId} = useContext(UserContext);
    
    
    const handleLogout = () => {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
      localStorage.removeItem('authorId');
  
      updateAuthStatus(false);
      updateUserAndAuthorId(null,null);
      navigate('/');
    };

    const handleSearch = async (event) => {
      event.preventDefault();
      try {
        const localResponse = await fetch(`http://localhost:5000/api/follow/usersearch?query=${searchQuery}`);
        if (!localResponse.ok) {
          console.error('Local search failed');
          return;
        }
        const localData = await localResponse.json();
        const localResults = localData.users.filter(user => user.id !== authorId).map(user => ({
          id: user.id,
          username: user.username,
          host: 'local',
        }));
        console.log('local',localResults)
        // External API 1
        const externalResponse1 = await fetch('https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/', {
          headers: {
            'accept': 'application/json',
            'Authorization': 'Basic Y3Jvc3Mtc2VydmVyOnBhc3N3b3Jk',
          },
        });
        if (!externalResponse1.ok) {
          console.error('External search 1 failed');
          return;
        }
        const externalData1 = await externalResponse1.json();
        const externalResults1 = externalData1.items.map(item => ({
          id: item.id.split('/').pop(),
          username: item.displayName,
          host: 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/',
        }));
        console.log('e1',externalResults1)

        // External API 2 - Pagination
        let nextLink = 'https://cmput-average-21-b54788720538.herokuapp.com/api/authors/?page=1&page_size=5';
        let allExternalResults2 = [];

        while (nextLink) {
          const externalResponse2 = await fetch(nextLink, {
            headers: {
              'accept': 'application/json',
              'Authorization': 'Basic Q3RybEFsdERlZmVhdDpzdHJpbmc=',
            },
          });
          if (!externalResponse2.ok) {
            console.error('External search 2 failed');
            return;
          }
          const externalData2 = await externalResponse2.json();
          const externalResults2 = externalData2.items.map(item => ({
            id: item.id.match(/\/([^/]+)\/?$/)[1], //stupid slash at the end
            username: item.displayName,
            host: 'https://cmput-average-21-b54788720538.herokuapp.com/api',
          }));

          // Update the next link for the next iteration
          nextLink = externalData2.next;
          allExternalResults2 = [...allExternalResults2, ...externalResults2];
        }
        console.log('e2',allExternalResults2)

        //External API 3
        const externalResponse3 = await fetch('https://chimp-chat-1e0cca1cc8ce.herokuapp.com/authors/?page=1&size=1000', {
          headers: {
            'accept': 'application/json',
            'Authorization': 'Basic bm9kZS1jdHJsLWFsdC1kZWZlYXQ6Y2hpbXBjaGF0YXBp',
          },
        });
        if (!externalResponse3.ok) {
          console.error('External search 3 failed');
          return;
        }
        const externalData3 = await externalResponse3.json();
        const externalResults3 = externalData3.items.map(item => ({
          id: item.id.split('/').pop(),
          username: item.displayName,
          host: 'https://chimp-chat-1e0cca1cc8ce.herokuapp.com/',
        }));
        console.log('e3',externalResults3)

        const filteredExternalResults1 = externalResults1.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));
        const filteredExternalResults2 = allExternalResults2.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));
        const filteredExternalResults3 = externalResults3.filter(user => user.username.toLowerCase().includes(searchQuery.toLowerCase()));
        
        const combinedResults = [...localResults, ...filteredExternalResults1, ...filteredExternalResults2, ...filteredExternalResults3];
        console.log('combined', combinedResults)
        navigate('/search', { state: combinedResults });
      } catch (error) {
        console.error('Error:', error);
      }
    };

 
  return (
    <div>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous"/>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark">
            
            <div class="container-fluid">
                <a class="navbar-brand" href="/homepage">🚀 Social Distribution</a>
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
                    <li>
                    <a class="nav-link" href={"/inbox/" + authorId}>Inbox</a>
                    </li>
                </ul>
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search Users" aria-label="Search" value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}/>
                    <button class="btn btn-outline-success" type="submit" onClick={(event) => handleSearch(event)}>Search</button>
                </form>
                    <button style={{marginLeft: 10}} type="button" class="btn btn-dark" onClick={handleLogout}>Logout</button>
                </div>
            </div>
        </nav>
    </div>
  )
}

export default Navbar