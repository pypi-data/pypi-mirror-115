import{a5 as t,d as e,N as i,a6 as o,h as n,a7 as s,f as a,I as r,l as d,p as l,_ as c,J as h,K as p,a8 as m,ax as u,q as f,e as g,T as v,ay as b,Z as y,az as _,aa as x,$ as w,af as T,ag as E,r as k,i as I,n as A,O as C,Y as O,o as R,M as S,X as z,E as F,aA as N,aB as B,aC as $,C as M,D as L,aD as D,aE as P,F as H,aF as U,a as j,m as G,aG as W,aH as K,aI as X,s as q,c as V}from"./main-adfe0fa2.js";import{r as Z,f as Y}from"./c.5c38779f.js";import{i as Q,I as J,s as tt}from"./c.6d9a9dbc.js";import{a as et,o as it}from"./c.58bec4f5.js";import{_ as ot,e as nt,R as st}from"./c.0b05eff9.js";import{P as at,h as rt,a as dt,d as lt,f as ct,I as ht,u as pt,g as mt}from"./c.097b259a.js";import"./c.b51cea2a.js";import{e as ut}from"./c.bfc48617.js";import"./c.c4e9c6f2.js";import"./c.afb2fde0.js";import"./c.78fa9899.js";import"./c.e2af0952.js";import"./c.100a4a91.js";function ft(t,e,i,o){var n,s=arguments.length,a=s<3?e:null===o?o=Object.getOwnPropertyDescriptor(e,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,i,o);else for(var r=t.length-1;r>=0;r--)(n=t[r])&&(a=(s<3?n(a):s>3?n(e,i,a):n(e,i))||a);return s>3&&a&&Object.defineProperty(e,i,a),a}class gt extends n{constructor(){super(...arguments),this.mini=!1,this.exited=!1,this.disabled=!1,this.extended=!1,this.showIconAtEnd=!1,this.reducedTouchTarget=!1,this.icon="",this.label="",this.shouldRenderRipple=!1,this.rippleHandlers=new s(()=>(this.shouldRenderRipple=!0,this.ripple))}render(){const t=this.mini&&!this.reducedTouchTarget,e={"mdc-fab--mini":this.mini,"mdc-fab--touch":t,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended,"icon-end":this.showIconAtEnd},i=this.label?this.label:this.icon;return a`<button
          class="mdc-fab ${r(e)}"
          ?disabled="${this.disabled}"
          aria-label="${i}"
          @mouseenter=${this.handleRippleMouseEnter}
          @mouseleave=${this.handleRippleMouseLeave}
          @focus=${this.handleRippleFocus}
          @blur=${this.handleRippleBlur}
          @mousedown=${this.handleRippleActivate}
          @touchstart=${this.handleRippleStartPress}
          @touchend=${this.handleRippleDeactivate}
          @touchcancel=${this.handleRippleDeactivate}><!--
        -->${this.renderBeforeRipple()}<!--
        -->${this.renderRipple()}<!--
        -->${this.showIconAtEnd?this.renderLabel():""}<!--
        --><span class="icon-slot-container"><!--
          --><slot name="icon">${this.renderIcon()}</slot><!--
        --></span><!--
        -->${this.showIconAtEnd?"":this.renderLabel()}<!--
        -->${this.renderTouchTarget()}<!--
      --></button>`}renderIcon(){return a`${this.icon?a`
          <span class="material-icons mdc-fab__icon">${this.icon}</span>`:""}`}renderTouchTarget(){const t=this.mini&&!this.reducedTouchTarget;return a`${t?a`<div class="mdc-fab__touch"></div>`:""}`}renderLabel(){const t=""!==this.label&&this.extended;return a`${t?a`<span class="mdc-fab__label">${this.label}</span>`:""}`}renderBeforeRipple(){return a``}renderRipple(){return this.shouldRenderRipple?a`<mwc-ripple class="ripple"></mwc-ripple>`:""}handleRippleActivate(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.handleRippleStartPress(t)}handleRippleStartPress(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}gt.shadowRootOptions={mode:"open",delegatesFocus:!0},ft([t("mwc-ripple")],gt.prototype,"ripple",void 0),ft([e({type:Boolean})],gt.prototype,"mini",void 0),ft([e({type:Boolean})],gt.prototype,"exited",void 0),ft([e({type:Boolean})],gt.prototype,"disabled",void 0),ft([e({type:Boolean})],gt.prototype,"extended",void 0),ft([e({type:Boolean})],gt.prototype,"showIconAtEnd",void 0),ft([e({type:Boolean})],gt.prototype,"reducedTouchTarget",void 0),ft([e()],gt.prototype,"icon",void 0),ft([e()],gt.prototype,"label",void 0),ft([i()],gt.prototype,"shouldRenderRipple",void 0),ft([o({passive:!0})],gt.prototype,"handleRippleStartPress",null);const vt=d`:host .mdc-fab .material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}:host{outline:none;--mdc-ripple-color: currentcolor;user-select:none;-webkit-tap-highlight-color:transparent;display:inline-flex}:host .mdc-touch-target-wrapper{display:inline}:host .mdc-elevation-overlay{position:absolute;border-radius:inherit;pointer-events:none;opacity:0;opacity:var(--mdc-elevation-overlay-opacity, 0);transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff;background-color:var(--mdc-elevation-overlay-color, #fff)}:host .mdc-fab{position:relative;display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1);background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2),0px 6px 10px 0px rgba(0, 0, 0, 0.14),0px 1px 18px 0px rgba(0,0,0,.12)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab.mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(.mdc-ripple-upgraded):focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab .mdc-fab__icon{width:24px;height:24px;font-size:24px}:host .mdc-fab,:host .mdc-fab:not(:disabled) .mdc-fab__icon,:host .mdc-fab:not(:disabled) .mdc-fab__label,:host .mdc-fab:disabled .mdc-fab__icon,:host .mdc-fab:disabled .mdc-fab__label{color:#fff;color:var(--mdc-theme-on-secondary, #fff)}:host .mdc-fab:not(.mdc-fab--extended){border-radius:50%}:host .mdc-fab:not(.mdc-fab--extended) .mdc-fab__ripple{border-radius:50%}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;right:0;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:"";pointer-events:none}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:0px;padding-right:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:0px;padding-left:max(0px, var(--mdc-fab-focus-outline-width, 0px));box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12))}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-color:initial;border-color:var(--mdc-fab-focus-outline-color, initial)}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:0px;padding-right:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:0px;padding-left:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab:hover,:host .mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}:host .mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12))}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab.mdc-fab--extended .ripple{border-radius:24px}:host .mdc-fab .icon-slot-container{display:inline-flex}:host .mdc-fab .mdc-fab__icon,:host .mdc-fab .icon-slot-container ::slotted([slot=icon]){width:24px;width:var(--mdc-icon-size, 24px);height:24px;height:var(--mdc-icon-size, 24px);font-size:24px;font-size:var(--mdc-icon-size, 24px);transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform;display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab.mdc-fab--extended{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:20px;padding-right:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:20px;padding-left:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px))}:host .mdc-fab.mdc-fab--extended:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab.mdc-fab--extended:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:20px;padding-right:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:20px;padding-left:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon]){margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}[dir=rtl] :host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon]),:host .mdc-fab.mdc-fab--extended .icon-slot-container ::slotted([slot=icon][dir=rtl]){margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}:host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon]){margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon]),:host .mdc-fab.mdc-fab--extended.icon-end .icon-slot-container ::slotted([slot=icon][dir=rtl]){margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}:host .mdc-fab.mdc-fab--exited .icon-slot-container ::slotted([slot=icon]){transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}`;let bt=class extends gt{};bt.styles=vt,bt=ft([l("mwc-fab")],bt),c([l("ha-fab")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(t){h(p(i.prototype),"firstUpdated",this).call(this,t),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),bt);const yt=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this["__"+String(e.key)]=t},get(){return this["__"+String(e.key)]},enumerable:!0,configurable:!0},finisher(i){const o=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(o.call(this),this[e.key]){const i=this.renderRoot.querySelector(t);if(!i)return;i.scrollTop=this[e.key]}}}});c([l("ha-tab")],(function(n,r){return{F:class extends r{constructor(...t){super(...t),n(this)}},d:[{kind:"field",decorators:[e({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[e({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[e()],key:"name",value:void 0},{kind:"field",decorators:[t("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[i()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${m(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?a`<slot name="icon"></slot>`:""}
        ${!this.narrow||this.active?a`<span class="name">${this.name}</span>`:""}
        ${this._shouldRenderRipple?a`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new s(()=>(this._shouldRenderRipple=!0,this._ripple))}},{kind:"method",key:"_handleKeyDown",value:function(t){13===t.keyCode&&t.target.click()}},{kind:"method",decorators:[o({passive:!0})],key:"handleRippleActivate",value:function(t){this._rippleHandlers.startPress(t)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }
    `}}]}}),n),c([l("hass-tabs-subpage")],(function(t,n){class s extends n{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[e({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[e({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[e()],key:"backCallback",value:void 0},{kind:"field",decorators:[e({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[e({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[e({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[e({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[e({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[e({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[i()],key:"_activeTab",value:void 0},{kind:"field",decorators:[yt(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return u((t,e,i,o,n,s,r)=>t.filter(t=>(!t.component||t.core||Q(this.hass,t.component))&&(!t.advancedOnly||i)).map(t=>a`
            <a href=${t.path}>
              <ha-tab
                .hass=${this.hass}
                .active=${t===e}
                .narrow=${this.narrow}
                .name=${t.translationKey?r(t.translationKey):t.name}
              >
                ${t.iconPath?a`<ha-svg-icon
                      slot="icon"
                      .path=${t.iconPath}
                    ></ha-svg-icon>`:a`<ha-icon slot="icon" .icon=${t.icon}></ha-icon>`}
              </ha-tab>
            </a>
          `))}},{kind:"method",key:"willUpdate",value:function(t){if(t.has("route")&&(this._activeTab=this.tabs.find(t=>`${this.route.prefix}${this.route.path}`.includes(t.path))),t.has("hass")){const e=t.get("hass");e&&e.language===this.hass.language||(this.rtl=et(this.hass))}h(p(s.prototype),"willUpdate",this).call(this,t)}},{kind:"method",key:"render",value:function(){var t,e;const i=this._getTabs(this.tabs,this._activeTab,null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),o=i.length>1||!this.narrow;return a`
      <div class="toolbar">
        ${this.mainPage||!this.backPath&&null!==(e=history.state)&&void 0!==e&&e.root?a`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?a`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:a`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?a`<div class="main-title"><slot name="header"></slot></div>`:""}
        ${o?a`
              <div id="tabbar" class=${r({"bottom-bar":this.narrow})}>
                ${i}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${r({tabs:o})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class="${r({tabs:o})}">
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[o({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }
      .bottom-bar a {
        width: 25%;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-around;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        max-height: var(--header-height);
        line-height: 20px;
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 2 * var(--header-height));
        height: calc(
          100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
        );
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),n),at({_template:rt`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[dt]});let _t=void 0;const xt={properties:{sizingTarget:{type:Object,value:function(){return this}},fitInto:{type:Object,value:window},noOverlap:{type:Boolean},positionTarget:{type:Element},horizontalAlign:{type:String},verticalAlign:{type:String},dynamicAlign:{type:Boolean},horizontalOffset:{type:Number,value:0,notify:!0},verticalOffset:{type:Number,value:0,notify:!0},autoFitOnAttach:{type:Boolean,value:!1},expandSizingTargetForScrollbars:{type:Boolean,value:!1},_fitInfo:{type:Object}},get _fitWidth(){return this.fitInto===window?this.fitInto.innerWidth:this.fitInto.getBoundingClientRect().width},get _fitHeight(){return this.fitInto===window?this.fitInto.innerHeight:this.fitInto.getBoundingClientRect().height},get _fitLeft(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().left},get _fitTop(){return this.fitInto===window?0:this.fitInto.getBoundingClientRect().top},get _defaultPositionTarget(){var t=lt(this).parentNode;return t&&t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&(t=t.host),t},get _localeHorizontalAlign(){if(this._isRTL){if("right"===this.horizontalAlign)return"left";if("left"===this.horizontalAlign)return"right"}return this.horizontalAlign},get __shouldPosition(){return(this.horizontalAlign||this.verticalAlign)&&this.positionTarget},get _isRTL(){return void 0===this._memoizedIsRTL&&(this._memoizedIsRTL="rtl"==window.getComputedStyle(this).direction),this._memoizedIsRTL},attached:function(){this.positionTarget=this.positionTarget||this._defaultPositionTarget,this.autoFitOnAttach&&("none"===window.getComputedStyle(this).display?setTimeout(function(){this.fit()}.bind(this)):(window.ShadyDOM&&ShadyDOM.flush(),this.fit()))},detached:function(){this.__deferredFit&&(clearTimeout(this.__deferredFit),this.__deferredFit=null)},fit:function(){this.position(),this.constrain(),this.center()},_discoverInfo:function(){if(!this._fitInfo){var t=window.getComputedStyle(this),e=window.getComputedStyle(this.sizingTarget);this._fitInfo={inlineStyle:{top:this.style.top||"",left:this.style.left||"",position:this.style.position||""},sizerInlineStyle:{maxWidth:this.sizingTarget.style.maxWidth||"",maxHeight:this.sizingTarget.style.maxHeight||"",boxSizing:this.sizingTarget.style.boxSizing||""},positionedBy:{vertically:"auto"!==t.top?"top":"auto"!==t.bottom?"bottom":null,horizontally:"auto"!==t.left?"left":"auto"!==t.right?"right":null},sizedBy:{height:"none"!==e.maxHeight,width:"none"!==e.maxWidth,minWidth:parseInt(e.minWidth,10)||0,minHeight:parseInt(e.minHeight,10)||0},margin:{top:parseInt(t.marginTop,10)||0,right:parseInt(t.marginRight,10)||0,bottom:parseInt(t.marginBottom,10)||0,left:parseInt(t.marginLeft,10)||0}}}},resetFit:function(){var t=this._fitInfo||{};for(var e in t.sizerInlineStyle)this.sizingTarget.style[e]=t.sizerInlineStyle[e];for(var e in t.inlineStyle)this.style[e]=t.inlineStyle[e];this._fitInfo=null},refit:function(){var t=this.sizingTarget.scrollLeft,e=this.sizingTarget.scrollTop;this.resetFit(),this.fit(),this.sizingTarget.scrollLeft=t,this.sizingTarget.scrollTop=e},position:function(){if(!this.__shouldPosition)return;this._discoverInfo(),window.ShadyDOM&&window.ShadyDOM.flush(),this.style.position="fixed",this.sizingTarget.style.boxSizing="border-box",this.style.left="0px",this.style.top="0px";var t=this.getBoundingClientRect(),e=this.__getNormalizedRect(this.positionTarget),i=this.__getNormalizedRect(this.fitInto);let o,n,s,a;this.expandSizingTargetForScrollbars&&(o=this.sizingTarget.offsetWidth,n=this.sizingTarget.offsetHeight,s=this.sizingTarget.clientWidth,a=this.sizingTarget.clientHeight);var r=this._fitInfo.margin,d={width:t.width+r.left+r.right,height:t.height+r.top+r.bottom},l=this.__getPosition(this._localeHorizontalAlign,this.verticalAlign,d,t,e,i),c=l.left+r.left,h=l.top+r.top,p=Math.min(i.right-r.right,c+t.width),m=Math.min(i.bottom-r.bottom,h+t.height);c=Math.max(i.left+r.left,Math.min(c,p-this._fitInfo.sizedBy.minWidth)),h=Math.max(i.top+r.top,Math.min(h,m-this._fitInfo.sizedBy.minHeight));const u=Math.max(p-c,this._fitInfo.sizedBy.minWidth),f=Math.max(m-h,this._fitInfo.sizedBy.minHeight);this.sizingTarget.style.maxWidth=u+"px",this.sizingTarget.style.maxHeight=f+"px";const g=c-t.left,v=h-t.top;if(this.style.left=g+"px",this.style.top=v+"px",this.expandSizingTargetForScrollbars){const t=this.sizingTarget.offsetHeight,e=t-this.sizingTarget.clientHeight-(n-a);if(e>0){const o=i.height-r.top-r.bottom,n=Math.min(o,f+e);this.sizingTarget.style.maxHeight=n+"px";const s=this.sizingTarget.offsetHeight,a=s-t;let d;"top"===l.verticalAlign?d=v:"middle"===l.verticalAlign?d=v-a/2:"bottom"===l.verticalAlign&&(d=v-a),d=Math.max(i.top+r.top,Math.min(d,i.bottom-r.bottom-s)),this.style.top=d+"px"}const d=this.sizingTarget.offsetWidth,c=d-this.sizingTarget.clientWidth-(o-s);if(c>0){const t=(()=>{if(void 0!==_t)return _t;const t=document.createElement("div");Object.assign(t.style,{overflow:"auto",position:"fixed",left:"0px",top:"0px",maxWidth:"100px",maxHeight:"100px"});const e=document.createElement("div");return e.style.width="200px",e.style.height="200px",t.appendChild(e),document.body.appendChild(t),_t=Math.abs(t.offsetWidth-100)>1?t.offsetWidth-t.clientWidth:0,document.body.removeChild(t),_t})(),e=i.width-r.left-r.right,o=Math.min(e,u+c-t);this.sizingTarget.style.maxWidth=o+"px";const n=this.sizingTarget.offsetWidth+t,s=n-d;let a;"left"===l.horizontalAlign?a=g:"center"===l.horizontalAlign?a=g-s/2:"right"===l.horizontalAlign&&(a=g-s),a=Math.max(i.left+r.left,Math.min(a,i.right-r.right-n)),this.style.left=a+"px"}}},constrain:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo;t.positionedBy.vertically||(this.style.position="fixed",this.style.top="0px"),t.positionedBy.horizontally||(this.style.position="fixed",this.style.left="0px"),this.sizingTarget.style.boxSizing="border-box";var e=this.getBoundingClientRect();t.sizedBy.height||this.__sizeDimension(e,t.positionedBy.vertically,"top","bottom","Height"),t.sizedBy.width||this.__sizeDimension(e,t.positionedBy.horizontally,"left","right","Width")}},_sizeDimension:function(t,e,i,o,n){this.__sizeDimension(t,e,i,o,n)},__sizeDimension:function(t,e,i,o,n){var s=this._fitInfo,a=this.__getNormalizedRect(this.fitInto),r="Width"===n?a.width:a.height,d=e===o,l=d?r-t[o]:t[i],c=s.margin[d?i:o],h="offset"+n,p=this[h]-this.sizingTarget[h];this.sizingTarget.style["max"+n]=r-c-l-p+"px"},center:function(){if(!this.__shouldPosition){this._discoverInfo();var t=this._fitInfo.positionedBy;if(!t.vertically||!t.horizontally){this.style.position="fixed",t.vertically||(this.style.top="0px"),t.horizontally||(this.style.left="0px");var e=this.getBoundingClientRect(),i=this.__getNormalizedRect(this.fitInto);if(!t.vertically){var o=i.top-e.top+(i.height-e.height)/2;this.style.top=o+"px"}if(!t.horizontally){var n=i.left-e.left+(i.width-e.width)/2;this.style.left=n+"px"}}}},__getNormalizedRect:function(t){return t===document.documentElement||t===window?{top:0,left:0,width:window.innerWidth,height:window.innerHeight,right:window.innerWidth,bottom:window.innerHeight}:t.getBoundingClientRect()},__getOffscreenArea:function(t,e,i){var o=Math.min(0,t.top)+Math.min(0,i.bottom-(t.top+e.height)),n=Math.min(0,t.left)+Math.min(0,i.right-(t.left+e.width));return Math.abs(o)*e.width+Math.abs(n)*e.height},__getPosition:function(t,e,i,o,n,s){var a,r=[{verticalAlign:"top",horizontalAlign:"left",top:n.top+this.verticalOffset,left:n.left+this.horizontalOffset},{verticalAlign:"top",horizontalAlign:"right",top:n.top+this.verticalOffset,left:n.right-i.width-this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"left",top:n.bottom-i.height-this.verticalOffset,left:n.left+this.horizontalOffset},{verticalAlign:"bottom",horizontalAlign:"right",top:n.bottom-i.height-this.verticalOffset,left:n.right-i.width-this.horizontalOffset}];if(this.noOverlap){for(var d=0,l=r.length;d<l;d++){var c={};for(var h in r[d])c[h]=r[d][h];r.push(c)}r[0].top=r[1].top+=n.height,r[2].top=r[3].top-=n.height,r[4].left=r[6].left+=n.width,r[5].left=r[7].left-=n.width}e="auto"===e?null:e,(t="auto"===t?null:t)&&"center"!==t||(r.push({verticalAlign:"top",horizontalAlign:"center",top:n.top+this.verticalOffset+(this.noOverlap?n.height:0),left:n.left-o.width/2+n.width/2+this.horizontalOffset}),r.push({verticalAlign:"bottom",horizontalAlign:"center",top:n.bottom-i.height-this.verticalOffset-(this.noOverlap?n.height:0),left:n.left-o.width/2+n.width/2+this.horizontalOffset})),e&&"middle"!==e||(r.push({verticalAlign:"middle",horizontalAlign:"left",top:n.top-o.height/2+n.height/2+this.verticalOffset,left:n.left+this.horizontalOffset+(this.noOverlap?n.width:0)}),r.push({verticalAlign:"middle",horizontalAlign:"right",top:n.top-o.height/2+n.height/2+this.verticalOffset,left:n.right-i.width-this.horizontalOffset-(this.noOverlap?n.width:0)})),"middle"===e&&"center"===t&&r.push({verticalAlign:"middle",horizontalAlign:"center",top:n.top-o.height/2+n.height/2+this.verticalOffset,left:n.left-o.width/2+n.width/2+this.horizontalOffset});for(d=0;d<r.length;d++){var p=r[d],m=p.verticalAlign===e,u=p.horizontalAlign===t;if(!this.dynamicAlign&&!this.noOverlap&&m&&u){a=p;break}var f=(!e||m)&&(!t||u);if(this.dynamicAlign||f){if(p.offscreenArea=this.__getOffscreenArea(p,i,s),0===p.offscreenArea&&f){a=p;break}a=a||p;var g=p.offscreenArea-a.offscreenArea;(g<0||0===g&&(m||u))&&(a=p)}}return a}};var wt=Element.prototype,Tt=wt.matches||wt.matchesSelector||wt.mozMatchesSelector||wt.msMatchesSelector||wt.oMatchesSelector||wt.webkitMatchesSelector;const Et=new class{getTabbableNodes(t){var e=[];return this._collectTabbableNodes(t,e)?this._sortByTabIndex(e):e}isFocusable(t){return Tt.call(t,"input, select, textarea, button, object")?Tt.call(t,":not([disabled])"):Tt.call(t,"a[href], area[href], iframe, [tabindex], [contentEditable]")}isTabbable(t){return this.isFocusable(t)&&Tt.call(t,':not([tabindex="-1"])')&&this._isVisible(t)}_normalizedTabIndex(t){if(this.isFocusable(t)){var e=t.getAttribute("tabindex")||0;return Number(e)}return-1}_collectTabbableNodes(t,e){if(t.nodeType!==Node.ELEMENT_NODE)return!1;var i=t;if(!this._isVisible(i))return!1;var o,n=this._normalizedTabIndex(i),s=n>0;n>=0&&e.push(i),o="content"===i.localName||"slot"===i.localName?lt(i).getDistributedNodes():lt(i.root||i).children;for(var a=0;a<o.length;a++)s=this._collectTabbableNodes(o[a],e)||s;return s}_isVisible(t){var e=t.style;return"hidden"!==e.visibility&&"none"!==e.display&&("hidden"!==(e=window.getComputedStyle(t)).visibility&&"none"!==e.display)}_sortByTabIndex(t){var e=t.length;if(e<2)return t;var i=Math.ceil(e/2),o=this._sortByTabIndex(t.slice(0,i)),n=this._sortByTabIndex(t.slice(i));return this._mergeSortByTabIndex(o,n)}_mergeSortByTabIndex(t,e){for(var i=[];t.length>0&&e.length>0;)this._hasLowerTabOrder(t[0],e[0])?i.push(e.shift()):i.push(t.shift());return i.concat(t,e)}_hasLowerTabOrder(t,e){var i=Math.max(t.tabIndex,0),o=Math.max(e.tabIndex,0);return 0===i||0===o?o>i:i>o}};at({_template:rt`
    <style>
      :host {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: var(--iron-overlay-backdrop-background-color, #000);
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
        @apply --iron-overlay-backdrop;
      }

      :host(.opened) {
        opacity: var(--iron-overlay-backdrop-opacity, 0.6);
        pointer-events: auto;
        @apply --iron-overlay-backdrop-opened;
      }
    </style>

    <slot></slot>
`,is:"iron-overlay-backdrop",properties:{opened:{reflectToAttribute:!0,type:Boolean,value:!1,observer:"_openedChanged"}},listeners:{transitionend:"_onTransitionend"},created:function(){this.__openedRaf=null},attached:function(){this.opened&&this._openedChanged(this.opened)},prepare:function(){this.opened&&!this.parentNode&&lt(document.body).appendChild(this)},open:function(){this.opened=!0},close:function(){this.opened=!1},complete:function(){this.opened||this.parentNode!==document.body||lt(this.parentNode).removeChild(this)},_onTransitionend:function(t){t&&t.target===this&&this.complete()},_openedChanged:function(t){if(t)this.prepare();else{var e=window.getComputedStyle(this);"0s"!==e.transitionDuration&&0!=e.opacity||this.complete()}this.isAttached&&(this.__openedRaf&&(window.cancelAnimationFrame(this.__openedRaf),this.__openedRaf=null),this.scrollTop=this.scrollTop,this.__openedRaf=window.requestAnimationFrame(function(){this.__openedRaf=null,this.toggleClass("opened",this.opened)}.bind(this)))}});const kt=new class{constructor(){this._overlays=[],this._minimumZ=101,this._backdropElement=null,ct(document.documentElement,"tap",(function(){})),document.addEventListener("tap",this._onCaptureClick.bind(this),!0),document.addEventListener("focus",this._onCaptureFocus.bind(this),!0),document.addEventListener("keydown",this._onCaptureKeyDown.bind(this),!0)}get backdropElement(){return this._backdropElement||(this._backdropElement=document.createElement("iron-overlay-backdrop")),this._backdropElement}get deepActiveElement(){var t=document.activeElement;for(t&&t instanceof Element!=!1||(t=document.body);t.root&&lt(t.root).activeElement;)t=lt(t.root).activeElement;return t}_bringOverlayAtIndexToFront(t){var e=this._overlays[t];if(e){var i=this._overlays.length-1,o=this._overlays[i];if(o&&this._shouldBeBehindOverlay(e,o)&&i--,!(t>=i)){var n=Math.max(this.currentOverlayZ(),this._minimumZ);for(this._getZ(e)<=n&&this._applyOverlayZ(e,n);t<i;)this._overlays[t]=this._overlays[t+1],t++;this._overlays[i]=e}}}addOrRemoveOverlay(t){t.opened?this.addOverlay(t):this.removeOverlay(t)}addOverlay(t){var e=this._overlays.indexOf(t);if(e>=0)return this._bringOverlayAtIndexToFront(e),void this.trackBackdrop();var i=this._overlays.length,o=this._overlays[i-1],n=Math.max(this._getZ(o),this._minimumZ),s=this._getZ(t);if(o&&this._shouldBeBehindOverlay(t,o)){this._applyOverlayZ(o,n),i--;var a=this._overlays[i-1];n=Math.max(this._getZ(a),this._minimumZ)}s<=n&&this._applyOverlayZ(t,n),this._overlays.splice(i,0,t),this.trackBackdrop()}removeOverlay(t){var e=this._overlays.indexOf(t);-1!==e&&(this._overlays.splice(e,1),this.trackBackdrop())}currentOverlay(){var t=this._overlays.length-1;return this._overlays[t]}currentOverlayZ(){return this._getZ(this.currentOverlay())}ensureMinimumZ(t){this._minimumZ=Math.max(this._minimumZ,t)}focusOverlay(){var t=this.currentOverlay();t&&t._applyFocus()}trackBackdrop(){var t=this._overlayWithBackdrop();(t||this._backdropElement)&&(this.backdropElement.style.zIndex=this._getZ(t)-1,this.backdropElement.opened=!!t,this.backdropElement.prepare())}getBackdrops(){for(var t=[],e=0;e<this._overlays.length;e++)this._overlays[e].withBackdrop&&t.push(this._overlays[e]);return t}backdropZ(){return this._getZ(this._overlayWithBackdrop())-1}_overlayWithBackdrop(){for(var t=this._overlays.length-1;t>=0;t--)if(this._overlays[t].withBackdrop)return this._overlays[t]}_getZ(t){var e=this._minimumZ;if(t){var i=Number(t.style.zIndex||window.getComputedStyle(t).zIndex);i==i&&(e=i)}return e}_setZ(t,e){t.style.zIndex=e}_applyOverlayZ(t,e){this._setZ(t,e+2)}_overlayInPath(t){t=t||[];for(var e=0;e<t.length;e++)if(t[e]._manager===this)return t[e]}_onCaptureClick(t){var e=this._overlays.length-1;if(-1!==e)for(var i,o=lt(t).path;(i=this._overlays[e])&&this._overlayInPath(o)!==i&&(i._onCaptureClick(t),i.allowClickThrough);)e--}_onCaptureFocus(t){var e=this.currentOverlay();e&&e._onCaptureFocus(t)}_onCaptureKeyDown(t){var e=this.currentOverlay();e&&(ht.keyboardEventMatchesKeys(t,"esc")?e._onCaptureEsc(t):ht.keyboardEventMatchesKeys(t,"tab")&&e._onCaptureTab(t))}_shouldBeBehindOverlay(t,e){return!t.alwaysOnTop&&e.alwaysOnTop}};var It,At,Ct={pageX:0,pageY:0},Ot=null,Rt=[],St=["wheel","mousewheel","DOMMouseScroll","touchstart","touchmove"];function zt(t){Nt.indexOf(t)>=0||(0===Nt.length&&function(){It=It||Bt.bind(void 0);for(var t=0,e=St.length;t<e;t++)document.addEventListener(St[t],It,{capture:!0,passive:!1})}(),Nt.push(t),At=Nt[Nt.length-1])}function Ft(t){var e=Nt.indexOf(t);-1!==e&&(Nt.splice(e,1),At=Nt[Nt.length-1],0===Nt.length&&function(){for(var t=0,e=St.length;t<e;t++)document.removeEventListener(St[t],It,{capture:!0,passive:!1})}())}const Nt=[];function Bt(t){if(t.cancelable&&function(t){var e=lt(t).rootTarget;"touchmove"!==t.type&&Ot!==e&&(Ot=e,Rt=function(t){for(var e=[],i=t.indexOf(At),o=0;o<=i;o++)if(t[o].nodeType===Node.ELEMENT_NODE){var n=t[o],s=n.style;"scroll"!==s.overflow&&"auto"!==s.overflow&&(s=window.getComputedStyle(n)),"scroll"!==s.overflow&&"auto"!==s.overflow||e.push(n)}return e}(lt(t).path));if(!Rt.length)return!0;if("touchstart"===t.type)return!1;var i=function(t){var e={deltaX:t.deltaX,deltaY:t.deltaY};if("deltaX"in t);else if("wheelDeltaX"in t&&"wheelDeltaY"in t)e.deltaX=-t.wheelDeltaX,e.deltaY=-t.wheelDeltaY;else if("wheelDelta"in t)e.deltaX=0,e.deltaY=-t.wheelDelta;else if("axis"in t)e.deltaX=1===t.axis?t.detail:0,e.deltaY=2===t.axis?t.detail:0;else if(t.targetTouches){var i=t.targetTouches[0];e.deltaX=Ct.pageX-i.pageX,e.deltaY=Ct.pageY-i.pageY}return e}(t);return!function(t,e,i){if(!e&&!i)return;for(var o=Math.abs(i)>=Math.abs(e),n=0;n<t.length;n++){var s=t[n];if(o?i<0?s.scrollTop>0:s.scrollTop<s.scrollHeight-s.clientHeight:e<0?s.scrollLeft>0:s.scrollLeft<s.scrollWidth-s.clientWidth)return s}}(Rt,i.deltaX,i.deltaY)}(t)&&t.preventDefault(),t.targetTouches){var e=t.targetTouches[0];Ct.pageX=e.pageX,Ct.pageY=e.pageY}}const $t={properties:{opened:{observer:"_openedChanged",type:Boolean,value:!1,notify:!0},canceled:{observer:"_canceledChanged",readOnly:!0,type:Boolean,value:!1},withBackdrop:{observer:"_withBackdropChanged",type:Boolean},noAutoFocus:{type:Boolean,value:!1},noCancelOnEscKey:{type:Boolean,value:!1},noCancelOnOutsideClick:{type:Boolean,value:!1},closingReason:{type:Object},restoreFocusOnClose:{type:Boolean,value:!1},allowClickThrough:{type:Boolean},alwaysOnTop:{type:Boolean},scrollAction:{type:String},_manager:{type:Object,value:kt},_focusedChild:{type:Object}},listeners:{"iron-resize":"_onIronResize"},observers:["__updateScrollObservers(isAttached, opened, scrollAction)"],get backdropElement(){return this._manager.backdropElement},get _focusNode(){return this._focusedChild||lt(this).querySelector("[autofocus]")||this},get _focusableNodes(){return Et.getTabbableNodes(this)},ready:function(){this.__isAnimating=!1,this.__shouldRemoveTabIndex=!1,this.__firstFocusableNode=this.__lastFocusableNode=null,this.__rafs={},this.__restoreFocusNode=null,this.__scrollTop=this.__scrollLeft=null,this.__onCaptureScroll=this.__onCaptureScroll.bind(this),this.__rootNodes=null,this._ensureSetup()},attached:function(){this.opened&&this._openedChanged(this.opened),this._observer=lt(this).observeNodes(this._onNodesChange)},detached:function(){for(var t in this._observer&&lt(this).unobserveNodes(this._observer),this._observer=null,this.__rafs)null!==this.__rafs[t]&&cancelAnimationFrame(this.__rafs[t]);this.__rafs={},this._manager.removeOverlay(this),this.__isAnimating&&(this.opened?this._finishRenderOpened():(this._applyFocus(),this._finishRenderClosed()))},toggle:function(){this._setCanceled(!1),this.opened=!this.opened},open:function(){this._setCanceled(!1),this.opened=!0},close:function(){this._setCanceled(!1),this.opened=!1},cancel:function(t){this.fire("iron-overlay-canceled",t,{cancelable:!0}).defaultPrevented||(this._setCanceled(!0),this.opened=!1)},invalidateTabbables:function(){this.__firstFocusableNode=this.__lastFocusableNode=null},_ensureSetup:function(){this._overlaySetup||(this._overlaySetup=!0,this.style.outline="none",this.style.display="none")},_openedChanged:function(t){t?this.removeAttribute("aria-hidden"):this.setAttribute("aria-hidden","true"),this.isAttached&&(this.__isAnimating=!0,this.__deraf("__openedChanged",this.__openedChanged))},_canceledChanged:function(){this.closingReason=this.closingReason||{},this.closingReason.canceled=this.canceled},_withBackdropChanged:function(){this.withBackdrop&&!this.hasAttribute("tabindex")?(this.setAttribute("tabindex","-1"),this.__shouldRemoveTabIndex=!0):this.__shouldRemoveTabIndex&&(this.removeAttribute("tabindex"),this.__shouldRemoveTabIndex=!1),this.opened&&this.isAttached&&this._manager.trackBackdrop()},_prepareRenderOpened:function(){this.__restoreFocusNode=this._manager.deepActiveElement,this._preparePositioning(),this.refit(),this._finishPositioning(),this.noAutoFocus&&document.activeElement===this._focusNode&&(this._focusNode.blur(),this.__restoreFocusNode.focus())},_renderOpened:function(){this._finishRenderOpened()},_renderClosed:function(){this._finishRenderClosed()},_finishRenderOpened:function(){this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-opened")},_finishRenderClosed:function(){this.style.display="none",this.style.zIndex="",this.notifyResize(),this.__isAnimating=!1,this.fire("iron-overlay-closed",this.closingReason)},_preparePositioning:function(){this.style.transition=this.style.webkitTransition="none",this.style.transform=this.style.webkitTransform="none",this.style.display=""},_finishPositioning:function(){this.style.display="none",this.scrollTop=this.scrollTop,this.style.transition=this.style.webkitTransition="",this.style.transform=this.style.webkitTransform="",this.style.display="",this.scrollTop=this.scrollTop},_applyFocus:function(){if(this.opened)this.noAutoFocus||this._focusNode.focus();else{if(this.restoreFocusOnClose&&this.__restoreFocusNode){var t=this._manager.deepActiveElement;(t===document.body||Mt(this,t))&&this.__restoreFocusNode.focus()}this.__restoreFocusNode=null,this._focusNode.blur(),this._focusedChild=null}},_onCaptureClick:function(t){this.noCancelOnOutsideClick||this.cancel(t)},_onCaptureFocus:function(t){if(this.withBackdrop){var e=lt(t).path;-1===e.indexOf(this)?(t.stopPropagation(),this._applyFocus()):this._focusedChild=e[0]}},_onCaptureEsc:function(t){this.noCancelOnEscKey||this.cancel(t)},_onCaptureTab:function(t){if(this.withBackdrop){this.__ensureFirstLastFocusables();var e=t.shiftKey,i=e?this.__firstFocusableNode:this.__lastFocusableNode,o=e?this.__lastFocusableNode:this.__firstFocusableNode,n=!1;if(i===o)n=!0;else{var s=this._manager.deepActiveElement;n=s===i||s===this}n&&(t.preventDefault(),this._focusedChild=o,this._applyFocus())}},_onIronResize:function(){this.opened&&!this.__isAnimating&&this.__deraf("refit",this.refit)},_onNodesChange:function(){this.opened&&!this.__isAnimating&&(this.invalidateTabbables(),this.notifyResize())},__ensureFirstLastFocusables:function(){var t=this._focusableNodes;this.__firstFocusableNode=t[0],this.__lastFocusableNode=t[t.length-1]},__openedChanged:function(){this.opened?(this._prepareRenderOpened(),this._manager.addOverlay(this),this._applyFocus(),this._renderOpened()):(this._manager.removeOverlay(this),this._applyFocus(),this._renderClosed())},__deraf:function(t,e){var i=this.__rafs;null!==i[t]&&cancelAnimationFrame(i[t]),i[t]=requestAnimationFrame(function(){i[t]=null,e.call(this)}.bind(this))},__updateScrollObservers:function(t,e,i){t&&e&&this.__isValidScrollAction(i)?("lock"===i&&(this.__saveScrollPosition(),zt(this)),this.__addScrollListeners()):(Ft(this),this.__removeScrollListeners())},__addScrollListeners:function(){if(!this.__rootNodes){if(this.__rootNodes=[],pt)for(var t=this;t;)t.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&t.host&&this.__rootNodes.push(t),t=t.host||t.assignedSlot||t.parentNode;this.__rootNodes.push(document)}this.__rootNodes.forEach((function(t){t.addEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this)},__removeScrollListeners:function(){this.__rootNodes&&this.__rootNodes.forEach((function(t){t.removeEventListener("scroll",this.__onCaptureScroll,{capture:!0,passive:!0})}),this),this.isAttached||(this.__rootNodes=null)},__isValidScrollAction:function(t){return"lock"===t||"refit"===t||"cancel"===t},__onCaptureScroll:function(t){if(!(this.__isAnimating||lt(t).path.indexOf(this)>=0))switch(this.scrollAction){case"lock":this.__restoreScrollPosition();break;case"refit":this.__deraf("refit",this.refit);break;case"cancel":this.cancel(t)}},__saveScrollPosition:function(){document.scrollingElement?(this.__scrollTop=document.scrollingElement.scrollTop,this.__scrollLeft=document.scrollingElement.scrollLeft):(this.__scrollTop=Math.max(document.documentElement.scrollTop,document.body.scrollTop),this.__scrollLeft=Math.max(document.documentElement.scrollLeft,document.body.scrollLeft))},__restoreScrollPosition:function(){document.scrollingElement?(document.scrollingElement.scrollTop=this.__scrollTop,document.scrollingElement.scrollLeft=this.__scrollLeft):(document.documentElement.scrollTop=document.body.scrollTop=this.__scrollTop,document.documentElement.scrollLeft=document.body.scrollLeft=this.__scrollLeft)}},Mt=(t,e)=>{for(let o=e;o;o=(i=o).assignedSlot||i.parentNode||i.host)if(o===t)return!0;var i;return!1};at({_template:rt`
    <style>
      :host {
        position: fixed;
      }

      #contentWrapper ::slotted(*) {
        overflow: auto;
      }

      #contentWrapper.animating ::slotted(*) {
        overflow: hidden;
        pointer-events: none;
      }
    </style>

    <div id="contentWrapper">
      <slot id="content" name="dropdown-content"></slot>
    </div>
`,is:"iron-dropdown",behaviors:[mt,ht,[xt,J,$t],[{properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,e){for(var i in e)t[i]=e[i]},_cloneConfig:function(t){var e={isClone:!0};return this._copyProperties(e,t),e},_getAnimationConfigRecursive:function(t,e,i){var o;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(o=t?this.animationConfig[t]:this.animationConfig,Array.isArray(o)||(o=[o]),o)for(var n,s=0;n=o[s];s++)if(n.animatable)n.animatable._getAnimationConfigRecursive(n.type||t,e,i);else if(n.id){var a=e[n.id];a?(a.isClone||(e[n.id]=this._cloneConfig(a),a=e[n.id]),this._copyProperties(a,n)):e[n.id]=n}else i.push(n)},getAnimationConfig:function(t){var e={},i=[];for(var o in this._getAnimationConfigRecursive(t,e,i),e)i.push(e[o]);return i}},{_configureAnimations:function(t){var e=[],i=[];if(t.length>0)for(let e,o=0;e=t[o];o++){let t=document.createElement(e.name);if(t.isNeonAnimation){let o=null;t.configure||(t.configure=function(t){return null}),o=t.configure(e),i.push({result:o,config:e,neonAnimation:t})}else console.warn(this.is+":",e.name,"not found!")}for(var o=0;o<i.length;o++){let t=i[o].result,n=i[o].config,s=i[o].neonAnimation;try{"function"!=typeof t.cancel&&(t=document.timeline.play(t))}catch(e){t=null,console.warn("Couldnt play","(",n.name,").",e)}t&&e.push({neonAnimation:s,config:n,animation:t})}return e},_shouldComplete:function(t){for(var e=!0,i=0;i<t.length;i++)if("finished"!=t[i].animation.playState){e=!1;break}return e},_complete:function(t){for(var e=0;e<t.length;e++)t[e].neonAnimation.complete(t[e].config);for(e=0;e<t.length;e++)t[e].animation.cancel()},playAnimation:function(t,e){var i=this.getAnimationConfig(t);if(i){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var o=this._configureAnimations(i);if(0!=o.length){this._active[t]=o;for(var n=0;n<o.length;n++)o[n].animation.onfinish=function(){this._shouldComplete(o)&&(this._complete(o),delete this._active[t],this.fire("neon-animation-finish",e,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",e,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var e=this._active[t];for(var i in e)e[i].animation.cancel()}this._active={}}}]],properties:{horizontalAlign:{type:String,value:"left",reflectToAttribute:!0},verticalAlign:{type:String,value:"top",reflectToAttribute:!0},openAnimationConfig:{type:Object},closeAnimationConfig:{type:Object},focusTarget:{type:Object},noAnimations:{type:Boolean,value:!1},allowOutsideScroll:{type:Boolean,value:!1,observer:"_allowOutsideScrollChanged"}},listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},observers:["_updateOverlayPosition(positionTarget, verticalAlign, horizontalAlign, verticalOffset, horizontalOffset)"],get containedElement(){for(var t=lt(this.$.content).getDistributedNodes(),e=0,i=t.length;e<i;e++)if(t[e].nodeType===Node.ELEMENT_NODE)return t[e]},ready:function(){this.scrollAction||(this.scrollAction=this.allowOutsideScroll?"refit":"lock"),this._readied=!0},attached:function(){this.sizingTarget&&this.sizingTarget!==this||(this.sizingTarget=this.containedElement||this)},detached:function(){this.cancelAnimation()},_openedChanged:function(){this.opened&&this.disabled?this.cancel():(this.cancelAnimation(),this._updateAnimationConfig(),$t._openedChanged.apply(this,arguments))},_renderOpened:function(){!this.noAnimations&&this.animationConfig.open?(this.$.contentWrapper.classList.add("animating"),this.playAnimation("open")):$t._renderOpened.apply(this,arguments)},_renderClosed:function(){!this.noAnimations&&this.animationConfig.close?(this.$.contentWrapper.classList.add("animating"),this.playAnimation("close")):$t._renderClosed.apply(this,arguments)},_onNeonAnimationFinish:function(){this.$.contentWrapper.classList.remove("animating"),this.opened?this._finishRenderOpened():this._finishRenderClosed()},_updateAnimationConfig:function(){for(var t=this.containedElement,e=[].concat(this.openAnimationConfig||[]).concat(this.closeAnimationConfig||[]),i=0;i<e.length;i++)e[i].node=t;this.animationConfig={open:this.openAnimationConfig,close:this.closeAnimationConfig}},_updateOverlayPosition:function(){this.isAttached&&this.notifyResize()},_allowOutsideScrollChanged:function(t){this._readied&&(t?this.scrollAction&&"lock"!==this.scrollAction||(this.scrollAction="refit"):this.scrollAction="lock")},_applyFocus:function(){var t=this.focusTarget||this.containedElement;t&&this.opened&&!this.noAutoFocus?t.focus():$t._applyFocus.apply(this,arguments)}});const Lt={properties:{animationTiming:{type:Object,value:function(){return{duration:500,easing:"cubic-bezier(0.4, 0, 0.2, 1)",fill:"both"}}}},isNeonAnimation:!0,created:function(){document.body.animate||console.warn("No web animations detected. This element will not function without a web animations polyfill.")},timingFromConfig:function(t){if(t.timing)for(var e in t.timing)this.animationTiming[e]=t.timing[e];return this.animationTiming},setPrefixedProperty:function(t,e,i){for(var o,n={transform:["webkitTransform"],transformOrigin:["mozTransformOrigin","webkitTransformOrigin"]}[e],s=0;o=n[s];s++)t.style[o]=i;t.style[e]=i},complete:function(t){}};at({is:"fade-in-animation",behaviors:[Lt],configure:function(t){var e=t.node;return this._effect=new KeyframeEffect(e,[{opacity:"0"},{opacity:"1"}],this.timingFromConfig(t)),this._effect}}),at({is:"fade-out-animation",behaviors:[Lt],configure:function(t){var e=t.node;return this._effect=new KeyframeEffect(e,[{opacity:"1"},{opacity:"0"}],this.timingFromConfig(t)),this._effect}});const Dt=rt`
<custom-style>
  <style is="custom-style">
    html {

      --shadow-transition: {
        transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
      };

      --shadow-none: {
        box-shadow: none;
      };

      /* from http://codepen.io/shyndman/pen/c5394ddf2e8b2a5c9185904b57421cdb */

      --shadow-elevation-2dp: {
        box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.14),
                    0 1px 5px 0 rgba(0, 0, 0, 0.12),
                    0 3px 1px -2px rgba(0, 0, 0, 0.2);
      };

      --shadow-elevation-3dp: {
        box-shadow: 0 3px 4px 0 rgba(0, 0, 0, 0.14),
                    0 1px 8px 0 rgba(0, 0, 0, 0.12),
                    0 3px 3px -2px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-4dp: {
        box-shadow: 0 4px 5px 0 rgba(0, 0, 0, 0.14),
                    0 1px 10px 0 rgba(0, 0, 0, 0.12),
                    0 2px 4px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-6dp: {
        box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14),
                    0 1px 18px 0 rgba(0, 0, 0, 0.12),
                    0 3px 5px -1px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-8dp: {
        box-shadow: 0 8px 10px 1px rgba(0, 0, 0, 0.14),
                    0 3px 14px 2px rgba(0, 0, 0, 0.12),
                    0 5px 5px -3px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-12dp: {
        box-shadow: 0 12px 16px 1px rgba(0, 0, 0, 0.14),
                    0 4px 22px 3px rgba(0, 0, 0, 0.12),
                    0 6px 7px -4px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-16dp: {
        box-shadow: 0 16px 24px 2px rgba(0, 0, 0, 0.14),
                    0  6px 30px 5px rgba(0, 0, 0, 0.12),
                    0  8px 10px -5px rgba(0, 0, 0, 0.4);
      };

      --shadow-elevation-24dp: {
        box-shadow: 0 24px 38px 3px rgba(0, 0, 0, 0.14),
                    0 9px 46px 8px rgba(0, 0, 0, 0.12),
                    0 11px 15px -7px rgba(0, 0, 0, 0.4);
      };
    }
  </style>
</custom-style>`;Dt.setAttribute("style","display: none;"),document.head.appendChild(Dt.content),at({is:"paper-menu-grow-height-animation",_template:null,behaviors:[Lt],configure:function(t){var e=t.node,i=e.getBoundingClientRect().height;return this._effect=new KeyframeEffect(e,[{height:i/2+"px"},{height:i+"px"}],this.timingFromConfig(t)),this._effect}}),at({is:"paper-menu-grow-width-animation",_template:null,behaviors:[Lt],configure:function(t){var e=t.node,i=e.getBoundingClientRect().width;return this._effect=new KeyframeEffect(e,[{width:i/2+"px"},{width:i+"px"}],this.timingFromConfig(t)),this._effect}}),at({is:"paper-menu-shrink-width-animation",_template:null,behaviors:[Lt],configure:function(t){var e=t.node,i=e.getBoundingClientRect().width;return this._effect=new KeyframeEffect(e,[{width:i+"px"},{width:i-i/20+"px"}],this.timingFromConfig(t)),this._effect}}),at({is:"paper-menu-shrink-height-animation",_template:null,behaviors:[Lt],configure:function(t){var e=t.node,i=e.getBoundingClientRect().height;return this.setPrefixedProperty(e,"transformOrigin","0 0"),this._effect=new KeyframeEffect(e,[{height:i+"px",transform:"translateY(0)"},{height:i/2+"px",transform:"translateY(-20px)"}],this.timingFromConfig(t)),this._effect}});var Pt={ANIMATION_CUBIC_BEZIER:"cubic-bezier(.3,.95,.5,1)",MAX_ANIMATION_TIME_MS:400};const Ht=at({_template:rt`
    <style>
      :host {
        display: inline-block;
        position: relative;
        padding: 8px;
        outline: none;

        @apply --paper-menu-button;
      }

      :host([disabled]) {
        cursor: auto;
        color: var(--disabled-text-color);

        @apply --paper-menu-button-disabled;
      }

      iron-dropdown {
        @apply --paper-menu-button-dropdown;
      }

      .dropdown-content {
        @apply --shadow-elevation-2dp;

        position: relative;
        border-radius: 2px;
        background-color: var(--paper-menu-button-dropdown-background, var(--primary-background-color));

        @apply --paper-menu-button-content;
      }

      :host([vertical-align="top"]) .dropdown-content {
        margin-bottom: 20px;
        margin-top: -10px;
        top: 10px;
      }

      :host([vertical-align="bottom"]) .dropdown-content {
        bottom: 10px;
        margin-bottom: -10px;
        margin-top: 20px;
      }

      #trigger {
        cursor: pointer;
      }
    </style>

    <div id="trigger" on-tap="toggle">
      <slot name="dropdown-trigger"></slot>
    </div>

    <iron-dropdown id="dropdown" opened="{{opened}}" horizontal-align="[[horizontalAlign]]" vertical-align="[[verticalAlign]]" dynamic-align="[[dynamicAlign]]" horizontal-offset="[[horizontalOffset]]" vertical-offset="[[verticalOffset]]" no-overlap="[[noOverlap]]" open-animation-config="[[openAnimationConfig]]" close-animation-config="[[closeAnimationConfig]]" no-animations="[[noAnimations]]" focus-target="[[_dropdownContent]]" allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" on-iron-overlay-canceled="__onIronOverlayCanceled" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">
      <div slot="dropdown-content" class="dropdown-content">
        <slot id="content" name="dropdown-content"></slot>
      </div>
    </iron-dropdown>
`,is:"paper-menu-button",behaviors:[ht,mt],properties:{opened:{type:Boolean,value:!1,notify:!0,observer:"_openedChanged"},horizontalAlign:{type:String,value:"left",reflectToAttribute:!0},verticalAlign:{type:String,value:"top",reflectToAttribute:!0},dynamicAlign:{type:Boolean},horizontalOffset:{type:Number,value:0,notify:!0},verticalOffset:{type:Number,value:0,notify:!0},noOverlap:{type:Boolean},noAnimations:{type:Boolean,value:!1},ignoreSelect:{type:Boolean,value:!1},closeOnActivate:{type:Boolean,value:!1},openAnimationConfig:{type:Object,value:function(){return[{name:"fade-in-animation",timing:{delay:100,duration:200}},{name:"paper-menu-grow-width-animation",timing:{delay:100,duration:150,easing:Pt.ANIMATION_CUBIC_BEZIER}},{name:"paper-menu-grow-height-animation",timing:{delay:100,duration:275,easing:Pt.ANIMATION_CUBIC_BEZIER}}]}},closeAnimationConfig:{type:Object,value:function(){return[{name:"fade-out-animation",timing:{duration:150}},{name:"paper-menu-shrink-width-animation",timing:{delay:100,duration:50,easing:Pt.ANIMATION_CUBIC_BEZIER}},{name:"paper-menu-shrink-height-animation",timing:{duration:200,easing:"ease-in"}}]}},allowOutsideScroll:{type:Boolean,value:!1},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1},_dropdownContent:{type:Object}},hostAttributes:{role:"group","aria-haspopup":"true"},listeners:{"iron-activate":"_onIronActivate","iron-select":"_onIronSelect"},get contentElement(){for(var t=lt(this.$.content).getDistributedNodes(),e=0,i=t.length;e<i;e++)if(t[e].nodeType===Node.ELEMENT_NODE)return t[e]},toggle:function(){this.opened?this.close():this.open()},open:function(){this.disabled||this.$.dropdown.open()},close:function(){this.$.dropdown.close()},_onIronSelect:function(t){this.ignoreSelect||this.close()},_onIronActivate:function(t){this.closeOnActivate&&this.close()},_openedChanged:function(t,e){t?(this._dropdownContent=this.contentElement,this.fire("paper-dropdown-open")):null!=e&&this.fire("paper-dropdown-close")},_disabledChanged:function(t){mt._disabledChanged.apply(this,arguments),t&&this.opened&&this.close()},__onIronOverlayCanceled:function(t){var e=t.detail,i=this.$.trigger;lt(e).path.indexOf(i)>-1&&t.preventDefault()}});Object.keys(Pt).forEach((function(t){Ht[t]=Pt[t]})),c([A("racelandshop-repository-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[g({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"racelandshop",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"status",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"removed",value:void 0},{kind:"field",decorators:[g({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[g({type:Boolean})],key:"addedToLovelace",value:void 0},{kind:"get",key:"_borderClass",value:function(){const t={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["status-update"]=!0:this.repository.new&&!this.repository.installed&&(t["status-new"]=!0):t["status-issue"]=!0,0!==Object.keys(t).length&&(t["status-border"]=!0),t}},{kind:"get",key:"_headerClass",value:function(){const t={};return this.addedToLovelace&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["update-header"]=!0:this.repository.new&&!this.repository.installed?t["new-header"]=!0:t["default-header"]=!0:t["issue-header"]=!0,t}},{kind:"get",key:"_headerTitle",value:function(){return this.addedToLovelace?"pending-restart"===this.repository.status?this.racelandshop.localize("repository_card.pending_restart"):this.repository.pending_upgrade?this.racelandshop.localize("repository_card.pending_update"):this.repository.new&&!this.repository.installed?this.racelandshop.localize("repository_card.new_repository"):"":this.racelandshop.localize("repository_card.not_loaded")}},{kind:"method",key:"render",value:function(){const t=this.repository.local_path.split("/");return v`
      <ha-card class=${ut(this._borderClass)} ?narrow=${this.narrow}>
        <div class="card-content">
          <div class="group-header">
            <div class="status-header ${ut(this._headerClass)}">${this._headerTitle}</div>
            <div class="title">
              <h1 class="pointer" @click=${this._showReopsitoryInfo}>${this.repository.name}</h1>
              ${"integration"!==this.repository.category?v` <racelandshop-chip
                    .icon=${Z}
                    .value=${this.racelandshop.localize("common."+this.repository.category)}
                  ></racelandshop-chip>`:""}
            </div>
          </div>
          <paper-item>
            <paper-item-body>${this.repository.description}</paper-item-body></paper-item
          >
        </div>
        <div class="card-actions">
          ${this.repository.new&&!this.repository.installed?v`<div>
                  <mwc-button @click=${this._installRepository}
                    >${this.racelandshop.localize("common.install")}</mwc-button
                  >
                </div>
                <div>
                  <mwc-button @click=${this._showReopsitoryInfo}
                    >${this.racelandshop.localize("repository_card.information")}</mwc-button
                  >
                </div>
                <div>
                  <racelandshop-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${this.racelandshop.localize("common.repository")}</mwc-button></racelandshop-link
                  >
                </div>
                <div>
                  <mwc-button @click=${this._setNotNew}
                    >${this.racelandshop.localize("repository_card.dismiss")}</mwc-button
                  >
                </div>`:this.repository.pending_upgrade&&this.addedToLovelace?v`<div>
                  <mwc-button class="update-header" @click=${this._updateRepository} raised
                    >${this.racelandshop.localize("common.update")}</mwc-button
                  >
                </div>
                <div>
                  <racelandshop-link .url="https://github.com/${this.repository.full_name}"
                    ><mwc-button>${this.racelandshop.localize("common.repository")}</mwc-button></racelandshop-link
                  >
                </div>`:v`<div>
                <racelandshop-link .url="https://github.com/${this.repository.full_name}"
                  ><mwc-button>${this.racelandshop.localize("common.repository")}</mwc-button></racelandshop-link
                >
              </div>`}
          ${this.repository.installed?v` <paper-menu-button
                horizontal-align="right"
                vertical-align="top"
                vertical-offset="40"
                close-on-activate
              >
                <mwc-icon-button slot="dropdown-trigger" alt="menu">
                  <ha-svg-icon .path=${b}></ha-svg-icon>
                </mwc-icon-button>
                <paper-listbox slot="dropdown-content">
                  <paper-item class="pointer" @tap=${this._showReopsitoryInfo}
                    >${this.racelandshop.localize("repository_card.information")}</paper-item
                  >

                  <paper-item class="pointer" @tap=${this._updateReopsitoryInfo}
                    >${this.racelandshop.localize("repository_card.update_information")}</paper-item
                  >

                  <paper-item @tap=${this._installRepository}
                    >${this.racelandshop.localize("repository_card.reinstall")}</paper-item
                  >

                  ${"plugin"===this.repository.category?v`<racelandshop-link
                        .url="/racelandshopfiles/${t.pop()}/${this.repository.file_name}"
                        newtab
                        ><paper-item class="pointer"
                          >${this.racelandshop.localize("repository_card.open_source")}</paper-item
                        ></racelandshop-link
                      >`:""}

                  <racelandshop-link .url="https://github.com/${this.repository.full_name}/issues"
                    ><paper-item class="pointer"
                      >${this.racelandshop.localize("repository_card.open_issue")}</paper-item
                    ></racelandshop-link
                  >

                  ${"172733314"!==String(this.repository.id)?v`<racelandshop-link
                          .url="https://github.com/racelandshop/integration/issues/new?assignees=ludeeus&labels=flag&template=removal.yml&repo=${this.repository.full_name}&title=Request for removal of ${this.repository.full_name}"
                          ><paper-item class="pointer uninstall"
                            >${this.racelandshop.localize("repository_card.report")}</paper-item
                          ></racelandshop-link
                        >
                        <paper-item
                          class="pointer uninstall"
                          @tap=${this._uninstallRepositoryDialog}
                          >${this.racelandshop.localize("common.uninstall")}</paper-item
                        >`:""}
                </paper-listbox>
              </paper-menu-button>`:""}
        </div>
      </ha-card>
    `}},{kind:"method",key:"_updateReopsitoryInfo",value:async function(){await y(this.hass,this.repository.id)}},{kind:"method",key:"_showReopsitoryInfo",value:async function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"repository-info",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_updateRepository",value:async function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"update",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_setNotNew",value:async function(){await _(this.hass,this.repository.id)}},{kind:"method",key:"_installRepository",value:function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"install",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepositoryDialog",value:async function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"progress",title:this.racelandshop.localize("dialog.uninstall.title"),confirmText:this.racelandshop.localize("dialog.uninstall.title"),content:this.racelandshop.localize("dialog.uninstall.message",{name:this.repository.name}),confirm:async()=>{await this._uninstallRepository()}},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepository",value:async function(){var t;if("plugin"===this.repository.category&&"yaml"!==(null===(t=this.racelandshop.status)||void 0===t?void 0:t.lovelace_mode)){const t=await x(this.hass),e=w({repository:this.repository,skipTag:!0});await Promise.all(t.filter(t=>t.url.includes(e)).map(t=>T(this.hass,String(t.id))))}await E(this.hass,this.repository.id)}},{kind:"get",static:!0,key:"styles",value:function(){return[k,I`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          width: 480px;
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
          border-color: transparent;
          border-radius: var(--ha-card-border-radius, 4px);
        }

        racelandshop-chip {
          margin: 8px 4px 0 0;
        }
        .title {
          display: flex;
          justify-content: space-between;
        }
        .card-content {
          padding: 0 0 3px 0;
          height: 100%;
        }
        .card-actions {
          border-top: none;
          bottom: 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 5px;
        }
        .group-header {
          height: auto;
          align-content: center;
        }
        .group-header h1 {
          margin: 0;
          padding: 8px 16px;
        }
        h1 {
          margin-top: 0;
          min-height: 24px;
        }
        paper-menu-button {
          padding: 0;
          float: right;
        }

        .pointer {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }

        .status-new {
          border-color: var(--hcv-color-new);
        }

        .status-update {
          border-color: var(--hcv-color-update);
        }

        .status-issue {
          border-color: var(--hcv-color-error);
        }

        .new-header {
          background-color: var(--hcv-color-new);
          color: var(--hcv-text-color-on-background);
        }

        .issue-header {
          background-color: var(--hcv-color-error);
          color: var(--hcv-text-color-on-background);
        }

        .update-header {
          background-color: var(--hcv-color-update);
          color: var(--hcv-text-color-on-background);
        }

        .default-header {
          padding: 10px 0 !important;
        }

        mwc-button.update-header {
          --mdc-theme-primary: var(--hcv-color-update);
          --mdc-theme-on-primary: var(--hcv-text-color-on-background);
        }

        .status-border {
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
        }

        .status-header {
          top: 0;
          padding: 6px 1px;
          margin: -1px;
          width: 100%;
          font-weight: 300;
          text-align: center;
          left: 0;
          border-top-left-radius: var(--ha-card-border-radius, 4px);
          border-top-right-radius: var(--ha-card-border-radius, 4px);
        }

        ha-card[narrow] {
          width: calc(100% - 24px);
          margin: 11px;
        }
      `]}}]}}),f);const Ut=t=>(e,i)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach((t,i)=>e.constructor._observers.set(i,t))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach((t,e)=>{const i=this.constructor._observers.get(e);void 0!==i&&i.call(this,this[e],t)})}}e.constructor._observers.set(i,t)};class jt extends f{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new st(()=>(this.shouldRenderRipple=!0,this.ripple)),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const e=t.type;this.onDown("mousedown"===e?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),e=this.graphic?this.renderGraphic():v``,i=this.hasMeta?this.renderMeta():v``;return v`
      ${this.renderRipple()}
      ${e}
      ${t}
      ${i}`}renderRipple(){return this.shouldRenderRipple?v`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?v`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return v`
      <span class="mdc-deprecated-list-item__graphic material-icons ${ut(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return v`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return v`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return v`<slot></slot>`}renderTwoline(){return v`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,e){const i=()=>{window.removeEventListener(t,i),this.rippleHandlers.endPress()};window.addEventListener(t,i),this.rippleHandlers.startPress(e)}fireRequestSelected(t,e){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:t}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const e of t.eventNames)t.target.addEventListener(e,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const e of t.eventNames)t.target.removeEventListener(e,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}ot([C("slot")],jt.prototype,"slotElement",void 0),ot([nt("mwc-ripple")],jt.prototype,"ripple",void 0),ot([g({type:String})],jt.prototype,"value",void 0),ot([g({type:String,reflect:!0})],jt.prototype,"group",void 0),ot([g({type:Number,reflect:!0})],jt.prototype,"tabindex",void 0),ot([g({type:Boolean,reflect:!0}),Ut((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],jt.prototype,"disabled",void 0),ot([g({type:Boolean,reflect:!0})],jt.prototype,"twoline",void 0),ot([g({type:Boolean,reflect:!0})],jt.prototype,"activated",void 0),ot([g({type:String,reflect:!0})],jt.prototype,"graphic",void 0),ot([g({type:Boolean})],jt.prototype,"multipleGraphics",void 0),ot([g({type:Boolean})],jt.prototype,"hasMeta",void 0),ot([g({type:Boolean,reflect:!0}),Ut((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],jt.prototype,"noninteractive",void 0),ot([g({type:Boolean,reflect:!0}),Ut((function(t){const e=this.getAttribute("role"),i="gridcell"===e||"option"===e||"row"===e||"tab"===e;i&&t?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],jt.prototype,"selected",void 0),ot([O()],jt.prototype,"shouldRenderRipple",void 0),ot([O()],jt.prototype,"_managingList",void 0);const Gt=I`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let Wt=class extends jt{};function Kt(t,e,i,o){var n,s=arguments.length,a=s<3?e:null===o?o=Object.getOwnPropertyDescriptor(e,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,i,o);else for(var r=t.length-1;r>=0;r--)(n=t[r])&&(a=(s<3?n(a):s>3?n(e,i,a):n(e,i))||a);return s>3&&a&&Object.defineProperty(e,i,a),a}function Xt(t,e,i,o){var n,s=arguments.length,a=s<3?e:null===o?o=Object.getOwnPropertyDescriptor(e,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,i,o);else for(var r=t.length-1;r>=0;r--)(n=t[r])&&(a=(s<3?n(a):s>3?n(e,i,a):n(e,i))||a);return s>3&&a&&Object.defineProperty(e,i,a),a}Wt.styles=[Gt],Wt=ot([A("mwc-list-item")],Wt);class qt extends n{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new s(()=>(this.shouldRenderRipple=!0,this.ripple)),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const e=t.type;this.onDown("mousedown"===e?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),e=this.graphic?this.renderGraphic():a``,i=this.hasMeta?this.renderMeta():a``;return a`
      ${this.renderRipple()}
      ${e}
      ${t}
      ${i}`}renderRipple(){return this.shouldRenderRipple?a`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?a`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return a`
      <span class="mdc-deprecated-list-item__graphic material-icons ${r(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return a`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return a`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return a`<slot></slot>`}renderTwoline(){return a`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,e){const i=()=>{window.removeEventListener(t,i),this.rippleHandlers.endPress()};window.addEventListener(t,i),this.rippleHandlers.startPress(e)}fireRequestSelected(t,e){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:t}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const e of t.eventNames)t.target.addEventListener(e,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const e of t.eventNames)t.target.removeEventListener(e,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}Xt([R("slot")],qt.prototype,"slotElement",void 0),Xt([t("mwc-ripple")],qt.prototype,"ripple",void 0),Xt([e({type:String})],qt.prototype,"value",void 0),Xt([e({type:String,reflect:!0})],qt.prototype,"group",void 0),Xt([e({type:Number,reflect:!0})],qt.prototype,"tabindex",void 0),Xt([e({type:Boolean,reflect:!0}),it((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],qt.prototype,"disabled",void 0),Xt([e({type:Boolean,reflect:!0})],qt.prototype,"twoline",void 0),Xt([e({type:Boolean,reflect:!0})],qt.prototype,"activated",void 0),Xt([e({type:String,reflect:!0})],qt.prototype,"graphic",void 0),Xt([e({type:Boolean})],qt.prototype,"multipleGraphics",void 0),Xt([e({type:Boolean})],qt.prototype,"hasMeta",void 0),Xt([e({type:Boolean,reflect:!0}),it((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],qt.prototype,"noninteractive",void 0),Xt([e({type:Boolean,reflect:!0}),it((function(t){const e=this.getAttribute("role"),i="gridcell"===e||"option"===e||"row"===e||"tab"===e;i&&t?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],qt.prototype,"selected",void 0),Xt([i()],qt.prototype,"shouldRenderRipple",void 0),Xt([i()],qt.prototype,"_managingList",void 0);const Vt=d`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let Zt=class extends qt{};Zt.styles=Vt,Zt=Xt([l("mwc-list-item")],Zt);var Yt="Unknown",Qt="Backspace",Jt="Enter",te="Spacebar",ee="PageUp",ie="PageDown",oe="End",ne="Home",se="ArrowLeft",ae="ArrowUp",re="ArrowRight",de="ArrowDown",le="Delete",ce="Escape",he="Tab",pe=new Set;pe.add(Qt),pe.add(Jt),pe.add(te),pe.add(ee),pe.add(ie),pe.add(oe),pe.add(ne),pe.add(se),pe.add(ae),pe.add(re),pe.add(de),pe.add(le),pe.add(ce),pe.add(he);var me=8,ue=13,fe=32,ge=33,ve=34,be=35,ye=36,_e=37,xe=38,we=39,Te=40,Ee=46,ke=27,Ie=9,Ae=new Map;Ae.set(me,Qt),Ae.set(ue,Jt),Ae.set(fe,te),Ae.set(ge,ee),Ae.set(ve,ie),Ae.set(be,oe),Ae.set(ye,ne),Ae.set(_e,se),Ae.set(xe,ae),Ae.set(we,re),Ae.set(Te,de),Ae.set(Ee,le),Ae.set(ke,ce),Ae.set(Ie,he);var Ce,Oe,Re=new Set;function Se(t){var e=t.key;if(pe.has(e))return e;var i=Ae.get(t.keyCode);return i||Yt}Re.add(ee),Re.add(ie),Re.add(oe),Re.add(ne),Re.add(se),Re.add(ae),Re.add(re),Re.add(de);var ze="mdc-list-item--activated",Fe="mdc-list-item",Ne="mdc-list-item--disabled",Be="mdc-list-item--selected",$e="mdc-list-item__text",Me="mdc-list-item__primary-text",Le="mdc-list";(Ce={})[""+ze]="mdc-list-item--activated",Ce[""+Fe]="mdc-list-item",Ce[""+Ne]="mdc-list-item--disabled",Ce[""+Be]="mdc-list-item--selected",Ce[""+Me]="mdc-list-item__primary-text",Ce[""+Le]="mdc-list";var De=((Oe={})[""+ze]="mdc-deprecated-list-item--activated",Oe[""+Fe]="mdc-deprecated-list-item",Oe[""+Ne]="mdc-deprecated-list-item--disabled",Oe[""+Be]="mdc-deprecated-list-item--selected",Oe[""+$e]="mdc-deprecated-list-item__text",Oe[""+Me]="mdc-deprecated-list-item__primary-text",Oe[""+Le]="mdc-deprecated-list",Oe),Pe={ACTION_EVENT:"MDCList:action",ARIA_CHECKED:"aria-checked",ARIA_CHECKED_CHECKBOX_SELECTOR:'[role="checkbox"][aria-checked="true"]',ARIA_CHECKED_RADIO_SELECTOR:'[role="radio"][aria-checked="true"]',ARIA_CURRENT:"aria-current",ARIA_DISABLED:"aria-disabled",ARIA_ORIENTATION:"aria-orientation",ARIA_ORIENTATION_HORIZONTAL:"horizontal",ARIA_ROLE_CHECKBOX_SELECTOR:'[role="checkbox"]',ARIA_SELECTED:"aria-selected",ARIA_INTERACTIVE_ROLES_SELECTOR:'[role="listbox"], [role="menu"]',ARIA_MULTI_SELECTABLE_SELECTOR:'[aria-multiselectable="true"]',CHECKBOX_RADIO_SELECTOR:'input[type="checkbox"], input[type="radio"]',CHECKBOX_SELECTOR:'input[type="checkbox"]',CHILD_ELEMENTS_TO_TOGGLE_TABINDEX:"\n    ."+Fe+" button:not(:disabled),\n    ."+Fe+" a,\n    ."+De[Fe]+" button:not(:disabled),\n    ."+De[Fe]+" a\n  ",DEPRECATED_SELECTOR:".mdc-deprecated-list",FOCUSABLE_CHILD_ELEMENTS:"\n    ."+Fe+" button:not(:disabled),\n    ."+Fe+" a,\n    ."+Fe+' input[type="radio"]:not(:disabled),\n    .'+Fe+' input[type="checkbox"]:not(:disabled),\n    .'+De[Fe]+" button:not(:disabled),\n    ."+De[Fe]+" a,\n    ."+De[Fe]+' input[type="radio"]:not(:disabled),\n    .'+De[Fe]+' input[type="checkbox"]:not(:disabled)\n  ',RADIO_SELECTOR:'input[type="radio"]',SELECTED_ITEM_SELECTOR:'[aria-selected="true"], [aria-current="true"]'},He={UNSET_INDEX:-1,TYPEAHEAD_BUFFER_CLEAR_TIMEOUT_MS:300};const Ue=(t,e)=>t-e,je=["input","button","textarea","select"];function Ge(t){return t instanceof Set}const We=t=>{const e=t===He.UNSET_INDEX?new Set:t;return Ge(e)?new Set(e):new Set([e])};class Ke extends S{constructor(t){super(Object.assign(Object.assign({},Ke.defaultAdapter),t)),this.isMulti_=!1,this.wrapFocus_=!1,this.isVertical_=!0,this.selectedIndex_=He.UNSET_INDEX,this.focusedItemIndex_=He.UNSET_INDEX,this.useActivatedClass_=!1,this.ariaCurrentAttrValue_=null}static get strings(){return Pe}static get numbers(){return He}static get defaultAdapter(){return{focusItemAtIndex:()=>{},getFocusedElementIndex:()=>0,getListItemCount:()=>0,isFocusInsideList:()=>!1,isRootFocused:()=>!1,notifyAction:()=>{},notifySelected:()=>{},getSelectedStateForElementIndex:()=>!1,setDisabledStateForElementIndex:()=>{},getDisabledStateForElementIndex:()=>!1,setSelectedStateForElementIndex:()=>{},setActivatedStateForElementIndex:()=>{},setTabIndexForElementIndex:()=>{},setAttributeForElementIndex:()=>{},getAttributeForElementIndex:()=>null}}setWrapFocus(t){this.wrapFocus_=t}setMulti(t){this.isMulti_=t;const e=this.selectedIndex_;if(t){if(!Ge(e)){const t=e===He.UNSET_INDEX;this.selectedIndex_=t?new Set:new Set([e])}}else if(Ge(e))if(e.size){const t=Array.from(e).sort(Ue);this.selectedIndex_=t[0]}else this.selectedIndex_=He.UNSET_INDEX}setVerticalOrientation(t){this.isVertical_=t}setUseActivatedClass(t){this.useActivatedClass_=t}getSelectedIndex(){return this.selectedIndex_}setSelectedIndex(t){this.isIndexValid_(t)&&(this.isMulti_?this.setMultiSelectionAtIndex_(We(t)):this.setSingleSelectionAtIndex_(t))}handleFocusIn(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,0)}handleFocusOut(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,-1),setTimeout(()=>{this.adapter.isFocusInsideList()||this.setTabindexToFirstSelectedItem_()},0)}handleKeydown(t,e,i){const o="ArrowLeft"===Se(t),n="ArrowUp"===Se(t),s="ArrowRight"===Se(t),a="ArrowDown"===Se(t),r="Home"===Se(t),d="End"===Se(t),l="Enter"===Se(t),c="Spacebar"===Se(t);if(this.adapter.isRootFocused())return void(n||d?(t.preventDefault(),this.focusLastElement()):(a||r)&&(t.preventDefault(),this.focusFirstElement()));let h,p=this.adapter.getFocusedElementIndex();if(!(-1===p&&(p=i,p<0))){if(this.isVertical_&&a||!this.isVertical_&&s)this.preventDefaultEvent(t),h=this.focusNextElement(p);else if(this.isVertical_&&n||!this.isVertical_&&o)this.preventDefaultEvent(t),h=this.focusPrevElement(p);else if(r)this.preventDefaultEvent(t),h=this.focusFirstElement();else if(d)this.preventDefaultEvent(t),h=this.focusLastElement();else if((l||c)&&e){const e=t.target;if(e&&"A"===e.tagName&&l)return;this.preventDefaultEvent(t),this.setSelectedIndexOnAction_(p,!0)}this.focusedItemIndex_=p,void 0!==h&&(this.setTabindexAtIndex_(h),this.focusedItemIndex_=h)}}handleSingleSelection(t,e,i){t!==He.UNSET_INDEX&&(this.setSelectedIndexOnAction_(t,e,i),this.setTabindexAtIndex_(t),this.focusedItemIndex_=t)}focusNextElement(t){let e=t+1;if(e>=this.adapter.getListItemCount()){if(!this.wrapFocus_)return t;e=0}return this.adapter.focusItemAtIndex(e),e}focusPrevElement(t){let e=t-1;if(e<0){if(!this.wrapFocus_)return t;e=this.adapter.getListItemCount()-1}return this.adapter.focusItemAtIndex(e),e}focusFirstElement(){return this.adapter.focusItemAtIndex(0),0}focusLastElement(){const t=this.adapter.getListItemCount()-1;return this.adapter.focusItemAtIndex(t),t}setEnabled(t,e){this.isIndexValid_(t)&&this.adapter.setDisabledStateForElementIndex(t,!e)}preventDefaultEvent(t){const e=(""+t.target.tagName).toLowerCase();-1===je.indexOf(e)&&t.preventDefault()}setSingleSelectionAtIndex_(t,e=!0){this.selectedIndex_!==t&&(this.selectedIndex_!==He.UNSET_INDEX&&(this.adapter.setSelectedStateForElementIndex(this.selectedIndex_,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(this.selectedIndex_,!1)),e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0),this.setAriaForSingleSelectionAtIndex_(t),this.selectedIndex_=t,this.adapter.notifySelected(t))}setMultiSelectionAtIndex_(t,e=!0){const i=((t,e)=>{const i=Array.from(t),o=Array.from(e),n={added:[],removed:[]},s=i.sort(Ue),a=o.sort(Ue);let r=0,d=0;for(;r<s.length||d<a.length;){const t=s[r],e=a[d];t!==e?void 0!==t&&(void 0===e||t<e)?(n.removed.push(t),r++):void 0!==e&&(void 0===t||e<t)&&(n.added.push(e),d++):(r++,d++)}return n})(We(this.selectedIndex_),t);if(i.removed.length||i.added.length){for(const t of i.removed)e&&this.adapter.setSelectedStateForElementIndex(t,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!1);for(const t of i.added)e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0);this.selectedIndex_=t,this.adapter.notifySelected(t,i)}}setAriaForSingleSelectionAtIndex_(t){this.selectedIndex_===He.UNSET_INDEX&&(this.ariaCurrentAttrValue_=this.adapter.getAttributeForElementIndex(t,Pe.ARIA_CURRENT));const e=null!==this.ariaCurrentAttrValue_,i=e?Pe.ARIA_CURRENT:Pe.ARIA_SELECTED;this.selectedIndex_!==He.UNSET_INDEX&&this.adapter.setAttributeForElementIndex(this.selectedIndex_,i,"false");const o=e?this.ariaCurrentAttrValue_:"true";this.adapter.setAttributeForElementIndex(t,i,o)}setTabindexAtIndex_(t){this.focusedItemIndex_===He.UNSET_INDEX&&0!==t?this.adapter.setTabIndexForElementIndex(0,-1):this.focusedItemIndex_>=0&&this.focusedItemIndex_!==t&&this.adapter.setTabIndexForElementIndex(this.focusedItemIndex_,-1),this.adapter.setTabIndexForElementIndex(t,0)}setTabindexToFirstSelectedItem_(){let t=0;"number"==typeof this.selectedIndex_&&this.selectedIndex_!==He.UNSET_INDEX?t=this.selectedIndex_:Ge(this.selectedIndex_)&&this.selectedIndex_.size>0&&(t=Math.min(...this.selectedIndex_)),this.setTabindexAtIndex_(t)}isIndexValid_(t){if(t instanceof Set){if(!this.isMulti_)throw new Error("MDCListFoundation: Array of index is only supported for checkbox based list");if(0===t.size)return!0;{let e=!1;for(const i of t)if(e=this.isIndexInRange_(i),e)break;return e}}if("number"==typeof t){if(this.isMulti_)throw new Error("MDCListFoundation: Expected array of index for checkbox based list but got number: "+t);return t===He.UNSET_INDEX||this.isIndexInRange_(t)}return!1}isIndexInRange_(t){const e=this.adapter.getListItemCount();return t>=0&&t<e}setSelectedIndexOnAction_(t,e,i){if(this.adapter.getDisabledStateForElementIndex(t))return;let o=t;if(this.isMulti_&&(o=new Set([t])),this.isIndexValid_(o)){if(this.isMulti_)this.toggleMultiAtIndex(t,i,e);else if(e||i)this.setSingleSelectionAtIndex_(t,e);else{this.selectedIndex_===t&&this.setSingleSelectionAtIndex_(He.UNSET_INDEX)}e&&this.adapter.notifyAction(t)}}toggleMultiAtIndex(t,e,i=!0){let o=!1;o=void 0===e?!this.adapter.getSelectedStateForElementIndex(t):e;const n=We(this.selectedIndex_);o?n.add(t):n.delete(t),this.setMultiSelectionAtIndex_(n,i)}}const Xe=t=>t.hasAttribute("mwc-list-item");function qe(){const t=this.itemsReadyResolver;this.itemsReady=new Promise(t=>this.itemsReadyResolver=t),t()}class Ve extends F{constructor(){super(),this.mdcAdapter=null,this.mdcFoundationClass=Ke,this.activatable=!1,this.multi=!1,this.wrapFocus=!1,this.itemRoles=null,this.innerRole=null,this.innerAriaLabel=null,this.rootTabbable=!1,this.previousTabindex=null,this.noninteractive=!1,this.itemsReadyResolver=()=>{},this.itemsReady=Promise.resolve([]),this.items_=[];const t=function(t,e=50){let i;return function(o=!0){clearTimeout(i),i=setTimeout(()=>{t(o)},e)}}(this.layout.bind(this));this.debouncedLayout=(e=!0)=>{qe.call(this),t(e)}}async _getUpdateComplete(){return this.getUpdateComplete()}async getUpdateComplete(){let t=!1;return super.getUpdateComplete?t=await super.getUpdateComplete():await super._getUpdateComplete(),await this.itemsReady,t}get assignedElements(){const t=this.slotElement;return t?t.assignedNodes({flatten:!0}).filter(N):[]}get items(){return this.items_}updateItems(){const t=this.assignedElements,e=[];for(const i of t)Xe(i)&&(e.push(i),i._managingList=this),i.hasAttribute("divider")&&!i.hasAttribute("role")&&i.setAttribute("role","separator");this.items_=e;const i=new Set;if(this.items_.forEach((t,e)=>{this.itemRoles?t.setAttribute("role",this.itemRoles):t.removeAttribute("role"),t.selected&&i.add(e)}),this.multi)this.select(i);else{const t=i.size?i.entries().next().value[1]:-1;this.select(t)}const o=new Event("items-updated",{bubbles:!0,composed:!0});this.dispatchEvent(o)}get selected(){const t=this.index;if(!Ge(t))return-1===t?null:this.items[t];const e=[];for(const i of t)e.push(this.items[i]);return e}get index(){return this.mdcFoundation?this.mdcFoundation.getSelectedIndex():-1}render(){const t=null===this.innerRole?void 0:this.innerRole,e=null===this.innerAriaLabel?void 0:this.innerAriaLabel,i=this.rootTabbable?"0":"-1";return a`
      <!-- @ts-ignore -->
      <ul
          tabindex=${i}
          role="${m(t)}"
          aria-label="${m(e)}"
          class="mdc-deprecated-list"
          @keydown=${this.onKeydown}
          @focusin=${this.onFocusIn}
          @focusout=${this.onFocusOut}
          @request-selected=${this.onRequestSelected}
          @list-item-rendered=${this.onListItemConnected}>
        <slot></slot>
        ${this.renderPlaceholder()}
      </ul>
    `}renderPlaceholder(){return void 0!==this.emptyMessage&&0===this.assignedElements.length?a`
        <mwc-list-item noninteractive>${this.emptyMessage}</mwc-list-item>
      `:null}firstUpdated(){super.firstUpdated(),this.items.length||(this.mdcFoundation.setMulti(this.multi),this.layout())}onFocusIn(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusIn(t,e)}}onFocusOut(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusOut(t,e)}}onKeydown(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t),i=t.target,o=Xe(i);this.mdcFoundation.handleKeydown(t,o,e)}}onRequestSelected(t){if(this.mdcFoundation){let e=this.getIndexOfTarget(t);if(-1===e&&(this.layout(),e=this.getIndexOfTarget(t),-1===e))return;if(this.items[e].disabled)return;const i=t.detail.selected,o=t.detail.source;this.mdcFoundation.handleSingleSelection(e,"interaction"===o,i),t.stopPropagation()}}getIndexOfTarget(t){const e=this.items,i=t.composedPath();for(const t of i){let i=-1;if(N(t)&&Xe(t)&&(i=e.indexOf(t)),-1!==i)return i}return-1}createAdapter(){return this.mdcAdapter={getListItemCount:()=>this.mdcRoot?this.items.length:0,getFocusedElementIndex:this.getFocusedItemIndex,getAttributeForElementIndex:(t,e)=>{if(!this.mdcRoot)return"";const i=this.items[t];return i?i.getAttribute(e):""},setAttributeForElementIndex:(t,e,i)=>{if(!this.mdcRoot)return;const o=this.items[t];o&&o.setAttribute(e,i)},focusItemAtIndex:t=>{const e=this.items[t];e&&e.focus()},setTabIndexForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.tabindex=e)},notifyAction:t=>{const e={bubbles:!0,composed:!0};e.detail={index:t};const i=new CustomEvent("action",e);this.dispatchEvent(i)},notifySelected:(t,e)=>{const i={bubbles:!0,composed:!0};i.detail={index:t,diff:e};const o=new CustomEvent("selected",i);this.dispatchEvent(o)},isFocusInsideList:()=>B(this),isRootFocused:()=>{const t=this.mdcRoot;return t.getRootNode().activeElement===t},setDisabledStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.disabled=e)},getDisabledStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.disabled},setSelectedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.selected=e)},getSelectedStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.selected},setActivatedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.activated=e)}},this.mdcAdapter}selectUi(t,e=!1){const i=this.items[t];i&&(i.selected=!0,i.activated=e)}deselectUi(t){const e=this.items[t];e&&(e.selected=!1,e.activated=!1)}select(t){this.mdcFoundation&&this.mdcFoundation.setSelectedIndex(t)}toggle(t,e){this.multi&&this.mdcFoundation.toggleMultiAtIndex(t,e)}onListItemConnected(t){const e=t.target;this.layout(-1===this.items.indexOf(e))}layout(t=!0){t&&this.updateItems();const e=this.items[0];for(const t of this.items)t.tabindex=-1;e&&(this.noninteractive?this.previousTabindex||(this.previousTabindex=e):e.tabindex=0),this.itemsReadyResolver()}getFocusedItemIndex(){if(!this.mdcRoot)return-1;if(!this.items.length)return-1;const t=$();if(!t.length)return-1;for(let e=t.length-1;e>=0;e--){const i=t[e];if(Xe(i))return this.items.indexOf(i)}return-1}focusItemAtIndex(t){for(const t of this.items)if(0===t.tabindex){t.tabindex=-1;break}this.items[t].tabindex=0,this.items[t].focus()}focus(){const t=this.mdcRoot;t&&t.focus()}blur(){const t=this.mdcRoot;t&&t.blur()}}Xt([e({type:String})],Ve.prototype,"emptyMessage",void 0),Xt([R(".mdc-deprecated-list")],Ve.prototype,"mdcRoot",void 0),Xt([R("slot")],Ve.prototype,"slotElement",void 0),Xt([e({type:Boolean}),it((function(t){this.mdcFoundation&&this.mdcFoundation.setUseActivatedClass(t)}))],Ve.prototype,"activatable",void 0),Xt([e({type:Boolean}),it((function(t,e){this.mdcFoundation&&this.mdcFoundation.setMulti(t),void 0!==e&&this.layout()}))],Ve.prototype,"multi",void 0),Xt([e({type:Boolean}),it((function(t){this.mdcFoundation&&this.mdcFoundation.setWrapFocus(t)}))],Ve.prototype,"wrapFocus",void 0),Xt([e({type:String}),it((function(t,e){void 0!==e&&this.updateItems()}))],Ve.prototype,"itemRoles",void 0),Xt([e({type:String})],Ve.prototype,"innerRole",void 0),Xt([e({type:String})],Ve.prototype,"innerAriaLabel",void 0),Xt([e({type:Boolean})],Ve.prototype,"rootTabbable",void 0),Xt([e({type:Boolean,reflect:!0}),it((function(t){const e=this.slotElement;if(t&&e){const t=z(e,'[tabindex="0"]');this.previousTabindex=t,t&&t.setAttribute("tabindex","-1")}else!t&&this.previousTabindex&&(this.previousTabindex.setAttribute("tabindex","0"),this.previousTabindex=null)}))],Ve.prototype,"noninteractive",void 0);const Ze=d`@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}:host{display:block}.mdc-deprecated-list{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-subtitle1-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1rem;font-size:var(--mdc-typography-subtitle1-font-size, 1rem);line-height:1.75rem;line-height:var(--mdc-typography-subtitle1-line-height, 1.75rem);font-weight:400;font-weight:var(--mdc-typography-subtitle1-font-weight, 400);letter-spacing:0.009375em;letter-spacing:var(--mdc-typography-subtitle1-letter-spacing, 0.009375em);text-decoration:inherit;text-decoration:var(--mdc-typography-subtitle1-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-subtitle1-text-transform, inherit);line-height:1.5rem;margin:0;padding:8px 0;list-style-type:none;color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));padding:var(--mdc-list-vertical-padding, 8px) 0}.mdc-deprecated-list:focus{outline:none}.mdc-deprecated-list-item{height:48px}.mdc-deprecated-list--dense{padding-top:4px;padding-bottom:4px;font-size:.812rem}.mdc-deprecated-list ::slotted([divider]){height:0;margin:0;border:none;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgba(0, 0, 0, 0.12)}.mdc-deprecated-list ::slotted([divider][padded]){margin:0 var(--mdc-list-side-padding, 16px)}.mdc-deprecated-list ::slotted([divider][inset]){margin-left:var(--mdc-list-inset-margin, 72px);margin-right:0;width:calc( 100% - var(--mdc-list-inset-margin, 72px) )}[dir=rtl] .mdc-deprecated-list ::slotted([divider][inset]),.mdc-deprecated-list ::slotted([divider][inset][dir=rtl]){margin-left:0;margin-right:var(--mdc-list-inset-margin, 72px)}.mdc-deprecated-list ::slotted([divider][inset][padded]){width:calc( 100% - var(--mdc-list-inset-margin, 72px) - var(--mdc-list-side-padding, 16px) )}.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:40px}.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 20px}.mdc-deprecated-list--two-line.mdc-deprecated-list--dense ::slotted([mwc-list-item]),.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:60px}.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 36px}:host([noninteractive]){pointer-events:none;cursor:default}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text){display:block;margin-top:0;line-height:normal;margin-bottom:-20px}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::before{display:inline-block;width:0;height:24px;content:"";vertical-align:0}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}`;let Ye=class extends Ve{};Ye.styles=Ze,Ye=Xt([l("mwc-list")],Ye);var Qe,Je,ti={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},ei={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},ii={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(Qe||(Qe={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(Je||(Je={}));var oi=function(t){function e(i){var o=t.call(this,L(L({},e.defaultAdapter),i))||this;return o.isSurfaceOpen=!1,o.isQuickOpen=!1,o.isHoistedElement=!1,o.isFixedPosition=!1,o.isHorizontallyCenteredOnViewport=!1,o.maxHeight=0,o.openAnimationEndTimerId=0,o.closeAnimationEndTimerId=0,o.animationRequestId=0,o.anchorCorner=Je.TOP_START,o.originCorner=Je.TOP_START,o.anchorMargin={top:0,right:0,bottom:0,left:0},o.position={x:0,y:0},o}return M(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return ti},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return ei},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return ii},enumerable:!1,configurable:!0}),Object.defineProperty(e,"Corner",{get:function(){return Je},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){},notifyClosing:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){var t=e.cssClasses,i=t.ROOT,o=t.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(o)&&(this.isSurfaceOpen=!0)},e.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},e.prototype.setAnchorCorner=function(t){this.anchorCorner=t},e.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^Qe.RIGHT},e.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},e.prototype.setIsHoisted=function(t){this.isHoistedElement=t},e.prototype.setFixedPosition=function(t){this.isFixedPosition=t},e.prototype.setAbsolutePosition=function(t,e){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(e)?e:0},e.prototype.setIsHorizontallyCenteredOnViewport=function(t){this.isHorizontallyCenteredOnViewport=t},e.prototype.setQuickOpen=function(t){this.isQuickOpen=t},e.prototype.setMaxHeight=function(t){this.maxHeight=t},e.prototype.isOpen=function(){return this.isSurfaceOpen},e.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(e.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(e.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.adapter.addClass(e.cssClasses.OPEN),t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(e.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),ii.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},e.prototype.close=function(t){var i=this;if(void 0===t&&(t=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(e.cssClasses.OPEN),this.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(e.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(e.cssClasses.OPEN),i.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(e.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),ii.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()}},e.prototype.handleBodyClick=function(t){var e=t.target;this.adapter.isElementInContainer(e)||this.close()},e.prototype.handleKeydown=function(t){var e=t.keyCode;("Escape"===t.key||27===e)&&this.close()},e.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),o=this.getMenuSurfaceMaxHeight(i),n=this.hasBit(i,Qe.BOTTOM)?"bottom":"top",s=this.hasBit(i,Qe.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(i),r=this.getVerticalOriginOffset(i),d=this.measurements,l=d.anchorSize,c=d.surfaceSize,h=((t={})[s]=a,t[n]=r,t);l.width/c.width>ii.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(s="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(h),this.adapter.setTransformOrigin(s+" "+n),this.adapter.setPosition(h),this.adapter.setMaxHeight(o?o+"px":""),this.hasBit(i,Qe.BOTTOM)||this.adapter.addClass(e.cssClasses.IS_OPEN_BELOW)},e.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),e=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),o=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:e,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:i.width-t.right,bottom:i.height-t.bottom,left:t.left},viewportSize:i,windowScroll:o}},e.prototype.getoriginCorner=function(){var t,i,o=this.originCorner,n=this.measurements,s=n.viewportDistance,a=n.anchorSize,r=n.surfaceSize,d=e.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,Qe.BOTTOM)?(t=s.top-d+this.anchorMargin.bottom,i=s.bottom-d-this.anchorMargin.bottom):(t=s.top-d+this.anchorMargin.top,i=s.bottom-d+a.height-this.anchorMargin.top),!(i-r.height>0)&&t>i&&(o=this.setBit(o,Qe.BOTTOM));var l,c,h=this.adapter.isRtl(),p=this.hasBit(this.anchorCorner,Qe.FLIP_RTL),m=this.hasBit(this.anchorCorner,Qe.RIGHT)||this.hasBit(o,Qe.RIGHT),u=!1;(u=h&&p?!m:m)?(l=s.left+a.width+this.anchorMargin.right,c=s.right-this.anchorMargin.right):(l=s.left+this.anchorMargin.left,c=s.right+a.width-this.anchorMargin.left);var f=l-r.width>0,g=c-r.width>0,v=this.hasBit(o,Qe.FLIP_RTL)&&this.hasBit(o,Qe.RIGHT);return g&&v&&h||!f&&v?o=this.unsetBit(o,Qe.RIGHT):(f&&u&&h||f&&!u&&m||!g&&l>=c)&&(o=this.setBit(o,Qe.RIGHT)),o},e.prototype.getMenuSurfaceMaxHeight=function(t){if(this.maxHeight>0)return this.maxHeight;var i=this.measurements.viewportDistance,o=0,n=this.hasBit(t,Qe.BOTTOM),s=this.hasBit(this.anchorCorner,Qe.BOTTOM),a=e.numbers.MARGIN_TO_EDGE;return n?(o=i.top+this.anchorMargin.top-a,s||(o+=this.measurements.anchorSize.height)):(o=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,s&&(o-=this.measurements.anchorSize.height)),o},e.prototype.getHorizontalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,Qe.RIGHT),o=this.hasBit(this.anchorCorner,Qe.RIGHT);if(i){var n=o?e.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?n-(this.measurements.viewportSize.width-this.measurements.bodySize.width):n}return o?e.width-this.anchorMargin.right:this.anchorMargin.left},e.prototype.getVerticalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,Qe.BOTTOM),o=this.hasBit(this.anchorCorner,Qe.BOTTOM);return i?o?e.height-this.anchorMargin.top:-this.anchorMargin.bottom:o?e.height+this.anchorMargin.bottom:this.anchorMargin.top},e.prototype.adjustPositionForHoistedElement=function(t){var e,i,o=this.measurements,n=o.windowScroll,s=o.viewportDistance,a=o.surfaceSize,r=o.viewportSize,d=Object.keys(t);try{for(var l=D(d),c=l.next();!c.done;c=l.next()){var h=c.value,p=t[h]||0;!this.isHorizontallyCenteredOnViewport||"left"!==h&&"right"!==h?(p+=s[h],this.isFixedPosition||("top"===h?p+=n.y:"bottom"===h?p-=n.y:"left"===h?p+=n.x:p-=n.x),t[h]=p):t[h]=(r.width-a.width)/2}}catch(t){e={error:t}}finally{try{c&&!c.done&&(i=l.return)&&i.call(l)}finally{if(e)throw e.error}}},e.prototype.maybeRestoreFocus=function(){var t=this.adapter.isFocused(),e=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(t||e)&&this.adapter.restoreFocus()},e.prototype.hasBit=function(t,e){return Boolean(t&e)},e.prototype.setBit=function(t,e){return t|e},e.prototype.unsetBit=function(t,e){return t^e},e.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},e}(S),ni=oi;const si={TOP_LEFT:Je.TOP_LEFT,TOP_RIGHT:Je.TOP_RIGHT,BOTTOM_LEFT:Je.BOTTOM_LEFT,BOTTOM_RIGHT:Je.BOTTOM_RIGHT,TOP_START:Je.TOP_START,TOP_END:Je.TOP_END,BOTTOM_START:Je.BOTTOM_START,BOTTOM_END:Je.BOTTOM_END};class ai extends F{constructor(){super(...arguments),this.mdcFoundationClass=ni,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=Je.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const t={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},e={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return a`
      <div
          class="mdc-menu-surface ${r(t)}"
          style="${P(e)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},H(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyClosing:()=>{const t=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>B(this),saveFocus:()=>{const t=$(),e=t.length;e||(this.previouslyFocused=null),this.previouslyFocused=t[e-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?t.left+"px":"",this.styleRight="right"in t?t.right+"px":"",this.styleTop="top"in t?t.top+"px":"",this.styleBottom="bottom"in t?t.bottom+"px":"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){if(this.stayOpenOnBodyClick)return;-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}close(){this.open=!1}show(){this.open=!0}}Kt([R(".mdc-menu-surface")],ai.prototype,"mdcRoot",void 0),Kt([R("slot")],ai.prototype,"slotElement",void 0),Kt([e({type:Boolean}),it((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],ai.prototype,"absolute",void 0),Kt([e({type:Boolean})],ai.prototype,"fullwidth",void 0),Kt([e({type:Boolean}),it((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(t)}))],ai.prototype,"fixed",void 0),Kt([e({type:Number}),it((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],ai.prototype,"x",void 0),Kt([e({type:Number}),it((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],ai.prototype,"y",void 0),Kt([e({type:Boolean}),it((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],ai.prototype,"quick",void 0),Kt([e({type:Boolean,reflect:!0}),it((function(t,e){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==e&&this.mdcFoundation.close())}))],ai.prototype,"open",void 0),Kt([e({type:Boolean})],ai.prototype,"stayOpenOnBodyClick",void 0),Kt([i(),it((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],ai.prototype,"bitwiseCorner",void 0),Kt([e({type:String}),it((function(t){if(this.mdcFoundation){const e="START"===t||"END"===t,i=null===this.previousMenuCorner,o=!i&&t!==this.previousMenuCorner,n=i&&"END"===t;e&&(o||n)&&(this.bitwiseCorner=this.bitwiseCorner^Qe.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],ai.prototype,"menuCorner",void 0),Kt([e({type:String}),it((function(t){if(this.mdcFoundation&&t){let e=si[t];"END"===this.menuCorner&&(e^=Qe.RIGHT),this.bitwiseCorner=e}}))],ai.prototype,"corner",void 0),Kt([i()],ai.prototype,"styleTop",void 0),Kt([i()],ai.prototype,"styleLeft",void 0),Kt([i()],ai.prototype,"styleRight",void 0),Kt([i()],ai.prototype,"styleBottom",void 0),Kt([i()],ai.prototype,"styleMaxHeight",void 0),Kt([i()],ai.prototype,"styleTransformOrigin",void 0);const ri=d`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let di=class extends ai{};di.styles=ri,di=Kt([l("mwc-menu-surface")],di);var li,ci={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},hi={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected"},pi={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(li||(li={}));var mi=function(t){function e(i){var o=t.call(this,L(L({},e.defaultAdapter),i))||this;return o.closeAnimationEndTimerId=0,o.defaultFocusState=li.LIST_ROOT,o}return M(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return ci},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return hi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return pi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,i=t.keyCode;("Tab"===e||9===i)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,i=this.adapter.getElementIndex(t);i<0||(this.adapter.notifySelected({index:i}),this.adapter.closeSurface(),this.closeAnimationEndTimerId=setTimeout((function(){var i=e.adapter.getElementIndex(t);i>=0&&e.adapter.isSelectableItemAtIndex(i)&&e.setSelectedIndex(i)}),oi.numbers.TRANSITION_CLOSE_DURATION))},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case li.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case li.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case li.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState=t},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,hi.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,ci.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,ci.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,hi.ARIA_CHECKED_ATTR,"true")},e.prototype.setEnabled=function(t,e){this.validatedIndex(t),e?(this.adapter.removeClassFromElementAtIndex(t,Ne),this.adapter.addAttributeToElementAtIndex(t,hi.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,Ne),this.adapter.addAttributeToElementAtIndex(t,hi.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(S);class ui extends F{constructor(){super(...arguments),this.mdcFoundationClass=mi,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){const t="menu"===this.innerRole?"menuitem":"option";return a`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-deprecated-list"
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!o.selected&&i.toggle(t,!0):o.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&("mdc-menu-item--selected"===e?o.selected&&i.toggle(t,!1):o.classList.remove(e))},addAttributeToElementAtIndex:(t,e,i)=>{const o=this.listElement;if(!o)return;const n=o.items[t];n&&n.setAttribute(e,i)},removeAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const o=i.items[t];o&&o.removeAttribute(e)},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const i=e.items[t];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const i=e.items[t];if(!i||!i.group)return-1;for(let o=0;o<e.items.length;o++){if(o===t)continue;const n=e.items[o];if(n.selected&&n.group===i.group)return o}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const i=e.items[t];return!!i&&i.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const i=t.detail.index,o=e.items[i];o&&this.mdcFoundation.handleItemAction(o)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async _getUpdateComplete(){return this.getUpdateComplete()}async getUpdateComplete(){let t=!1;return await this._listUpdateComplete,super.getUpdateComplete?t=await super.getUpdateComplete():await super._getUpdateComplete(),t}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}Kt([R(".mdc-menu")],ui.prototype,"mdcRoot",void 0),Kt([R("slot")],ui.prototype,"slotElement",void 0),Kt([e({type:Object})],ui.prototype,"anchor",void 0),Kt([e({type:Boolean,reflect:!0})],ui.prototype,"open",void 0),Kt([e({type:Boolean})],ui.prototype,"quick",void 0),Kt([e({type:Boolean})],ui.prototype,"wrapFocus",void 0),Kt([e({type:String})],ui.prototype,"innerRole",void 0),Kt([e({type:String})],ui.prototype,"corner",void 0),Kt([e({type:Number})],ui.prototype,"x",void 0),Kt([e({type:Number})],ui.prototype,"y",void 0),Kt([e({type:Boolean})],ui.prototype,"absolute",void 0),Kt([e({type:Boolean})],ui.prototype,"multi",void 0),Kt([e({type:Boolean})],ui.prototype,"activatable",void 0),Kt([e({type:Boolean})],ui.prototype,"fixed",void 0),Kt([e({type:Boolean})],ui.prototype,"forceGroupSelection",void 0),Kt([e({type:Boolean})],ui.prototype,"fullwidth",void 0),Kt([e({type:String})],ui.prototype,"menuCorner",void 0),Kt([e({type:Boolean})],ui.prototype,"stayOpenOnBodyClick",void 0),Kt([e({type:String}),it((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(li[t])}))],ui.prototype,"defaultFocus",void 0);const fi=d`mwc-list ::slotted([mwc-list-item]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let gi=class extends ui{};gi.styles=fi,gi=Kt([l("mwc-menu")],gi),c([l("ha-button-menu")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[e()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[e({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[e({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[e({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[e({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[R("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.items}},{kind:"get",key:"selected",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.selected}},{kind:"method",key:"render",value:function(){return a`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n),c([A("racelandshop-tabbed-menu")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[g({attribute:!1})],key:"configuration",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"racelandshop",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"status",value:void 0},{kind:"method",key:"render",value:function(){var t,e,i;return v`
      <ha-button-menu corner="BOTTOM_START" slot="toolbar-icon">
        <mwc-icon-button slot="trigger" alt="menu">
          <ha-svg-icon .path=${b}></ha-svg-icon>
        </mwc-icon-button>

        <mwc-list-item action="documentation">
          <racelandshop-link url="https://racelandshop.xyz/">
            ${this.racelandshop.localize("menu.documentation")}
          </racelandshop-link>
        </mwc-list-item>

        ${0!==(null===(t=this.repositories)||void 0===t?void 0:t.filter(t=>t.new).length)?v`<mwc-list-item @click=${this._clearAllNewRepositories}>
              ${this.racelandshop.localize("menu.dismiss")}
            </mwc-list-item>`:""}

        <mwc-list-item><racelandshop-link url="https://github.com/racelandshop">GitHub</racelandshop-link></mwc-list-item>
        <mwc-list-item>
          <racelandshop-link url="https://racelandshop.xyz/docs/issues"
            >${this.racelandshop.localize("menu.open_issue")}</racelandshop-link
          >
        </mwc-list-item>

        ${null!==(e=this.status)&&void 0!==e&&e.disabled||null!==(i=this.status)&&void 0!==i&&i.background_task?"":v`<mwc-list-item @click=${this._showCustomRepositoriesDialog}>
              ${this.racelandshop.localize("menu.custom_repositories")}
            </mwc-list-item>`}

        <mwc-list-item @click=${this._showAboutDialog}>
          ${this.racelandshop.localize("menu.about")}
        </mwc-list-item>
      </ha-button-menu>
    `}},{kind:"method",key:"_clearAllNewRepositories",value:async function(){var t;await U(this.hass,(null===(t=j(this.racelandshop.language,this.route))||void 0===t?void 0:t.categories)||[])}},{kind:"method",key:"_showAboutDialog",value:function(){tt(this,this.racelandshop)}},{kind:"method",key:"_showCustomRepositoriesDialog",value:function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"custom-repositories",repositories:this.repositories},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return I``}}]}}),f);let vi=c([A("racelandshop-store-panel")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[g({attribute:!1})],key:"filters",value:()=>({})},{kind:"field",decorators:[g({attribute:!1})],key:"racelandshop",value:void 0},{kind:"field",decorators:[g()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[g({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"isWide",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"repositories",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[g({attribute:!1})],key:"sections",value:void 0},{kind:"field",decorators:[g()],key:"section",value:void 0},{kind:"field",key:"_repositoriesInActiveSection",value(){return G((t,e)=>[(null==t?void 0:t.filter(t=>{var i,o,n;return(null===(i=this.racelandshop.sections)||void 0===i||null===(o=i.find(t=>t.id===e))||void 0===o||null===(n=o.categories)||void 0===n?void 0:n.includes(t.category))&&t.installed}))||[],(null==t?void 0:t.filter(t=>{var i,o,n;return(null===(i=this.racelandshop.sections)||void 0===i||null===(o=i.find(t=>t.id===e))||void 0===o||null===(n=o.categories)||void 0===n?void 0:n.includes(t.category))&&t.new&&!t.installed}))||[]])}},{kind:"get",key:"allRepositories",value:function(){const[t,e]=this._repositoriesInActiveSection(this.repositories,this.section);return e.concat(t)}},{kind:"field",key:"_filterRepositories",value:()=>G(Y)},{kind:"get",key:"visibleRepositories",value:function(){const t=this.allRepositories.filter(t=>{var e,i;return null===(e=this.filters[this.section])||void 0===e||null===(i=e.find(e=>e.id===t.category))||void 0===i?void 0:i.checked});return this._filterRepositories(t,this._searchInput)}},{kind:"method",key:"firstUpdated",value:async function(){this.addEventListener("filter-change",t=>this._updateFilters(t))}},{kind:"method",key:"_updateFilters",value:function(t){var e;const i=null===(e=this.filters[this.section])||void 0===e?void 0:e.find(e=>e.id===t.detail.id);this.filters[this.section].find(t=>t.id===i.id).checked=!i.checked,this.requestUpdate()}},{kind:"method",key:"render",value:function(){var t;if(!this.racelandshop)return v``;const e=this._repositoriesInActiveSection(this.repositories,this.section)[1];if(!this.filters[this.section]&&this.racelandshop.configuration.categories){var i;const t=null===(i=j(this.racelandshop.language,this.route))||void 0===i?void 0:i.categories;this.filters[this.section]=[],null==t||t.filter(t=>{var e;return null===(e=this.racelandshop.configuration)||void 0===e?void 0:e.categories.includes(t)}).forEach(t=>{this.filters[this.section].push({id:t,value:t,checked:!0})})}return v`<hass-tabs-subpage
      back-path="/racelandshop/entry"
      .hass=${this.hass}
      .narrow=${this.narrow}
      .route=${this.route}
      .tabs=${this.racelandshop.sections}
      hasFab
    >
      <racelandshop-tabbed-menu
        slot="toolbar-icon"
        .hass=${this.hass}
        .racelandshop=${this.racelandshop}
        .route=${this.route}
        .narrow=${this.narrow}
        .configuration=${this.racelandshop.configuration}
        .lovelace=${this.racelandshop.resources}
        .status=${this.racelandshop.status}
        .repositories=${this.repositories}
      >
      </racelandshop-tabbed-menu>
      ${this.narrow?v`
            <div slot="header">
              <slot name="header">
                <search-input
                  class="header"
                  no-label-float
                  .label=${this.racelandshop.localize("search.installed")}
                  .filter=${this._searchInput||""}
                  @value-changed=${this._inputValueChanged}
                ></search-input>
              </slot>
            </div>
          `:v`<div class="search">
            <search-input
              no-label-float
              .label=${0===e.length?this.racelandshop.localize("search.installed"):this.racelandshop.localize("search.installed_new")}
              .filter=${this._searchInput||""}
              @value-changed=${this._inputValueChanged}
            ></search-input>
          </div>`}
      <div class="content ${this.narrow?"narrow-content":""}">
        ${(null===(t=this.filters[this.section])||void 0===t?void 0:t.length)>1?v`<div class="filters">
              <racelandshop-filter
                .racelandshop=${this.racelandshop}
                .filters="${this.filters[this.section]}"
              ></racelandshop-filter>
            </div>`:""}
        ${(null==e?void 0:e.length)>10?v`<div class="new-repositories">
              ${this.racelandshop.localize("store.new_repositories_note")}
            </div>`:""}
        <div class="container ${this.narrow?"narrow":""}">
          ${void 0===this.repositories?"":0===this.allRepositories.length?this._renderEmpty():0===this.visibleRepositories.length?this._renderNoResultsFound():this._renderRepositories()}
        </div>
      </div>
      <ha-fab
        slot="fab"
        .label=${this.racelandshop.localize("store.add")}
        extended
        @click=${this._addRepository}
      >
        <ha-svg-icon slot="icon" .path=${W}></ha-svg-icon>
      </ha-fab>
    </hass-tabs-subpage>`}},{kind:"method",key:"_renderRepositories",value:function(){return this.visibleRepositories.map(t=>v`<racelandshop-repository-card
          .hass=${this.hass}
          .racelandshop=${this.racelandshop}
          .repository=${t}
          .narrow=${this.narrow}
          ?narrow=${this.narrow}
          .status=${this.racelandshop.status}
          .removed=${this.racelandshop.removed}
          .addedToLovelace=${this.racelandshop.addedToLovelace(this.racelandshop,t)}
        ></racelandshop-repository-card>`)}},{kind:"method",key:"_renderNoResultsFound",value:function(){return v`<ha-card class="no-repositories">
      <div class="header">${this.racelandshop.localize("store.no_repositories")} 😕</div>
      <p>
        ${this.racelandshop.localize("store.no_repositories_found_desc1").replace("{searchInput}",this._searchInput)}
        <br />
        ${this.racelandshop.localize("store.no_repositories_found_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_renderEmpty",value:function(){return v`<ha-card class="no-repositories">
      <div class="header">${this.racelandshop.localize("store.no_repositories")} 😕</div>
      <p>
        ${this.racelandshop.localize("store.no_repositories_desc1")}<br />${this.racelandshop.localize("store.no_repositories_desc2")}
      </p>
    </ha-card>`}},{kind:"method",key:"_inputValueChanged",value:function(t){this._searchInput=t.detail.value,window.localStorage.setItem("racelandshop-search",this._searchInput)}},{kind:"method",key:"_addRepository",value:function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog",{detail:{type:"add-repository",repositories:this.repositories,section:this.section},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[k,K,X,q,V,I`
        .filter {
          border-bottom: 1px solid var(--divider-color);
        }
        .content {
          height: calc(100vh - 128px);
          overflow: auto;
        }
        .narrow-content {
          height: calc(100vh - 128px);
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
          justify-items: center;
          grid-gap: 8px 8px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        .no-repositories {
          width: 100%;
          text-align: center;
          margin-top: 12px;
        }
        .new-repositories {
          margin: 4px 16px 0 16px;
          color: var(--hcv-text-color-primary);
        }
        racelandshop-repository-card {
          max-width: 500px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        racelandshop-repository-card[narrow] {
          width: 100%;
        }
        racelandshop-repository-card[narrow]:last-of-type {
          margin-bottom: 64px;
        }
        .narrow {
          width: 100%;
          display: block;
          padding: 0px;
          margin: 0;
        }

        .container .narrow {
          margin-bottom: 128px;
        }

        .bottom-bar {
          position: fixed !important;
        }
      `]}}]}}),f);export{vi as RacelandshopStorePanel};
