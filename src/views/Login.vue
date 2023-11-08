<template>
    <div class="wrapper">
        <div class="container-form">
            <div class="container login" :style="{left:valuePosition + '%'}">
                <div class="container-elem image">
                    <img src="../assets/img/icons/android-chrome-192x192.png" alt="logo">
                </div>
                <div class="container-elem">
                    <h3>Iniciar Sesión</h3>
                </div>
                <div class="container-elem inputs">
                    <label for="user">Email/User</label>
                    <input type="text" name="user" v-model="userLogin" :class="{isError:msjErrAutEmail}" @input="isNotNull('user')"> 
                    <p class="msjErr" v-if="msjErrAutEmail">{{ msjErrAutEmail }}</p>
                </div>
                <div class="container-elem inputs">
                    <label for="pass">Contraseña</label>
                    <input type="password" name="pass" v-model="passLogin" :class="{isError:msjErrAutPass}" @input="isNotNull" @keyup.enter="verificationLogin">
                    <p class="msjErr" v-if="msjErrAutPass">{{ msjErrAutPass }}</p>
                    <div class="container-elem changePass">
                        <router-link :to="{ name: 'restore-password' }">Olvide la contraseña</router-link>
                    </div>
                </div>
                <div class="container-elem">
                    <button type="button" class="btn" @click="verificationLogin">Iniciar Sesión</button>
                    <p class="msjErr" v-if="msjErrorAut">{{ msjErrorAut }}</p>
                </div>
                <div class="container-elem toRegister">
                    <p>No tenes una cuenta?</p><a @click="toRegister">Registrate!</a>
                </div>
            </div>


            <div class="container register" :style="{left:valuePosition + 100 + '%'}">
                <div class="container-elem image">
                    <img src="../assets/img/icons/android-chrome-192x192.png" alt="logo">
                </div>
                <div class="container-elem">
                    <h3>Registrarme</h3>
                </div>
                <div class="container-elem inputs">
                    <label for="user">Email</label>
                    <input type="email" name="user" v-model="emailRegister" @blur="validationEmail" :class="{isError:msjErrEmail}">
                    <p class="msjErr" v-if="msjErrEmail">{{ msjErrEmail }}</p>
                </div>
                <div class="container-elem inputs">
                    <label for="user">User</label>
                    <input type="text" name="user" v-model="userRegister" @blur="validationUser" :class="{isError:msjErrUser}">
                    <p class="msjErr" v-if="msjErrUser">{{ msjErrUser }}</p>
                </div>
                <div class="container-elem inputs">
                    <label for="pass">Contraseña</label>
                    <input type="password" name="pass" v-model="passRegister" @blur="validationPass" :class="{isError:msjErrPass}">
                    <p class="msjErr" v-if="msjErrPass">{{ msjErrPass }}</p>
                </div>
                <div class="container-elem inputs">
                    <label for="pass">Repita la contraseña</label>
                    <input type="password" name="pass" v-model="rPassRegister" @input="validationPass" :class="{isError:msjErrPass2}">
                    <p class="msjErr" v-if="msjErrPass2">{{ msjErrPass2 }}</p>
                </div>
                <div class="container-elem terms">
                    <input type="checkbox" name="terms" v-model="checkbox" id="terms"><label for="terms">Acepto todos los terminos y condiciones.</label>
                </div>
                <div class="container-elem">
                    <button type="button" class="btn" @click="register" :disabled="!validationRegister" :class="{success:registrationCompleted}">{{msjBtn}}</button>
                </div>
                <div class="container-elem toRegister">
                    <p>Ya tenes una cuenta?</p><a @click="toLogin">Inicia Sesión!</a>
                </div>
            </div>
            <div class="container-info" :style="{right:xOffset+'%', boxShadow: shadow}">
                <p>Una nueva forma de experimentar tu estado real en el infinito espacio virtual.</p>
                <p>Conócenos más.</p>
            </div>
            <div class="background" :style="{right:xOffset+'%'}">
                <div v-for="i in 100" :key="i" class="box" :class="{ animate: animatedBoxes.includes(i) }"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
        //animacion background
        animatedBoxes: [],
        //background
        xOffset: 0,
        shadow: '-20px 0 25px rgba(0, 0, 0, 0.5)',
        valuePosition: 0,
        //login
        userLogin: null,
        passLogin: null,
        //register
        emailRegister: null,
        userRegister: null,
        passRegister: null,
        rPassRegister: null,
        checkbox: false,
        //validacion register
        isValidEmail: null,
        isUser: [],
        isOkUser: false,
        isEmail: [],
        isOkEmail: false,
        msjErrEmail: '',
        msjErrUser: '',
        msjErrPass: '',
        msjErrPass2: '',
        registrationCompleted: false,
        msjBtn: 'Registrarme',
        //autentication login
        msjErrAutEmail: '',
        msjErrAutPass: '',
        msjErrorAut: '',
    };
  },
  methods: {
    // Muestra iniciar sesión
    // modifica los estilos del container-info y background
    toLogin(){
        this.xOffset = 0;
        this.shadow = '-20px 0 25px rgba(0, 0, 0, 0.5)';
        this.valuePosition += 100;
    },
    // Muestra registrarse
    // modifica los estilos del container-info y background
    toRegister(){
        this.xOffset = 50;
        this.shadow = '20px 0 25px rgba(0, 0, 0, 0.5)';
        this.valuePosition -= 100;
    },
    // Genera div's
    // rastrea las cajas animadas y se agrega la clase 'animate'
    // cada 2s se elimina la clase 'animate' para que la animacion pueda repetirse
    animateBox() {
      const num = Math.floor(Math.random() * 100) + 1; // Genera un número aleatorio entre 1 y 100
      if (!this.animatedBoxes.includes(num)) {
        this.animatedBoxes.push(num);
        setTimeout(() => {
          this.animatedBoxes = this.animatedBoxes.filter((boxNum) => boxNum !== num);
        }, 2000); // Quita la clase 'animate' después de 2 segundos
      }
    },
    validationEmail(){
        if(this.emailRegister){
            this.isOkEmail = true;
        }
    },
    validationUser(){
        if(this.userRegister){
            this.isOkUser = true;
        }
    },
    // Se comienza la validacion cuando el input tenga almenos un caracter
    // en el campo 'Contraseña' debe tener igual o mas de 8 caract y almenos un mayuscula
    // si no se cumple da mensaje de error, si se cumple se limpia el mensaje de error
    // verificar si los campos de pass y repetir pass sean iguales, sino con su respectivo mensaje
    validationPass(){
        if(this.passRegister){
            if(this.passRegister.length <= 8 || !/[A-Z]/.test(this.passRegister)){
                this.msjErrPass = 'La contraseña debe tener más de 8 caracteres y mayúscula.';
                return
            }else{
                this.msjErrPass = '';
            }

            if(this.passRegister !== this.rPassRegister){
                this.msjErrPass2 = 'Las contraseñas no coinicen.';
            }else{
                this.msjErrPass2 = '';
            }
        }
    },
    register(){
        // Validar email segun los caracteres ingresados para el registro
        // isValidEmail valdrá true o false
        // si es false muestra mensaje de error, aplica estilos al input
        // si es true realiza un fetch para verificar si el email ya esta registrado en la db
        if(this.emailRegister){
            const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            this.isValidEmail = emailRegex.test(this.emailRegister);

            if(!this.isValidEmail){
                this.msjErrEmail = 'Email ingresado incorrecto.';
            }else{
                this.msjErrEmail = '';

                fetch('http://localhost:5000/users')
                .then(res=>{
                        if(res.ok){
                            return res.json();
                        }else{
                            throw new Error ('Error en la solicitud');
                        }
                    })
                    .then(data=>{
                        this.isEmail = data.filter(elem => elem.email === this.emailRegister);
                        if(this.isEmail.length !== 0){
                            this.msjErrEmail = 'Este email ya existe.';
                            this.isOkEmail = false;
                            return
                        }else{
                            this.msjErrEmail = '';
                            this.isOkEmail = true;
                            this.isValidEmail = null;
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err);
                    })
                }
            } else {
                this.msjErrEmail = 'Completa el campo por favor.';
                this.isOkEmail = false;
                return
            }
        // Validar User del registro con fetch
        // filtrar el user en la db y almacenarlo en un array
        // si no encuentra el user, el array.length es 0, sino daría 1 y muestra mensaje de error
        // llama al method newUser() si no existe el user
        if(this.userRegister.includes(' ')) {
            this.msjErrUser = 'El usuario no puede contener espacios.'
            return
        } else {
            if(this.userRegister){
            fetch('http://localhost:5000/users')
                .then(res=>{
                    if(res.ok){
                        return res.json();
                    }else{
                        throw new Error ('Error en la solicitud');
                    }
                })
                .then(data=>{
                    this.isUser = data.filter(elem => elem.user === this.userRegister);
                    if(this.isUser.length !== 0){
                        this.msjErrUser = 'Este usuario ya existe.';
                        this.isOkUser = false;
                        return
                    }else{
                        this.msjErrUser = '';
                        this.isOkUser = true;
                        this.newUser();
                    }
                })
                .catch(err=>{
                    console.error('Error: ',err);
                })
            } else {
                this.msjErrUser = 'Completa el campo por favor.';
                this.isOkUser = false;
                return
            }
        }
    },
    // Agregar nuevo usuario a la db
    // si la respuesta es 200 muestra msj de registro exitoso
    // se restaura los campos del registro 
    newUser(){
        const user = {
            email : this.emailRegister,
            user : this.userRegister,
            pass : this.passRegister
        }

        const url = 'http://localhost:5000/users';

        const options = {
            headers: {'Content-Type':'application/json'},
            method: 'POST',
            body: JSON.stringify(user)
        }

        if(this.isOkEmail && this.isOkUser){
            fetch(url,options)
                .then(res=>{
                    if(res.ok){
                        this.registrationCompleted = true;
                        this.msjBtn = 'Registro Completado!';
                        // Llamada al method para crear perfil con el email registrado
                        this.createProfile(this.emailRegister)
                        // Restablecer los campos del registro desp de 2s
                        setTimeout(() => {
                            this.emailRegister = '';
                            this.userRegister = '';
                            this.passRegister = '';
                            this.rPassRegister = '';
                            this.checkbox = false;
                            this.msjBtn = 'Registrarme';
                            this.registrationCompleted = false;
                            this.toLogin();
                        }, 1000)
                        return res.json()
                    }
                    else{
                        throw new Error ('Error en la solicitud')
                    }
                })
                .catch(err=>{
                    console.error('Error: ', err)
                })
        }
    },
    // Verifica si los campos estan vacios, si lo están muestra msj de error
    // Se checkea si se ingresó un email o un user, si es un email se obtiene su user por medio de un filter
    // Se manda las crendenciales del usuario autenticado con su user y password. Llama al metodo login()
    verificationLogin(){
        if(!this.userLogin){
            this.msjErrAutEmail = 'Introduce tu Email o User, por favor.';
        }
        else if(!this.passLogin){
            this.msjErrAutPass = 'Introduce la contraseña, por favor.';
        }
        else{
            const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            this.isValidEmail = emailRegex.test(this.userLogin);

            let credentials = null;
            let emailUser = null;

            if(this.isValidEmail){
                fetch('http://localhost:5000/users')
                    .then(res=>{
                        if(res.ok){
                            return res.json();
                        } else {
                            return res.json();
                        }
                    })
                    .then(data=>{
                        if(data && data.error){
                            this.msjErrAutEmail = 'Email o Usuario incorrecto.';
                        } else {
                            const usuario = data.filter(elem => elem.email == this.userLogin);
                            emailUser = usuario[0].user;
                            credentials = {email : null, user : emailUser, password : this.passLogin};
                            this.login(credentials);
                        }
                    })
            } else {
                credentials = {email : null, user : this.userLogin, password : this.passLogin};
                this.login(credentials);
            }
        }
    },
    // Recbie como parametro las credenciales del usuario y realiza una peticion 
    // Se autentica el user y da permiso de ingresar a las otras rutas 
    login(credentials){
        const url = 'http://localhost:5000/logs';
        const options = {
            headers:{'Content-Type':'application/json'},
            method:'POST',
            body:JSON.stringify(credentials)
        }

        fetch(url, options)
            .then((res)=>{
                if(res.ok){               
                    return res.json()
                }else if (res.status === 400) {
                    return res.json()
                }else{
                    throw new Error ('Error en la solicitud')
                }
            })
            .then((data)=>{
                if(data && data.error){
                    this.userLogin = '';
                    this.passLogin = '';
                    this.msjErrorAut = data.error;
                }else{
                    const states = {user:credentials.user, user_id:data.id};
                    this.$store.dispatch('userLogIn', states);
                    this.$router.push({ name: 'home' });
                    this.userLogin = '';
                    this.passLogin = '';
                }
            })
            .catch((err)=>{
                console.error('Error: ', err)
            })

    },
    // Restablece los mensaje de error y estilos aplicados al introducir texto en los campos
    isNotNull(user){
        if(user === 'user'){
            this.msjErrAutEmail = '';
        }
        else{
            this.msjErrAutPass = '';
        }
    },
    // Crear un perfil con el email ingresado en el registro y recibido como parametro
    // aplico un filter en el backend para saber el usuario el cual sera la url de su perfil
    createProfile(email){
        const url = 'http://localhost:5000/profiles';
        const options = {
            headers:{'Content-Type':'application/json'},
            method: 'POST',
            body: JSON.stringify({email:email})
        }

        fetch(url, options)
            .then(res=>{
                if(res.ok){
                    return res.json();
                } else if(res.status===400){
                    return res.json()
                } else {
                    throw new Error ('Erro en la solicitud.');
                }
            })
            .then(data=>{
                if(data && data.error){
                    console.log(data.error)
                }
            })
            .catch(err=>{
                console.error('Error: ', err);
            })
    }
  },
  mounted() {
    setInterval(this.animateBox, 50); // Llama a animateBox cada 0.05s
  },
  computed:{
    validationRegister(){
        return this.isOkEmail && this.isOkUser && this.passRegister !== '' && this.rPassRegister !== '' && this.rPassRegister == this.passRegister && this.checkbox;
    },
  },
};
</script>

<style scoped>
.wrapper{
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
}

.container-form{
    width: 55%;
    height: 60%;
    background: #0B666A;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.container{
    width: 50%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 1% 10%;
}


.container-elem{
    width: 100%;
    color: #fff;
}


.container-elem.image{
    height: 1%;
}

.container-elem img{
    height: 100px;
    width: 170px;
    filter: opacity(.7);
    transform: translateX(-70%);
}

.container-elem h3{
    font-size: 2em;
    text-align: center;
}


.container-elem.inputs{
    display: flex;
    flex-direction: column;
}
.container-elem.inputs input:focus{
    background-color: #97FEED;
    outline: none;
    border: none;
}
.container-elem.inputs input{
    height: 40px;
    padding: 2%;
    border: none;
    transition: .3s ease;
}


.container-elem.terms{
    display: flex;
    align-items: center;
    width: 100%;
}
.container-elem.terms input{
    border: none;
    margin-right: 3%;
    accent-color: #97FEED;
    height: 15px;
    width: 15px;
    cursor: pointer;
}
.container-elem.terms label{
    font-size: .9em;
    cursor: pointer;
}


.container-elem.toRegister{
    display: flex;
}
.container-elem.toRegister a{
    margin-left: 2%;
    font-size: 1em;
    font-weight: 600;
    cursor: pointer;
}
.container-elem.toRegister p{
    font-size: 1em;

}


.container-elem.changePass{
    margin-top: 5%;
}
.container-elem.changePass a{
    cursor: pointer;
    font-size: .8em;
    letter-spacing: .5px;
    text-decoration: none;
    color: #fff;
    font-weight: 600;
    font-size: .9em;
}


.container-elem.toRegister a:hover,
.container-elem.changePass a:hover{
    text-decoration: underline;
}


.btn{
    width: 100%;
    padding: 3%;
    margin-bottom: 5%;
    letter-spacing: 2px;
    word-spacing: 5px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    background-color: #97FEED;
    transition: .3s ease;
}
.btn:hover{
    background: #35A29F;
    color: #fff;
}


.container-info{
    position: absolute;
    top: -5%;
    right: 0;
    background: transparent;
    background: linear-gradient(340deg, rgba(221,230,237,0) 0%, rgba(53,162,159,1) 70%);
    height: 110%;
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 5%;
    color: #fff;
    text-shadow: 0 2px 5px black;
    letter-spacing: 2px;
    line-height: 40px;
    z-index: 9;
    transition: .3s ease;
}

.background{
    position: absolute;
    width: 50%;
    height: 110%;
    right: 0;
    background: #35A29F;
    overflow: hidden;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    transition: .3s ease;
}
.background .box{
    position: relative;
    width: 40px;
    height: 40px;
    transition: .5s ease;
    transform: rotate(45deg);
}
.background .box:hover{
    background-color: #0B666A;
}
.animate{
    animation: animate 2s linear forwards
}
@keyframes animate{
    0%{background: transparent;}
    50%{background: #0B666A;}
    100%{background: transparent;}
}
.success{
    background-color: green;
    color: #fff;
    cursor: not-allowed;
}
.success:hover{
    background-color: green;
}
.msjErr{
    color: rgb(185, 71, 71);
    font-size: .9em;
    font-weight: 600;
}
.isError{
    background-color: rgb(189, 130, 130);
}

.btn:disabled{
    background: #60837d;
    cursor: not-allowed;
    color: #6b6b6b !important;
}


@media (max-width: 768px){
    .wrapper{
        margin: 0;
    }
    .container-elem.image{
        z-index: 99;
    }
    .container-elem img{
        transform: translate(-50%, -10%);
        height: 80px;
        width: 150px;
    }
    .container-form{
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    .container{
        width: 100%;
    }
    .container.login{
        position: absolute;
        left: 0;
        transition: .1s ease;
    }
    .container.register{
        position: absolute;
        left: 100%;
        transition: .1s ease;
    }
    .container-elem{
        background-color: #0B666A;
    }

    .container-info{
        display: none;
    }
    .background{
        display: none;
    }

    .container-elem h3{
        font-size: 2.5em;
    }
    .container-elem.inputs label{
        font-size: 1.7em;
    }
    .container-elem.inputs input{
        font-size: 1.5em;
    }
    .container-elem.changePass{
        font-size: 1.7em;
    }
    .container-elem .btn{
        font-size: 1.5em;
    }
    .container-elem.toRegister{
        font-size: 1.5em;
    }
    .container-elem.terms{
        font-size: 1.6em;
    }
    .container-elem.terms input{
        width: 25px;
        height: 25px;
    }
}

@media (min-width: 768px) and (max-width: 1023px) {
    .wrapper{
        margin: 0;
    }
    .container-elem img{
        width: 80px;
        height: 80px;
        transform: translate(-30%, -30%);
    }
    .container.register .container-elem img{
        display: none;
    }
    .container-form{
        width: 90%;
        height: 80%;
        overflow: hidden;
    }
    .container{
        width: 100%;
        padding: 1% 5%;
    }
    .container-elem{
        background-color: #0B666A;
    }
    .container-elem h3{
        font-size: 2.5em;
    }
    .container-elem.inputs label{
        font-size: 1.7em;
    }
    .container-elem.inputs input{
        font-size: 1.5em;
    }
    .container-elem.changePass{
        font-size: 1.7em;
    }
    .container-elem .btn{
        font-size: 1.5em;
    }
    .container-elem.toRegister{
        flex-direction: column;
        font-size: 1.5em;
    }
    .container-elem.terms{
        font-size: 1.4em;
    }
    .container-elem.terms input{
        width: 30px;
        height: 30px;
    }

    .container-info{
        font-size: 1.5em;
    }
}

@media (min-width: 1024px) {
    .container-form{
        width: 80%;
        height: 80%;
    }
    .container-elem.inputs{
        padding: 2% 0;
    }
    .container-elem.inputs input{
        height: 25px;
    }
}
</style>