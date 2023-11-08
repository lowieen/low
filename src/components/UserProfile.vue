<template>
    <div class="wrapper">
        <div class="container">
            <Nav @toProfile="toProfile"></Nav>
            <div class="logo">
                <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
            </div>
            <div class="loader" v-if="isLoading"></div>
            <main class="main" v-else>
                <div class="presentation">
                    <div class="imgPresentation">
                        <div class="banner">
                            <img :src="imgPortadaUrl" alt="foto de banner" v-if="infoUser.user === userLogged">
                            <img :src="imgPortadaOtherUser" alt="foto de banner" v-else>
                            <label for="img-portada"><ion-icon :src="create" class="editIcon-banner" v-if="infoUser.user === this.$store.state.user"></ion-icon></label>
                            <input type="file" name="img-portada" id="img-portada" style="display: none;" accept="image/*" @change="filterImgPortada">
                        </div>
                        <div class="imgPerfil">
                            <img :src="imgPerfilUrl" alt="foto de perfil" v-if="infoUser.user === userLogged">
                            <img :src="imgPerfilOtherUser" alt="foto de perfil" v-else>
                            <label for="img-perfil"><ion-icon :src="create" class="editIcon-perfil" v-if="infoUser.user === this.$store.state.user"></ion-icon></label>
                            <input type="file" name="img-perfil" id="img-perfil" style="display:none;" accept="image/*" @change="filterImgPerfil">
                        </div>
                    </div>
                    <div class="inf-presentation">
                        <div class="names">
                            <h2 v-if="infoUser.nombre !== '-'">{{ infoUser.nombre }} {{ infoUser.apellido }}</h2>
                            <span>@{{ infoUser.user }}</span>
                        </div>
                        <div class="description">
                            <p>{{ infoUser.descripcion }}</p>
                        </div>
                        <div class="other">
                            <div class="link" v-if="infoUser.url !== null">
                                <ion-icon :src="linkSharp" class="urlIcon"></ion-icon>
                                <a :href='url'>{{ truncatedText(infoUser.url) }}</a>
                                <input type="url" name="url" id="url" class="input-url" v-if="inputUrl">
                            </div>
                            <div class="date" v-if="infoUser.fecha_nacimiento">
                                <ion-icon :src="balloon"></ion-icon>
                                <span>Fecha de nacimiento: {{ infoUser.fecha_nacimiento }}</span>
                            </div>
                            <div class="country" v-if="infoUser.pais !== '-'">
                                <ion-icon :src="location"></ion-icon>
                                <span>{{ infoUser.pais }}</span>
                            </div>
                        </div>
                        <div class="follows">
                            <div class="followers">
                                <span>{{ followers }} seguidores</span>
                            </div>
                            <div class="followed">
                                <span>{{ follows }} seguidos</span>
                            </div>
                            <div class="send-msj" v-if="infoUser.user !== userLogged">
                                <ion-icon :src="mailSharp" @click="sendMsj(infoUser.user)"></ion-icon>
                            </div>
                            <div class="btn-follow" v-if="infoUser.user !== userLogged">
                                <button class="btn" :class="{disabled: isFollowed}" @click="follow(infoUser.user)">{{ changeNameBtn(infoUser.user) }}</button>
                            </div> 
                        </div>
                    </div>
                </div>

                <div class="sections">
                    <div class="nav-sections">
                        <div class="principal-view" @click="visited('publ')" :class="{show:onStyle==='publ'}"><p>Publicaciones</p></div>
                        <div class="pictures" @click="visited('fotos')" :class="{show:onStyle==='fotos'}"><p>Fotos</p></div>
                        <div class="likes" @click="visited('likes')" :class="{show:onStyle==='likes'}"><p>Me Gusta</p></div>
                    </div>
                </div>

                <!-- SECCIONES Y SUS PUBLICACIONES -->
                <div class="data">
                    <!-- PUBLICACIONES -->
                    <div class="dta principal" v-if="onStyle==='publ'">
                        <div class="publication" v-for="elem in allPublications" :key="elem.id">
                            <div class="options">
                                <p>{{ calculateTimeAgo(elem.fecha_creacion) }}</p>
                                <ion-icon :src="ellipsisHorizontalOutline" @click="showed(elem)" v-if="this.allPublications.map(elem => elem.user_id).includes(elem.user_id)"></ion-icon>
                                <span :class="{visible:show === elem.id}" @click="deletePublication(elem)">{{ optionsMsj(elem) }}</span>
                            </div>
                            <div class="img-publ normal">
                                <img :src="imgPerfilUrl" alt="imagen perfil" v-if="elem.user_id === userLogged">
                                <img :src="'data:image/jpeg;base64,' + elem.img_perfil" alt="imagen perfil" v-else>
                                <div class="data-publ">
                                    <h3>{{ elem.user_id }}</h3>
                                    <p>{{ elem.contenido }}</p>
                                </div>
                            </div>
                            <div class="img-post" v-if="elem.imagen">
                                <img :src="'data:image/jpeg;base64,' + elem.imagen" alt="Imagen">
                            </div>
                            <div class="ups">
                                <span>{{ elem.likes }}</span>
                                <ion-icon 
                                :src="diamondOutline" :class="{liked: idPublicationsLikes.includes(elem.id) || isLiked.includes(elem.id)}"
                                @click="giveLike(elem.id)">
                                </ion-icon>
                            </div>
                        </div>
                    </div>
                    <!-- FOTOS -->
                    <div class="dta pic" v-else-if="onStyle==='fotos'">
                        <div class="publication" v-for="elem in publicationsWithImg" :key="elem.id">
                            <div class="options">
                                <p>{{ calculateTimeAgo(elem.fecha_creacion) }}</p>
                                <ion-icon :src="ellipsisHorizontalOutline" @click="showed(elem)" v-if="this.allPublications.map(elem => elem.user_id).includes(elem.user_id)"></ion-icon>
                                <span :class="{visible:show === elem.id}" @click="deletePublication(elem)">{{ optionsMsj(elem) }}</span>
                            </div>
                            <div class="img-publ normal">
                                <img :src="imgPerfilUrl" alt="imagen perfil" v-if="elem.user_id === userLogged">
                                <img :src="'data:image/jpeg;base64,' + elem.img_perfil" alt="imagen perfil" v-else>
                                <div class="data-publ">
                                    <h3>{{ elem.user_id }}</h3>
                                    <p>{{ elem.contenido }}</p>
                                </div>
                            </div>
                            <div class="img-post" v-if="elem.imagen">
                                <img :src="'data:image/jpeg;base64,' + elem.imagen" alt="Imagen">
                            </div>
                            <div class="ups">
                                <span>{{ elem.likes }}</span>
                                <ion-icon 
                                :src="diamondOutline" :class="{liked: idPublicationsLikes.includes(elem.id) || isLiked.includes(elem.id)}"
                                @click="giveLike(elem.id)">
                                </ion-icon>
                            </div>
                        </div>
                    </div>
                    <!-- LIKES -->
                    <div class="dta likes" v-else>
                        <div class="publication" v-for="elem in userLiked" :key="elem.id">
                            <div class="options">
                                <p>{{ calculateTimeAgo(elem.fecha_creacion) }}</p>
                                <ion-icon :src="ellipsisHorizontalOutline"  @click="showed(elem)" v-if="this.userLiked.map(elem => elem.user_id).includes(elem.user_id)"></ion-icon>
                                <span :class="{visible:show === elem.id}" @click="deletePublication(elem)">{{ optionsMsj(elem) }}</span>
                            </div>
                            <div class="img-publ normal" @click="goToProfile(elem.user_id)">
                                <img :src="imgPerfilUrl" alt="imagen perfil" v-if="elem.user_id === userLogged">
                                <img :src="elem.img_perfil" alt="imagen perfil" v-else>
                                <div class="data-publ">
                                    <h3>{{ elem.user_id }}</h3>
                                    <p>{{ elem.contenido }}</p>
                                </div>
                            </div>
                            <div class="img-post" v-if="elem.imagen">
                                <img :src="'data:image/jpeg;base64,' + elem.imagen" alt="Imagen">
                            </div>
                            <div class="ups">
                                <span>{{ elem.likes }}</span>
                                <ion-icon 
                                :src="diamondOutline" :class="{liked: idPublicationsLikes.includes(elem.id) || isLiked.includes(elem.id)}"
                                @click="giveLike(elem.id)">
                                </ion-icon>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import { diamondOutline, createOutline, ellipsisHorizontalOutline, linkSharp, create, balloon, location, mailSharp } from 'ionicons/icons'
import Nav from './NavBar.vue'
export default{
    props: ['user'],
    data(){
        return{
            //loading
            isLoading: true,
            //icons
            mailSharp,
            location,
            balloon,
            create,
            linkSharp,
            diamondOutline,
            createOutline,
            ellipsisHorizontalOutline,
            //vistas y estilos
            classActive: 'active',
            onStyle: 'publ',
            show: '',
            //publicaciones hechas
            allPublications: [], //todas las publicaciones hechas por el usuario
            publicationsWithImg: [], //publicaciones con img
            publicationsLike: [], //todas las publicaciones likeadas
            idPublicationsLikes: [], //solo el id de las pub likeadas
            isLiked: [], //pub actualmente likeadas
            userLiked: [], //pub likeadas por el usuario
            //informacion del usuario
            infoUser: [],
            url: '',
            follows: [],
            followers: [],
            isFollowed: false,
            userLogged: this.$store.state.user,
            userFollows: [],
            allFollows: [],
            //editar perfil
            btnEdit: false,
            inputUrl: false,
            //imagenes
            imgPerfilUrl: this.$store.state.img_perfil,
            imgPortadaUrl: this.$store.state.img_portada,
            imgPerfilOtherUser: null,
            imgPortadaOtherUser: null,
        }
    },
    methods:{
        filterImgPortada(event){
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('image', file);
            const user = this.userLogged;

            const url = `http://localhost:5000/upload/img-portada/${user}`;

            this.changeImg(formData,url);
        },
        filterImgPerfil(event){
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('image', file);
            const user = this.userLogged;

            const url = `http://localhost:5000/upload/img-profile/${user}`;

            this.changeImg(formData ,url);
        },
        changeImg(formData, url){
            let options = {
                method: 'PUT',
                body: formData
            }

            fetch(url, options)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else if(res.status === 400){
                        return res.json();
                    } else {
                        throw new Error ('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    if(data && data.error){
                        console.log(data.error);
                    }else {
                        if(data.perfil){
                            this.imgPerfilUrl = 'data:image/jpeg;base64,' + data.perfil;
                            this.$store.state.img_perfil = this.imgPerfilUrl
                        } else {
                            this.imgPortadaUrl = 'data:image/jpeg;base64,' + data.portada;
                            this.$store.state.img_portada = this.imgPortadaUrl;
                        }   
                    }   
                })
                .catch(err=>{
                    console.error('Error: ',err);
                })
        },
        // Al hacer click en el icon de mensaje, redirige a la url messages
        // Actualiza el estado de la propiedad chat_user en la store 
        // Para despues poder utilizarlo e iniciar automaticamente una conversación con el user
        sendMsj(username){
            this.$router.push({ name: 'messages' });
            this.$store.dispatch('chatUser', username);
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
            if(this.isFollowed){
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
                            // Al dejar de seguir, actualiza los seguidores y seguidos 
                            this.followers -= 1;
                            this.isFollowed = false;
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
                            // Al dar en 'Seguir' actualiza los seguidores y seguidos 
                            this.followers += 1;
                            this.isFollowed = true;
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
            }
        },
        // Recibe como parametro el usuario filtrado en la busqueda
        // Cambia el nombre del btn dependiendo si el usuario recibido es seguido o no por el user logeado
        changeNameBtn(){
            if(this.isFollowed){
                return 'Siguiendo';
            } else {
                return 'Seguir';
            }
        },
        truncatedText(text){
            if(text){
                return text.slice(0,30) + (text.length > 30 ? "...": "");
            }
        },
        // Recibe como parametro el nombre del usuario al cual hicimos click para ver su perfil
        // Actualiza la ruta con el nuevo valor del username
        // Llama al metodo toProfile para actualizar la obtención de datos con el nuevo user
        // Restablece onStyle para mostrar la vista principal de 'Perfil'
        goToProfile(username){
            this.$router.push({ name: 'user-profile', params: {user:username} });
            this.toProfile(username);
            this.onStyle = 'publ';
        },
        // Evento emitido desde la barra de nav
        // Evita el problema de estar en el perfil de otro usuario y dar click en Perfil de la barra nav
        // Y que no se vuelvan a aplicar las solicitudes al servidor 
        // Recibe un nuevo username si es que queremos ver otro perfil y no el nuestro 
        toProfile(newUser){
            this.getPublications();
            this.refresh_likes();
            this.getPublicationsLikes();
            this.getInfo(newUser);
        },
        // Cambia el formato de la fecha de nacimiento obtenido de la db
        // Parsear la fecha obtenida 
        // Almacena el dia, mes y año por separado
        // Suma +1 al dia obtenido de la fecha por los indicies que maneja js, que incian desde 0 
        // Array de nombre de meses, pasarle el numero de mes obtenido de la fecha para que funcione como indice
        // Cambia el formato de la fecha y almacena el valor obtenido en el array infoUser
        changeDate(){
            const fecha = this.infoUser.fecha_nacimiento;
            if(fecha){
                const fechaParseada = new Date(fecha);

                const dia = fechaParseada.getDate() + 1;
                const mes = fechaParseada.getMonth();
                const año = fechaParseada.getFullYear();

                const nombresMeses = [
                    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
                ];

                const nombreMes = nombresMeses[mes];

                const fechaFormateada = `${dia} de ${nombreMes} de ${año}`;

                this.infoUser.fecha_nacimiento = fechaFormateada;
            }
        },
        // Obtiene los datos personales del usuario
        // Llama al método changeDate para cambiar el formato de la fecha de nacimiento
        // newUser representa el username del perfil que queremos visitar(otro que no es el nuestro)
        // Verifica si contiene un valor indefinido, si lo es le agregamos el valor del prop de la ruta 
        getInfo(newUser){
            const userLogged = this.userLogged
            let user = null
            if(newUser === undefined){
                user = this.user;
            }else{
                user = newUser;
            }
            fetch(`http://localhost:5000/information/${user}/${userLogged}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    this.infoUser = data.dataUser;

                    this.imgPortadaOtherUser = 'data:image/jpeg;base64,' + this.infoUser.img_portada;
                    this.imgPerfilOtherUser = 'data:image/jpeg;base64,' + this.infoUser.img_perfil;

                    this.url = this.infoUser.url;
                    this.follows = data.seguidos;
                    this.followers = data.seguidores;
                    
                    const checkFollowed = data.seguimiento.some(seguimiento => seguimiento.followed_user === user);
                    if(checkFollowed){
                        this.isFollowed = true;
                    }

                    this.changeDate();
                    this.getPublications();
                    this.refresh_likes();
                    this.getPublicationsLikes();

                    this.isLoading = false;
                })
                .catch(err=>{
                    console.error('Error: ',err);
                })
        },
        // Detecta si el que le dá click al 'option' de la publicación es su user autenticado
        // Si lo es, elimina la publicación recibiendo el id de la publicación
        // Llama a los métodos para refrescar las publiaciones si la respuesta es status 200
        deletePublication(publicacion){
            const user = this.$store.state.user;
            const id = publicacion.id;
            if (publicacion.user_id === user){
                const options={
                    method:'DELETE',
                }

                fetch(`http://localhost:5000/publications/${id}/delete`, options)
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
                            console.error(data.error);
                        } else {
                            this.getPublicationsLikes();
                            this.getPublications();
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
            // Sino lo es, aplica el 'ocultar'
            // Envia el id de la publicación y el user que le dió a ocultar
            // La publicación se almacena en la tabla de publicaciones ocultas
            // Quita la publicación del objeto de publicaciones likeadas
            } else {
                let data = {
                    id : id,
                    user : user
                }

                let options = {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify(data)
                }

                fetch('http://localhost:5000/publications/hidden', options)
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud');
                        }
                    })
                    .then(data=>{
                        for(let i = 0; i < this.userLiked.length; i++){
                            if(this.userLiked[i].id === id){
                                this.userLiked.splice(i, id);
                                break;
                            }
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
            }
        },
        // Obtiene todos los likes hechos por el usuario
        // Los ordena de más reciente a la más antigua
        getPublicationsLikes(){
            const user = this.user;
            fetch(`http://127.0.0.1:5000/publication/liked/${user}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud');
                    }
                })
                .then(data=>{
                    this.userLiked=data.sort((a,b)=>{
                        const dataA = new Date(a.fecha_creacion);
                        const dataB = new Date(b.fecha_creacion);
                        return dataB - dataA;
                    })

                    this.userLiked.forEach(elem=>{
                        elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
                    })
                })
                .catch(err=>{
                    console.error('Error: ',err)
                })
        },
        // Obterngo los id de las publicaciones likeadas por el usuario
        // Se alamacenan en idPublicationsLikes para ser utilizado en el :class del icon de la pub
        // Utilizando un .includes()
        // Para saber si el id de las publicaciones que se visualizan es igual al id de las pub likeadas por el user
        likeUser(){
            if(this.publicationsLike.length > 0){
                this.idPublicationsLikes = this.publicationsLike.map((elem) => elem.publication_id);
            }
        },
        // Obtener todas las publicaciones que el usuario autenticado le dio like
        // Almacenarlas en publicationsLike
        // Llamar al metodo likeUser() 
        refresh_likes(){
        const user = this.$store.state.user;
        const url = `http://127.0.0.1:5000/publications/likes/${user}`;

        let options = {
            method:'GET',
            headers:{'Content-Type':'application/json'},
        }

        fetch(url,options)
            .then(res =>{
            if(res.ok){
                return res.json();
            }
            })
            .then(data =>{
            if(data){
                this.publicationsLike = data;
                this.likeUser();
            }
            })
        },
        // Envio el id del user que dio like y el id de la publicacion 
        // Primero detecta si ya le dió like o no
        // Si ya dió like, elimina ese like y actualiza las propiedades isLiked y idPublicationsLikes
        // Sino, guarda en la db los usuarios que le dan like a dichas pub
        // Hace una llamada al método getPublicationsLikes() para actualizar los elem visibles
        giveLike(pub_id){
            const user = this.user;

            const url = `http://127.0.0.1:5000/publications/${pub_id}/like`;
            const newLike = {
                user : user
            };

            if (this.isLiked.includes(pub_id) || this.idPublicationsLikes.includes(pub_id)) {
                let options = {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newLike)
                };
                fetch(url, options)
                    .then(res => {
                        if (res.ok) {
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                    .then(data => {
                        if (data && data.error) {
                            console.log(data.error);
                        } else {
                            this.RestarLike(pub_id);
                            this.isLiked = this.isLiked.filter(id => id !== pub_id); // Eliminar el id de isLiked
                            this.idPublicationsLikes = this.idPublicationsLikes.filter(id => id !== pub_id);
                            this.getPublicationsLikes();
                        }
                    })
                    .catch(err => {
                        console.error('Error: ', err);
                    });
            }else{
                let options = {
                    method:'POST',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify(newLike)
                }
                fetch(url, options)
                    .then(res =>{
                        if(res.ok){
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                .then(data =>{
                    if(data && data.error){
                        console.log(data.error);
                    } else {
                        this.SumarLike(pub_id);
                        this.isLiked.push(pub_id);
                        this.getPublicationsLikes();
                    }
                })
                .catch(err =>{
                    console.error('Error: ',err);
                })
            };
        },
        // Resta -1 la cantidad de likes que se visualizan si se saca el like
        RestarLike(pub_id){
            this.userLiked.forEach(pub => {
                if (pub.id == pub_id) {
                    if (pub.likes > 0) {
                        pub.likes -= 1;
                    }
                }
            });

            this.allPublications.forEach(pub => {
                if (pub.id == pub_id) {
                    if (pub.likes > 0) {
                        pub.likes -= 1;
                    }
                }
            });
        },
        // Suma un like a los likes visualizados cuando se le dá like
        SumarLike(pub_id){
            this.userLiked.forEach(pub => {
                if (pub.id == pub_id) {
                    pub.likes += 1;
                }
            });

            this.allPublications.forEach(pub => {
                if (pub.id == pub_id) {
                    pub.likes += 1;
                }
            });
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
        // Muestra o esconde las opciones de la publicación
        // Recibe por parametro la publicación
        // Si la propiedad show esta vacía le dá el valor del id de la publicacion 
        // Si ya tiene un valor, lo vacía
        // Al tener el valor del id de la publicación aplica estilos para mostrar el elemento span
        showed(publicacion){
            if(this.show){
                if(this.show !== publicacion.id){
                    this.show = publicacion.id;
                } else {
                    this.show = '';
                }
            } else {
                    this.show = publicacion.id;
            }
        },
        // Obtiene la publicación por parametro
        // Si el creador de la publicación es el mismo que el user logeado
        // Muestra 'Eliminar' en el span sino 'Ocultar'
        optionsMsj(publicacion) {
            const user = this.$store.state.user;
            if (publicacion.user_id === user) {
                return 'Eliminar';
            } else {
                return 'Ocultar';
            }
        },
        // Recibe como parametro el valor de la sección clickeada
        // Cambia las vistas
        visited(elem){
            if(elem === 'publ'){
                this.onStyle = elem;
            } else if (elem === 'fotos'){
                this.onStyle = elem;
            } else {
                this.onStyle = elem;
            }
        },
        // Obtiene todas las publicaciones realizadas por el usuario
        // Las ordena de la mas reciente a la antigua y las almacena 
        getPublications(){
            const user = this.user;
            fetch(`http://127.0.0.1:5000/publications/${user}`)
                .then(res =>{
                if(res.ok){
                    return res.json();
                } else {
                    throw new Error('Error en la solicitud.');
                }
                })
                .then(data =>{
                    this.allPublications = data.sort((a, b) => {
                        const dateA = new Date(a.fecha_creacion);
                        const dateB = new Date(b.fecha_creacion);
                        return dateB - dateA;
                    });

                    this.publicationsWithImg = this.allPublications.filter(elem => elem.imagen !== null);
                })
                .catch(err =>{
                    console.error('Error: ',err);
                })
        },
    },
    components:{
        Nav,
    },
    mounted(){
        this.getPublications();
        this.refresh_likes();
        this.getPublicationsLikes();
        this.getInfo();
    }
}
</script>

<style scoped>
.container{
    display: flex;
}

/*******************  PRESENTACION *******************/
.presentation{
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
}
.imgPresentation{
    position: relative;
}
.banner{
    width: 100%;
    height: 400px;
    position: relative;
}
.banner::after{
    content: '';
    width: 100%;
    height: 100%;
    position: absolute;
    background: transparent;
    background: linear-gradient(180deg, rgba(221,230,237,0) 85%, rgba(11,102,106,1) 100%);
    top: 0;
    left: 0;
}
.banner img{
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.imgPerfil{
    width: 220px;
    height: 220px;
    position: absolute;
    top: calc(100% - 100px);
    left: 50px;
}
.imgPerfil img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 3px;
}
.inf-presentation{
    margin-top: 10%;
    padding: 2%;
    position: relative;
}
.editIcon-banner,
.editIcon-perfil{
    font-size: 1.5em;
    cursor: pointer;
    position: absolute;
    top: 2%;
    right: 1%;
    transition: .2s ease;
    color: #fff;
    filter: drop-shadow(0 0 3px rgba(0, 0, 0, 1));
    z-index: 9;
}
.editIcon-banner:hover,
.editIcon-perfil:hover{
    color: #97FEED;
    filter: drop-shadow(0 0 10px #97feed81);
}
.names h2{
    color: #fff;
    letter-spacing: 1px;
    font-size: 2em;
}
.names span{
    color: rgb(200, 200, 200);
    font-weight: 600;
    font-size: 1.2em;
    padding: .5% 0;
}
.description p{
    color: rgb(145, 145, 145);
    padding: .5% 0;
}
.other{
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.link{
    display: flex;
    align-items: center;
    padding: .5% 0;
}
.link a{
    color: #97FEED;
    margin-left: .5%;
}
.link .urlIcon{
    color: #fff;
    transform: rotate(140deg);
    font-size: 1.2em;
}

.other span{
    color: rgb(158, 158, 158);
}
.date,
.country{
    display: flex;
    align-items: center;
    padding: .5% 0;
}
.date ion-icon,
.country ion-icon{
    color: rgb(200, 200, 200);
    margin-right: .5%;
}

.follows{
    display: flex;
    align-items: center;
    justify-content: end;
}

.followers,
.followed{
    color: rgb(158, 158, 158);
    font-weight: 600;
    padding-right: 2%;
}
.send-msj{
    padding-right: 2%;
}
.send-msj ion-icon{
    border: 2px solid #fff;
    border-radius: 3px;
    color: #fff;
    padding: 5px;
    cursor: pointer;
    transition: .1s ease;
    font-size: 1.3em;
}
.send-msj ion-icon:hover{
    color: #97FEED;
    border: 2px solid #97FEED;
    filter: drop-shadow(0 0 10px #97feed81);
}

.btn-follow{
    width: 100px;
}
.btn-follow .btn{
    width: 100%;
    padding: 5px;
}

.disabled{
    background-color: lightgray;
    box-shadow: none;
    color: gray;
}
/*******************  SECCIONES *******************/
.sections{
    padding-top: 5%;
    width: 100%;
    height: 10%;
}
.nav-sections{
    height: 50%;
    width: 100%;
    display: flex;
    justify-content: space-around;
}
.nav-sections div{
    margin: 0 2%;
    position: relative;
}
.nav-sections div::after{
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
.nav-sections div:hover::after{
    transform-origin: left;
    transform: scaleX(1);
}
.nav-sections div p{
    font-size: 1.5em;
    cursor: pointer;
    color: #fff;
}

.show::before{
    content: '';
    background-color: #97FEED;
    position: absolute;
    bottom: -6px;
    left: 0;
    width: 100%;
    height: 3px;
    border-radius: 5px;
}


.data{
    width: 100%;
    padding-top: 5%;
}

.dta.principal,
.dta.pic,
.dta.likes{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 5%;
}

@media (width < 1350px) {
    .wrapper{
        margin: 0;
    }
    .editIcon-banner,
    .editIcon-perfil{
        font-size: 2.5em;
    }
    .editIcon-banner{
        top: 30%;
        right: 3%;
    }
    .inf-presentation{
        margin-top: 15%;
    }
    .names h2{
        font-size: 1.8em;
    }
    .names span{
        font-size: 1.4em;
    }
    .description{
        font-size: 1.4em;
    }
    .other ion-icon,
    .other .link .urlIcon{
        font-size: 1.8em;
    }

    .other a,
    .other span{
        font-size: 1.3em;
    }

    .follows span{
        font-size: 1.3em;
    }

    .send-msj ion-icon{
        font-size: 2em;
    }
    .btn-follow{
        width: 18%;
    }
    .btn-follow .btn{
        font-size: 1.3em;
    }
    
}
@media (width > 1023px) {
    .editIcon-banner{
        top: 5%;
    }
}

@media (width < 675px){
    .inf-presentation{
        margin-top: 20%;
    }
    .btn-follow{
        width: 22%;
    }
}

@media (width < 555px){
    .inf-presentation{
        margin-top: 25%;
    }
    .btn-follow{
        width: 25%;
    }
}

@media (width < 455px){
    .follows{
        display: grid;
        grid-template-columns: 1fr 1fr;
        row-gap: 20px;
        place-items: end;
    }
    .followers{
        transform: translateX(40%);
    }
    .btn-follow{
        width: 70%;
    }
}
</style>