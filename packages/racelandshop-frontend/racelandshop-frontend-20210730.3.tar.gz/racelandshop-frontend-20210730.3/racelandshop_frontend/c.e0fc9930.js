import{_ as i,R as e,e as o,T as a,v as t,d as s,r as n,i as d,n as l}from"./main-0b50267d.js";import{c}from"./c.9f29b77f.js";i([l("racelandshop-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[o({type:Boolean})],key:"hideActions",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"scrimClickAction",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"escapeKeyAction",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"noClose",value:()=>!1},{kind:"field",decorators:[o()],key:"title",value:void 0},{kind:"method",key:"render",value:function(){return this.active?a` <ha-dialog
      ?open=${this.active}
      ?scrimClickAction=${this.scrimClickAction}
      ?escapeKeyAction=${this.escapeKeyAction}
      @closed=${this.closeDialog}
      ?hideActions=${this.hideActions}
      .heading=${this.noClose?this.title:c(this.hass,this.title)}
    >
      <div class="content scroll" ?narrow=${this.narrow}>
        <slot></slot>
      </div>
      <slot class="primary" name="primaryaction" slot="primaryAction"></slot>
      <slot class="secondary" name="secondaryaction" slot="secondaryAction"></slot>
    </ha-dialog>`:a``}},{kind:"method",key:"closeDialog",value:function(){this.active=!1,this.dispatchEvent(new CustomEvent("closed",{bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[t,s,n,d`
        .content {
          overflow: auto;
        }
        ha-dialog {
          --mdc-dialog-max-width: var(--racelandshop-dialog-max-width, calc(100vw - 16px));
          --mdc-dialog-min-width: var(--racelandshop-dialog-min-width, 280px);
        }
        .primary {
          margin-left: 52px;
        }

        @media only screen and (min-width: 1280px) {
          ha-dialog {
            --mdc-dialog-max-width: var(--racelandshop-dialog-max-width, 990px);
          }
        }
      `]}}]}}),e);
