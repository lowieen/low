<template>
    <div class="wrapper">
        <div class="container">
            <Nav></Nav>
            <div class="logo">
                <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
            </div>
            <main class="main">          
                <div class="box-config">

                    <!-- SECCIONES DE CONFIGURACION -->
                    <div class="section">
                        <h2>Configuración</h2>
                        <div class="personalData" :class="{actived:selector==='account'}" @click="selector='account'">
                            <h4>Tu cuenta</h4>
                        </div>
                        <div class="privacity" :class="{actived:selector==='privacity'}" @click="selector='privacity'">
                            <h4>Privacidad</h4>
                        </div>
                    </div>
                
                    <div class="config" v-if="selector === 'account'">
                        <!-- EDITAR INFORMACIÓN -->
                        <div class="your-account" @click="showed('data')" :class="{activedOptions:show === 'data'}">
                            <ion-icon :src="personSharp"></ion-icon>
                            <h4>Información de la cuenta</h4>
                            <p>Ve la información de tu cuenta y tus datos personales.</p>
                        </div>
                        <div class="data" :style="{height:height+'px'}" v-if="show === 'data'">
                            <div class="personal-data info" :style="{transform:'translateX('+xOffsetWatch+'%)'}">
                                <div class="h-form">
                                    <h3>Tus datos personales</h3>
                                </div>
                                <div class="container-form" v-if="userData !== null">
                                    <form>
                                        <div class="box name">
                                            <label for="nombre">Nombre</label>
                                            <span>{{ userData.nombre }}</span>
                                        </div>
                                        <div class="box lastname">
                                            <label for="apellido">Apellido</label>
                                            <span>{{ userData.apellido }}</span>
                                        </div>
                                        <div class="box country">
                                            <label for="pais">País</label>
                                            <span>{{ userData.pais }}</span>
                                        </div>
                                        <div class="box phone">
                                            <label for="telefono">Teléfono</label>
                                            <span>{{ userData.telefono }}</span>
                                        </div>
                                        <div class="box date">
                                            <label for="fechaNac">Fecha de nacimiento</label>
                                            <span>{{ userData.fecha_nacimiento }}</span>
                                        </div>
                                        <div class="box url">
                                            <label for="url">URL</label>
                                            <span>{{ truncatedText(userData.url) }}</span>
                                        </div>
                                        <div class="box description">
                                            <label for="description">Descripción breve de ti</label>
                                            <span>{{ truncatedText(userData.descripcion) }}</span>
                                        </div>
                                        <div class="box button">
                                            <button type="button" class="btn" @click=changeEdit>Editar</button>
                                        </div>
                                    </form>
                                </div>
                            </div>

                            <div class="personal-data form" :style="{transform:'translateX('+(xOffsetEdit)+'%)'}">
                                <div class="h-form">
                                    <h3>Tus nuevos datos personales</h3>
                                </div>
                                <div class="container-form">
                                    <form>
                                        <div class="container-input">
                                            <label for="nombre">Nombre</label>
                                            <input type="text" name="nombre" required v-model="name">
                                        </div>
                                        <div class="container-input">
                                            <label for="apellido">Apellido</label>
                                            <input type="text" name="apellido" required v-model="lastname">
                                        </div>
                                        <div class="container-input">
                                            <label for="pais">País</label>
                                            <input type="text" name="pais" required v-model="country">
                                        </div>
                                        <div class="container-input">
                                            <label for="telefono">Teléfono</label>
                                            <input type="text" name="telefono" required v-model="phone">
                                        </div>
                                        <div class="container-input">
                                            <label for="fechaNac">Fecha de nacimiento</label>
                                            <input type="date" name="fechaNac" required v-model="date">
                                        </div>
                                        <div class="container-input">
                                            <label for="url">URL</label>
                                            <input type="url" name="url" id="url" v-model="url">
                                        </div>
                                        <div class="container-input">
                                            <label for="description">Descripción breve de ti</label>
                                            <textarea name="descripition" id="descripition" cols="30" rows="3" v-model="description"></textarea>
                                        </div>
                                        <div class="container-buttons">
                                            <button type="button" class="btn" @click="changeInfo">Cancelar</button>
                                            <button type="button" class="btn" @click="save">Guardar</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>

                        <!-- CAMBIO DE PASS -->
                        <div class="change-password" @click="showed('info')" :class="{activedOptions:show === 'info'}">
                            <ion-icon :src="keySharp"></ion-icon>
                            <h4>Cambia tu contraseña</h4>
                            <p>Cambia tu contraseña en cualquier momento.</p>
                        </div>
                        <div class="pass" v-if="show === 'info'">
                            <div class="container-input">
                                <label for="pass">Contraseña actual</label>
                                <input type="password" name="pass" id="pass" v-model="password">
                                <p v-if="msjErrorPass" class="msjError">{{ msjErrorPass }}</p>
                            </div>
                            <div class="container-input">
                                <label for="newPass">Nueva contraseña</label>
                                <input type="password" name="newPass" id="newPass" v-model="newPassword">
                            </div>
                            <div class="container-input">
                                <label for="rNewPass">Repita la nueva contraseña</label>
                                <input type="password" name="rNewPass" id="rNewPass" v-model="rNewPassword">
                                <p v-if="msjErrorNewPass" class="msjError">{{ msjErrorNewPass }}</p>
                            </div>
                            <div class="container-buttons">
                                <button type="button" class="btn" @click="checkPass" :class="{success:passSuccess}">{{ msjBtn }}</button>
                            </div>
                        </div>

                        <!-- ELIMINAR CUENTA -->
                        <div class="delete-account" @click="showed('delete')" :class="{activedOptions:show === 'delete'}">
                            <ion-icon :src="closeCircleSharp"></ion-icon>
                            <h4>Elimina tu cuenta</h4>
                            <p>Averigua cómo puedes eleminar tu cuenta.</p>
                        </div>
                        <div class="delete" v-if="show === 'delete'">
                            <div class="container-deleted" v-if="showDelete == 'question'">
                                <h4>Deseas eliminar tu cuenta?</h4>
                                <button type="button" class="btn" @click="showDelete = 'confirm'">Eliminar</button>
                            </div>
                            <div class="container-confirm" v-else-if="showDelete == 'confirm'">
                                <p>Si realmente quieres eliminar tu cuenta, introduce tu contraseña</p>
                                <input type="password" name="pass" id="pass" v-model="passwordDelete">
                                <p class="msjError" v-if="msjErrorConfirm">{{ msjErrorConfirm }}</p>
                                <button type="button" class="btn" @click="confirmDelete" :class="{success:confirmSuccess}">{{ msjBtnDelete }}</button>
                            </div>
                        </div>
                    </div>

                    <!-- PRIVACIDAD -->
                    <div class="config two" v-else>
                        <div class="hidden-publications" @click="showPublications" :class="{activedOptions:visiblePublications}">
                            <ion-icon :src="eyeOff"></ion-icon>
                            <h4>Publicaciones ocultas</h4>
                            <p>Mira y elige si deseas volver a ver algunas publicaciones ocultas.</p>
                        </div>
                    </div>
                </div>
                <div class="box-publications" v-if="visiblePublications && selector==='privacity'">
                    <div class="publication" v-for="elem in hiddens" :key="elem.id">
                        <div class="options">
                            <p>{{ calculateTimeAgo(elem.fecha_creacion) }}</p>
                            <ion-icon :src="ellipsisHorizontalOutline"  @click="showOption(elem.id)"></ion-icon>
                            <span :class="{visible: showOptions === elem.id}" @click="restore(elem)">Restaurar</span>
                        </div>
                        <div class="img-publ normal">
                            <img :src="elem.img_perfil" alt="imagen perfil">
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
                                :src="diamondOutline">
                            </ion-icon>
                        </div>
                    </div>
                    <div class="publication msj" v-if="msjPubNull">
                        <p>{{ msjPubNull }}</p>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import Nav from '../components/NavBar.vue'
import { personSharp, keySharp, closeCircleSharp, eyeOff, diamondOutline, ellipsisHorizontalOutline } from 'ionicons/icons';

export default{
    data(){
        return{
            //icons
            ellipsisHorizontalOutline,
            diamondOutline,
            eyeOff,
            personSharp,
            keySharp,
            closeCircleSharp,
            //estilos
            selector: 'account',
            show: null,
            xOffsetWatch: 0,
            xOffsetEdit: 100,
            height: 650,
            showDelete: 'question',
            //edit datos personales
            userData: [],
            name: null,
            lastname: null,
            country: null,
            phone: null,
            date: null,
            url: null,
            description: null,
            //edit password
            password: null,
            newPassword: null,
            rNewPassword: null,
            msjErrorPass: '',
            msjErrorNewPass: '',
            passSuccess: false,
            msjBtn: 'Guardar',
            //deleted account
            passwordDelete: null,
            msjErrorConfirm: '',
            confirmSuccess: false,
            msjBtnDelete: 'Confirmar',
            //hidden publications
            visiblePublications: false,
            hiddens: [],
            showOptions: null,
            msjPubNull: '',
        }
    },
    methods:{
        truncatedText(text){
            if(text){
                return text.slice(0,25) + (text.length > 30 ? "...": "");
            }
        },
        // Envia las credenciales del id de la publicación a restaurar y el username logeado
        // Se elimina la publicación de la tabla de publicaciones ocultas
        // Al tener una respuesta 200, se quita la publicación del objeto de arrays de publicaciones ocultas que se visualizan
        restore(publicacion){
            let data = {
                id : publicacion.id,
                user : this.$store.state.user,
            }

            let options = {
                method:'DELETE',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify(data)
            }

            fetch('http://localhost:5000/publication/hidden/delete',options)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.');
                    }
                })
                .then(data=>{
                    for (let i = 0; i < this.hiddens.length; i++) {
                        if (this.hiddens[i].id === publicacion.id) {
                            // Encuentra el objeto que contiene el contenido
                            this.hiddens.splice(i, 1); // Elimina el objeto del array
                            break; // Sal del bucle una vez que se elimine el objeto
                        }
                    }
                })
                .catch(err=>{
                    console.error('Error: ',err)
                })

        },
        showOption(publicacion_id){
            if(!this.showOptions){
                this.showOptions = publicacion_id;
            } else {
                if(this.showOptions !== publicacion_id){
                    this.showOptions = publicacion_id;
                } else {
                    this.showOptions = null;
                }
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
        // Obtiene todas las publicaciones ocultas 
        // Las ordena según la fecha de creación
        showPublications(){
            this.visiblePublications = !this.visiblePublications;
            const user = this.$store.state.user;

            fetch(`http://localhost:5000/publication/hidden/${user}`)
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    } else if(res.stauts === 400){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud.')
                    }
                })
                .then(data=>{
                    if(data && data.message){
                        this.msjPubNull = data.message;
                    }else{
                        this.hiddens = data.sort((a,b)=>{
                            const dataA = a.fecha_creacion;
                            const dataB = b.fecha_creacion;
                            return dataB - dataA;
                        })
                        
                        this.hiddens.forEach(elem=>{
                            elem.img_perfil = 'data:image/jpeg;base64,' + elem.img_perfil;
                        })
                    } 
                })
                .catch(err=>{
                    console.error('Error: ',err)
                })
        },
        // Envia la password introducida por el usuario al servidor con una peticion delete
        // Checkea si la password coincide, si no lo es devuelve mensaje de error
        // Si coincide, elimina el usuario y todo lo relacionado 
        // Quita la autenticación llamando a la mutación y redirige al login
        confirmDelete(){
            this.msjErrorConfirm = '';
            if(this.passwordDelete){
                const user = this.$store.state.user;
                let data = {
                    password : this.passwordDelete,
                    user_id : this.$store.state.user_id
                }

                const options = {
                    method:'DELETE',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(data)
                }

                fetch(`http://localhost:5000/delete/${user}`, options)
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else if(res.status === 400) {
                            return res.json();
                        } else {
                            throw new Error('Error en la solicitud.');
                        }
                    })
                    .then(data=>{
                        if(data && data.error){
                            this.msjErrorConfirm = data.error;
                        } else {
                            this.confirmSuccess = true;
                            this.msjBtnDelete = 'Cuenta eliminada.';
                            setTimeout(()=>{
                                this.$store.dispatch('userLoggedOut');
                                this.$router.push({ name:'login' });
                            },3000)
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err)
                    })
            } else {
                this.msjErrorConfirm = 'Introduzca una contraseña valida.';
            }   
        },
        // Limpia los mensajes de error y obtiene el usuario logeado
        // Checkea si el campo de la actual password contiene caracteres sino muestra msj de error
        // Si la nueva contraseña y el repeat son iguales procede 
        // Checkea si la nueva pass tiene mas de 8 caracteres y al menos una mayuscula 
        // Si cumple todas las condiciones, envia las credenciales de la actual pass, la nueva y el user
        // Autentica la password actual, y procede a cambiar si esta bien sino devuelve msj de error 400
        // Al realizar el cambio de password, restablece los campos y aplica animación al btn con msj de success
        checkPass(){
            this.msjErrorNewPass='';
            this.msjErrorPass='';
            const user = this.$store.state.user;
            if(this.password){
                if(this.newPassword === this.rNewPassword){
                    if(this.rNewPassword.length > 8 && /[A-Z]/.test(this.rNewPassword)){
                        let data = {
                            password : this.password,
                            nueva_password : this.newPassword
                        }

                        const options = {
                            method:'PUT',
                            headers:{'Content-Type':'application/json'},
                            body: JSON.stringify(data)
                        }

                        fetch(`http://localhost:5000/password/${user}`, options)
                            .then(res =>{
                                if(res.ok){
                                    return res.json();
                                } else if(res.status === 400) {
                                    return res.json();
                                } else {
                                    throw new Error('Error en la solicitud.');
                                }
                            })
                            .then(data =>{
                                if(data && data.error){
                                    this.msjErrorPass = data.error;
                                } else {
                                    this.password = '';
                                    this.newPassword = '';
                                    this.rNewPassword = '';
                                    this.passSuccess = true;
                                    this.msjBtn = 'Contraseña actualizada!';
                                    setTimeout(() => {
                                        this.passSuccess = false;
                                        this.msjBtn = 'Guardar';
                                    }, 4000)
                                }
                            })
                            .catch(err =>{
                                console.error('Error: ',err);
                            })
                    } else {
                        this.msjErrorNewPass = 'La contraseña debe tener más de 8 carácteres y al menos una mayúscula.';
                    }
                } else {
                    this.msjErrorNewPass = 'Las contraseñas no coinciden.';
                }
            } else {
                this.msjErrorPass = 'Introduce la contraseña.';
            }
        },
        // Cambia el formato de la fecha de nacimiento obtenido de la db
        // Parsear la fecha obtenida 
        // Almacena el dia, mes y año por separado
        // Suma +1 al dia obtenido de la fecha por los indicies que maneja js, que incian desde 0 
        // Array de nombre de meses, pasarle el numero de mes obtenido de la fecha para que funcione como indice
        // Cambia el formato de la fecha y almacena el valor obtenido en el array userData
        changeDate(){
            const fecha = this.userData.fecha_nacimiento;
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

                this.userData.fecha_nacimiento = fechaFormateada;
            }
        },
        // Obtiene los datos personales del usuario 
        // Completa los campos con los datos obtenidos de usuario para que el usuario no los complete si no desea cambiar
        // Los almacena en userData []
        loadUserData(user){
            fetch(`http://localhost:5000/profile/${user}`)
                .then(res =>{
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud');
                    }
                })
                .then(data =>{
                    this.userData = data;
                    this.name = this.userData.nombre;
                    this.lastname = this.userData.apellido;
                    this.country = this.userData.pais;
                    this.phone = this.userData.telefono;
                    this.date = this.userData.fecha_nacimiento;
                    this.url = this.userData.url
                    this.description = this.userData.descripcion
                    this.changeDate();
                })
                .catch(err =>{
                    console.error('Error: ',err)
                })
        },
        // Guarda los nuevos datos en la db
        // Llama al metodo changeInfo() para aplicar estilos y muestra los datos personales actualizados
        save(){
            const user = this.$store.state.user;
            const url = `http://localhost:5000/profile/${user}`;
            const data = {
                nombre : this.name,
                apellido : this.lastname,
                pais : this.country,
                telefono : this.phone,
                fechaNac : this.date,
                url: this.url,
                description : this.description,
            }

            let options = {
                method:'PUT',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify(data)
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
                    this.userData=data;
                    this.changeInfo();
                    this.changeDate();
                })
                .catch(err =>{
                    console.error('Error: ',err)
                })
        },
        // Al clickear el boton 'Editar' aplica estilos
        // Desplaza el contenedor y cambia la altura
        changeEdit(){
            this.xOffsetWatch = -105;
            this.xOffsetEdit = -5;
            this.height = 800;
        },
        // Al clickear el boton 'Cancelar' aplica estilos
        // Desplaza el contenedor y cambia la altura
        changeInfo(){
            this.xOffsetWatch = 0;
            this.xOffsetEdit = 105;
            this.height = 650;
        },
        // Cambia el valor de this.show dependiendo el valor del parametro
        showed(elem){
            if(elem === 'data'){
                if(this.show !== 'data'){
                    this.show = 'data';
                } else {
                    this.show = null;
                }
            } else if (elem === 'info'){
                if(this.show !== 'info' ){
                    this.show = 'info';
                } else {
                    this.show = null;
                }
            } else {
                if(this.show !== 'delete'){
                    this.show = 'delete';
                } else {
                    this.show = null;
                }
            }
        }
    },
    mounted(){
        this.loadUserData(this.$store.state.user);
    },  
    components:{
        Nav
    }
}
</script>

<style scoped>
.box-config{
    width: 90%;
    margin: auto;
    border-radius: 3px;
    background-color: #0B666A;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    border-top: 1px solid #ffffff65;
    display: flex;
    padding: 1%;
    position: relative;
}
/* SECCIONES */
.section{
    width: 100%;
    color: #fff;
    display: flex;
    flex-direction: column;
    margin-right: 1%;
}
.section h2{
    letter-spacing: 1px;
    padding-bottom: 1%;
}
.section div{
    height: 100px;
    display: flex;
    align-items: center;
    padding: 0 2%;
    cursor: pointer;
    transition: .1s ease;
    position: relative;
}
.section div:hover{
    background-color: #156266;
    border-radius: 3px;
}
.section div::after{
    content: '';
    height: 10px;
    width: 10px;
    border-top: 3px solid #fff;
    border-right: 3px solid #fff;
    border-radius: 2px;
    position: absolute;
    right: 10%;
    transform: rotate(45deg);
}

.actived{
    background-color: #156266;
}
.actived::before{
    content: '';
    height: 100%;
    width: 2px;
    position: absolute;
    background-color: #97FEED;
    right: 0;
    border-radius: 3px;
}
.activedOptions{
    background-color: #156266;
}

/*OPCIONES DE CONFIG*/
.config{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 1%;
    
}
.your-account,
.change-password,
.delete-account,
.hidden-publications{
    padding: 1% 1% 1% 9%;
    position: relative;
    transition: .1s ease;
}
.your-account:hover,
.change-password:hover,
.delete-account:hover,
.hidden-publications:hover{
    background-color: #156266;
    border-radius: 3px;
    cursor: pointer;
}
.your-account::after,
.change-password::after,
.delete-account::after,
.hidden-publications::after{
    content: '';
    height: 10px;
    width: 10px;
    border-top: 3px solid #fff;
    border-right: 3px solid #fff;
    border-radius: 2px;
    position: absolute;
    top: 50%;
    right: 1%;
    transform: translateY(-50%) rotate(45deg);
}
.config div ion-icon{
    position: absolute;
    left: 1%;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.5em;
    color: rgb(140, 140, 140);
}
.config div h4{
    color: #fff;
    letter-spacing: 1px;
}
.config div p{
    color: rgb(140, 140, 140);
}

/* CONFIGURAR DATOS PERSONALES */
.data{
    overflow: hidden;
    position: relative;
    display: flex;
    transition: .1s ease;
    padding: 5%;
}
.personal-data{
    width: 100%;
    flex-direction: column;
}
.personal-data.info{
    transition: transform .1s ease;
    padding: 5%;
}
.personal-data.form{
    position: absolute;
    transition: transform .1s ease;
    padding: 5%;
}
.h-form{
    text-align: center;
}
.h-form h3{
    color: #fff;
    letter-spacing: 2px;
    font-size: 1.5em;
}
.h-form h4{
    color: #222831;
}
.container-form{
    width: 100%;
}
.container-input,
.box{
    display: flex;
    flex-direction: column;
    margin: 5% 0;
}
.container-input label,
.box label{
    font-weight: 600;
    letter-spacing: 1px;
    color: #fff;
}
.box span{
    font-size: 1.1em;
    padding: 0% 2%;
    color: rgb(140, 140, 140);
    font-weight: 500;
}
.container-input input,
.container-confirm input,
.container-input textarea{
    padding: 2% 3%;
    border: none;
    border-radius: 2px;
    outline: none;
    color: #222831;
    font-weight: 500;
    transition: .3s ease;
    resize: none;
}
.container-input input:focus,
.container-confirm input:focus{
    background-color: #35A29F;
    color: #fff;
}
.container-buttons,
.box.button{
    width: 100%;
    display: flex;
    justify-content: end;
    align-items: end;
}
.container-buttons button{
    margin-left: 3%;
}
.container-buttons button:first-child{
    background-color: #fff;
}


/* CAMBIAR PASSWORD */
.pass{
    padding: 5%;
}
.pass .container-input:first-child{
    margin-top: 0;
}
.pass .container-buttons .btn{
    background-color: #97FEED;
    transition: .3s ease;
}


/* ELIMINAR CUENTA */
.container-deleted{
    width: 100%;
    margin-top: 5%;
    color: #222831;
    display: flex;
    justify-content: space-around;
    align-items: center;    
}
.container-deleted .btn,
.container-confirm .btn{
    background: rgb(167, 65, 65);
    color: #fff;
}
.container-confirm{
    display: flex;
    flex-direction: column;
    margin-top: 5%;
}
.container-confirm p:first-child{
    color: #fff  !important;
}
.container-confirm input{
    margin: 3% 0;
}
.container-confirm .btn{
    align-self: end;
}

/* ESTILOS DE MSJ ERROR Y BTN SUCCES */
.msjError{
    font-weight: 600;
    color: rgb(196, 88, 88) !important;
    font-size: .9em;
}
.container-buttons .btn.success,
.container-confirm .btn.success{
    background: green !important;
    color: #fff !important;
    width: 100%;
    cursor: not-allowed;
}

/* PUBLICACIONES OCULTAS */
.config.two{
    justify-content: start;
}
.publication{
    margin-top: 10%;
}
.ups ion-icon{
    cursor: auto;
}
.ups ion-icon:hover{
    color: rgb(158, 158, 158);
}

@media (width < 768px){
    .section{
        width: 100%;
        margin-top: 5%;
    }
    .box-config{
        width: 100%;
        margin: 0;
    }
    .config{
        padding: 0;
        position: absolute;
        top: 100%;
    }
    .section h2{
        font-size: 1.7em;
    }
    .section h4{
        font-size: 1.4em;
    }
    .your-account,
    .change-password,
    .delete-account,
    .hidden-publications{
        font-size: 1.3em;
        margin: 15% 0;
    }
    .your-account p,
    .change-password p,
    .delete-account p,
    .hidden-publications p{
        padding: 2% 10%;
    }
    .your-account::after,
    .change-password::after,
    .delete-account::after,
    .hidden-publications::after{
        right: 5%;
    }

    .container-form .box{
        font-size: 1.2em;
    }

    .box.button .btn,
    .container-buttons .btn{
        font-size: 1.2em;
        margin-bottom: 5%;
    }
    .container-input label{
        font-size: 1.3em;
    }
    .container-input input{
        font-size: 1em;
    }
    .container-deleted{
        flex-direction: column;
    }
    .container-deleted h4{
        font-size: 1.3em;
    }
    .container-deleted .btn{
        font-size: 1.2em;
        padding: 2%;
        margin-top: 5%;
    }
    .container-confirm{
        font-size: 1.3em;
    }
    .container-confirm .btn{
        font-size: 1em;
        width: 60%;
        padding: 2% 5%;
    }

    .box-publications{
        margin-top: 60%;
    }
    .publication{
        width: 100%;
        font-size: 1.3em;
    }

    .delete{
        padding-bottom: 25%;
    }
}

@media (width > 768px) {
    .data{
        padding: 0;
        margin-bottom: 5%;
    }
    .section h2{
        font-size: 1.7em;
    }
    .section h4{
        font-size: 1.4em;
    }

    .your-account,
    .change-password,
    .delete-account,
    .hidden-publications{
        font-size: 1.3em;
    }
    .your-account p,
    .change-password p,
    .delete-account p,
    .hidden-publications p{
        padding: 2% 7%;
        font-size: 1.1em;
    }

    .container-form .box{
        font-size: 1.2em;
    }
    .box.button .btn,
    .container-buttons .btn{
        font-size: 1.2em;
        margin-bottom: 5%;
        width: 40%;
    }
    .container-input{
        margin: 0;
        margin-bottom: 3%;
    }
    .container-input label{
        font-size: 1.3em;
    }
    .container-input input,
    .container-input textarea{
        font-size: 1.3em;
    }
    .container-deleted h4{
        font-size: 1.3em;
    }
    .container-deleted{
        flex-direction: column;
    }
    .container-deleted .btn{
        width: 50%;
        font-size: 1.2em;
        padding: 2%;
        margin-top: 5%;
    }
    .container-confirm{
        font-size: 1.3em;
    }
    .container-confirm .btn{
        font-size: 1em;
        width: 60%;
        padding: 2% 5%;
    }
    .publication{
        width: 90%;
        font-size: 1.3em;
    }
}
</style>