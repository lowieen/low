import{m as P,l as L,j as U,n as E,o as j,d as C,q as S,e as I,N as O,_ as T}from"./android-chrome-B-192x192-4517b689.js";import{_ as D,r as v,o as c,c as a,a as o,b as p,w as F,l as k,f as d,t as u,n as _,F as w,e as y,p as M,g as N}from"./index-b58b0c5a.js";const A={props:["user"],data(){return{isLoading:!0,mailSharp:P,location:L,balloon:U,create:E,linkSharp:j,diamondOutline:C,createOutline:S,ellipsisHorizontalOutline:I,classActive:"active",onStyle:"publ",show:"",allPublications:[],publicationsWithImg:[],publicationsLike:[],idPublicationsLikes:[],isLiked:[],userLiked:[],infoUser:[],url:"",follows:[],followers:[],isFollowed:!1,userLogged:this.$store.state.user,userFollows:[],allFollows:[],btnEdit:!1,inputUrl:!1,imgPerfilUrl:this.$store.state.img_perfil,imgPortadaUrl:this.$store.state.img_portada,imgPerfilOtherUser:null,imgPortadaOtherUser:null}},methods:{filterImgPortada(e){const i=e.target.files[0],l=new FormData;l.append("image",i);const s=`http://localhost:5000/upload/img-portada/${this.userLogged}`;this.changeImg(l,s)},filterImgPerfil(e){const i=e.target.files[0],l=new FormData;l.append("image",i);const s=`http://localhost:5000/upload/img-profile/${this.userLogged}`;this.changeImg(l,s)},changeImg(e,i){fetch(i,{method:"PUT",body:e}).then(n=>{if(n.ok)return n.json();if(n.status===400)return n.json();throw new Error("Error en la solicitud.")}).then(n=>{n&&n.error?console.log(n.error):n.perfil?(this.imgPerfilUrl="data:image/jpeg;base64,"+n.perfil,this.$store.state.img_perfil=this.imgPerfilUrl):(this.imgPortadaUrl="data:image/jpeg;base64,"+n.portada,this.$store.state.img_portada=this.imgPortadaUrl)}).catch(n=>{console.error("Error: ",n)})},sendMsj(e){this.$router.push({name:"messages"}),this.$store.dispatch("chatUser",e)},follow(e){const i="http://localhost:5000/follow";let l={follower_user:this.userLogged,followed_user:e};if(this.isFollowed){let n={method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify(l)};fetch(i,n).then(s=>{if(s.ok)return s.json();if(s.status===400)return s.json();throw new Error("Error en la solicitud.")}).then(s=>{s&&s.error?console.log(s.error):(this.followers-=1,this.isFollowed=!1)}).catch(s=>{console.error("Error: ",s)})}else{let n={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(l)};fetch(i,n).then(s=>{if(s.ok)return s.json();if(s.status===400)return s.json();throw new Error("Error en la solicitud.")}).then(s=>{s&&s.error?s.error:(this.followers+=1,this.isFollowed=!0)}).catch(s=>{console.error("Error: ",s)})}},changeNameBtn(){return this.isFollowed?"Siguiendo":"Seguir"},truncatedText(e){if(e)return e.slice(0,30)+(e.length>30?"...":"")},goToProfile(e){this.$router.push({name:"user-profile",params:{user:e}}),this.toProfile(e),this.onStyle="publ"},toProfile(e){this.getPublications(),this.refresh_likes(),this.getPublicationsLikes(),this.getInfo(e)},changeDate(){const e=this.infoUser.fecha_nacimiento;if(e){const i=new Date(e),l=i.getDate()+1,n=i.getMonth(),s=i.getFullYear(),f=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][n],b=`${l} de ${f} de ${s}`;this.infoUser.fecha_nacimiento=b}},getInfo(e){const i=this.userLogged;let l=null;e===void 0?l=this.user:l=e,fetch(`http://localhost:5000/information/${l}/${i}`).then(n=>{if(n.ok)return n.json();throw new Error("Error en la solicitud.")}).then(n=>{this.infoUser=n.dataUser,this.imgPortadaOtherUser="data:image/jpeg;base64,"+this.infoUser.img_portada,this.imgPerfilOtherUser="data:image/jpeg;base64,"+this.infoUser.img_perfil,this.url=this.infoUser.url,this.follows=n.seguidos,this.followers=n.seguidores,n.seguimiento.some(r=>r.followed_user===l)&&(this.isFollowed=!0),this.changeDate(),this.getPublications(),this.refresh_likes(),this.getPublicationsLikes(),this.isLoading=!1}).catch(n=>{console.error("Error: ",n)})},deletePublication(e){const i=this.$store.state.user,l=e.id;if(e.user_id===i){const n={method:"DELETE"};fetch(`http://localhost:5000/publications/${l}/delete`,n).then(s=>{if(s.ok)return s.json();if(s.status===400)return s.json();throw new Error("Error en la solicitud.")}).then(s=>{s&&s.error?console.error(s.error):(this.getPublicationsLikes(),this.getPublications())}).catch(s=>{console.error("Error: ",s)})}else{let s={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:l,user:i})};fetch("http://localhost:5000/publications/hidden",s).then(r=>{if(r.ok)return r.json();throw new Error("Error en la solicitud")}).then(r=>{for(let f=0;f<this.userLiked.length;f++)if(this.userLiked[f].id===l){this.userLiked.splice(f,l);break}}).catch(r=>{console.error("Error: ",r)})}},getPublicationsLikes(){const e=this.user;fetch(`http://127.0.0.1:5000/publication/liked/${e}`).then(i=>{if(i.ok)return i.json();throw new Error("Error en la solicitud")}).then(i=>{this.userLiked=i.sort((l,n)=>{const s=new Date(l.fecha_creacion);return new Date(n.fecha_creacion)-s}),this.userLiked.forEach(l=>{l.img_perfil="data:image/jpeg;base64,"+l.img_perfil})}).catch(i=>{console.error("Error: ",i)})},likeUser(){this.publicationsLike.length>0&&(this.idPublicationsLikes=this.publicationsLike.map(e=>e.publication_id))},refresh_likes(){const i=`http://127.0.0.1:5000/publications/likes/${this.$store.state.user}`;fetch(i,{method:"GET",headers:{"Content-Type":"application/json"}}).then(n=>{if(n.ok)return n.json()}).then(n=>{n&&(this.publicationsLike=n,this.likeUser())})},giveLike(e){const i=this.user,l=`http://127.0.0.1:5000/publications/${e}/like`,n={user:i};if(this.isLiked.includes(e)||this.idPublicationsLikes.includes(e)){let s={method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)};fetch(l,s).then(r=>{if(r.ok)return r.json();throw new Error("Error en la solicitud.")}).then(r=>{r&&r.error?console.log(r.error):(this.RestarLike(e),this.isLiked=this.isLiked.filter(f=>f!==e),this.idPublicationsLikes=this.idPublicationsLikes.filter(f=>f!==e),this.getPublicationsLikes())}).catch(r=>{console.error("Error: ",r)})}else{let s={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)};fetch(l,s).then(r=>{if(r.ok)return r.json();throw new Error("Error en la solicitud.")}).then(r=>{r&&r.error?console.log(r.error):(this.SumarLike(e),this.isLiked.push(e),this.getPublicationsLikes())}).catch(r=>{console.error("Error: ",r)})}},RestarLike(e){this.userLiked.forEach(i=>{i.id==e&&i.likes>0&&(i.likes-=1)}),this.allPublications.forEach(i=>{i.id==e&&i.likes>0&&(i.likes-=1)})},SumarLike(e){this.userLiked.forEach(i=>{i.id==e&&(i.likes+=1)}),this.allPublications.forEach(i=>{i.id==e&&(i.likes+=1)})},calculateTimeAgo(e){const i=new Date,l=new Date(e),n=i-l,s=Math.floor(n/(1e3*60));return s<60?`${s} min`:s<1440?`${Math.floor(s/60)} h`:`${Math.floor(s/1440)} d`},showed(e){this.show?this.show!==e.id?this.show=e.id:this.show="":this.show=e.id},optionsMsj(e){const i=this.$store.state.user;return e.user_id===i?"Eliminar":"Ocultar"},visited(e){e==="publ"?this.onStyle=e:e==="fotos"?this.onStyle=e:this.onStyle=e},getPublications(){const e=this.user;fetch(`http://127.0.0.1:5000/publications/${e}`).then(i=>{if(i.ok)return i.json();throw new Error("Error en la solicitud.")}).then(i=>{this.allPublications=i.sort((l,n)=>{const s=new Date(l.fecha_creacion);return new Date(n.fecha_creacion)-s}),this.publicationsWithImg=this.allPublications.filter(l=>l.imagen!==null)}).catch(i=>{console.error("Error: ",i)})}},components:{Nav:O},mounted(){this.getPublications(),this.refresh_likes(),this.getPublicationsLikes(),this.getInfo()}},m=e=>(M("data-v-08da32b6"),e=e(),N(),e),B={class:"wrapper"},J={class:"container"},z={class:"logo"},x=m(()=>o("img",{src:T,alt:"imagen logo"},null,-1)),H={key:0,class:"loader"},V={key:1,class:"main"},W={class:"presentation"},G={class:"imgPresentation"},R={class:"banner"},q=["src"],Y=["src"],K={for:"img-portada"},Q={class:"imgPerfil"},X=["src"],Z=["src"],$={for:"img-perfil"},ss={class:"inf-presentation"},es={class:"names"},is={key:0},os={class:"description"},ts={class:"other"},rs={key:0,class:"link"},ns=["href"],ls={key:0,type:"url",name:"url",id:"url",class:"input-url"},cs={key:1,class:"date"},as={key:2,class:"country"},us={class:"follows"},hs={class:"followers"},ds={class:"followed"},fs={key:0,class:"send-msj"},gs={key:1,class:"btn-follow"},_s={class:"sections"},ps={class:"nav-sections"},ks=m(()=>o("p",null,"Publicaciones",-1)),ms=[ks],bs=m(()=>o("p",null,"Fotos",-1)),vs=[bs],ws=m(()=>o("p",null,"Me Gusta",-1)),ys=[ws],Ps={class:"data"},Ls={key:0,class:"dta principal"},Us={class:"options"},Es=["onClick"],js={class:"img-publ normal"},Cs=["src"],Ss=["src"],Is={class:"data-publ"},Os={key:0,class:"img-post"},Ts=["src"],Ds={class:"ups"},Fs={key:1,class:"dta pic"},Ms={class:"options"},Ns=["onClick"],As={class:"img-publ normal"},Bs=["src"],Js=["src"],zs={class:"data-publ"},xs={key:0,class:"img-post"},Hs=["src"],Vs={class:"ups"},Ws={key:2,class:"dta likes"},Gs={class:"options"},Rs=["onClick"],qs=["onClick"],Ys=["src"],Ks=["src"],Qs={class:"data-publ"},Xs={key:0,class:"img-post"},Zs=["src"],$s={class:"ups"};function se(e,i,l,n,s,r){const f=v("Nav"),b=v("router-link"),g=v("ion-icon");return c(),a("div",B,[o("div",J,[p(f,{onToProfile:r.toProfile},null,8,["onToProfile"]),o("div",z,[p(b,{to:{name:"home"}},{default:F(()=>[x]),_:1})]),s.isLoading?(c(),a("div",H)):(c(),a("main",V,[o("div",W,[o("div",G,[o("div",R,[s.infoUser.user===s.userLogged?(c(),a("img",{key:0,src:s.imgPortadaUrl,alt:"foto de banner"},null,8,q)):(c(),a("img",{key:1,src:s.imgPortadaOtherUser,alt:"foto de banner"},null,8,Y)),o("label",K,[s.infoUser.user===this.$store.state.user?(c(),k(g,{key:0,src:s.create,class:"editIcon-banner"},null,8,["src"])):d("",!0)]),o("input",{type:"file",name:"img-portada",id:"img-portada",style:{display:"none"},accept:"image/*",onChange:i[0]||(i[0]=(...t)=>r.filterImgPortada&&r.filterImgPortada(...t))},null,32)]),o("div",Q,[s.infoUser.user===s.userLogged?(c(),a("img",{key:0,src:s.imgPerfilUrl,alt:"foto de perfil"},null,8,X)):(c(),a("img",{key:1,src:s.imgPerfilOtherUser,alt:"foto de perfil"},null,8,Z)),o("label",$,[s.infoUser.user===this.$store.state.user?(c(),k(g,{key:0,src:s.create,class:"editIcon-perfil"},null,8,["src"])):d("",!0)]),o("input",{type:"file",name:"img-perfil",id:"img-perfil",style:{display:"none"},accept:"image/*",onChange:i[1]||(i[1]=(...t)=>r.filterImgPerfil&&r.filterImgPerfil(...t))},null,32)])]),o("div",ss,[o("div",es,[s.infoUser.nombre!=="-"?(c(),a("h2",is,u(s.infoUser.nombre)+" "+u(s.infoUser.apellido),1)):d("",!0),o("span",null,"@"+u(s.infoUser.user),1)]),o("div",os,[o("p",null,u(s.infoUser.descripcion),1)]),o("div",ts,[s.infoUser.url!==null?(c(),a("div",rs,[p(g,{src:s.linkSharp,class:"urlIcon"},null,8,["src"]),o("a",{href:s.url},u(r.truncatedText(s.infoUser.url)),9,ns),s.inputUrl?(c(),a("input",ls)):d("",!0)])):d("",!0),s.infoUser.fecha_nacimiento?(c(),a("div",cs,[p(g,{src:s.balloon},null,8,["src"]),o("span",null,"Fecha de nacimiento: "+u(s.infoUser.fecha_nacimiento),1)])):d("",!0),s.infoUser.pais!=="-"?(c(),a("div",as,[p(g,{src:s.location},null,8,["src"]),o("span",null,u(s.infoUser.pais),1)])):d("",!0)]),o("div",us,[o("div",hs,[o("span",null,u(s.followers)+" seguidores",1)]),o("div",ds,[o("span",null,u(s.follows)+" seguidos",1)]),s.infoUser.user!==s.userLogged?(c(),a("div",fs,[p(g,{src:s.mailSharp,onClick:i[2]||(i[2]=t=>r.sendMsj(s.infoUser.user))},null,8,["src"])])):d("",!0),s.infoUser.user!==s.userLogged?(c(),a("div",gs,[o("button",{class:_(["btn",{disabled:s.isFollowed}]),onClick:i[3]||(i[3]=t=>r.follow(s.infoUser.user))},u(r.changeNameBtn(s.infoUser.user)),3)])):d("",!0)])])]),o("div",_s,[o("div",ps,[o("div",{class:_(["principal-view",{show:s.onStyle==="publ"}]),onClick:i[4]||(i[4]=t=>r.visited("publ"))},ms,2),o("div",{class:_(["pictures",{show:s.onStyle==="fotos"}]),onClick:i[5]||(i[5]=t=>r.visited("fotos"))},vs,2),o("div",{class:_(["likes",{show:s.onStyle==="likes"}]),onClick:i[6]||(i[6]=t=>r.visited("likes"))},ys,2)])]),o("div",Ps,[s.onStyle==="publ"?(c(),a("div",Ls,[(c(!0),a(w,null,y(s.allPublications,t=>(c(),a("div",{class:"publication",key:t.id},[o("div",Us,[o("p",null,u(r.calculateTimeAgo(t.fecha_creacion)),1),this.allPublications.map(h=>h.user_id).includes(t.user_id)?(c(),k(g,{key:0,src:s.ellipsisHorizontalOutline,onClick:h=>r.showed(t)},null,8,["src","onClick"])):d("",!0),o("span",{class:_({visible:s.show===t.id}),onClick:h=>r.deletePublication(t)},u(r.optionsMsj(t)),11,Es)]),o("div",js,[t.user_id===s.userLogged?(c(),a("img",{key:0,src:s.imgPerfilUrl,alt:"imagen perfil"},null,8,Cs)):(c(),a("img",{key:1,src:"data:image/jpeg;base64,"+t.img_perfil,alt:"imagen perfil"},null,8,Ss)),o("div",Is,[o("h3",null,u(t.user_id),1),o("p",null,u(t.contenido),1)])]),t.imagen?(c(),a("div",Os,[o("img",{src:"data:image/jpeg;base64,"+t.imagen,alt:"Imagen"},null,8,Ts)])):d("",!0),o("div",Ds,[o("span",null,u(t.likes),1),p(g,{src:s.diamondOutline,class:_({liked:s.idPublicationsLikes.includes(t.id)||s.isLiked.includes(t.id)}),onClick:h=>r.giveLike(t.id)},null,8,["src","class","onClick"])])]))),128))])):s.onStyle==="fotos"?(c(),a("div",Fs,[(c(!0),a(w,null,y(s.publicationsWithImg,t=>(c(),a("div",{class:"publication",key:t.id},[o("div",Ms,[o("p",null,u(r.calculateTimeAgo(t.fecha_creacion)),1),this.allPublications.map(h=>h.user_id).includes(t.user_id)?(c(),k(g,{key:0,src:s.ellipsisHorizontalOutline,onClick:h=>r.showed(t)},null,8,["src","onClick"])):d("",!0),o("span",{class:_({visible:s.show===t.id}),onClick:h=>r.deletePublication(t)},u(r.optionsMsj(t)),11,Ns)]),o("div",As,[t.user_id===s.userLogged?(c(),a("img",{key:0,src:s.imgPerfilUrl,alt:"imagen perfil"},null,8,Bs)):(c(),a("img",{key:1,src:"data:image/jpeg;base64,"+t.img_perfil,alt:"imagen perfil"},null,8,Js)),o("div",zs,[o("h3",null,u(t.user_id),1),o("p",null,u(t.contenido),1)])]),t.imagen?(c(),a("div",xs,[o("img",{src:"data:image/jpeg;base64,"+t.imagen,alt:"Imagen"},null,8,Hs)])):d("",!0),o("div",Vs,[o("span",null,u(t.likes),1),p(g,{src:s.diamondOutline,class:_({liked:s.idPublicationsLikes.includes(t.id)||s.isLiked.includes(t.id)}),onClick:h=>r.giveLike(t.id)},null,8,["src","class","onClick"])])]))),128))])):(c(),a("div",Ws,[(c(!0),a(w,null,y(s.userLiked,t=>(c(),a("div",{class:"publication",key:t.id},[o("div",Gs,[o("p",null,u(r.calculateTimeAgo(t.fecha_creacion)),1),this.userLiked.map(h=>h.user_id).includes(t.user_id)?(c(),k(g,{key:0,src:s.ellipsisHorizontalOutline,onClick:h=>r.showed(t)},null,8,["src","onClick"])):d("",!0),o("span",{class:_({visible:s.show===t.id}),onClick:h=>r.deletePublication(t)},u(r.optionsMsj(t)),11,Rs)]),o("div",{class:"img-publ normal",onClick:h=>r.goToProfile(t.user_id)},[t.user_id===s.userLogged?(c(),a("img",{key:0,src:s.imgPerfilUrl,alt:"imagen perfil"},null,8,Ys)):(c(),a("img",{key:1,src:t.img_perfil,alt:"imagen perfil"},null,8,Ks)),o("div",Qs,[o("h3",null,u(t.user_id),1),o("p",null,u(t.contenido),1)])],8,qs),t.imagen?(c(),a("div",Xs,[o("img",{src:"data:image/jpeg;base64,"+t.imagen,alt:"Imagen"},null,8,Zs)])):d("",!0),o("div",$s,[o("span",null,u(t.likes),1),p(g,{src:s.diamondOutline,class:_({liked:s.idPublicationsLikes.includes(t.id)||s.isLiked.includes(t.id)}),onClick:h=>r.giveLike(t.id)},null,8,["src","class","onClick"])])]))),128))]))])]))])])}const oe=D(A,[["render",se],["__scopeId","data-v-08da32b6"]]);export{oe as default};
