<template>
  <div class="wrapper">
    <div class="container">
      <Nav></Nav>
      <div class="logo">
        <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
      </div>
      <div class="loader" v-if="isLoading"></div>
      <main class="main" v-else>
        <!-- CREAR UNA NUEVA PUBLICACION -->
        <div class="container-newPost">
          <img :src="imgPerfilUrl" alt="imagen perfil">
          <div class="container-write">
            <textarea name="publicacion" rows="1" cols="50" placeholder="¿Qué estás pensando?..." v-model="content"></textarea>
            <label for="fileInput" class="custom-file-upload">
              <ion-icon :src="attachOutline" :class="{isUsed:imgPost}"></ion-icon>
            </label>
            <input type="file" name="imagen" id="fileInput" style="display:none;" accept="image/*" @change="handleFileChange">
          </div>
          <button class="btn" @click="newPost">Publicar</button>
        </div>

        <!-- PUBLICACIONES -->
        <div class="container-posts">
          <div class="publication" v-for="elem in publications" :key="elem.id">
            <div class="options">
                <p>{{ calculateTimeAgo(elem.fecha_creacion) }}</p>
                <ion-icon :src="ellipsisHorizontalOutline" @click="showed(elem)"></ion-icon>
                <span :class="{visible: show==elem.id}" @click="options(elem)">{{ optionsMsj(elem) }}</span>
            </div>
            <div class="img-publ normal" @click="goToProfile(elem.user_id)">
              <img :src="imgPerfilUrl" alt="imagen perfil" v-if="elem.user_id === this.$store.state.user">
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
      </main>
    </div>
  </div>
</template>

<script>
import Nav from '../components/NavBar.vue'
import { diamondOutline, attachOutline, ellipsisHorizontalOutline } from 'ionicons/icons';

export default{
  data(){
    return{
      //loader
      isLoading: true,
      //icons
      diamondOutline,
      attachOutline,
      ellipsisHorizontalOutline,
      //nueva publicacion
      content: null,
      imgPost: null,
      //publicaciones
      publications: [],
      publicationsLike: [], //todas las publicaciones likeadas
      idPublicationsLikes: [], //solo el id de las pub likeadas
      show: '',
      isLiked: [], //pub actualmente likeadas
      //img del user logeado
      imgUserLogged: this.$store.state.img_perfil,
      imgPerfilUrl: null,
      imgPortadaUrl: null,
    }
  },
  components:{
    Nav
  },
  methods:{
    // Carga las imagenes de perfil y portada del usuario
    // Las almacena en las propiedades de la store utilizando las mutaciones y estados
    loadProfileImage(){
      const user = this.$store.state.user;
      fetch(`http://localhost:5000/profile-image/${user}`)
        .then(res=>{
          if(res.ok){
            return res.json();
          } else if(res.status === 400){
            return res.json();
          } 
          else {
            throw new Error('Error al obtener la imagen de perfil');
          }
        })
        .then(data=>{
          if (data.img_perfil) {
            this.imgPerfilUrl = `data:image/jpeg;base64, ${data.img_perfil}`;    
          }
          if (data.img_portada) {
            this.imgPortadaUrl = `data:image/jpeg;base64, ${data.img_portada}`;
          }
          const imgs = {'img_perfil' : this.imgPerfilUrl, 'img_portada' : this.imgPortadaUrl}
          this.$store.dispatch('imgPerfil',imgs);

          this.isLoading = false;
        })
        .catch(err=>{
          console.error(err);
        })
    },
    goToProfile(username){
      this.$router.push({ name: 'user-profile', params: {user:username} });
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
    // Recibe como parametro la publicación a la cual aplica el eliminar u ocultar
    // Si es su publicación, se aplica una solicitud DELETE a la tabla de publicaciones
    // Pasando credenciales del nombre de user y el id de la publicación a eliminar
    options(publicacion){
      const user = this.$store.state.user;
      const publicacionID = publicacion.id

      if(publicacion.user_id === user){
        const options={
          method:'DELETE',
        }

      fetch(`http://localhost:5000/publications/${publicacionID}/delete`, options)
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
            for (let i = 0; i < this.publications.length; i++) {
              if (this.publications[i].id === publicacion.id) {
                // Encuentra el objeto que contiene el contenido
                this.publications.splice(i, 1); // Elimina el objeto del array
                break; // Sal del bucle una vez que se elimine el objeto
              }
            }
          }
        })
        .catch(err=>{
          console.error('Error: ',err);
        })
      // Si la publicación no pertenece al usuario logeado envía el id y el user logeado para un POST
      // Se agregan a la tabla de publicaciones ocultas
      // Si la respuesta es correcta, se elimina la publicación del objeto this.publications 
      // Para dejar de visualizarla en el momento
      } else {
        let data = {
          id : publicacionID,
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
            this.getPublications();
          })
          .catch(err=>{
            console.error('Error: ',err);
          })

      }
    },
    // Manejar el cambio en el campo de entrada de archivo
    // Se crea un formData para el manejo de img 
    handleFileChange(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('image', file);
      this.imgPost = formData;
    },
    getUserUsername(){
      return this.$store.state.user;
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
    // Envio el id del user que dio like y el id de la publicacion 
    // Primero detecta si ya le dió like o no
    // Si ya dió like, elimina ese like y actualiza las propiedades isLiked y idPublicationsLikes
    // Sino, guarda en la db los usuarios que le dan like a dichas pub
    giveLike(pub_id){
      const user = this.$store.state.user;

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
              this.publications.forEach(pub => {
                if (pub.id == pub_id) {
                  if (pub.likes > 0) {
                    pub.likes -= 1;
                  }
                }
              });
              this.isLiked = this.isLiked.filter(id => id !== pub_id); // Eliminar el id de isLiked
              this.idPublicationsLikes = this.idPublicationsLikes.filter(id => id !== pub_id);
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
              this.publications.forEach(pub =>{
                if(pub.id == pub_id){
                  pub.likes += 1;
                }
              })
              this.isLiked.push(pub_id);
            }
          })
          .catch(err =>{
            console.error('Error: ',err);
          })
      };
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
    // Envia el nombre del usuario autenticado y logeado
    // Del lado del servidor, se obtiene primero a las personas que sigue para desp almacenar sus publicaciones 
    // Obtiene todas las publicaciones de los usuarios que sigue y las propias
    // Utiliza .sort() para ordernar el array de la mas reciente a la mas antigua 
    getPublications(){
      const user = this.$store.state.user;
      fetch(`http://127.0.0.1:5000/followed_publications/${user}`)
        .then(res =>{
          if(res.ok){
            return res.json();
          } else {
            throw new Error('Error en la solicitud.');
          }
        })
        .then(data =>{
          this.publications = data.publicaciones.sort((a, b) => {
            const dateA = new Date(a.fecha_creacion);
            const dateB = new Date(b.fecha_creacion);
            return dateB - dateA;
          });
          
          this.publications.forEach(elem=>{
            elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
          })
        })
        .catch(err =>{
          console.error('Error: ',err)
        })
    },
    // Si en el input hay contenido, obtengo ese valor y el del user almacenado con Vuex
    // Realiza un POST para crear una nueva publicación
    newPost(){
      if(this.content){
        let options = {}

        if(this.imgPost){
          this.imgPost.append('contenido', this.content)
          this.imgPost.append('usuario', this.$store.state.user)

          options = {
            method: 'POST',
            body: this.imgPost
          }
        } else {
          const data = {
            contenido : this.content,
            usuario : this.$store.state.user,
            imagen : null
          }

          options = {
            method: 'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify(data)
          };
        }

        const url = 'http://127.0.0.1:5000/publications';

        fetch(url,options)
          .then(res => {
            if(res.ok){
              return res.json();
            } else {
              throw new Error ('Error en la solicitud')
            }
          })
          .then(data => {
            if(data && data.error){
              console.error('Error: ', data.error)
            } else {
              this.content = '';
              this.imgPost = null;
              this.getPublications();
            }
          })
          .catch(err =>{
            console.error('Error: ', err);
          })
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
    }
  },
  mounted(){
    this.getPublications();
    this.refresh_likes();
    this.loadProfileImage();
  },
}
</script>

<style scoped>

/* VENTANA DE NUEVA PUBLICACION */
.container-newPost{
  width: 80%;
  height: 100px;
  margin: auto;
  display: flex;
  justify-content: start;
  align-items: center;
  margin-bottom: 5%;
  padding: 0 1%;
  border-radius: 3px;
  background-color: #35A29F;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
  border-top: 1px solid #ffffff65;
}
.container-newPost img{
  width: 70px;
  height: 70px;
  border-radius: 50%;
}
.container-write{
  display: flex;
  align-items: center;
  width: calc(100% - 170px);
  padding-left: 2%;
}
.container-write textarea{
  border: none;
  border-bottom: 1px solid #fff;
  background: transparent;
  font-size: .9em;
  padding: 1%;
  resize: none;
  color: #fff;
  width: 100%;
  transition: .3s ease;
}
.container-write textarea:focus{
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
}
.container-write textarea::placeholder{
  color: #fff;
  text-shadow: 0 2px 2px rgba(0, 0, 0, 0.3);
}

.custom-file-upload {
  width: 30px;
  padding: 3px 0;
  color: #fff;
  border: none;
  cursor: pointer;
  margin-top: 1%;
}

.custom-file-upload ion-icon{
  font-size: 1.7em;
  width: 30px;
}

.isUsed{
  filter: drop-shadow(0 0 2px #ffffff);
  color: #97FEED;
}

@media (max-width: 1023px) {
  .container-newPost{
    width: 90%;
  }
  .container-newPost img{
    width: 90px;
    height: 90px;
  }
  .container-write{
    width: calc(85% - 170px);
  }
  .container-write textarea{
    font-size: 1.5em;
  }
  .custom-file-upload {
    width: 50px;
    padding: 3px 0;

  }

  .custom-file-upload ion-icon{
    font-size: 3em;
    width: 50px;
  }

  .btn{
    font-size: 1.5em;
    width: 20%;
    margin-left: 5%;
  }
}
</style>