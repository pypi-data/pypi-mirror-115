import{C as e,D as t,M as i,d as o,o as r,E as a,X as s,f as n,I as l,l as c,p as d,_ as p,R as h,e as m,Y as f,m as g,Z as y,U as u,T as v,$ as b,a0 as _,a1 as w,a2 as k,a3 as x,i as $,n as R}from"./main-adfe0fa2.js";import"./c.b9197e79.js";import"./c.097b259a.js";import"./c.b51cea2a.js";import{F as z}from"./c.4f8fa8c3.js";import{o as E}from"./c.58bec4f5.js";import"./c.acd02a7e.js";import{s as j}from"./c.100a4a91.js";import{u as I}from"./c.271b66e4.js";import"./c.afb2fde0.js";import"./c.1fecd8b4.js";import"./c.78fa9899.js";import"./c.95b81bea.js";function C(e,t,i,o){var r,a=arguments.length,s=a<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,o);else for(var n=e.length-1;n>=0;n--)(r=e[n])&&(s=(a<3?r(s):a>3?r(t,i,s):r(t,i))||s);return a>3&&s&&Object.defineProperty(t,i,s),s}var B={ROOT:"mdc-form-field"},O={LABEL_SELECTOR:".mdc-form-field > label"},P=function(i){function o(e){var r=i.call(this,t(t({},o.defaultAdapter),e))||this;return r.click=function(){r.handleClick()},r}return e(o,i),Object.defineProperty(o,"cssClasses",{get:function(){return B},enumerable:!1,configurable:!0}),Object.defineProperty(o,"strings",{get:function(){return O},enumerable:!1,configurable:!0}),Object.defineProperty(o,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),o.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},o.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},o.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},o}(i);class T extends a{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=P}createAdapter(){return{registerInteractionHandler:(e,t)=>{this.labelEl.addEventListener(e,t)},deregisterInteractionHandler:(e,t)=>{this.labelEl.removeEventListener(e,t)},activateInputRipple:async()=>{const e=this.input;if(e instanceof z){const t=await e.ripple;t&&t.startPress()}},deactivateInputRipple:async()=>{const e=this.input;if(e instanceof z){const t=await e.ripple;t&&t.endPress()}}}}get input(){return s(this.slotEl,"*")}render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return n`
      <div class="mdc-form-field ${l(e)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const e=this.input;e&&(e.focus(),e.click())}}C([o({type:Boolean})],T.prototype,"alignEnd",void 0),C([o({type:Boolean})],T.prototype,"spaceBetween",void 0),C([o({type:Boolean})],T.prototype,"nowrap",void 0),C([o({type:String}),E((async function(e){const t=this.input;t&&("input"===t.localName?t.setAttribute("aria-label",e):t instanceof z&&(await t.updateComplete,t.setAriaLabel(e)))}))],T.prototype,"label",void 0),C([r(".mdc-form-field")],T.prototype,"mdcRoot",void 0),C([r("slot")],T.prototype,"slotEl",void 0),C([r("label")],T.prototype,"labelEl",void 0);const A=c`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`;let H=class extends T{};H.styles=A,H=C([d("mwc-formfield")],H),p([d("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"get",static:!0,key:"styles",value:function(){return[H.styles,c`
        :host(:not([alignEnd])) ::slotted(ha-switch) {
          margin-right: 10px;
        }
        :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {
          margin-left: 10px;
          margin-right: auto;
        }
      `]}}]}}),H);let L=p([R("racelandshop-install-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[m()],key:"repository",value:void 0},{kind:"field",decorators:[m()],key:"_repository",value:void 0},{kind:"field",decorators:[m()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[m()],key:"_installing",value:()=>!1},{kind:"field",decorators:[m()],key:"_error",value:void 0},{kind:"field",decorators:[f()],key:"_version",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return e.forEach((e,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===t&&(this._repository=this._getRepository(this.repositories,this.repository))}),e.has("sidebarDocked")||e.has("narrow")||e.has("active")||e.has("_toggle")||e.has("_error")||e.has("_version")||e.has("_repository")||e.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>g((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"field",key:"_getInstallPath",value:()=>g(e=>{let t=e.local_path;return"theme"===e.category&&(t=`${t}/${e.file_name}`),t})},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await y(this.hass,this._repository.id),this.repositories=await u(this.hass)),this._toggle=!1,this.hass.connection.subscribeEvents(e=>this._error=e.data,"racelandshop/error")}},{kind:"method",key:"render",value:function(){if(!this.active||!this._repository)return v``;const e=this._getInstallPath(this._repository);return v`
      <racelandshop-dialog
        .active=${this.active}
        .narrow=${this.narrow}
        .hass=${this.hass}
        .secondary=${this.secondary}
        .title=${this._repository.name}
        dynamicHeight
      >
        <div class="content">
          ${"version"===this._repository.version_or_commit?v`<div class="beta-container">
                  <ha-formfield .label=${this.racelandshop.localize("dialog_install.show_beta")}>
                    <ha-switch
                      ?disabled=${this._toggle}
                      .checked=${this._repository.beta}
                      @change=${this._toggleBeta}
                    ></ha-switch>
                  </ha-formfield>
                </div>
                <div class="version-select-container">
                  <ha-paper-dropdown-menu
                    ?disabled=${this._toggle}
                    class="version-select-dropdown"
                    label="${this.racelandshop.localize("dialog_install.select_version")}"
                  >
                    <paper-listbox
                      id="version"
                      class="version-select-list"
                      slot="dropdown-content"
                      selected="0"
                      @iron-select=${this._versionSelectChanged}
                    >
                      ${this._repository.releases.map(e=>v`<paper-item .version=${e} class="version-select-item"
                            >${e}</paper-item
                          >`)}
                      ${"racelandshop/integration"===this._repository.full_name||this._repository.hide_default_branch?"":v`
                            <paper-item
                              .version=${this._repository.default_branch}
                              class="version-select-item"
                              >${this._repository.default_branch}</paper-item
                            >
                          `}
                    </paper-listbox>
                  </ha-paper-dropdown-menu>
                </div>`:""}
          ${this._repository.can_install?"":v`<p class="error">
                ${this.racelandshop.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",this._repository.homeassistant)}
              </p>`}
          <div class="note">
            ${this.racelandshop.localize("repository.note_installed")}
            <code>'${e}'</code>
            ${"plugin"===this._repository.category&&"storage"!==this.racelandshop.status.lovelace_mode?v`
                  <p>${this.racelandshop.localize("repository.lovelace_instruction")}</p>
                  <pre>
                url: ${b({repository:this._repository,skipTag:!0})}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?v`<p>${this.racelandshop.localize("dialog_install.restart")}</p>`:""}
          </div>
          ${this._error?v`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!this._repository.can_install||this._toggle}
          @click=${this._installRepository}
          >${this._installing?v`<ha-circular-progress active size="small"></ha-circular-progress>`:this.racelandshop.localize("common.install")}</mwc-button
        >
        <racelandshop-link slot="secondaryaction" .url="https://github.com/${this._repository.full_name}"
          ><mwc-button>${this.racelandshop.localize("common.repository")}</mwc-button></racelandshop-link
        >
      </racelandshop-dialog>
    `}},{kind:"method",key:"_versionSelectChanged",value:function(e){e.currentTarget.selectedItem.version!==this._version&&(this._version=e.currentTarget.selectedItem.version)}},{kind:"method",key:"_toggleBeta",value:async function(){this._toggle=!0,await _(this.hass,this.repository),this.repositories=await u(this.hass),this._toggle=!1}},{kind:"method",key:"_installRepository",value:async function(){var e;if(this._installing=!0,this._repository){if("commit"!==(null===(e=this._repository)||void 0===e?void 0:e.version_or_commit)){const e=this._version||this._repository.available_version||this._repository.default_branch;await w(this.hass,this._repository.id,e)}else await k(this.hass,this._repository.id);this.racelandshop.log.debug(this._repository.category,"_installRepository"),this.racelandshop.log.debug(this.racelandshop.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.racelandshop.status.lovelace_mode&&await I(this.hass,this._repository,this._version),this._installing=!1,this.dispatchEvent(new Event("racelandshop-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("racelandshop-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&"storage"===this.racelandshop.status.lovelace_mode&&j(this,{title:this.racelandshop.localize("common.reload"),text:v`${this.racelandshop.localize("dialog.reload.description")}</br>${this.racelandshop.localize("dialog.reload.confirm")}`,dismissText:this.racelandshop.localize("common.cancel"),confirmText:this.racelandshop.localize("common.reload"),confirm:()=>{x.location.href=x.location.href}})}}},{kind:"get",static:!0,key:"styles",value:function(){return[$`
        .version-select-dropdown {
          width: 100%;
        }
        .content {
          padding: 32px 8px;
        }
        .note {
          margin-bottom: -32px;
          margin-top: 12px;
        }
        .lovelace {
          margin-top: 8px;
        }
        .error {
          color: var(--racelandshop-error-color, var(--google-red-500));
        }
        paper-menu-button {
          color: var(--secondary-text-color);
          padding: 0;
        }
        paper-item {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
        }
        pre {
          white-space: pre-line;
          user-select: all;
        }
      `]}}]}}),h);export{L as RacelandshopInstallDialog};
