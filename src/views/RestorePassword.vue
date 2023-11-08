<template>
    <div class="wrapper">
      <div class="container">
        <div class="container-correo">
          <div>
            <h2>Ingresa tu Correo Electrónico</h2>
          </div>
          <div>
            <input type="email" v-model="email" required @input="validarEmail" placeholder="ejemplo@gmail.com" @keyup.enter="isOkEmail">
            <div class="verification" v-if="messageError">{{ messageError }}</div>
          </div>
          <div class="container-btn">
            <button class="btn" type="button" @click="isOkEmail" :disabled="!isEmailValid" :class="{ success:msjBtn !== 'Continuar' }">{{msjBtn}}</button>
            <div class="loader" v-if="isLoading"></div>
          </div>
        </div>
      </div>
    </div>
    
</template>

<script>
export default {
    data() {
        return {
            email: '',
            isEmailValid: false,
            allUsers: [],
            messageError: '',
            msjBtn: 'Continuar',
            isLoading: false
        };
    },
    methods: {
        validarEmail() {
            const patronEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            this.isEmailValid = patronEmail.test(this.email);
        },
        isOkEmail(){
            this.isLoading = true;
            const url = 'http://127.0.0.1:5000/users'
            fetch(url)
                .then(res => {
                    if(res.ok){
                        return res.json();
                    } else {
                        throw new Error('Error en la solicitud');
                    }
                })
                .then(data => {
                    this.allUsers = data;
                    if(this.allUsers.some(elem => elem.email == this.email)){
                        this.sendEmail(this.email);
                    } else {
                        this.messageError = 'El correo electrónico ingresado es incorrecto o no está registrado.';
                    }
                })
                .catch(err => {
                    console.error('Error: ', err)
                })
        },
        sendEmail(email){
            const mail={
                email:email
            }
            let url = 'http://localhost:5000/restablecer-contrasena';
            var options = {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(mail)
            }
            fetch(url, options)
                .then(res => {
                if(res.ok){
                    this.isLoading = false;
                    this.msjBtn = 'Correo Enviado!';
                    return res.json();
                } else {
                    throw new Error('Error en la solicitud');
                }
                })
                .catch(err => {
                    console.error('Error: ', err);
                })
        }
    },
};
</script>

<style scoped>
.container-correo h2{
    color: #fff;
    font-size: 2em;
    margin-bottom: 10%;
    letter-spacing: 1px;
}
.container-correo{
    transition: transform .18s ease;
    transform: translateX(0);
    margin-top: 5%;
}
.container input{
    width: 100%;
    height: 100%;
    background: transparent;
    border: none;
    outline: none;
    font-size: 1em;
    color: #fff;
    font-weight: 600;
    padding: 5%;
    margin: 5% 0;
    border-bottom: 1px solid #97feed;
}

.btn{
    width: 40%;
}

.btn:disabled{
    background: gray;
    cursor: not-allowed;
}

.success{
    background-color: rgb(0, 255, 0);
    cursor: not-allowed;
}

.verification{
    color: red;
    padding: 5px;
    font-size: .7em;
    font-weight: 700;
}
.container-btn{
    position: relative;
}
.loader{
    width: 20px;
    height: 20px;
    border: 5px solid #0B666A;
    margin: 0;
    border-top: 5px solid #97feed;
    top: 18%;
    left: 45%; 
}

@media (width < 1023px) {
    .container input{
        font-size: 1.6em;
    }
    .btn{
        font-size: 1.3em;
        width: 50%;
    }
    .verification{
        font-size: 1.1em;
    }
    .loader{
        top: 30%;
        left: 55%;
    }
}

@media (width < 768px){
    .wrapper{
        margin: 0;
    }
    .container input{
        font-size: 1.4em;
    }
    .btn{
        font-size: 1.2em;
        width: 70%;
    }
    .loader{
        top: 45%;
        left: 75%;
    }
    .verification{
        font-size: .9em;
    }
}

@media (width < 585px) {
    .container{
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .container-correo{
        width: 90%;
    }
    .container-correo h2{
        text-align: center;
        padding: 2%;
    }
    .container input{
        font-size: 1.6em;
    }
    .btn{
        font-size: 1.5em;
    }
    .loader{
        top: 30%;
    }
}
</style>