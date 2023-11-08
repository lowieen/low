import { createStore } from 'vuex';

const store = createStore({
    state(){
        return{
            user: null,
            user_id: null,
            requiresAuth: false,
            img_perfil: null,
            img_portada: null,
            is_router: null,
        }
    },
    mutations: {
        setRouter(state, value){
            state.is_router = value;
        },
        setImgPerfil(state, imagenes){
            state.img_perfil = imagenes.img_perfil;
            state.img_portada = imagenes.img_portada;
        },
        setChatUser(state, user){
            state.chat_user = user;
        },
        nullChatUser(state){
            state.chat_user = null;
        },
        setUser(state, payload){
            state.user = payload.user;
            state.user_id = payload.user_id
            state.requiresAuth = true;
        },
        logout(state) {
            state.user = null;
            state.user_id = null;
            state.requiresAuth = false;
            state.chat_user = null;
            state.img_perfil = null;
            state.img_portada = null;
            state.is_router = null;
        },
    },
    actions: {
        imgPerfil({commit},imagenes){
            commit('setImgPerfil', imagenes);
        },
        cleanChatUser({commit}){
            commit('nullChatUser');
        },
        chatUser({commit},user){
            commit('setChatUser',user);
        },
        userLogIn({ commit }, payload) {
            commit('setUser', payload);
        },
        userLoggedOut({commit}){
            commit('logout');
        }
    },
    getters: {
        isAuthenticated: (state) => !!state.user,
    },
});
    
export default store;