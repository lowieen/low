import{d as k,a as b,e as w,N as P,_ as E}from"./android-chrome-B-192x192-4517b689.js";import{_ as v,r as g,o as c,c as h,a as r,b as u,w as y,d as L,v as C,n as m,F as j,e as T,t as d,f as O,p as U,g as D}from"./index-b58b0c5a.js";const S={data(){return{isLoading:!0,diamondOutline:k,attachOutline:b,ellipsisHorizontalOutline:w,content:null,imgPost:null,publications:[],publicationsLike:[],idPublicationsLikes:[],show:"",isLiked:[],imgUserLogged:this.$store.state.img_perfil,imgPerfilUrl:null,imgPortadaUrl:null}},components:{Nav:P},methods:{loadProfileImage(){const s=this.$store.state.user;fetch(`http://localhost:5000/profile-image/${s}`).then(t=>{if(t.ok)return t.json();if(t.status===400)return t.json();throw new Error("Error al obtener la imagen de perfil")}).then(t=>{t.img_perfil&&(this.imgPerfilUrl=`data:image/jpeg;base64, ${t.img_perfil}`),t.img_portada&&(this.imgPortadaUrl=`data:image/jpeg;base64, ${t.img_portada}`);const o={img_perfil:this.imgPerfilUrl,img_portada:this.imgPortadaUrl};this.$store.dispatch("imgPerfil",o),this.isLoading=!1}).catch(t=>{console.error(t)})},goToProfile(s){this.$router.push({name:"user-profile",params:{user:s}})},optionsMsj(s){const t=this.$store.state.user;return s.user_id===t?"Eliminar":"Ocultar"},options(s){const t=this.$store.state.user,o=s.id;if(s.user_id===t){const l={method:"DELETE"};fetch(`http://localhost:5000/publications/${o}/delete`,l).then(i=>{if(i.ok)return i.json();if(i.status===400)return i.json();throw new Error("Error en la solicitud.")}).then(i=>{if(i&&i.error)console.error(i.error);else for(let e=0;e<this.publications.length;e++)if(this.publications[e].id===s.id){this.publications.splice(e,1);break}}).catch(i=>{console.error("Error: ",i)})}else{let i={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:o,user:t})};fetch("http://localhost:5000/publications/hidden",i).then(e=>{if(e.ok)return e.json();throw new Error("Error en la solicitud")}).then(e=>{this.getPublications()}).catch(e=>{console.error("Error: ",e)})}},handleFileChange(s){const t=s.target.files[0],o=new FormData;o.append("image",t),this.imgPost=o},getUserUsername(){return this.$store.state.user},likeUser(){this.publicationsLike.length>0&&(this.idPublicationsLikes=this.publicationsLike.map(s=>s.publication_id))},giveLike(s){const t=this.$store.state.user,o=`http://127.0.0.1:5000/publications/${s}/like`,l={user:t};if(this.isLiked.includes(s)||this.idPublicationsLikes.includes(s)){let i={method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify(l)};fetch(o,i).then(e=>{if(e.ok)return e.json();throw new Error("Error en la solicitud.")}).then(e=>{e&&e.error?console.log(e.error):(this.publications.forEach(a=>{a.id==s&&a.likes>0&&(a.likes-=1)}),this.isLiked=this.isLiked.filter(a=>a!==s),this.idPublicationsLikes=this.idPublicationsLikes.filter(a=>a!==s))}).catch(e=>{console.error("Error: ",e)})}else{let i={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(l)};fetch(o,i).then(e=>{if(e.ok)return e.json();throw new Error("Error en la solicitud.")}).then(e=>{e&&e.error?console.log(e.error):(this.publications.forEach(a=>{a.id==s&&(a.likes+=1)}),this.isLiked.push(s))}).catch(e=>{console.error("Error: ",e)})}},refresh_likes(){const t=`http://127.0.0.1:5000/publications/likes/${this.$store.state.user}`;fetch(t,{method:"GET",headers:{"Content-Type":"application/json"}}).then(l=>{if(l.ok)return l.json()}).then(l=>{l&&(this.publicationsLike=l,this.likeUser())})},calculateTimeAgo(s){const t=new Date,o=new Date(s),l=t-o,i=Math.floor(l/(1e3*60));return i<60?`${i} min`:i<1440?`${Math.floor(i/60)} h`:`${Math.floor(i/1440)} d`},getPublications(){const s=this.$store.state.user;fetch(`http://127.0.0.1:5000/followed_publications/${s}`).then(t=>{if(t.ok)return t.json();throw new Error("Error en la solicitud.")}).then(t=>{this.publications=t.publicaciones.sort((o,l)=>{const i=new Date(o.fecha_creacion);return new Date(l.fecha_creacion)-i}),this.publications.forEach(o=>{o.img_perfil="data:image/jpeg;base64,"+o.img_perfil})}).catch(t=>{console.error("Error: ",t)})},newPost(){if(this.content){let s={};if(this.imgPost)this.imgPost.append("contenido",this.content),this.imgPost.append("usuario",this.$store.state.user),s={method:"POST",body:this.imgPost};else{const o={contenido:this.content,usuario:this.$store.state.user,imagen:null};s={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(o)}}fetch("http://127.0.0.1:5000/publications",s).then(o=>{if(o.ok)return o.json();throw new Error("Error en la solicitud")}).then(o=>{o&&o.error?console.error("Error: ",o.error):(this.content="",this.imgPost=null,this.getPublications())}).catch(o=>{console.error("Error: ",o)})}},showed(s){this.show?this.show!==s.id?this.show=s.id:this.show="":this.show=s.id}},mounted(){this.getPublications(),this.refresh_likes(),this.loadProfileImage()}},N=s=>(U("data-v-c61099bb"),s=s(),D(),s),I={class:"wrapper"},A={class:"container"},$={class:"logo"},x=N(()=>r("img",{src:E,alt:"imagen logo"},null,-1)),F={key:0,class:"loader"},M={key:1,class:"main"},V={class:"container-newPost"},B=["src"],H={class:"container-write"},J={for:"fileInput",class:"custom-file-upload"},z={class:"container-posts"},G={class:"options"},Q=["onClick"],q=["onClick"],K=["src"],R=["src"],W={class:"data-publ"},X={key:0,class:"img-post"},Y=["src"],Z={class:"ups"};function ee(s,t,o,l,i,e){const a=g("Nav"),_=g("router-link"),p=g("ion-icon");return c(),h("div",I,[r("div",A,[u(a),r("div",$,[u(_,{to:{name:"home"}},{default:y(()=>[x]),_:1})]),i.isLoading?(c(),h("div",F)):(c(),h("main",M,[r("div",V,[r("img",{src:i.imgPerfilUrl,alt:"imagen perfil"},null,8,B),r("div",H,[L(r("textarea",{name:"publicacion",rows:"1",cols:"50",placeholder:"¿Qué estás pensando?...","onUpdate:modelValue":t[0]||(t[0]=n=>i.content=n)},null,512),[[C,i.content]]),r("label",J,[u(p,{src:i.attachOutline,class:m({isUsed:i.imgPost})},null,8,["src","class"])]),r("input",{type:"file",name:"imagen",id:"fileInput",style:{display:"none"},accept:"image/*",onChange:t[1]||(t[1]=(...n)=>e.handleFileChange&&e.handleFileChange(...n))},null,32)]),r("button",{class:"btn",onClick:t[2]||(t[2]=(...n)=>e.newPost&&e.newPost(...n))},"Publicar")]),r("div",z,[(c(!0),h(j,null,T(i.publications,n=>(c(),h("div",{class:"publication",key:n.id},[r("div",G,[r("p",null,d(e.calculateTimeAgo(n.fecha_creacion)),1),u(p,{src:i.ellipsisHorizontalOutline,onClick:f=>e.showed(n)},null,8,["src","onClick"]),r("span",{class:m({visible:i.show==n.id}),onClick:f=>e.options(n)},d(e.optionsMsj(n)),11,Q)]),r("div",{class:"img-publ normal",onClick:f=>e.goToProfile(n.user_id)},[n.user_id===this.$store.state.user?(c(),h("img",{key:0,src:i.imgPerfilUrl,alt:"imagen perfil"},null,8,K)):(c(),h("img",{key:1,src:n.img_perfil,alt:"imagen perfil"},null,8,R)),r("div",W,[r("h3",null,d(n.user_id),1),r("p",null,d(n.contenido),1)])],8,q),n.imagen?(c(),h("div",X,[r("img",{src:"data:image/jpeg;base64,"+n.imagen,alt:"Imagen"},null,8,Y)])):O("",!0),r("div",Z,[r("span",null,d(n.likes),1),u(p,{src:i.diamondOutline,class:m({liked:i.idPublicationsLikes.includes(n.id)||i.isLiked.includes(n.id)}),onClick:f=>e.giveLike(n.id)},null,8,["src","class","onClick"])])]))),128))])]))])])}const ie=v(S,[["render",ee],["__scopeId","data-v-c61099bb"]]);export{ie as default};
