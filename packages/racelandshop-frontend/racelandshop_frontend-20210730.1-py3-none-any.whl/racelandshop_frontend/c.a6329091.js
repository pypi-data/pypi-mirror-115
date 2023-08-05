import{_ as i,R as e,e as a,T as s,i as t,aa as o,af as r,ag as l,n}from"./main-adfe0fa2.js";import"./c.1fecd8b4.js";import"./c.95b81bea.js";import"./c.58bec4f5.js";let c=i([n("racelandshop-removed-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"_updating",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.active)return s``;const i=this.racelandshop.removed.find(i=>i.repository===this.repository.full_name);return s`
      <racelandshop-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.racelandshop.localize("entry.messages.removed",{repository:""})}
      >
        <div class="content">
          <div><b>${this.racelandshop.localize("dialog_removed.name")}:</b> ${this.repository.name}</div>
          ${i.removal_type?s` <div>
                <b>${this.racelandshop.localize("dialog_removed.type")}:</b> ${i.removal_type}
              </div>`:""}
          ${i.reason?s` <div>
                <b>${this.racelandshop.localize("dialog_removed.reason")}:</b> ${i.reason}
              </div>`:""}
          ${i.link?s`          <div>
            </b><racelandshop-link .url=${i.link}>${this.racelandshop.localize("dialog_removed.link")}</racelandshop-link>
          </div>`:""}
        </div>
        <mwc-button class="uninstall" slot="primaryaction" @click=${this._uninstallRepository}
          >${this._updating?s`<ha-circular-progress active size="small"></ha-circular-progress>`:this.racelandshop.localize("common.uninstall")}</mwc-button
        >
        <!--<mwc-button slot="secondaryaction" @click=${this._ignoreMessage}
          >${this.racelandshop.localize("common.ignore")}</mwc-button
        >-->
      </racelandshop-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return t`
      .uninstall {
        --mdc-theme-primary: var(--hcv-color-error);
      }
    `}},{kind:"method",key:"_lovelaceUrl",value:function(){var i,e;return`/racelandshopfiles/${null===(i=this.repository)||void 0===i?void 0:i.full_name.split("/")[1]}/${null===(e=this.repository)||void 0===e?void 0:e.file_name}`}},{kind:"method",key:"_uninstallRepository",value:async function(){if(this._updating=!0,"plugin"===this.repository.category&&this.racelandshop.status&&"yaml"!==this.racelandshop.status.lovelace_mode){(await o(this.hass)).filter(i=>i.url===this._lovelaceUrl()).forEach(i=>{r(this.hass,String(i.id))})}await l(this.hass,this.repository.id),this._updating=!1,this.active=!1}},{kind:"method",key:"_ignoreMessage",value:async function(){this._updating=!1,this.active=!1}}]}}),e);export{c as RacelandshopRemovedDialog};
