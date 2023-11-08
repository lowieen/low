<template>
    <div class="wrapper">
        <div class="container">
            <Nav></Nav>
            <main class="main">
                <div class="logo">
                    <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
                </div>
                <div class="box search">
                    <ion-icon :src="searchSharp"></ion-icon>
                    <input type="text" placeholder="Buscar.." v-model="username">
                </div>
                <div class="box content">
                    <div class="user" v-for="elem in filterUser()" :key="elem.id">
                        <div class="user-img" @click="goToProfile(elem.user)">
                            <img :src="imgPerfilUser" alt="foto perfil" v-if="elem.user === userLogged">
                            <img :src="elem.img" alt="foto perfil" v-else>
                        </div>
                        <div class="user-name" @click="goToProfile(elem.user)">
                            <h4>@{{ elem.user }}</h4>
                            <h5 v-if="elem.nombre !== '-'">{{ elem.nombre }}</h5>
                            <div class="follows">
                                <p>{{ elem.followers }} Seguidores</p>
                                <p>{{ elem.follows }} Seguidos</p>
                            </div>
                        </div>
                        <div class="user-btn">
                            <button class="btn" v-if="elem.user !== userLogged" :class="{disabled: userFollows.includes(elem.user)}" @click="follow(elem.user)">{{ isFollowed(elem.user) }}</button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import Nav from '../components/NavBar.vue'
import { searchSharp } from 'ionicons/icons'

export default{
    data(){
        return{
            //icons
            searchSharp,
            //buscador
            username: '',
            allUsers: [],
            userLogged: this.$store.state.user,
            allFollows: [],
            userFollows: [],
            //imagenes perfil
            imgPerfilUser: this.$store.state.img_perfil,
        }
    },
    methods:{
        goToProfile(username){
            this.$router.push({ name: 'user-profile', params: { user: username } });
        },
        // Recibe como parametro el usuario filtrado en la busqueda
        // Cambia el nombre del btn dependiendo si el usuario recibido es seguido o no por el user logeado
        isFollowed(user){
            if(this.userFollows.includes(user)){
                return 'Siguiendo';
            } else {
                return 'Seguir';
            }
        },
        // Recibe como parametro el usuario al cual se le dió 'Seguir'
        // Checkea si el usuario seguido recibido por parametro esta dentro de los seguidos por el user logeado
        // Si ya lo sigue, procede a dejar de seguir y actualiza los follows de los usuarios 
        // Si no lo sigue se envia una solicitud POST con el seguidor y seguido
        // Del lado del sevidor, agrega los usuarios en la tabla followUp y actualiza los seguidores de los usuarios
        // Retorna todos los seguimientos 
        follow(userFollowed){
            const url = `http://localhost:5000/follow`;
                let data = {
                    follower_user : this.userLogged,
                    followed_user : userFollowed
                }
            if(this.userFollows.includes(userFollowed)){
                let options = {
                    method:'DELETE',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(data)
                }

                fetch(url,options)
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else if(res.status === 400){
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                    .then(data=>{
                        if(data && data.error){
                            console.log(data.error);
                        } else {
                            this.userFollows = data.user.map(elem => elem.followed_user);
                            this.allFollows = data.all.filter(elem => elem.follower_user == this.userLogged);  
                            // Al dejar de seguir, actualiza los seguidores y seguidos 
                            this.allUsers.forEach(users =>{
                                if(users.user == this.userLogged){
                                    if(users.follows > 0){
                                        users.follows -= 1;
                                    }  
                                }
                            })
                            this.allUsers.forEach(users =>{
                                if(users.user == userFollowed){
                                    if(users.followers > 0){
                                        users.followers -= 1;
                                    }                                 
                                }
                            })
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
            } else {
                let options = {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(data)
                }

                fetch(url,options)
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else if(res.status === 400){
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                    .then(data=>{
                        if(data && data.error){
                            const error = data.error;
                        } else {
                            this.userFollows = data.user.map(elem => elem.followed_user);
                            this.allFollows = data.all.filter(elem => elem.follower_user == this.userLogged); 
                            // Al dar en 'Seguir' actualiza los seguidores y seguidos 
                            this.allUsers.forEach(users =>{
                                if(users.user == this.userLogged){
                                    users.follows += 1;
                                }
                            })
                            this.allUsers.forEach(users =>{
                                if(users.user == userFollowed){
                                    users.followers += 1;
                                }
                            })
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
            }
        },
        // Obtiene los datos de todos los follows y los follows del usuario logeado
        getAllFollows(){
            const user = this.userLogged;
            fetch(`http://localhost:5000/follow/${user}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud');
                    }
                })
                .then(data=>{
                    this.userFollows = data.user.map(elem => elem.followed_user);
                    this.allFollows = data.all.filter(elem => elem.follower_user == this.userLogged);    
                })
                .catch(err=>{
                    console.error('Error: ',err)
                })
        },
        // Obtiene todos los usuarios registrados
        // Los almacena en allUsers
        getAllUsers(){
            fetch('http://localhost:5000/search_users')
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud');
                    }
                })
                .then(data=>{
                    this.allUsers = data.users_with_profile;
                    this.allUsers.forEach(elem =>{
                        elem.img = 'data:image/jpeg;base64,' + elem.img;
                    })
                })
                .catch(err=>{
                    console.error('Error: ',err);
                })
        },
        // Devuelve un filtro del array donde estan todos los usuarios 
        // Convierte los user del array en minuscula 
        // Verifica si lo tipeado por el usuario coincide con los usuarios 
        filterUser(){
            if(!this.username){
                return this.allUsers;
            }
            const usernameLower = this.username.toLowerCase();
            return this.allUsers.filter(elem=>{
                return elem.user.toLowerCase().startsWith(usernameLower) ||
                elem.nombre.toLowerCase().startsWith(usernameLower);
            })
        }
    },
    components:{
        Nav
    },
    mounted(){
        this.getAllUsers();
        this.getAllFollows();
    }
}
</script>

<style scoped>
.main{
    align-items: center;
}
.box{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 70%;
}
.box.search{
    flex-direction: row;
    position: relative;
}
.box.search input{
    width: 100%;
    padding: 3%;
    font-size: 1.2em;
    border: none;
    background: transparent;
    border-bottom: 1px solid #35a29f;
    color: #fff;
    letter-spacing: 1px;
}
.box.search input:focus{
    outline: none;
}
.box.search ion-icon{
    color: #35a29f;
    font-size: 2em;
    position: absolute;
    right: 3%;
}

.box.content{
    margin-top: 3%;
}
.box.content .user{
    width: 80%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5% 3%;
    margin-bottom: 5%;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
}
.user-img{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    cursor: pointer;
}
.user-img img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.user-name{
    width: calc(100% - 200px);
    padding: 0 5%;
    cursor: pointer;
}
.user-name h4{
    font-size: 1.4em;
    color: #fff;
    letter-spacing: 1px;
}
.user-name h5{
    color: rgb(158, 158, 158);
    font-size: 1.1em;
    margin: 1% 0;
}
.follows{
    display: flex;
}
.follows p{
    font-size: .9em;
    font-weight: 600;
    color: rgb(158, 158, 158);
    margin-right: 10%;
}
.user-btn{
    width: 100px;
}
.user-btn .btn{
    padding: 10%;
}

.disabled{
    background-color: lightgray;
    box-shadow: none;
    color: gray;
}

@media (width < 722px){
    .box{
        width: 90%;
        margin-top: 10%;
    }
    .box.search input{
        font-size: 1.4em;
    }
    .box.content{
        padding: 0;
    }
    .box.content .user{
        flex-direction: column;
    }
    .user-name,
    .user-btn{
        width: 100%;
        text-align: center;
    }
    .user-name h4{
        font-size: 1.6em;
    }
    .user-name h5{
        font-size: 1.4em;
    }
    .follows p{
        font-size: 1.1em;
        margin-right: 5%;
    }
    .follows{
        width: 100%;
        justify-content: center;
        padding-left: 10%;
    }
    .user-btn .btn{
        width: 50%;
        padding: 2%;
        margin-top: 5%;
        font-size: 1.1em;
    }
}

@media (min-width: 722px) and (max-width: 1023px) {
    .box{
        width: 90%;
    }
    .box.search input{
        font-size: 1.7em;
    }
    .box.search ion-icon{
        font-size: 2.5em;
    }
    .box.content .user{
        width: 90%;
    }
    .user-img{
        width: 80px;
        height: 80px;
    }
    .user-name{
        width: calc(100% - 210px);
    }
    .user-name h4{
        font-size: 1.8em;
    }
    .user-name h5{
        font-size: 1.6em;
    }
    .follows p{
        font-size: 1.3em;
        margin-right: 5%;
    }
    .user-btn{
        width: 130px;
    }
    .user-btn .btn{
        width: 100%;
        font-size: 1.2em;
        
    }
}

@media (min-width: 1024px) and (max-width: 1920px) {
    .box{
        width: 85%;
    }
    .box.search input{
        font-size: 1.5em;
    }
    .box.search ion-icon{
        font-size: 2.2em;
    }
    .box.content .user{
        width: 90%;
    }
    .user-img{
        width: 80px;
        height: 80px;
    }
    .user-name{
        width: calc(100% - 180px);
    }
    .user-name h4{
        font-size: 1.5em;
    }
    .user-name h5{
        font-size: 1.2em;
    }
    .follows p{
        font-size: 1em;
        margin-right: 5%;
    }
    .user-btn{
        width: 100px;
    }
    .user-btn .btn{
        width: 100%;
        font-size: .9em;
        
    }
}
</style>