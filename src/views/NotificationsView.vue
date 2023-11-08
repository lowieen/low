<template>
    <div class="wrapper">
        <div class="container">
            <Nav></Nav>
            <div class="logo">
                <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
            </div>
            <main class="main">      
                <div class="nav-noti">
                    <span @click="visited('all')" :class="{active:onStyle==='all'}">Todas</span>
                    <span @click="visited('mg')" :class="{active:onStyle==='mg'}">Me Gustas</span>
                    <span @click="visited('follow')" :class="{active:onStyle==='follow'}">Seguimientos</span>
                </div>
                <div class="container-noti" v-if="onStyle==='all'">
                    <div class="noti" v-for="elem in allNotifications" :key="elem.id">
                        <div class="box img">
                            <img :src="elem.img_perfil" alt="foto perfil">
                        </div>
                        <div class="box data">
                            <p><span>@{{ elem.user_emisor }}</span> {{ elem.contenido }}</p>
                        </div>
                        <div class="time">
                            <p>{{ calculateTimeAgo(elem.fecha_notificacion) }}</p>
                        </div>
                    </div>
                </div>
                <div class="container-noti" v-else-if="onStyle==='mg'">
                    <div class="noti" v-for="elem in likesNoti" :key="elem.id">
                        <div class="box img">
                            <img :src="elem.img_perfil" alt="foto perfil">
                        </div>
                        <div class="box data">
                            <p><span>@{{ elem.user_emisor }}</span> {{ elem.contenido }}</p>
                        </div>
                        <div class="time">
                            <p>{{ calculateTimeAgo(elem.fecha_notificacion) }}</p>
                        </div>
                    </div>
                </div>
                <div class="container-noti" v-else>
                    <div class="noti" v-for="elem in followedNoti" :key="elem.id">
                        <div class="box img">
                            <img :src="elem.img_perfil" alt="foto perfil">
                        </div>
                        <div class="box data">
                            <p><span>@{{ elem.user_emisor }}</span> {{ elem.contenido }}</p>
                        </div>
                        <div class="time">
                            <p>{{ calculateTimeAgo(elem.fecha_notificacion) }}</p>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import Nav from '../components/NavBar.vue'

export default{
    data(){
        return{
            //vistas y estilos
            classActive: 'active',
            onStyle: 'all',
            //publicaciones
            allNotifications: [],
            likesNoti: [],
            followedNoti: [],
        }
    },
    methods:{
        // Calcula hace cuanto tiempo se realizó la publicación
        // Obteniendo primeramente la diferencia de la hora de creacion y la actual en minutos
        // Se realiza 'if' para determinar si son minutos, horas o dias. Dependiendo hace cuantos minutos fue 
        calculateTimeAgo(fecha_creacion){
            const now = new Date();
            const createdDate = new Date(fecha_creacion);
            const timeDifference = now - createdDate;
            const minutesAgo = Math.floor(timeDifference / (1000 * 60));

            if(minutesAgo < 60){
                return `${minutesAgo} min`;
            } else if(minutesAgo < 1440){
                const hoursAgo = Math.floor(minutesAgo / 60);
                return `${hoursAgo} h`;
            } else {
                const daysAgo = Math.floor(minutesAgo / 1440);
                return `${daysAgo} d`;
            }
        },
        // Recibe como parametro el valor de la sección clickeada
        // Cambia las vistas
        visited(elem){
            if(elem === 'all'){
                this.onStyle = elem;
            } else if (elem === 'mg'){
                this.onStyle = elem;
            } else {
                this.onStyle = elem;
            }
        },
        // Obtiene todas las notificaciones filtradas por el usuario logeado
        // Retorna las notificaciones ordenadas por su fecha de la mas reciente a la antigua
        // Filtra dependiendo si el tipo de notificacion es un like o un follow y las almacena en arrays
        getAllNotification(){
            const user = this.$store.state.user;
            fetch(`http://localhost:5000/notifications/${user}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    this.allNotifications = data.sort((a, b) => {
                        const dateA = new Date(a.fecha_notificacion);
                        const dateB = new Date(b.fecha_notificacion);
                        return dateB - dateA;
                    })
                    this.likesNoti = this.allNotifications.filter(elem => elem.tipo === 'like');
                    this.followedNoti = this.allNotifications.filter(elem => elem.tipo === 'follow');

                    this.allNotifications.forEach(elem=>{
                        elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
                    })
                })
                .catch(err=>{
                    console.error('Error: ', err);
                })
        }
    },
    mounted(){
        this.getAllNotification();
    },
    components:{
        Nav,
    }
}
</script>

<style scoped>
.nav-noti{
    width: 100% ;
    display: flex;
    justify-content: space-around;
    align-items: center;
    color: #fff;
}
.nav-noti span{
    font-size: 1.5em;
    letter-spacing: 1px;
    padding: 1%;
    cursor: pointer;
    position: relative;
}

.nav-noti span::after{
    content: '';
    background-color: #97FEED;
    position: absolute;
    bottom: -6px;
    left: 0;
    width: 100%;
    height: 3px;
    border-radius: 5px;
    transform-origin: right;
    transform: scaleX(0);
    transition: transform 0.5s;
}
.nav-noti span:hover::after{
    transform-origin: left;
    transform: scaleX(1);
}
.active::before{
    content: '';
    background-color: #97FEED;
    position: absolute;
    bottom: -6px;
    left: 0;
    width: 100%;
    height: 3px;
    border-radius: 5px;
}

.container-noti{
    padding-top: 5%;
    width: 70%;
    margin: auto;
}
.noti{
    display: flex;
    align-items: center;
    margin-bottom: 5%;
    padding: 1% 2%;
    color: #fff;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
    cursor: pointer;
    position: relative;
}
.noti .box.img{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    margin-right: 2%;
}
.noti .box.img img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
.noti .box.data p{
    color: rgb(200, 200, 200);
}
.noti .box.data span{
    font-weight: 600;
    color: #fff;
}

.noti .time{
    position: absolute;
    top: 10%;
    right: 2%;
    font-size: .8em;
    color: rgb(200, 200, 200);
}
@media (width < 500px){
    .nav-noti{
        padding: 5% 0;
    }
    .nav-noti span{
        font-size: 1.3em;
        letter-spacing: 0;
    }
    .container-noti{
        width: 90%;
    }
    .noti{
        padding: 4% 10% 4% 2%;
    }
    .box.data{
        font-size: 1.2em;
    }
    .time p{
        font-size: 1.2em;
    }
}
@media (width < 1023px){
    .main{
        margin-top: 5%;
    }
    .container-noti{
        width: 90%;
    }
    .noti{
        padding: 4% 10% 4% 2%;
    }
    .box.data{
        font-size: 1.2em;
    }
    .time p{
        font-size: 1.2em;
    }
}

</style>