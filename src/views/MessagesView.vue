<template>
    <div class="wrapper">
        <div class="container">
            <Nav></Nav>
            <div class="logo">
                <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
            </div>
            <div class="loader" v-if="isLoading"></div>
            <main class="main" v-else>
                <div class="container-msj">
                    <!-- OTROS USUARIOS -->
                    <div class="containerUsers" @touchstart="startDrag" @touchmove="drag" @touchend="stopDrag">
                        <div class="box users" ref="carousel" :style="{ transform: 'translateX(' + translateX + 'px)' }">
                            <div class="user" v-for="elem in usersFollowed" :key="elem.id" @click="newChat(elem.followed_user)">
                                <img :src="elem.img_perfil" alt="imagen perfil">
                                <span class="name">@{{ elem.followed_user }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="newChat" v-if="allChats == 0 && showMsj">
                        <p>No hay conversaciones recientes.</p>
                    </div>
                    <!-- MENSAJES -->
                    <div class="containerMessages">
                        <div class="containerChat">
                            <div class="box chats" v-for="elem in allChats" :key="elem.id">
                                <div class="chat" @click="getThisChat(elem.recipient_user.user, elem.sender_user.user)">
                                    <div class="img-user">
                                        <img :src="elem.img_perfil" alt="imagen perfil">
                                    </div>
                                    <div class="info-user">
                                        <div class="name">
                                            <span v-if="elem.sender_user.user === userLogged && elem.recipient_user.nombre !== '-'">{{ truncatedText(elem.recipient_user.nombre) }}</span>
                                            <span v-if="elem.recipient_user.user === userLogged && elem.sender_user.nombre !== '-'">{{ truncatedText(elem.sender_user.nombre) }}</span>
                                            <span v-if="elem.sender_user.user === userLogged">@{{ truncatedText(elem.recipient_user.user) }}</span>
                                            <span v-if="elem.recipient_user.user === userLogged">@{{ truncatedText(elem.sender_user.user) }}</span>
                                            <span>{{ calculateTimeAgo(elem.latest_message_date) }}</span>
                                        </div>
                                        <div class="last-msj">
                                            <p v-if="elem.sender_user.user === userLogged">Tú: {{truncatedText(elem.latest_message_content) }}</p>
                                            <p v-if="elem.recipient_user.user === userLogged">{{ truncatedText(elem.latest_message_content) }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- CHAT -->
                        <div class="containerMsj" v-if="show">
                            <router-link :to="{ name : 'user-profile', params: { user: receptorChat }}" class="h-chat">{{ receptorChat }}</router-link>
                            <div class="box msj" v-for="elem in getChat" :key="elem.id">
                                <div class="msj" :class="{emit:elem.sender_user === userLogged, receive:elem.sender_user !== userLogged}">
                                    <p>{{ elem.contenido }}</p>
                                </div>
                            </div>
                            <div class="newMsj">
                                <textarea rows="1" ref="textarea" name="send" id="send" v-model="msj" @input="resizeTextarea" placeholder="Hola.." @keydown="handleKeyDown"></textarea>
                                <ion-icon :src="sendSharp" @click="sendMsj"></ion-icon>
                            </div>   
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import Nav from '../components/NavBar.vue'
import { sendSharp } from 'ionicons/icons'
export default{
    props:['user'],
    data(){
        return{
            //loader
            isLoading: true,
            //icon
            sendSharp,
            //estilos
            isDragging: false,
            startPosition: 0,
            currentTranslateX: 0,
            translateX: 0,
            minTranslateX: 0, // Límite mínimo de desplazamiento
            maxTranslateX: 0, // Límite máximo de desplazamiento
            //mensaje
            msj: '',
            usersFollowed: [],
            getChat: [],
            allChats: [],
            emisorChat: '',
            receptorChat: '',
            userLogged: this.$store.state.user,
            show: false,
            showMsj: true,
            userReceived: null,
        }
    },
    methods: {
        truncatedText(text){
            if(text){
                return text.slice(0,12) + (text.length > 12 ? "...": "");
            }
        },
        // Si se le quiere enviar un mensaje a un usuario desde el perfil
        // Obtiene el nombre del usuario para poder iniciar el chat 
        startChat(){
            const user_received = this.$store.state.chat_user;
            if(user_received){
                this.receptorChat = user_received;
                this.show = true;
                this.newChat(this.receptorChat);
            }
        },
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
        // Filtra el nombre del usuario con el que se chatea
        // Para pasarle como argumento a newChat y muestre la conversación
        getThisChat(receptor, emisor){
            if(receptor === this.userLogged){
                this.newChat(emisor);
            } else {
                this.newChat(receptor);
            }
        },
        // Obtiene la conversación entre el usuario logeado y el usuario recibido por parametro
        newChat(receptor){
            this.receptorChat = receptor;
            this.showMsj = false;
            const user = this.$store.state.user;

            fetch(`http://localhost:5000/message/${user}/${receptor}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error ('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    this.getChat = data.chats;
                    this.emisorChat = data.emisor;
                    this.receptorChat = data.receptor;
                    this.show = true;
                })
                .catch(err=>{
                    console.error('Error: ',err);
                })
        },
        // Evita el salto de línea y llama al método para enviar el mensaje
        handleKeyDown(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); 
                this.sendMsj();
            }
        },
        sendMsj(){
            if(this.msj && /\S/.test(this.msj)){
                const emisor = this.emisorChat;
                const receptor = this.receptorChat;

                let options = {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({contenido : this.msj})
                }

                fetch(`http://localhost:5000/message/${emisor}/${receptor}`,options)
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                    .then(data=>{
                        this.msj = '';
                        this.getChat = data;
                        this.newChat(receptor);
                        this.getAllChats();
                    })
                    .catch(error=>{
                        console.error('Error: ',err);
                    })
            }
        },
        // Obtén una referencia al elemento textarea
        // Ajusta la altura automáticamente
        resizeTextarea() {
            if (this.$refs.textarea) {
                const textarea = this.$refs.textarea;
                textarea.style.height = 'auto';
                textarea.style.height = textarea.scrollHeight + 'px';
            }
        },
        // Se llama cuando comienza la interacción del usuario
        // Registra la posición inicial y el estado de arrastre.
        startDrag(event) {
            this.isDragging = true;
            this.startPosition = event.touches[0].clientX;
            this.currentTranslateX = this.translateX;
        },
        // Se llama mientras el usuario arrastra el carrusel
        // Calcula la posición actual y ajusta la posición del carrusel en consecuencia, aplicando límites
        drag(event) {
            if (this.isDragging) {
            const clientX = event.touches[0].clientX;
            const deltaX = clientX - this.startPosition;

            // Aplicar límites de desplazamiento
            this.translateX = Math.min(Math.max(this.minTranslateX, this.currentTranslateX + deltaX), this.maxTranslateX);
            }
        },
        // Se llama cuando el usuario suelta el carrusel. Indica que ya no se está arrastrando.
        stopDrag() {
            this.isDragging = false;
        },
        // Calcula los límites de desplazamiento del carrusel
        // Asegura que el elemento esté montado en el DOM antes de hacerlo
        // Calcula los límites en función del ancho del contenedor y el ancho del carrusel para evitar desplazamientos más allá del contenido visible.
        calculateLimits() {
            if (this.$refs.carousel) {
            const containerWidth = this.$el.clientWidth;
            const carouselWidth = this.$refs.carousel.scrollWidth;

            this.maxTranslateX = 0;
            this.minTranslateX = Math.min(0, containerWidth - carouselWidth);
            }
        },
        // Obtiene todos los usuarios seguidos y los ordena según la fecha de seguimiento
        getUsuersFollowed(){
            const user = this.$store.state.user;
            fetch(`http://localhost:5000/follow/${user}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    this.usersFollowed = data.user.sort((a,b) => {
                        const dataA = new Date(a.fecha_seguimiento);
                        const dataB = new Date(b.fecha_seguimiento);
                        return dataB - dataA;
                    });
                    
                    this.usersFollowed.forEach(elem=>{
                        elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
                    })
                })
                .catch(err=>{
                    console.error('Error: ', err);
                })
        },
        getAllChats(){
            const user = this.userLogged;
            fetch(`http://localhost:5000/message/${user}`)
            .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    this.allChats = data.sort((a,b) =>{
                        const dataA = new Date(a.latest_message_date);
                        const dataB = new Date(b.latest_message_date);
                        return dataB - dataA;
                    })
                    
                    this.allChats.forEach(elem => {
                        elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
                    })

                    this.isLoading = false;
                    
                })
                .catch(err=>{
                    console.error('Error: ', err);
                })
        }
    },
    mounted(){
        this.getUsuersFollowed();
        this.getAllChats();
        this.startChat();
        // Asegúrate de que el elemento esté montado antes de calcular los límites
        // Luego, se agrega un event listener para el evento resize de la ventana para recalcular los límites si la ventana se redimensiona.
        this.$nextTick(() => {
            this.calculateLimits();
        });
        window.addEventListener('resize', this.calculateLimits);
    },
    beforeUnmount() {
        this.$store.dispatch('cleanChatUser');
        // Se elimina el event listener del evento resize
        window.removeEventListener('resize', this.calculateLimits);
    },
    components:{
        Nav
  }
}
</script>

<style scoped>
.container-msj{
    width: 100%;
    margin: auto;
    display: flex;
    flex-direction: column;
}
.containerUsers {
    width: 100%;
    overflow: hidden; 
    overflow-x: auto;
    border-bottom: 2px solid #fff;
    padding-bottom: 3%;
}
.box.users{
    display: flex;
    transition: transform 0.1s ease;
    padding: 2% 0 4%;
}
/* Estilos para la barra de desplazamiento horizontal */
.container-users::-webkit-scrollbar {
    background-color: transparent;
    height: 7px;
}
.container-users::-webkit-scrollbar-thumb {
    background: #97FEED;
    border-radius: 20px;
}
.container-users::-webkit-scrollbar-thumb:hover {
    background: #35A29F;
}


/* OTROS USUARIOS */
.user{
    flex: 0 0 100px; /* Ancho fijo para cada elemento del carrusel */
    height: 100px;
    margin: 0 15px;
    position: relative;
    border-radius: 50%;
    cursor: pointer;
    transition: .1s ease;
}
.user:hover,
.user:hover > span{
    filter: drop-shadow(0 1px 5px black);
    text-decoration: underline;
}
.user img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.user span{
    position: absolute;
    bottom: -30%;
    left: 50%;
    transform: translateX(-50%);
    font-weight: 600;
    color: #fff;
    padding: 1% 0;
}

/* MENSAJES */
.containerMessages{
    display: flex;
}
.containerChat{
    display: flex;
    flex-direction: column;
    height: 70vh;
    width: 100%;
    overflow: hidden;
    overflow-y: auto;
    margin-top: 5%;
}
.box.chats{
    margin-bottom: 5%;
}

.newChat{
    width: 100%;
    padding: 1% 2%;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
    margin: 5% 0;
    color: #fff;
}

.chat{
    width: 100%;
    display: flex;
    cursor: pointer;
    padding: 1% 2%;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
    margin-bottom: 2px;
    transition: .1s ease;
}
.chat:hover{
    background-color: #156266;
}
.img-user{
    width: 75px;
    height: 75px;
    border-radius: 50%;
}
.img-user img{
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.info-user{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 2%;
}
.info-user .name span{
    margin-right: 1%;
    font-weight: 500;
    color: rgb(158, 158, 158);
}
.name span:first-child{
    color: #fff;
    letter-spacing: .5px;
}
.name span:last-child{
    font-size: .8em;
}
.last-msj{
    color: rgb(180, 180, 180);
}


/* CHAT */
.containerMsj{
    width: 100%;
    height: 70vh;
    overflow: hidden;
    overflow-y: auto;
    padding: 2% 0 2% 1.5%;
    display: flex;
    flex-direction: column;
    justify-content: end;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
    margin: 5% 0 0 1%;
    position: relative;
}
.h-chat{
    color: #fff;
    font-size: 1.5em;
    font-weight: 800;
    position: absolute;
    top: 0%;
    left: 0%;
    padding: 3% 2% 7%;
    text-decoration: underline;
    width: 110%;
    background-color: #0B666A;
    background: linear-gradient(0deg, rgba(221,230,237,0) 0%, rgba(11,102,106,1) 30%);
    cursor: pointer;
}
.box.msj{
    width: 100%;
    display: flex;
    flex-direction: column;
    color: rgb(158, 158, 158);
    padding: 0 5%;
}
.msj.receive,
.msj.emit{
    max-width: 75%;
    align-self: start;
    padding: 1%;
    margin-bottom: 3%;
    background-color: rgb(110, 110, 110);
    color: #fff;
    position: relative;
    border-radius: 3px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
}
.msj.receive::before{
    content: '';
    position: absolute;
    bottom: 0;
    left: -10px;
    border-right: 15px solid rgb(110, 110, 110);
    border-top: 15px solid transparent;
    border-radius: 5px;
}
.msj.emit{
    align-self: end;
    background-color: #35A29F;
}
.msj.emit::before{
    content: '';
    position: absolute;
    bottom: 0;
    right: -10px;
    border-left: 15px solid #35A29F;
    border-top: 15px solid transparent;
    border-radius: 5px;
}

.newMsj{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}
.newMsj textarea{
    width: 90%;
    padding: 1% 2% 1% 1%;
    background: transparent;
    border: none;
    color: #fff;
    border: 1.5px solid #fff;
    border-radius: 3px;
    font-size: 1.2em;
    resize: none;
    overflow: hidden;
}
.newMsj textarea:focus{
    outline: none;
}
.newMsj textarea::placeholder{
    color: rgb(120, 120, 120);
}
.newMsj ion-icon{
    position: absolute;
    right: 6%;
    color: #35A29F;
    cursor: pointer;
    font-size: 1.5em;
    transition: .1s ease;
}
.newMsj ion-icon:hover{
    color: #97FEED;
    filter: drop-shadow(0 0 5px #97FEED);
}

@media (max-width: 1023px) {
    .container-msj{
        width: 90%;
        padding: 0;
    }
    .box.users{
        padding-bottom: 7%;
    }
    .user span{
        font-size: 1.5em;
        bottom: -40%;
    }
    .img-user{
        width: 90px;
        height: 90px;
    }
    .info-user .name span{
        font-size: 1.4em;
    }
    .info-user .last-msj p{
        font-size: 1.5em;
    }
    .containerMsj{
        height: 55vh;
    }
    .msj.emit,
    .msj.receive{
        font-size: 1.5em;
        margin: 5% 0;
        padding: 2% 4%;
    }
    .newMsj textarea{
        font-size: 1.4em;
    }
}

@media (min-width: 1024px) and (max-width: 1980px) {
    .container-msj{
        width: 95%;
    }
}
</style>