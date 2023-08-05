import{_ as e,R as t,e as i,m as o,T as r,n as s}from"./main-0b50267d.js";import{m as a}from"./c.a1faf29f.js";import"./c.e0fc9930.js";import"./c.15cfaaaf.js";import"./c.9f29b77f.js";import"./c.2b0d6d1d.js";let d=e([s("racelandshop-generic-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[i()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"header",value:void 0},{kind:"field",decorators:[i()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((e,t)=>null==e?void 0:e.find(e=>e.id===t))},{kind:"method",key:"render",value:function(){if(!this.active)return r``;const e=this._getRepository(this.repositories,this.repository);return r`
      <racelandshop-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?a.html(this.content||"",e):a.html(this.content||""):this.content||""}
      </racelandshop-dialog>
    `}}]}}),t);export{d as RacelandshopGenericDialog};
