import{_ as i,H as s,e as t,T as e,i as a,a3 as o,a7 as r,a8 as l,n}from"./main-22e9dfb2.js";import"./c.0b4f23dc.js";import"./c.a6b3038d.js";import"./c.c2de2fed.js";let c=i([n("racelandshop-removed-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"_updating",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.active)return e``;const i=this.racelandshop.removed.find(i=>i.repository===this.repository.full_name);return e`
      <racelandshop-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.racelandshop.localize("entry.messages.removed",{repository:""})}
      >
        <div class="content">
          <div><b>${this.racelandshop.localize("dialog_removed.name")}:</b> ${this.repository.name}</div>
          ${i.removal_type?e` <div>
                <b>${this.racelandshop.localize("dialog_removed.type")}:</b> ${i.removal_type}
              </div>`:""}
          ${i.reason?e` <div>
                <b>${this.racelandshop.localize("dialog_removed.reason")}:</b> ${i.reason}
              </div>`:""}
          ${i.link?e`          <div>
            </b><racelandshop-link .url=${i.link}>${this.racelandshop.localize("dialog_removed.link")}</racelandshop-link>
          </div>`:""}
        </div>
        <mwc-button class="uninstall" slot="primaryaction" @click=${this._uninstallRepository}
          >${this._updating?e`<ha-circular-progress active size="small"></ha-circular-progress>`:this.racelandshop.localize("common.uninstall")}</mwc-button
        >
        <!--<mwc-button slot="secondaryaction" @click=${this._ignoreMessage}
          >${this.racelandshop.localize("common.ignore")}</mwc-button
        >-->
      </racelandshop-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      .uninstall {
        --mdc-theme-primary: var(--hcv-color-error);
      }
    `}},{kind:"method",key:"_lovelaceUrl",value:function(){var i,s;return`/racelandshopfiles/${null===(i=this.repository)||void 0===i?void 0:i.full_name.split("/")[1]}/${null===(s=this.repository)||void 0===s?void 0:s.file_name}`}},{kind:"method",key:"_uninstallRepository",value:async function(){if(this._updating=!0,"plugin"===this.repository.category&&this.racelandshop.status&&"yaml"!==this.racelandshop.status.lovelace_mode){(await o(this.hass)).filter(i=>i.url===this._lovelaceUrl()).forEach(i=>{r(this.hass,String(i.id))})}await l(this.hass,this.repository.id),this._updating=!1,this.active=!1}},{kind:"method",key:"_ignoreMessage",value:async function(){this._updating=!1,this.active=!1}}]}}),s);export{c as RacelandshopRemovedDialog};
