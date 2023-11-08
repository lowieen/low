<template>
    <!-- NAV BAR DEFAULT -->
    <nav class="nav-bar">
        <div class="inicio">
            <router-link :to="{ name: 'home' }">
                <ion-icon :src="homeOutline"></ion-icon><span>Inicio</span>
            </router-link>
        </div>
        <div class="msj">
            <router-link :to="{ name: 'messages' }">
                <ion-icon :src="mailOutline"></ion-icon><span>Mensajes</span>
            </router-link>
        </div>
        <div class="search">
            <router-link :to="{ name: 'search' }">
                <ion-icon :src="searchSharp"></ion-icon><span>Buscar</span>
            </router-link>
        </div>
        <div class="notifications">
            <router-link :to="{ name: 'notifications' }">
                <ion-icon :src="notificationsOutline"></ion-icon><span>Notificaciones</span>
            </router-link>
        </div>
        <div class="config">
            <router-link :to="{ name: 'options' }">
                <ion-icon :src="settingsOutline"></ion-icon><span>Configuración</span>
            </router-link>
        </div>
        <div class="support">
            <router-link :to="{ name: 'support' }">
                <ion-icon :src="helpOutline"></ion-icon><span>Soporte</span>
            </router-link>
        </div>
        <div class="profile" @click="toProfile">
            <router-link :to="{ name: 'user-profile', params: { user: userLogged } }">
                <img :src="this.$store.state.img_perfil" alt="imagen de perfil"><span>Perfil</span>
            </router-link>
        </div>
        <div class="logout" @click="logout">
            <router-link :to="{ name: 'login'}">
                <ion-icon :src="logOutOutline"></ion-icon><span>Cerrar Sesión</span>
            </router-link>
        </div>
    </nav>

    <!-- NAV BAR MOBILE -->
    <nav class="nav-bar-mobile" >
        <!-- SECCIÓN ARRIBA -->
        <div class="top">
            <div class="menu" @click="showMenu = !showMenu">
                <img :src="this.$store.state.img_perfil" alt="imagen de perfil">
            </div>
            <div class="more-options" v-if="showMenu">
                <div class="profile" @click="toProfile">
                    <router-link :to="{ name: 'user-profile', params: { user: userLogged } }">
                        <ion-icon :src="personOutline"></ion-icon><span>Perfil</span>
                    </router-link>
                </div>
                <div class="config">
                    <router-link :to="{ name: 'options' }">
                        <ion-icon :src="settingsOutline"></ion-icon><span>Configuración</span>
                    </router-link>
                </div>
                <div class="support">
                    <router-link :to="{ name: 'support' }">
                        <ion-icon :src="helpOutline"></ion-icon><span>Soporte</span>
                    </router-link>
                </div>
                <div class="logout" @click="logout">
                    <router-link :to="{ name: 'login'}">
                        <ion-icon :src="logOutOutline"></ion-icon><span>Cerrar Sesión</span>
                    </router-link>
                </div>
            </div>
        </div>
        <!-- SECCIÓN ABAJO -->
        <div class="buttom">
            <div class="inicio">
                <router-link :to="{ name: 'home' }">
                    <ion-icon :src="homeOutline"></ion-icon>
                </router-link>
            </div>
            <div class="msj">
                <router-link :to="{ name: 'messages' }">
                    <ion-icon :src="mailOutline"></ion-icon>
                </router-link>
            </div>
            <div class="search">
                <router-link :to="{ name: 'search' }">
                    <ion-icon :src="searchSharp"></ion-icon>
                </router-link>
            </div>
            <div class="notifications">
                <router-link :to="{ name: 'notifications' }">
                    <ion-icon :src="notificationsOutline"></ion-icon>
                </router-link>
            </div>
        </div>
    </nav>
</template>

<script>
import{ homeOutline, mailOutline,searchSharp, notificationsOutline, settingsOutline, helpOutline, logOutOutline, personOutline} from 'ionicons/icons';
export default{
    data(){
        return{
            //icons
            personOutline,
            homeOutline,
            mailOutline,
            searchSharp,
            notificationsOutline,
            settingsOutline,
            helpOutline,
            logOutOutline,
            //user
            userLogged: this.$store.state.user,
            //opciones
            showMenu: false,
        }
    },
    methods:{
        toProfile(){
            this.$emit('toProfile');
        },
        logout(){
            this.$root.logout();
        }
    },
}
</script>

<style scoped>
.nav-bar{
    width: 100px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    left: 13%;
    padding: 3% 0;
    z-index: 99;
}
.nav-bar div{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    width: 50px;
    height: 50px;
    border-radius: 50%;
}
.nav-bar div img{
    width: 40px;
    height: 40px;
    object-fit: cover;
    border-radius: 50%;
    transition: .1s ease;
}
.nav-bar div img:hover{
    filter: drop-shadow(0 0 5px rgb(151, 254, 237));
}
.nav-bar div a{
    text-decoration: none;
    text-align: center;
}
.nav-bar div ion-icon{
    font-size: 2em;
    color: #35A29F;
    transition: .1s ease;
}
.nav-bar div a:hover > ion-icon,
.nav-bar div a:hover > span{
    color: #97FEED;
    filter: drop-shadow(0 0 5px #97FEED);
}
.nav-bar div span{
    font-size: .8em;
    color: rgb(158, 158, 158);
    transition: .1s ease;
}

/* BARRA NAV PARA MOBILE */
.nav-bar-mobile{
    display: none;
}
.top{
    width: 100%;
    padding: 2% 5%;
    border-bottom: 2px solid #fff;
    background: rgba(34,40,49,1);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 99;
}
.menu{
    width: 65px;
    height: 65px;
}
.menu img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}
.more-options{
    width: 100%;
    height: 95vh;
    z-index: 99;
    background-color: rgba(34,40,49,1);
    position: absolute;
    top: 90%;
    left: 0;
}
.more-options div{
    width: 100%;
    padding: 10% 5%;
    font-size: 1.5em;
}
.more-options div ion-icon{
    color: #fff;
    font-size: 2em;
}
.more-options div a{
    width: 100%;
    text-decoration: none;
    color: #fff;
    display: flex;
    align-items: center;
}
.more-options div span{
    margin-left: 3%;
}
.buttom{
    width: 100%;
    padding: 3% 0 1%;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: rgba(34,40,49,1);
    background: linear-gradient(180deg, rgba(221,230,237,0) 0%, rgba(34,40,49,1) 20%);
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 99;
}
.buttom div ion-icon{
    color: #fff;
    font-size: 2.7em;
}

@media (max-width: 1023px) {
    .nav-bar{
        display: none;
    }
    .nav-bar-mobile{
        display: flex;
    }
}

@media (width > 1023px) and (width < 1350px) {
    .nav-bar{
        left: 6%;
    }
}
</style>
