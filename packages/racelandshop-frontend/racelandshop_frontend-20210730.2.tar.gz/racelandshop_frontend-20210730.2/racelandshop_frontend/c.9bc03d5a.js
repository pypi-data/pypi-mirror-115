import{_ as i,H as s,e as t,m as o,R as e,L as a,T as r,ac as c,ad as h,ae as n,af as l,ag as d,d as p,i as u,n as y}from"./main-22e9dfb2.js";import{m as _}from"./c.2d4b5637.js";import"./c.6565b5e2.js";import"./c.c04c5224.js";import"./c.0b4f23dc.js";import"./c.a6b3038d.js";import"./c.c2de2fed.js";let m=i([y("racelandshop-repository-info-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[t()],key:"repository",value:void 0},{kind:"field",decorators:[t()],key:"_repository",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((i,s)=>null==i?void 0:i.find(i=>i.id===s))},{kind:"field",key:"_getAuthors",value:()=>o(i=>{const s=[];if(!i.authors)return s;if(i.authors.forEach(i=>s.push(i.replace("@",""))),0===s.length){const t=i.full_name.split("/")[0];if(["custom-cards","custom-components","home-assistant-community-themes"].includes(t))return s;s.push(t)}return s})},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach((i,s)=>{"hass"===s&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===s&&(this._repository=this._getRepository(this.repositories,this.repository))}),i.has("sidebarDocked")||i.has("narrow")||i.has("active")||i.has("_repository")}},{kind:"method",key:"firstUpdated",value:async function(){this._repository=this._getRepository(this.repositories,this.repository),this._repository.updated_info||(await e(this.hass,this._repository.id),this.repositories=await a(this.hass))}},{kind:"method",key:"render",value:function(){if(!this.active)return r``;const i=this._getAuthors(this._repository);return r`
      <racelandshop-dialog
        .noActions=${this._repository.installed}
        .active=${this.active}
        .title=${this._repository.name||""}
        .hass=${this.hass}
        ><div class="content scroll">
          ${this._repository.updated_info?r`
            <div class="chips">
              ${this._repository.installed?r`<racelandshop-chip
                    title="${this.racelandshop.localize("dialog_info.version_installed")}"
                    .icon=${c}
                    .value=${this._repository.installed_version}
                  ></racelandshop-chip>`:""}
              ${i?i.map(i=>r`<racelandshop-chip
                      title="${this.racelandshop.localize("dialog_info.author")}"
                      .url="https://github.com/${i}"
                      .icon=${h}
                      .value="@${i}"
                    ></racelandshop-chip>`):""}
              ${this._repository.downloads?r` <racelandshop-chip
                    title="${this.racelandshop.localize("dialog_info.downloads")}"
                    .icon=${n}
                    .value=${this._repository.downloads}
                  ></racelandshop-chip>`:""}
              <racelandshop-chip
                title="${this.racelandshop.localize("dialog_info.stars")}"
                .icon=${l}
                .value=${this._repository.stars}
              ></racelandshop-chip>
              <racelandshop-chip
                title="${this.racelandshop.localize("dialog_info.open_issues")}"
                .icon=${d}
                .value=${this._repository.issues}
                .url="https://github.com/${this._repository.full_name}/issues"
              ></racelandshop-chip>
            </div>
            ${_.html(this._repository.additional_info||this.racelandshop.localize("dialog_info.no_info"),this._repository)}`:r`
            <div class="loading">
              <ha-circular-progress active size="large"></ha-circular-progress>
            </div>
          `}
        </div>
        ${!this._repository.installed&&this._repository.updated_info?r`
              <mwc-button slot="primaryaction" @click=${this._installRepository}
                >${this.racelandshop.localize("dialog_info.install")}</mwc-button
              ><racelandshop-link
                slot="secondaryaction"
                .url="https://github.com/${this._repository.full_name}"
                ><mwc-button>${this.racelandshop.localize("dialog_info.open_repo")}</mwc-button></racelandshop-link
              >
            `:""}
      </racelandshop-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[p,u`
        .content {
          width: 100%;
          overflow: auto;
        }
        img {
          max-width: 100%;
        }
        .loading {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 4rem 8rem;
        }
        .chips {
          display: flex;
          padding-bottom: 8px;
        }
        racelandshop-chip {
          margin: 0 4px;
        }
        div.chips racelandshop-link {
          margin: -24px 4px;
        }
        racelandshop-link mwc-button {
          margin-top: -18px;
        }
      `]}},{kind:"method",key:"_installRepository",value:async function(){this.dispatchEvent(new CustomEvent("racelandshop-dialog-secondary",{detail:{type:"install",repository:this._repository.id},bubbles:!0,composed:!0}))}}]}}),s);export{m as RacelandshopRepositoryDialog};
