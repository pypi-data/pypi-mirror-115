import{_ as e,k as a,e as s,o as i,T as o,ab as t,b as n,q as r,i as l,n as d,R as c,m as h,F as p,G as m,ac as u,ad as v,W as g,X as y,Y as f,d as _}from"./main-0b50267d.js";import{m as x}from"./c.a1faf29f.js";import{u as b}from"./c.1d384d2f.js";import"./c.15cfaaaf.js";import"./c.e0fc9930.js";import{s as k}from"./c.48a1c043.js";import"./c.9f29b77f.js";import"./c.2b0d6d1d.js";const $=()=>new Promise(e=>{var a;a=e,requestAnimationFrame(()=>setTimeout(a,0))});e([d("ha-expansion-panel")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[s({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[s({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[s()],key:"header",value:void 0},{kind:"field",decorators:[s()],key:"secondary",value:void 0},{kind:"field",decorators:[i(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return o`
      <div class="summary" @click=${this._toggleContainer}>
        <slot class="header" name="header">
          ${this.header}
          <slot class="secondary" name="secondary">${this.secondary}</slot>
        </slot>
        <ha-svg-icon
          .path=${t}
          class="summary-icon ${n({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${n({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
      >
        <slot></slot>
      </div>
    `}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height")}},{kind:"method",key:"_toggleContainer",value:async function(){const e=!this.expanded;r(this,"expanded-will-change",{expanded:e}),e&&await $();const a=this._container.scrollHeight;this._container.style.height=a+"px",e||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=e,r(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
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

      .header {
        display: block;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),a);let w=e([d("racelandshop-update-dialog")],(function(e,a){class i extends a{constructor(...a){super(...a),e(this)}}return{F:i,d:[{kind:"field",decorators:[s()],key:"repository",value:void 0},{kind:"field",decorators:[s({type:Boolean})],key:"_updating",value:()=>!1},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>h((e,a)=>e.find(e=>e.id===a))},{kind:"method",key:"firstUpdated",value:async function(e){p(m(i.prototype),"firstUpdated",this).call(this,e);const a=this._getRepository(this.repositories,this.repository);a&&("commit"!==a.version_or_commit&&(this._releaseNotes=await u(this.hass,a.id),this._releaseNotes=this._releaseNotes.filter(e=>e.tag>a.installed_version)),this.hass.connection.subscribeEvents(e=>this._error=e.data,"racelandshop/error"))}},{kind:"method",key:"render",value:function(){if(!this.active)return o``;const e=this._getRepository(this.repositories,this.repository);return e?o`
      <racelandshop-dialog
        .active=${this.active}
        .title=${this.racelandshop.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${n({content:!0,narrow:this.narrow})}>
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
                .path=${v}
              ></ha-svg-icon>
            </span>

            <div class="version-element">
                <span class="version-number">${e.available_version}</span>
                <small class="version-text">${this.racelandshop.localize("dialog_update.available_version")}</small>
              </div>
            </div>
          </div>

          ${this._releaseNotes.length>0?this._releaseNotes.map(a=>o`
                    <ha-expansion-panel
                      .header=${a.name&&a.name!==a.tag?`${a.tag}: ${a.name}`:a.tag}
                      outlined
                      ?expanded=${1===this._releaseNotes.length}
                    >
                      ${a.body?x.html(a.body,e):this.racelandshop.localize("dialog_update.no_info")}
                    </ha-expansion-panel>
                  `):""}
          ${e.can_install?"":o`<p class="error">
                  ${this.racelandshop.localize("confirm.home_assistant_version_not_correct").replace("{haversion}",this.hass.config.version).replace("{minversion}",e.homeassistant)}
                </p>`}
          ${"integration"===e.category?o`<p>${this.racelandshop.localize("dialog_install.restart")}</p>`:""}
          ${this._error?o`<div class="error">${this._error.message}</div>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!e.can_install}
          @click=${this._updateRepository}
          >${this._updating?o`<ha-circular-progress active size="small"></ha-circular-progress>`:this.racelandshop.localize("common.update")}</mwc-button
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
    `:o``}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const e=this._getRepository(this.repositories,this.repository);e&&("commit"!==e.version_or_commit?await g(this.hass,e.id,e.available_version):await y(this.hass,e.id),"plugin"===e.category&&"storage"===this.racelandshop.status.lovelace_mode&&await b(this.hass,e,e.available_version),this._updating=!1,this.dispatchEvent(new Event("racelandshop-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===e.category&&k(this,{title:this.racelandshop.localize("common.reload"),text:o`${this.racelandshop.localize("dialog.reload.description")}</br>${this.racelandshop.localize("dialog.reload.confirm")}`,dismissText:this.racelandshop.localize("common.cancel"),confirmText:this.racelandshop.localize("common.reload"),confirm:()=>{f.location.href=f.location.href}}))}},{kind:"method",key:"_getChanglogURL",value:function(){const e=this._getRepository(this.repositories,this.repository);if(e)return"commit"===e.version_or_commit?`https://github.com/${e.full_name}/compare/${e.installed_version}...${e.available_version}`:`https://github.com/${e.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[_,l`
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
      `]}}]}}),c);export{w as RacelandshopUpdateDialog};
