<!-- This Vue component is used for handling user login and displaying a list of travel information.
 The component has two main sections, one for displaying the login form and one for displaying 
 a table of travel information.

The login form allows the user to enter a username and password, which are then sent to the 
server for authentication using the handleLogin method. If the login is successful, the component's 
isAuthenticated data property is set to true and the table of travel information is displayed.

The table of travel information is populated with data from an API call made in the component's 
created lifecycle hook. The data is stored in the tableData data property and the keys of the first 
object in the data are used to create the table's column headers.

The component also has two buttons, one for switching between the table of all travel information 
and the table of the user's reserved travel, and another for logging out.

When the user clicks on reserve button, the reserve method is called, when the user clicks on 
cancel button, the cancel method is called and when the user clicks on "Logout" button, the logout 
method is called.

The component also uses the axios library to make the API calls, and it uses the localStorage 
object to store the authentication status. -->


<template>
  <div v-if="isAuthenticated == false">
      <form class="form-login" @submit.prevent="handleLogin">
        <label>
          Username:
          <input class="form-input" type="text" v-model="username" required />
        </label>
        <br />
        <label>
          Password:
          <input class="form-input" type="password" v-model="password" required />
        </label>
        <br />
        <button class="form-button" type="submit">Login</button>
      </form>
    </div>
    <div v-if="cond_vue_all_flights == true">
      <h1>All Travels</h1>
      <table>
        <thead>
          <tr>
            <th v-for="key in columns" :key="key">{{ key }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in tableData" :key="data.id">
            <td v-for="key in columns" :key="key">{{ data[key] }}</td>
            <td ><button v-on:click="reserve(data.id)">Reserve</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="cond_vue_my_flights == true">
      <h1>My Travels</h1>
      <table>
        <thead>
          <tr>
            <th v-for="key in columns2" :key="key">{{ key }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in tableData2" :key="data.id">
            <td v-for="key in columns2" :key="key">{{ data[key] }}</td>
            <td ><button v-on:click="cancel(data.id),seeMyFly()">Cancel</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <button v-on:click="seeMyFly(),my_flights(1)" v-if="cond_vue_all_flights == true">My flights</button>
    <button v-on:click="seeMyFly()" v-if="cond_vue_my_flights == true">All flights</button>
    <button v-on:click="logout()" v-if="isAuthenticated == true">Logout</button>
  </template>
  
  <script>

  import axios from 'axios';
  
  export default {
    data() {
      return {
        tableData: [],
        columns: [],
        tableData2: [],
        columns2: [],
        cond_vue_my_flights:false,
        cond_vue_all_flights:false,
        username: '',
        password: '',
        isAuthenticated: false,
      };
    },
    created() {
      axios.get('http://127.0.0.1:8000/api_r/travel/',{
                headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
                }
           })
        .then(response => {
          this.tableData = response.data;
          this.columns = Object.keys(this.tableData[0]);
        })
        .catch(error => {
          console.log(error);
        });
    },
    methods: {
        handleLogin() {
        const url = 'http://127.0.0.1:8000/api_u/login';

        const data = {
          username: this.username,
          password: this.password,
        };


        axios.post(url, data)
          .then(response => {

            this.cond_vue_all_flights = true;
            this.isAuthenticated = true;
            console.log(this.isAuthenticated);
            localStorage.setItem('logAut', this.isAuthenticated)
            localStorage.setItem('token', response.data.token)
            localStorage.setItem('user', response.data.user.id)
            localStorage.setItem('refresh-token', response.data['refresh-token'])
          })
          .catch(error => {
            console.log(error);
          });
      },
      reserve(id) {
        const url_axios = 'http://127.0.0.1:8000/api_r/passenger/';
        axios({
          url:  url_axios,
          headers: 
          {
              Authorization: 'Bearer ' + localStorage.getItem('token')
          },
          method: "POST",
          data:
          {
            "passenger":localStorage.getItem('user'),
            "Air_travel":id,
            "creator": localStorage.getItem('user')
          }
        })
        .catch(err=>{
          console.log(err);
        })
      },
      my_flights(id) {
        axios.get('http://127.0.0.1:8000/api_r/my_travel/'+id+"/",{
                headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
                },
           })
        .then(response => {
          this.tableData2 = response.data;
          this.columns2 = Object.keys(this.tableData2[0]);
        })
        .catch(error => {
          console.log(error);
        });
      },
      cancel(id) {
        axios.delete('http://127.0.0.1:8000/api_r/passenger/'+id+"/",{
                headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
                }
           })
        .catch(error => {
          console.log(error);
        });
      },
      logout() {
        const url = 'http://127.0.0.1:8000/api_u/logout';

        const data = {
          user: localStorage.getItem('user'),
        };


        axios.post(url, data)
          .then(response => {


            this.isAuthenticated = false;
            this.cond_vue_my_flights=false,
            this.cond_vue_all_flights=false,
            console.log(this.isAuthenticated);
            localStorage.setItem('token', null)
            localStorage.setItem('user', null)
            localStorage.setItem('refresh-token', null)
          })
          .catch(error => {
            console.log(error);
          });
      },
      seeMyFly() {
        this.cond_vue_my_flights = !this.cond_vue_my_flights
        this.cond_vue_all_flights = !this.cond_vue_all_flights
      },
    },
  };
  </script>
  
  <style>
  .form-login {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
  }
  
  .form-input {
      margin: 10px;
      padding: 10px;
      border-radius: 5px;
      border: none;
  }
  
  .form-button {
      margin: 10px;
      padding: 10px;
      border-radius: 5px;
      background-color: blue;
      color: white;
      border: none;
  }
  
  table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
  }
  
  th, td {
      border: 1px solid black;
      padding: 10px;
  }
  
  th {
      background-color: lightgray;
  }
  
  tr:nth-child(even) {
      background-color: lightgray;
  }
  
  button {
      margin: 10px;
      padding: 10px;
      border-radius: 5px;
      background-color: blue;
      color: white;
      border: none;
  }
  </style>