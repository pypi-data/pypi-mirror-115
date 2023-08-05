import{_ as e,h as a,d as i,o as s,f as t,ah as o,I as n,k as r,l,p as d,R as c,e as h,m as p,J as m,K as u,ai as v,T as g,aj as f,a1 as y,a2 as _,a3 as x,c as b,i as k,n as $}from"./main-adfe0fa2.js";import"./c.0b05eff9.js";import{e as w}from"./c.bfc48617.js";import{m as z}from"./c.e2af0952.js";import{u as j}from"./c.271b66e4.js";import"./c.afb2fde0.js";import"./c.1fecd8b4.js";import{s as R}from"./c.100a4a91.js";import"./c.95b81bea.js";import"./c.58bec4f5.js";const N=()=>new Promise(e=>{var a;a=e,requestAnimationFrame(()=>setTimeout(a,0))});e([d("ha-expansion-panel")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[s(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return t`
      <div class="summary" @click=${this._toggleContainer}>
        <slot name="header">${this.header}</slot>
        <ha-svg-icon
          .path=${o}
          class="summary-icon ${n({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${n({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
      >
        <slot></slot>
      </div>
    `}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height")}},{kind:"method",key:"_toggleContainer",value:async function(){const e=!this.expanded;r(this,"expanded-will-change",{expanded:e}),e&&await N();const a=this._container.scrollHeight;this._container.style.height=a+"px",e||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=e,r(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        padding: 0 8px;
      }

      .summary {
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: auto;
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .container {
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }
    `}}]}}),a);let T=e([$("racelandshop-update-dialog")],(function(e,a){class i extends a{constructor(...a){super(...a),e(this)}}return{F:i,d:[{kind:"field",decorators:[h()],key:"repository",value:void 0},{kind:"field",decorators:[h({type:Boolean})],key:"_updating",value:()=>!1},{kind:"field",decorators:[h()],key:"_error",value:void 0},{kind:"field",decorators:[h({attribute:!1})],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>p((e,a)=>e.find(e=>e.id===a))},{kind:"method",key:"firstUpdated",value:async function(e){m(u(i.prototype),"firstUpdated",this).call(this,e);const a=this._getRepository(this.repositories,this.repository);a&&("commit"!==a.version_or_commit&&(this._releaseNotes=await v(this.hass,a.id),this._releaseNotes=this._releaseNotes.filter(e=>e.tag>a.installed_version)),this.hass.connection.subscribeEvents(e=>this._error=e.data,"racelandshop/error"))}},{kind:"method",key:"render",value:function(){if(!this.active)return g``;const e=this._getRepository(this.repositories,this.repository);return e?g`
      <racelandshop-dialog
        .active=${this.active}
        .title=${this.racelandshop.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${w({content:!0,narrow:this.narrow})}>
          <p class="message">
            ${this.racelandshop.localize("dialog_update.message",{name:e.name})}
          </p>
          <div class="version-container">
            <div class="version-element">
              <span class="version-number">${e.installed_version}</span>
              <small class="version-text">${this.racelandshop.localize("dialog_update.installed_version")}</small>
            </div>

            <span class="version-separator">
              <ha-svg-icon
                .path=${f}
              ></ha-svg-icon>
            </span>

            <div class="version-element">
                <span class="version-number">${e.available_version}</span>
                <small class="version-text">${this.racelandshop.localize("dialog_update.available_version")}</small>
              </div>
            </div>
          </div>

          ${this._releaseNotes.length>0?this._releaseNotes.map(a=>g`
                    <ha-expansion-panel
                      .header=${a.name&&a.name!==a.tag?`${a.tag}: ${a.name}`:a.tag}
                      outlined
                      ?expanded=${1===this._releaseNotes.length}
                    >
                      ${a.body?z.html(a.body,e):this.racelandshop.localize("dialog_update.no_info")}
                    </ha-expansion-panel>
                  `):""}
          ${e.can_install?"":g`<p class="error">
                  ${this.racelandshop.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",e.homeassistant)}
                </p>`}
          ${"integration"===e.category?g`<p>${this.racelandshop.localize("dialog_install.restart")}</p>`:""}
          ${this._error?g`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!e.can_install}
          @click=${this._updateRepository}
          >${this._updating?g`<ha-circular-progress active size="small"></ha-circular-progress>`:this.racelandshop.localize("common.update")}</mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <racelandshop-link .url=${this._getChanglogURL()}
            ><mwc-button>${this.racelandshop.localize("dialog_update.changelog")}</mwc-button></racelandshop-link
          >
          <racelandshop-link .url="https://github.com/${e.full_name}"
            ><mwc-button>${this.racelandshop.localize("common.repository")}</mwc-button></racelandshop-link
          >
        </div>
      </racelandshop-dialog>
    `:g``}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const e=this._getRepository(this.repositories,this.repository);e&&("commit"!==e.version_or_commit?await y(this.hass,e.id,e.available_version):await _(this.hass,e.id),"plugin"===e.category&&"storage"===this.racelandshop.status.lovelace_mode&&await j(this.hass,e,e.available_version),this._updating=!1,this.dispatchEvent(new Event("racelandshop-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===e.category&&R(this,{title:this.racelandshop.localize("common.reload"),text:g`${this.racelandshop.localize("dialog.reload.description")}</br>${this.racelandshop.localize("dialog.reload.confirm")}`,dismissText:this.racelandshop.localize("common.cancel"),confirmText:this.racelandshop.localize("common.reload"),confirm:()=>{x.location.href=x.location.href}}))}},{kind:"method",key:"_getChanglogURL",value:function(){const e=this._getRepository(this.repositories,this.repository);if(e)return"commit"===e.version_or_commit?`https://github.com/${e.full_name}/compare/${e.installed_version}...${e.available_version}`:`https://github.com/${e.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[b,k`
        .content {
          width: 360px;
          display: contents;
        }
        .error {
          color: var(--racelandshop-error-color, var(--google-red-500));
        }
        ha-expansion-panel {
          margin: 8px 0;
        }
        ha-expansion-panel[expanded] {
          padding-bottom: 16px;
        }

        .secondary {
          display: flex;
        }
        .message {
          text-align: center;
          margin: 0;
        }
        .version-container {
          margin: 24px 0 12px 0;
          width: 360px;
          min-width: 100%;
          max-width: 100%;
          display: flex;
          flex-direction: row;
        }
        .version-element {
          display: flex;
          flex-direction: column;
          flex: 1;
          padding: 0 12px;
          text-align: center;
        }
        .version-text {
          color: var(--secondary-text-color);
        }
        .version-number {
          font-size: 1.5rem;
          margin-bottom: 4px;
        }
      `]}}]}}),c);export{T as RacelandshopUpdateDialog};
