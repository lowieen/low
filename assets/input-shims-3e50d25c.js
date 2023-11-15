import{f as O,g as k,a as F}from"./index8-27dbfa4a.js";import{B,C as P,z as H,s as U}from"./index-b58b0c5a.js";import{K as Y,a as $}from"./keyboard-d2582346.js";import{w as m}from"./index5-98865fd5.js";/*!
 * (C) Ionic http://ionicframework.com - MIT License
 */const A=new WeakMap,D=(e,o,t,s=0,n=!1)=>{A.has(e)!==t&&(t?z(e,o,s,n):G(e,o))},q=e=>e===e.getRootNode().activeElement,z=(e,o,t,s=!1)=>{const n=o.parentNode,i=o.cloneNode(!1);i.classList.add("cloned-input"),i.tabIndex=-1,s&&(i.disabled=!0),n.appendChild(i),A.set(e,i);const a=e.ownerDocument.dir==="rtl"?9999:-9999;e.style.pointerEvents="none",o.style.transform=`translate3d(${a}px,${t}px,0) scale(0)`},G=(e,o)=>{const t=A.get(e);t&&(A.delete(e),t.remove()),e.style.pointerEvents="",o.style.transform=""},N=50,W=(e,o,t)=>{if(!t||!o)return()=>{};const s=a=>{q(o)&&D(e,o,a)},n=()=>D(e,o,!1),i=()=>s(!0),c=()=>s(!1);return B(t,"ionScrollStart",i),B(t,"ionScrollEnd",c),o.addEventListener("blur",n),()=>{P(t,"ionScrollStart",i),P(t,"ionScrollEnd",c),o.removeEventListener("blur",n)}},I="input, textarea, [no-blur], [contenteditable]",j=()=>{let e=!0,o=!1;const t=document,s=()=>{o=!0},n=()=>{e=!0},i=c=>{if(o){o=!1;return}const a=t.activeElement;if(!a||a.matches(I))return;const f=c.target;f!==a&&(f.matches(I)||f.closest(I)||(e=!1,setTimeout(()=>{e||a.blur()},50)))};return B(t,"ionScrollStart",s),t.addEventListener("focusin",n,!0),t.addEventListener("touchend",i,!1),()=>{P(t,"ionScrollStart",s,!0),t.removeEventListener("focusin",n,!0),t.removeEventListener("touchend",i,!1)}},J=.3,Q=(e,o,t,s)=>{var n;const i=(n=e.closest("ion-item,[ion-item]"))!==null&&n!==void 0?n:e;return V(i.getBoundingClientRect(),o.getBoundingClientRect(),t,s)},V=(e,o,t,s)=>{const n=e.top,i=e.bottom,c=o.top,a=Math.min(o.bottom,s-t),f=c+15,v=a-N-i,d=f-n,l=Math.round(v<0?-v:d>0?-d:0),S=Math.min(l,n-c),T=Math.abs(S)/J,r=Math.min(400,Math.max(150,T));return{scrollAmount:S,scrollDuration:r,scrollPadding:t,inputSafeY:-(n-f)+4}},R="$ionPaddingTimer",M=(e,o,t)=>{const s=e[R];s&&clearTimeout(s),o>0?e.style.setProperty("--keyboard-offset",`${o}px`):e[R]=setTimeout(()=>{e.style.setProperty("--keyboard-offset","0px"),t&&t()},120)},p=(e,o,t)=>{const s=()=>{o&&M(o,0,t)};e.addEventListener("focusout",s,{once:!0})};let g=0;const K="data-ionic-skip-scroll-assist",X=(e,o,t,s,n,i,c,a=!1)=>{const f=i&&(c===void 0||c.mode===$.None);let u=!1;const v=m!==void 0?m.innerHeight:0,d=h=>{if(u===!1){u=!0;return}_(e,o,t,s,h.detail.keyboardHeight,f,a,v,!1)},l=()=>{u=!1,m===null||m===void 0||m.removeEventListener("ionKeyboardDidShow",d),e.removeEventListener("focusout",l,!0)},S=async()=>{if(o.hasAttribute(K)){o.removeAttribute(K);return}_(e,o,t,s,n,f,a,v),m===null||m===void 0||m.addEventListener("ionKeyboardDidShow",d),e.addEventListener("focusout",l,!0)};return e.addEventListener("focusin",S,!0),()=>{e.removeEventListener("focusin",S,!0),m===null||m===void 0||m.removeEventListener("ionKeyboardDidShow",d),e.removeEventListener("focusout",l,!0)}},C=e=>{document.activeElement!==e&&(e.setAttribute(K,"true"),e.focus())},_=async(e,o,t,s,n,i,c=!1,a=0,f=!0)=>{if(!t&&!s)return;const u=Q(e,t||s,n,a);if(t&&Math.abs(u.scrollAmount)<4){C(o),i&&t!==null&&(M(t,g),p(o,t,()=>g=0));return}if(D(e,o,!0,u.inputSafeY,c),C(o),U(()=>e.click()),i&&t&&(g=u.scrollPadding,M(t,g)),typeof window<"u"){let v;const d=async()=>{v!==void 0&&clearTimeout(v),window.removeEventListener("ionKeyboardDidShow",l),window.removeEventListener("ionKeyboardDidShow",d),t&&await F(t,0,u.scrollAmount,u.scrollDuration),D(e,o,!1,u.inputSafeY),C(o),i&&p(o,t,()=>g=0)},l=()=>{window.removeEventListener("ionKeyboardDidShow",l),window.addEventListener("ionKeyboardDidShow",d)};if(t){const S=await k(t),h=S.scrollHeight-S.clientHeight;if(f&&u.scrollAmount>h-S.scrollTop){o.type==="password"?(u.scrollAmount+=N,window.addEventListener("ionKeyboardDidShow",l)):window.addEventListener("ionKeyboardDidShow",d),v=setTimeout(d,1e3);return}}d()}},Z=!0,re=async(e,o)=>{const t=document,s=o==="ios",n=o==="android",i=e.getNumber("keyboardHeight",290),c=e.getBoolean("scrollAssist",!0),a=e.getBoolean("hideCaretOnScroll",s),f=e.getBoolean("inputBlurring",s),u=e.getBoolean("scrollPadding",!0),v=Array.from(t.querySelectorAll("ion-input, ion-textarea")),d=new WeakMap,l=new WeakMap,S=await Y.getResizeMode(),h=async r=>{await new Promise(b=>H(r,b));const y=r.shadowRoot||r,w=y.querySelector("input")||y.querySelector("textarea"),L=O(r),x=L?null:r.closest("ion-footer");if(!w)return;if(L&&a&&!d.has(r)){const b=W(r,w,L);d.set(r,b)}if(!(w.type==="date"||w.type==="datetime-local")&&(L||x)&&c&&!l.has(r)){const b=X(r,w,L,x,i,u,S,n);l.set(r,b)}},T=r=>{if(a){const y=d.get(r);y&&y(),d.delete(r)}if(c){const y=l.get(r);y&&y(),l.delete(r)}};f&&Z&&j();for(const r of v)h(r);t.addEventListener("ionInputDidLoad",r=>{h(r.detail)}),t.addEventListener("ionInputDidUnload",r=>{T(r.detail)})};export{re as startInputShims};
