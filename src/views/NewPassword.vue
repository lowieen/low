<template>
    <div class="wrapper">
        <div class="container">
            <div class="container-password">
                <h2>Restablecer Contraseña</h2>
                <form>
                  <div class="form-group">
                    <label for="password">Nueva Contraseña</label>
                    <input type="password" id="password" v-model="password" required>
                  </div>
                  <div class="form-group">
                    <label for="confirmPassword">Confirmar Contraseña</label>
                    <input type="password" id="confirmPassword" v-model="confirmPassword" required @input="validarPass">
                  </div>
                  <button type="button" class="btn" @click="resetPassword" :disabled="!isOk">Restablecer Contraseña</button>
                  <div class="verification">
                    <p v-if="messageError">{{ messageError }}</p>
                  </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            messageError: '',
            password: '',
            confirmPassword: '',
            isOk: false,
            token: '',
            checkResetToken: [],
        };
    },
    created() {
        // Cuando se carga el componente, obtén el token de la URL
        this.token = this.$route.params.token;
    },
    methods: {
    checkToken(){
        fetch('http://localhost:5000/users')
        .then(res => {
            if(res.ok){
                return res.json()
            } else {
                throw new Error ('Erro en la solucitud')
            }
        })
        .then(data =>{
            this.checkResetToken = data.filter(elem => elem.reset_token)
            if(this.checkResetToken.length == 0){ 
                alert('El Token para el cambio de contraseña ha expirado.')
                this.$router.push({ name: 'login' });
            }
        })
        .catch(err =>{
            console.error('Error: ',err)
        })
    },
    validarPass() {
        this.msjError = '';
        if(this.password){
            if(this.password.length <= 8 || !/[A-Z]/.test(this.password)){
                this.messageError = 'La contraseña debe tener más de 8 caracteres y mayúscula.';
                return
            }else{
                this.messageError = '';
            }

            if(this.password !== this.confirmPassword){
                this.messageError = 'Las contraseñas no coinicen.';
            }else{
                this.messageError = '';
                this.isOk = true;
            }
        }
    },
    resetPassword() {
        const newPassword = this.password;

        fetch(`http://localhost:5000/new-password/${this.token}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify({ password: newPassword }),
        })
        .then((response) => {
            if (response.ok) {
                this.token = '';
                this.$router.push({ name: 'login' });
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    },
    mounted(){
        this.checkToken();
    }
};
</script>

<style scoped>
.container-password{
    width: 50%;
    margin-top: 5%;
    transition: 0.2s ease;
}
.container-password h2{
    color: #fff;
    font-size: 2em;
    margin-bottom: 10%;
    letter-spacing: 1px;
    text-align: center;
}
.container-password label{
    font-size: 1em;
    color: rgb(180, 180, 180);
    font-weight: 500;
    pointer-events: none;
    transition: .5s;
    letter-spacing: 1px;
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
    width: 50%;
}

.btn:disabled{
    background: #27374d79;
    cursor: not-allowed;
}

.verification{
    color: rgb(167, 78, 78);
    padding: 5% 0;
    font-size: .9em;
    font-weight: 500;
}

@media (max-width: 1023px) {
    .wrapper{
        margin: 0;
    }
    .container-password{
        width: 90%;
    }
    .container input{
        font-size: 1.5em;
    }
    .container label{
        font-size: 1.5em;
    }
    .btn{
        font-size: 1.3em;
        width: 100%;
        padding: 2%;
    }
    .verification p{
        font-size: 1.5em;
    }
}

@media (max-width: 768px){
  .wrapper{
    height: 100vh;
  }
  .container{
    height: 100%;
    width: 95%;
  }
  .container-password{
    width: 90%;
  }
  .container input{
    font-size: 1.2em;
  }
  .btn{
    margin-top: 5%;
  }
  .verification p{
    font-size: 1.1em;
  }
}
@media (max-width: 450px){
  .wrapper{
    margin: 0;
  }
  .container input{
    font-size: 1.5em;
  }
  .container label{
    font-size: 1.5em;
  }
  .btn{
    font-size: 1.3em;
    width: 100%;
    padding: 2%;
  }
  .verification p{
    font-size: 1.1em;
  }
}
</style>