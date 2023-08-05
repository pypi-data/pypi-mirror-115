import{_ as e,R as i,e as t,a as o,m as a,T as r,b as s,c as d,s as n,d as l,i as c,n as p}from"./main-0b50267d.js";import"./c.1558eeb6.js";import"./c.b4cd1f42.js";import"./c.531db01a.js";import{f as h,r as u}from"./c.1c18faba.js";import"./c.e56a6082.js";import"./c.b800b779.js";import"./c.e0fc9930.js";import"./c.14f75282.js";import"./c.decf12bf.js";import"./c.2b0d6d1d.js";import"./c.9f29b77f.js";let f=e([p("racelandshop-add-repository-dialog")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[t({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[t({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[t()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[t()],key:"_sortBy",value:()=>"stars"},{kind:"field",decorators:[t()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return e.forEach((e,i)=>{"hass"===i&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),e.has("narrow")||e.has("filters")||e.has("active")||e.has("_searchInput")||e.has("_load")||e.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(e,i)=>null==e?void 0:e.filter(e=>{var t,o;return!e.installed&&(null===(t=this.racelandshop.sections)||void 0===t||null===(o=t.find(e=>e.id===this.section).categories)||void 0===o?void 0:o.includes(e.category))&&!e.installed&&(null==i?void 0:i.includes(e.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var e;if(this.addEventListener("filter-change",e=>this._updateFilters(e)),0===(null===(e=this.filters)||void 0===e?void 0:e.length)){var i;const e=null===(i=o(this.racelandshop.language,this.route))||void 0===i?void 0:i.categories;null==e||e.filter(e=>{var i;return null===(i=this.racelandshop.configuration)||void 0===i?void 0:i.categories.includes(e)}).forEach(e=>{this.filters.push({id:e,value:e,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(e){const i=this.filters.find(i=>i.id===e.detail.id);this.filters.find(e=>e.id===i.id).checked=!i.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>a(h)},{kind:"method",key:"render",value:function(){var e;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("racelandshop-search")||"";let i=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(e=this.racelandshop.configuration)||void 0===e?void 0:e.categories),this._searchInput);return 0!==this.filters.length&&(i=i.filter(e=>{var i;return null===(i=this.filters.find(i=>i.id===e.category))||void 0===i?void 0:i.checked})),r`
      <racelandshop-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.racelandshop.localize("dialog_add_repo.title")}
        hideActions
      >
        <div class="searchandfilter">
          <search-input
            no-label-float
            .label=${this.racelandshop.localize("search.placeholder")}
            .filter=${this._searchInput||""}
            @value-changed=${this._inputValueChanged}
            ?narrow=${this.narrow}
          ></search-input>
          <div class="filter">
            <ha-paper-dropdown-menu
              label="${this.racelandshop.localize("dialog_add_repo.sort_by")}"
              ?narrow=${this.narrow}
            >
              <paper-listbox slot="dropdown-content" selected="0">
                <paper-item @tap=${()=>this._sortBy="stars"}
                  >${this.racelandshop.localize("store.stars")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="name"}
                  >${this.racelandshop.localize("store.name")}</paper-item
                >
                <paper-item @tap=${()=>this._sortBy="last_updated"}
                  >${this.racelandshop.localize("store.last_updated")}</paper-item
                >
              </paper-listbox>
            </ha-paper-dropdown-menu>
          </div>
        </div>
        ${this.filters.length>1?r`<div class="filters">
              <racelandshop-filter .racelandshop=${this.racelandshop} .filters="${this.filters}"></racelandshop-filter>
            </div>`:""}
        <div class=${s({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${s({list:!0,narrow:this.narrow})}>
            ${i.sort((e,i)=>"name"===this._sortBy?e.name.toLocaleLowerCase()<i.name.toLocaleLowerCase()?-1:1:e[this._sortBy]>i[this._sortBy]?-1:1).slice(0,this._load).map(e=>r`<paper-icon-item
                  class=${s({narrow:this.narrow})}
                  @click=${()=>this._openInformation(e)}
                >
                  ${"integration"===e.category?r`
                        <img
                          loading="lazy"
                          src="https://brands.home-assistant.io/_/${e.domain}/icon.png"
                          referrerpolicy="no-referrer"
                          @error=${this._onImageError}
                          @load=${this._onImageLoad}
                        />
                      `:r`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`}
                  <paper-item-body two-line
                    >${e.name}
                    <div class="category-chip">
                      <racelandshop-chip
                        .icon=${u}
                        .value=${this.racelandshop.localize("common."+e.category)}
                      ></racelandshop-chip>
                    </div>
                    <div secondary>${e.description}</div>
                  </paper-item-body>
                </paper-icon-item>`)}
            ${0===i.length?r`<p>${this.racelandshop.localize("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </racelandshop-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(e){const i=e.target.scrollTop;i>=this._top?this._load+=1:this._load-=1,this._top=i}},{kind:"method",key:"_inputValueChanged",value:function(e){this._searchInput=e.detail.value,window.localStorage.setItem("racelandshop-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(e){this.dispatchEvent(new CustomEvent("racelandshop-dialog-secondary",{detail:{type:"repository-info",repository:e.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target&&(e.target.outerHTML=`<ha-svg-icon .path=${d} slot="item-icon"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[n,l,c`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 70vh;
        }

        .filter {
          margin-top: -12px;
          display: flex;
          width: 200px;
          float: right;
        }

        .list {
          margin-top: 16px;
          width: 1024px;
          max-width: 100%;
        }
        .category-chip {
          position: absolute;
          top: 8px;
          right: 8px;
        }
        ha-icon {
          --mdc-icon-size: 36px;
        }
        search-input {
          float: left;
          width: 60%;
          border-bottom: 1px var(--mdc-theme-primary) solid;
        }
        search-input[narrow],
        div.filter[narrow],
        ha-paper-dropdown-menu[narrow] {
          width: 100%;
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

        paper-icon-item:focus {
          background-color: var(--divider-color);
        }

        paper-icon-item {
          cursor: pointer;
          padding: 2px 0;
        }

        ha-paper-dropdown-menu {
          margin: 0 12px 4px 0;
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-icon-item.narrow {
          border-bottom: 1px solid var(--divider-color);
          padding: 8px 0;
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .add {
          border-top: 1px solid var(--divider-color);
          margin-top: 32px;
        }
        .filters {
          width: 100%;
          display: flex;
        }
        .add-actions {
          justify-content: space-between;
        }
        .add,
        .add-actions {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: 65px;
          background-color: var(--sidebar-background-color);
          border-bottom: 1px solid var(--divider-color);
          padding: 0 16px;
          box-sizing: border-box;
        }
        .add-input {
          width: calc(100% - 80px);
          height: 40px;
          border: 0;
          padding: 0 16px;
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

        racelandshop-filter {
          width: 100%;
        }
        div[secondary] {
          width: 88%;
        }
      `]}}]}}),i);export{f as RacelandshopAddRepositoryDialog};
