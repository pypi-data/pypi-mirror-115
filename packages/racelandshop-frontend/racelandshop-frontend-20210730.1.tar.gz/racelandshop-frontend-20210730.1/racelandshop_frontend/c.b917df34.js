import{_ as o,R as i,e,O as t,T as r,b as a,Q as s,S as n,U as d,V as c,c as l,i as p,n as h}from"./main-adfe0fa2.js";import"./c.b9197e79.js";import"./c.097b259a.js";import"./c.b51cea2a.js";import"./c.acd02a7e.js";import"./c.1fecd8b4.js";import"./c.58bec4f5.js";import"./c.78fa9899.js";import"./c.95b81bea.js";let u=o([h("racelandshop-custom-repositories-dialog")],(function(o,i){return{F:class extends i{constructor(...i){super(...i),o(this)}},d:[{kind:"field",decorators:[e()],key:"_inputRepository",value:void 0},{kind:"field",decorators:[e()],key:"_error",value:void 0},{kind:"field",decorators:[t("#add-input")],key:"_addInput",value:void 0},{kind:"field",decorators:[t("#category")],key:"_addCategory",value:void 0},{kind:"method",key:"shouldUpdate",value:function(o){return o.has("narrow")||o.has("active")||o.has("_error")||o.has("repositories")}},{kind:"method",key:"render",value:function(){var o;if(!this.active)return r``;const i=null===(o=this.repositories)||void 0===o?void 0:o.filter(o=>o.custom);return r`
      <racelandshop-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.racelandshop.localize("dialog_custom_repositories.title")}
        hideActions
      >
        <div class="content">
          <div class="list">
            ${this._error?r`<div class="error">${this._error.message}</div>`:""}
            ${null==i?void 0:i.filter(o=>this.racelandshop.configuration.categories.includes(o.category)).map(o=>r`<paper-icon-item>
                  ${"integration"===o.category?r`
                        <img
                          loading="lazy"
                          src="https://brands.home-assistant.io/_/${o.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${a} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body
                    @click=${()=>this._showReopsitoryInfo(String(o.id))}
                    three-line
                    >${o.name}
                    <div secondary>${o.description}</div>
                    <div secondary>Category: ${o.category}</div></paper-item-body
                  >
                  <mwc-icon-button @click=${()=>this._removeRepository(o.id)}>
                    <ha-svg-icon class="delete" .path=${s}></ha-svg-icon>
                  </mwc-icon-button>
                </paper-icon-item>`)}
          </div>
        </div>
        <div class="add-repository" ?narrow=${this.narrow}>
          <input
            id="add-input"
            class="add-input"
            slot="secondaryaction"
            placeholder="${this.racelandshop.localize("dialog_custom_repositories.url_placeholder")}"
            .value=${this._inputRepository||""}
            @input=${this._inputValueChanged}
            ?narrow=${this.narrow}
          />

          <ha-paper-dropdown-menu
            ?narrow=${this.narrow}
            class="category"
            label="${this.racelandshop.localize("dialog_custom_repositories.category")}"
          >
            <paper-listbox id="category" slot="dropdown-content" selected="-1">
              ${this.racelandshop.configuration.categories.map(o=>r`
                  <paper-item class="categoryitem" .category=${o}>
                    ${this.racelandshop.localize("common."+o)}
                  </paper-item>
                `)}
            </paper-listbox>
          </ha-paper-dropdown-menu>
          <mwc-button
            ?narrow=${this.narrow}
            slot="primaryaction"
            raised
            @click=${this._addRepository}
          >
            ${this.racelandshop.localize("common.add")}
          </mwc-button>
        </div>
      </racelandshop-dialog>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.hass.connection.subscribeEvents(o=>this._error=o.data,"racelandshop/error")}},{kind:"method",key:"_inputValueChanged",value:function(){var o;this._inputRepository=null===(o=this._addInput)||void 0===o?void 0:o.value}},{kind:"method",key:"_addRepository",value:async function(){var o,i;this._error=void 0;const e=this._inputRepository,t=null===(o=this._addCategory)||void 0===o||null===(i=o.selectedItem)||void 0===i?void 0:i.category;t?e?(await n(this.hass,e,t),this.repositories=await d(this.hass)):this._error={message:this.racelandshop.localize("dialog_custom_repositories.no_repository")}:this._error={message:this.racelandshop.localize("dialog_custom_repositories.no_category")}}},{kind:"method",key:"_removeRepository",value:async function(o){this._error=void 0,await c(this.hass,o),this.repositories=await d(this.hass)}},{kind:"method",key:"_onImageLoad",value:function(o){o.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(o){o.target.outerHTML='<ha-icon\n      icon="mdi:github-circle"\n      slot="item-icon"\n    ></ha-icon>'}},{kind:"method",key:"_showReopsitoryInfo",value:async function(o){this.dispatchEvent(new CustomEvent("racelandshop-dialog-secondary",{detail:{type:"repository-info",repository:o},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l,p`
        .content {
          width: 1024px;
          display: contents;
        }
        .list {
          position: relative;
          margin-top: 16px;
          max-height: 870px;
          overflow: auto;
        }
        ha-icon {
          color: var(--secondary-text-color);
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
          position: absolute;
        }
        .delete {
          color: var(--racelandshop-error-color, var(--google-red-500));
        }
        paper-item-body {
          cursor: pointer;
        }
        .error {
          line-height: 0px;
          margin: 12px;
          color: var(--racelandshop-error-color, var(--google-red-500, red));
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add-repository {
          display: grid;
          width: 100%;
          justify-items: right;
        }

        .add-input {
          width: 100%;
          height: 40px;
          margin-top: 32px;
          border: 0;
          border-bottom: 1px var(--mdc-theme-primary) solid;
          text-align: left;
          padding: 0px;
          font-size: initial;
          color: var(--sidebar-text-color);
          font-family: var(--paper-font-body1_-_font-family);
        }
        input:focus {
          outline-offset: 0;
          outline: 0;
        }
        input {
          background-color: var(--sidebar-background-color);
        }
        ha-paper-dropdown-menu {
          width: 100%;
        }
        mwc-button {
          width: fit-content;
          margin-top: 16px;
        }

        input[narrow],
        .add-repository[narrow],
        ha-paper-dropdown-menu[narrow],
        mwc-button[narrow] {
          margin: 0;
          padding: 0;
          left: 0;
          top: 0;
          width: 100%;
          max-width: 100%;
        }
        .add-repository[narrow] {
          display: contents;
        }
      `]}}]}}),i);export{u as RacelandshopCustomRepositoriesDialog};
