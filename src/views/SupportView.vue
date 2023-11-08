<template>
    <div class="wrapper">
        <div class="container">
            <Nav></Nav>
            <main class="main">
                <div class="containerSections">
                    <div class="logo">
                        <router-link :to="{ name: 'home' }"><img src="../assets/img/icons/android-chrome-B-192x192.png" alt="imagen logo"></router-link>
                    </div>
                    <div class="h-support">
                        <h2>Soporte</h2>
                    </div>
                    <div class="box admin">
                        <div class="title">
                            <ion-icon :src="constructSharp"></ion-icon><span>Administrar tu cuenta</span>
                        </div>
                        <div class="section" @click="showInf(adminTitleA, adminA)">
                            <a href="#info"><span>Ayuda con las cuentas bloqueadas o limitadas</span></a>
                        </div>
                        <div class="section" @click="showInf(adminTitleB, adminB)">
                            <a href="#info"><span>Cómo agregar un número de teléfono a una cuenta</span></a>
                        </div>
                        <div class="section" @click="showInf(adminTitleC, adminC)">
                            <a href="#info"><span>Cómo actualizar la dirección de correo electrónico</span></a>
                        </div>
                    </div>

                    <div class="box security">
                        <div class="title">
                            <ion-icon :src="shieldCheckmarkSharp"></ion-icon><span>Seguridad y prevención</span>
                        </div>
                        <div class="section" @click="showInf(securityTitleA, securityA)">
                            <a href="#info"><span>Intercambio de información adicional con socios comerciales</span></a>
                        </div>
                    </div>

                    <div class="box rules">
                        <div class="title">
                            <ion-icon :src="readerSharp"></ion-icon><span>Reglas y políticas</span>
                        </div>
                        <div class="section" @click="showInf(rulesTitleA, rulesA)">
                            <a href="#info"><span>Cómo hacemos cumplir nuestras reglas</span></a>
                        </div>
                    </div>

                    <div class="box report">
                        <div class="title">
                            <ion-icon :src="alertCircleSharp"></ion-icon><span>Reportar problema</span>
                        </div>
                        <div class="section field">
                            <textarea name="description" cols="30" rows="4" v-model="msjReport"></textarea>
                            <p v-if="msjError" class="msjError">{{ msjError }}</p>
                            <button class="btn" @click="sendReport" :class="{success:isSuccess}">{{ msjBtn }}</button>
                        </div>
                    </div>
                </div>
                <div class="container-info" id="info">
                    <div class="title-info">
                        <h3>{{ title }}</h3>
                    </div>
                    <div class="data-info">
                        <p>{{ info }}</p>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import Nav from '../components/NavBar.vue'
import { shieldCheckmarkSharp, readerSharp, alertCircleSharp, constructSharp } from 'ionicons/icons'

export default{
    data(){
        return{
            //icons
            shieldCheckmarkSharp,
            readerSharp,
            alertCircleSharp,
            constructSharp,
            //info
            title: '',
            info: '',
            adminTitleA: 'Ayuda con las cuentas bloqueadas o limitadas',
            adminA: 'Si tu cuenta se bloquea o queda limitada a ciertas funciones, es posible que se haya vulnerado o que haya incumplido las Reglas o los Términos de servicio. Cuando sucede algo así, el primer paso es verificar que eres el propietario legítimo de la cuenta. Sigue leyendo para obtener información sobre cómo restaurar el acceso a la cuenta, o consulta nuestras preguntas frecuentes para saber más sobre las cuentas bloqueadas y limitadas. Con el fin de garantizar que sea lo más seguro posible, es posible que te enviemos un mensaje que lee Verifica tu cuenta.  Cuando veas este mensaje, deberás verificar que eres el propietario por teléfono, correo o recaptcha.',
            adminTitleB: 'Cómo agregar un número de teléfono a una cuenta',
            adminB: 'Agregar un número de teléfono a tu cuenta es una excelente manera de mejorar tu experiencia. Si estás pensando en agregar tu número, estos son algunos de los beneficios que obtendrás: Mantener tu cuenta segura. Al asociar un número de teléfono a tu cuenta, podrás activar funciones de seguridad como la verificación de inicio de sesión. Recuperar la cuenta más rápidamente Si alguna vez pierdes el acceso a tu cuenta, tener un número de teléfono asociado puede facilitar tu reingreso. Conectarte con amigos y contactos. Al asociar un número de teléfono a tu cuenta, puedes conectarte fácilmente con las personas que conoces. Obtén más información sobre cómo permitir que otras personas te busquen por tu número de teléfono.',
            adminTitleC: 'Cómo actualizar la dirección de correo electrónico',
            adminC: 'Tener una dirección de correo electrónico actualizada asociada a tu cuenta es una excelente manera de mejorar la seguridad de la cuenta. Nota: Cada vez que la dirección de correo electrónico asociada a tu cuenta se actualice, te enviaremos una notificación de correo electrónico a la dirección de correo electrónico anterior para informarte sobre este cambio. Para obtener más información sobre estos tipos de alertas, consulta nuestro artículo sobre seguridad de la cuenta. Además, seguiremos almacenando tus direcciones de correo electrónico utilizadas anteriormente y utilizaremos esta información para propósitos de seguridad. Puedes acceder a un historial completo de las direcciones de correo electrónico asociadas con tu cuenta si descargas tus datos mediante Tus datos.',
            securityTitleA: 'Intercambio de información adicional con socios comerciales',
            securityA: 'Cuando recibimos información sobre ti, la utilizamos para mejorar nuestros servicios, para personalizar tu experiencia y para otros propósitos que se describen en nuestra Política de privacidad. En algunos casos, esto implica compartir información personal que no es pública con nuestros socios. En el caso de las siguientes asociaciones, te proporcionamos un control adicional sobre la posibilidad de compartir los datos personales no públicos si te encuentras en las regiones que se especifican. Puedes ejercer este control mediante la configuración Permitir compartir información adicional con socios comerciales de la configuración de Personalización y datos. Es posible que los cambios que hagas en esta configuración no sean inmediatos.',
            rulesTitleA: 'Cómo hacemos cumplir nuestras reglas',
            rulesA: 'Reflejar conversaciones reales que suceden en el mundo y eso a veces incluye perspectivas que pueden ser ofensivas, controvertidas y/o intolerantes para los demás. Si bien invitamos a todos a expresarse en nuestro servicio, no toleraremos comportamientos que acosen, amenacen o utilicen el miedo para silenciar las voces de los demás.Contamos con las Reglas para ayudar a garantizar que todos se sientan seguros al expresar sus creencias y nos esforzamos por hacerlas cumplir con una coherencia uniforme. El propósito es servir a la conversación pública. La violencia, el acoso y otros tipos de comportamiento similares desalientan a las personas a expresarse y, en última instancia, disminuyen el valor de la conversación pública global. Nuestras reglas son para garantizar que todas las personas puedan participar en la conversación pública de forma libre y segura.',
            msjReport: '',
            msjError: '',
            msjBtn: 'Enviar',
            isSuccess: false,
        }
    },
    methods:{
        sendReport(){
            this.msjError = '';
            if(this.msjReport){
                let data = {
                    message : this.msjReport,
                    user : this.$store.state.user
                }

                const options = {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify(data)
                }

                fetch(`http://localhost:5000/report`,options)
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
                            this.msjError = data.error;
                        } else {
                            this.msjReport = '';
                            this.isSuccess = true;
                            this.msjBtn = 'Mensaje enviado exitosamente!';
                            setTimeout(()=>{
                                this.msjBtn = 'Enviar';
                                this.isSuccess = false;
                            }, 3000)
                        }
                    })
                    .catch(err=>{
                        console.error('Error: ',err)
                    })
            } else {
                this.msjError = 'Introduzca el problema a reportar.';
            }
        },
        // Muestra información dependiendo la sección clickeada
        showInf(title, content){
            this.title = title;
            this.info = content;
        }
    },
    components:{
        Nav,
    }
}

</script>

<style scoped>
.containerSections{
    width: 90%;
    margin: 5% auto 0;
    display: inline-block;
    columns: 2;
    column-gap: 50px;
}

.h-support{
    color: #fff;
    font-size: 3em;
    letter-spacing: 5px;
    width: 100%;
    border-bottom: 2px solid #fff;
    padding-bottom: 2%;
}

.box{
    width: 100%;
    margin-top: 50px;
    border-radius: 3px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.5);
    break-inside: avoid;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: #0B666A;
}
.title{
    color: #fff;
    font-size: 1.5em;
    letter-spacing: 1px;
    padding: 6% 5%;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #fff;
}
.title ion-icon{
    margin-right: 3%;
    font-size: 1.2em;
}
.section{
    padding: 5% 5%;
    cursor: pointer;
    transition: box-shadow .2s ease;
}
.section:hover:not(.section.field){
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
}
.section a{
    text-decoration: none;
    color: rgb(180, 180, 180);
}
.section.field{
    display: flex;
    flex-direction: column;
    cursor: auto;
}
.section.field textarea{
    resize: none;
    padding: 2%;
    color: #222831;
    border-radius: 2px;
    max-width: 100%;
}
.section.section.field textarea:focus{
    outline: none;
    border-radius: 2px;
}
.btn{
    align-self: end;
    margin-top: 5%;
    transition: .3s ease;
}


.container-info{
    width: 90%;
    margin: 10% auto;
    display: flex;
    flex-direction: column;
}
.title-info{
    width: 100%;
    letter-spacing: 1px;
    font-size: 1.2em;
    color: #fff;
}
.data-info{
    width: 100%;
    margin-top: 10%;
    color: rgb(158, 158, 158);
    word-spacing: 3px;
}

.msjError{
    font-weight: 600;
    color: rgb(196, 88, 88);
    font-size: .9em;
}

.btn.success{
    background: green;
    color: #fff;
    width: 100%;
    cursor: not-allowed;
}

@media (width < 1023px){
    .containerSections{
        column-gap: 10px;
    }
    .h-support h2{
        font-size: 1em;
    }

    .title{
        font-size: 1.4em;
    }
    .title ion-icon{
        font-size: 2em;
        margin-right: 7%;
    }
    .section{
        border: 1px solid #095256;
    }
    .section span{
        font-size: 1.2em;
    }
    .section.field textarea{
        font-size: 1.4em;
    }
    .section.field p{
        font-size: 1.3em;
    }
    .btn{
        font-size: 1.3em;
    }

    .title-info{
        font-size: 1.3em;
    }
    .data-info{
        font-size: 1.3em;
    }
}

@media (width < 455px) {
    .containerSections{
        columns: 1;
    }
    .h-support h2{
        font-size: .7em;
    }
    .title{
        font-size: 1.7em;
    }
    .section{
        border: 1px solid #095256;
    }
    .section span{
        font-size: 1.4em;
    }
    .section.field textarea{
        font-size: 1.4em;
    }
    .section.field p{
        font-size: 1.3em;
    }
    .btn{
        font-size: 1.3em;
    }

    .title-info{
        font-size: 1.4em;
    }

    .data-info{
        font-size: 1.5em;
    }
}
</style>
