const e=!(window.ShadyDOM&&window.ShadyDOM.inUse);let t,n;function r(n){t=(!n||!n.shimcssproperties)&&(e||Boolean(!navigator.userAgent.match(/AppleWebKit\/601|Edge\/15/)&&window.CSS&&CSS.supports&&CSS.supports("box-shadow","0 0 0 var(--foo)")))}window.ShadyCSS&&void 0!==window.ShadyCSS.cssBuild&&(n=window.ShadyCSS.cssBuild);const i=Boolean(window.ShadyCSS&&window.ShadyCSS.disableRuntime);window.ShadyCSS&&void 0!==window.ShadyCSS.nativeCss?t=window.ShadyCSS.nativeCss:window.ShadyCSS?(r(window.ShadyCSS),window.ShadyCSS=void 0):r(window.WebComponents&&window.WebComponents.flags);const s=t;class o{constructor(){this.start=0,this.end=0,this.previous=null,this.parent=null,this.rules=null,this.parsedCssText="",this.cssText="",this.atRule=!1,this.type=0,this.keyframesName="",this.selector="",this.parsedSelector=""}}function a(e){return function e(t,n){let r=n.substring(t.start,t.end-1);if(t.parsedCssText=t.cssText=r.trim(),t.parent){let e=t.previous?t.previous.end:t.parent.start;r=n.substring(e,t.start-1),r=function(e){return e.replace(/\\([0-9a-f]{1,6})\s/gi,(function(){let e=arguments[1],t=6-e.length;for(;t--;)e="0"+e;return"\\"+e}))}(r),r=r.replace(h.multipleSpaces," "),r=r.substring(r.lastIndexOf(";")+1);let i=t.parsedSelector=t.selector=r.trim();t.atRule=0===i.indexOf(_),t.atRule?0===i.indexOf(f)?t.type=p.MEDIA_RULE:i.match(h.keyframesRule)&&(t.type=p.KEYFRAMES_RULE,t.keyframesName=t.selector.split(h.multipleSpaces).pop()):0===i.indexOf(u)?t.type=p.MIXIN_RULE:t.type=p.STYLE_RULE}let i=t.rules;if(i)for(let t,r=0,s=i.length;r<s&&(t=i[r]);r++)e(t,n);return t}(function(e){let t=new o;t.start=0,t.end=e.length;let n=t;for(let r=0,i=e.length;r<i;r++)if(e[r]===d){n.rules||(n.rules=[]);let e=n,t=e.rules[e.rules.length-1]||null;n=new o,n.start=r+1,n.parent=e,n.previous=t,e.rules.push(n)}else e[r]===c&&(n.end=r+1,n=n.parent||t);return t}(e=e.replace(h.comments,"").replace(h.port,"")),e)}function l(e,t,n=""){let r="";if(e.cssText||e.rules){let n=e.rules;if(n&&!function(e){let t=e[0];return Boolean(t)&&Boolean(t.selector)&&0===t.selector.indexOf(u)}(n))for(let e,i=0,s=n.length;i<s&&(e=n[i]);i++)r=l(e,t,r);else r=t?e.cssText:function(e){return function(e){return e.replace(h.mixinApply,"").replace(h.varApply,"")}(e=function(e){return e.replace(h.customProp,"").replace(h.mixinProp,"")}(e))}(e.cssText),r=r.trim(),r&&(r="  "+r+"\n")}return r&&(e.selector&&(n+=e.selector+" "+d+"\n"),n+=r,e.selector&&(n+=c+"\n\n")),n}const p={STYLE_RULE:1,KEYFRAMES_RULE:7,MEDIA_RULE:4,MIXIN_RULE:1e3},d="{",c="}",h={comments:/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,port:/@import[^;]*;/gim,customProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?(?:[;\n]|$)/gim,mixinProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?{[^}]*?}(?:[;\n]|$)?/gim,mixinApply:/@apply\s*\(?[^);]*\)?\s*(?:[;\n]|$)?/gim,varApply:/[^;:]*?:[^;]*?var\([^;]*\)(?:[;\n]|$)?/gim,keyframesRule:/^@[^\s]*keyframes/,multipleSpaces:/\s+/g},u="--",f="@media",_="@",m=/(?:^|[;\s{]\s*)(--[\w-]*?)\s*:\s*(?:((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^)]*?\)|[^};{])+)|\{([^}]*)\}(?:(?=[;\s}])|$))/gi,y=/(?:^|\W+)@apply\s*\(?([^);\n]*)\)?/gi,g=/@media\s(.*)/,b=new Set;function v(e){const t=e.textContent;if(!b.has(t)){b.add(t);const e=document.createElement("style");e.setAttribute("shady-unscoped",""),e.textContent=t,document.head.appendChild(e)}}function w(e){return e.hasAttribute("shady-unscoped")}function C(e,t){return e?("string"==typeof e&&(e=a(e)),t&&x(e,t),l(e,s)):""}function P(e){return!e.__cssRules&&e.textContent&&(e.__cssRules=a(e.textContent)),e.__cssRules||null}function x(e,t,n,r){if(!e)return;let i=!1,s=e.type;if(r&&s===p.MEDIA_RULE){let t=e.selector.match(g);t&&(window.matchMedia(t[1]).matches||(i=!0))}s===p.STYLE_RULE?t(e):n&&s===p.KEYFRAMES_RULE?n(e):s===p.MIXIN_RULE&&(i=!0);let o=e.rules;if(o&&!i)for(let e,i=0,s=o.length;i<s&&(e=o[i]);i++)x(e,t,n,r)}window.ShadyDOM&&window.ShadyDOM.wrap;function S(e){if(void 0!==n)return n;if(void 0===e.__cssBuild){const t=e.getAttribute("css-build");if(t)e.__cssBuild=t;else{const t=function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;if(t instanceof Comment){const e=t.textContent.trim().split(":");if("css-build"===e[0])return e[1]}return""}(e);""!==t&&function(e){const t="template"===e.localName?e.content.firstChild:e.firstChild;t.parentNode.removeChild(t)}(e),e.__cssBuild=t}}return e.__cssBuild||""}function E(e){return""!==S(e)}function T(e,t){for(let n in t)null===n?e.style.removeProperty(n):e.style.setProperty(n,t[n])}function O(e,t){const n=window.getComputedStyle(e).getPropertyValue(t);return n?n.trim():""}const k=/;\s*/m,A=/^\s*(initial)|(inherit)\s*$/,N=/\s*!important/;class I{constructor(){this._map={}}set(e,t){e=e.trim(),this._map[e]={properties:t,dependants:{}}}get(e){return e=e.trim(),this._map[e]||null}}let L=null;class M{constructor(){this._currentElement=null,this._measureElement=null,this._map=new I}detectMixin(e){return function(e){const t=y.test(e)||m.test(e);return y.lastIndex=0,m.lastIndex=0,t}(e)}gatherStyles(t){const n=function(t){const n=[],r=t.querySelectorAll("style");for(let t=0;t<r.length;t++){const i=r[t];w(i)?e||(v(i),i.parentNode.removeChild(i)):(n.push(i.textContent),i.parentNode.removeChild(i))}return n.join("").trim()}(t.content);if(n){const e=document.createElement("style");return e.textContent=n,t.content.insertBefore(e,t.content.firstChild),e}return null}transformTemplate(e,t){void 0===e._gatheredStyle&&(e._gatheredStyle=this.gatherStyles(e));const n=e._gatheredStyle;return n?this.transformStyle(n,t):null}transformStyle(e,t=""){let n=P(e);return this.transformRules(n,t),e.textContent=C(n),n}transformCustomStyle(e){let t=P(e);return x(t,e=>{":root"===e.selector&&(e.selector="html"),this.transformRule(e)}),e.textContent=C(t),t}transformRules(e,t){this._currentElement=t,x(e,e=>{this.transformRule(e)}),this._currentElement=null}transformRule(e){e.cssText=this.transformCssText(e.parsedCssText,e),":root"===e.selector&&(e.selector=":host > *")}transformCssText(e,t){return e=e.replace(m,(e,n,r,i)=>this._produceCssProperties(e,n,r,i,t)),this._consumeCssProperties(e,t)}_getInitialValueForProperty(e){return this._measureElement||(this._measureElement=document.createElement("meta"),this._measureElement.setAttribute("apply-shim-measure",""),this._measureElement.style.all="initial",document.head.appendChild(this._measureElement)),window.getComputedStyle(this._measureElement).getPropertyValue(e)}_fallbacksFromPreviousRules(e){let t=e;for(;t.parent;)t=t.parent;const n={};let r=!1;return x(t,t=>{r=r||t===e,r||t.selector===e.selector&&Object.assign(n,this._cssTextToMap(t.parsedCssText))}),n}_consumeCssProperties(e,t){let n=null;for(;n=y.exec(e);){let r=n[0],i=n[1],s=n.index,o=s+r.indexOf("@apply"),a=s+r.length,l=e.slice(0,o),p=e.slice(a),d=t?this._fallbacksFromPreviousRules(t):{};Object.assign(d,this._cssTextToMap(l));let c=this._atApplyToCssProperties(i,d);e=`${l}${c}${p}`,y.lastIndex=s+c.length}return e}_atApplyToCssProperties(e,t){e=e.replace(k,"");let n=[],r=this._map.get(e);if(r||(this._map.set(e,{}),r=this._map.get(e)),r){let i,s,o;this._currentElement&&(r.dependants[this._currentElement]=!0);const a=r.properties;for(i in a)o=t&&t[i],s=[i,": var(",e,"_-_",i],o&&s.push(",",o.replace(N,"")),s.push(")"),N.test(a[i])&&s.push(" !important"),n.push(s.join(""))}return n.join("; ")}_replaceInitialOrInherit(e,t){let n=A.exec(t);return n&&(t=n[1]?this._getInitialValueForProperty(e):"apply-shim-inherit"),t}_cssTextToMap(e,t=!1){let n,r,i=e.split(";"),s={};for(let e,o,a=0;a<i.length;a++)e=i[a],e&&(o=e.split(":"),o.length>1&&(n=o[0].trim(),r=o.slice(1).join(":"),t&&(r=this._replaceInitialOrInherit(n,r)),s[n]=r));return s}_invalidateMixinEntry(e){if(L)for(let t in e.dependants)t!==this._currentElement&&L(t)}_produceCssProperties(e,t,n,r,i){if(n&&function e(t,n){let r=t.indexOf("var(");if(-1===r)return n(t,"","","");let i=function(e,t){let n=0;for(let r=t,i=e.length;r<i;r++)if("("===e[r])n++;else if(")"===e[r]&&0==--n)return r;return-1}(t,r+3),s=t.substring(r+4,i),o=t.substring(0,r),a=e(t.substring(i+1),n),l=s.indexOf(",");return-1===l?n(o,s.trim(),"",a):n(o,s.substring(0,l).trim(),s.substring(l+1).trim(),a)}(n,(e,t)=>{t&&this._map.get(t)&&(r=`@apply ${t};`)}),!r)return e;let s=this._consumeCssProperties(""+r,i),o=e.slice(0,e.indexOf("--")),a=this._cssTextToMap(s,!0),l=a,p=this._map.get(t),d=p&&p.properties;d?l=Object.assign(Object.create(d),a):this._map.set(t,l);let c,h,u=[],f=!1;for(c in l)h=a[c],void 0===h&&(h="initial"),d&&!(c in d)&&(f=!0),u.push(`${t}_-_${c}: ${h}`);return f&&this._invalidateMixinEntry(p),p&&(p.properties=l),n&&(o=`${e};${o}`),`${o}${u.join("; ")};`}}M.prototype.detectMixin=M.prototype.detectMixin,M.prototype.transformStyle=M.prototype.transformStyle,M.prototype.transformCustomStyle=M.prototype.transformCustomStyle,M.prototype.transformRules=M.prototype.transformRules,M.prototype.transformRule=M.prototype.transformRule,M.prototype.transformTemplate=M.prototype.transformTemplate,M.prototype._separator="_-_",Object.defineProperty(M.prototype,"invalidCallback",{get:()=>L,set(e){L=e}});const R={},D="_applyShimCurrentVersion",H="_applyShimNextVersion",F=Promise.resolve();function B(e){let t=R[e];t&&function(e){e[D]=e[D]||0,e._applyShimValidatingVersion=e._applyShimValidatingVersion||0,e[H]=(e[H]||0)+1}(t)}function z(e){return e[D]===e[H]}let j,K=null,q=window.HTMLImports&&window.HTMLImports.whenReady||null;function Y(e){requestAnimationFrame((function(){q?q(e):(K||(K=new Promise(e=>{j=e}),"complete"===document.readyState?j():document.addEventListener("readystatechange",()=>{"complete"===document.readyState&&j()})),K.then((function(){e&&e()})))}))}const V="__shadyCSSCachedStyle";let U=null,$=null;class X{constructor(){this.customStyles=[],this.enqueued=!1,Y(()=>{window.ShadyCSS.flushCustomStyles&&window.ShadyCSS.flushCustomStyles()})}enqueueDocumentValidation(){!this.enqueued&&$&&(this.enqueued=!0,Y($))}addCustomStyle(e){e.__seenByShadyCSS||(e.__seenByShadyCSS=!0,this.customStyles.push(e),this.enqueueDocumentValidation())}getStyleForCustomStyle(e){if(e[V])return e[V];let t;return t=e.getStyle?e.getStyle():e,t}processStyles(){const e=this.customStyles;for(let t=0;t<e.length;t++){const n=e[t];if(n[V])continue;const r=this.getStyleForCustomStyle(n);if(r){const e=r.__appliedElement||r;U&&U(e),n[V]=e}}return e}}X.prototype.addCustomStyle=X.prototype.addCustomStyle,X.prototype.getStyleForCustomStyle=X.prototype.getStyleForCustomStyle,X.prototype.processStyles=X.prototype.processStyles,Object.defineProperties(X.prototype,{transformCallback:{get:()=>U,set(e){U=e}},validateCallback:{get:()=>$,set(e){let t=!1;$||(t=!0),$=e,t&&this.enqueueDocumentValidation()}}});const J=new M;class G{constructor(){this.customStyleInterface=null,J.invalidCallback=B}ensure(){this.customStyleInterface||window.ShadyCSS.CustomStyleInterface&&(this.customStyleInterface=window.ShadyCSS.CustomStyleInterface,this.customStyleInterface.transformCallback=e=>{J.transformCustomStyle(e)},this.customStyleInterface.validateCallback=()=>{requestAnimationFrame(()=>{this.customStyleInterface.enqueued&&this.flushCustomStyles()})})}prepareTemplate(e,t){if(this.ensure(),E(e))return;R[t]=e;let n=J.transformTemplate(e,t);e._styleAst=n}flushCustomStyles(){if(this.ensure(),!this.customStyleInterface)return;let e=this.customStyleInterface.processStyles();if(this.customStyleInterface.enqueued){for(let t=0;t<e.length;t++){let n=e[t],r=this.customStyleInterface.getStyleForCustomStyle(n);r&&J.transformCustomStyle(r)}this.customStyleInterface.enqueued=!1}}styleSubtree(e,t){if(this.ensure(),t&&T(e,t),e.shadowRoot){this.styleElement(e);let t=e.shadowRoot.children||e.shadowRoot.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}else{let t=e.children||e.childNodes;for(let e=0;e<t.length;e++)this.styleSubtree(t[e])}}styleElement(e){this.ensure();let{is:t}=function(e){let t=e.localName,n="",r="";return t?t.indexOf("-")>-1?n=t:(r=t,n=e.getAttribute&&e.getAttribute("is")||""):(n=e.is,r=e.extends),{is:n,typeExtension:r}}(e),n=R[t];if((!n||!E(n))&&n&&!z(n)){(function(e){return!z(e)&&e._applyShimValidatingVersion===e[H]})(n)||(this.prepareTemplate(n,t),function(e){e._applyShimValidatingVersion=e[H],e._validating||(e._validating=!0,F.then((function(){e[D]=e[H],e._validating=!1})))}(n));let r=e.shadowRoot;if(r){let e=r.querySelector("style");e&&(e.__cssRules=n._styleAst,e.textContent=C(n._styleAst))}}}styleDocument(e){this.ensure(),this.styleSubtree(document.body,e)}}if(!window.ShadyCSS||!window.ShadyCSS.ScopingShim){const t=new G;let r=window.ShadyCSS&&window.ShadyCSS.CustomStyleInterface;window.ShadyCSS={prepareTemplate(e,n,r){t.flushCustomStyles(),t.prepareTemplate(e,n)},prepareTemplateStyles(e,t,n){window.ShadyCSS.prepareTemplate(e,t,n)},prepareTemplateDom(e,t){},styleSubtree(e,n){t.flushCustomStyles(),t.styleSubtree(e,n)},styleElement(e){t.flushCustomStyles(),t.styleElement(e)},styleDocument(e){t.flushCustomStyles(),t.styleDocument(e)},getComputedStyleValue:(e,t)=>O(e,t),flushCustomStyles(){t.flushCustomStyles()},nativeCss:s,nativeShadow:e,cssBuild:n,disableRuntime:i},r&&(window.ShadyCSS.CustomStyleInterface=r)}window.ShadyCSS.ApplyShim=J,window.JSCompiler_renameProperty=function(e,t){return e};let W,Z,Q=/(url\()([^)]*)(\))/g,ee=/(^\/)|(^#)|(^[\w-\d]*:)/;function te(e,t){if(e&&ee.test(e))return e;if(void 0===W){W=!1;try{const e=new URL("b","http://a");e.pathname="c%20d",W="http://a/c%20d"===e.href}catch(e){}}return t||(t=document.baseURI||window.location.href),W?new URL(e,t).href:(Z||(Z=document.implementation.createHTMLDocument("temp"),Z.base=Z.createElement("base"),Z.head.appendChild(Z.base),Z.anchor=Z.createElement("a"),Z.body.appendChild(Z.anchor)),Z.base.href=t,Z.anchor.href=e,Z.anchor.href||e)}function ne(e,t){return e.replace(Q,(function(e,n,r,i){return n+"'"+te(r.replace(/["']/g,""),t)+"'"+i}))}function re(e){return e.substring(0,e.lastIndexOf("/")+1)}const ie=!window.ShadyDOM;Boolean(!window.ShadyCSS||window.ShadyCSS.nativeCss);let se=re(document.baseURI||window.location.href),oe=window.Polymer&&window.Polymer.sanitizeDOMValue||void 0,ae=0;const le=function(e){let t=e.__mixinApplications;t||(t=new WeakMap,e.__mixinApplications=t);let n=ae++;return function(r){let i=r.__mixinSet;if(i&&i[n])return r;let s=t,o=s.get(r);o||(o=e(r),s.set(r,o));let a=Object.create(o.__mixinSet||i||null);return a[n]=!0,o.__mixinSet=a,o}};let pe={},de={};class ce extends HTMLElement{static get observedAttributes(){return["id"]}static import(e,t){if(e){let n=function(e){return pe[e]||de[e.toLowerCase()]}(e);return n&&t?n.querySelector(t):n}return null}attributeChangedCallback(e,t,n,r){t!==n&&this.register()}get assetpath(){if(!this.__assetpath){const e=window.HTMLImports&&HTMLImports.importForElement?HTMLImports.importForElement(this)||document:this.ownerDocument,t=te(this.getAttribute("assetpath")||"",e.baseURI);this.__assetpath=re(t)}return this.__assetpath}register(e){var t;(e=e||this.id)&&(this.id=e,function(e,t){pe[e]=de[e.toLowerCase()]=t}(e,this),(t=this).querySelector("style")&&console.warn("dom-module %s has style outside template",t.id))}}ce.prototype.modules=pe,customElements.define("dom-module",ce);function he(e){return ce.import(e)}function ue(e){const t=ne((e.body?e.body:e).textContent,e.baseURI),n=document.createElement("style");return n.textContent=t,n}function fe(e){const t=e.trim().split(/\s+/),n=[];for(let e=0;e<t.length;e++)n.push(..._e(t[e]));return n}function _e(e){const t=he(e);if(!t)return console.warn("Could not find style data in module named",e),[];if(void 0===t._styles){const e=[];e.push(...ye(t));const n=t.querySelector("template");n&&e.push(...me(n,t.assetpath)),t._styles=e}return t._styles}function me(e,t){if(!e._styles){const n=[],r=e.content.querySelectorAll("style");for(let e=0;e<r.length;e++){let i=r[e],s=i.getAttribute("include");s&&n.push(...fe(s).filter((function(e,t,n){return n.indexOf(e)===t}))),t&&(i.textContent=ne(i.textContent,t)),n.push(i)}e._styles=n}return e._styles}function ye(e){const t=[],n=e.querySelectorAll("link[rel=import][type~=css]");for(let e=0;e<n.length;e++){let r=n[e];if(r.import){const e=r.import,n=r.hasAttribute("shady-unscoped");if(n&&!e._unscopedStyle){const t=ue(e);t.setAttribute("shady-unscoped",""),e._unscopedStyle=t}else e._style||(e._style=ue(e));t.push(n?e._unscopedStyle:e._style)}}return t}function ge(e){let t=he(e);if(t&&void 0===t._cssText){let e=function(e){let t="",n=ye(e);for(let e=0;e<n.length;e++)t+=n[e].textContent;return t}(t),n=t.querySelector("template");n&&(e+=function(e,t){let n="";const r=me(e,t);for(let e=0;e<r.length;e++){let t=r[e];t.parentNode&&t.parentNode.removeChild(t),n+=t.textContent}return n}(n,t.assetpath)),t._cssText=e||null}return t||console.warn("Could not find style data in module named",e),t&&t._cssText||""}function be(e){return e.indexOf(".")>=0}function ve(e){let t=e.indexOf(".");return-1===t?e:e.slice(0,t)}function we(e,t){return 0===e.indexOf(t+".")}function Ce(e,t){return 0===t.indexOf(e+".")}function Pe(e,t,n){return t+n.slice(e.length)}function xe(e){if(Array.isArray(e)){let t=[];for(let n=0;n<e.length;n++){let r=e[n].toString().split(".");for(let e=0;e<r.length;e++)t.push(r[e])}return t.join(".")}return e}function Se(e){return Array.isArray(e)?xe(e).split("."):e.toString().split(".")}function Ee(e,t,n){let r=e,i=Se(t);for(let e=0;e<i.length;e++){if(!r)return;r=r[i[e]]}return n&&(n.path=i.join(".")),r}function Te(e,t,n){let r=e,i=Se(t),s=i[i.length-1];if(i.length>1){for(let e=0;e<i.length-1;e++){if(r=r[i[e]],!r)return}r[s]=n}else r[t]=n;return i.join(".")}const Oe={},ke=/-[a-z]/g,Ae=/([A-Z])/g;function Ne(e){return Oe[e]||(Oe[e]=e.indexOf("-")<0?e:e.replace(ke,e=>e[1].toUpperCase()))}function Ie(e){return Oe[e]||(Oe[e]=e.replace(Ae,"-$1").toLowerCase())}let Le=0,Me=0,Re=[],De=0,He=document.createTextNode("");new window.MutationObserver((function(){const e=Re.length;for(let t=0;t<e;t++){let e=Re[t];if(e)try{e()}catch(e){setTimeout(()=>{throw e})}}Re.splice(0,e),Me+=e})).observe(He,{characterData:!0});const Fe={after:e=>({run:t=>window.setTimeout(t,e),cancel(e){window.clearTimeout(e)}}),run:(e,t)=>window.setTimeout(e,t),cancel(e){window.clearTimeout(e)}},Be={run:e=>window.requestAnimationFrame(e),cancel(e){window.cancelAnimationFrame(e)}},ze={run:e=>(He.textContent=De++,Re.push(e),Le++),cancel(e){const t=e-Me;if(t>=0){if(!Re[t])throw new Error("invalid async handle: "+e);Re[t]=null}}},je=ze,Ke=le(e=>class extends e{static createProperties(e){const t=this.prototype;for(let n in e)n in t||t._createPropertyAccessor(n)}static attributeNameForProperty(e){return e.toLowerCase()}static typeForProperty(e){}_createPropertyAccessor(e,t){this._addPropertyToAttributeMap(e),this.hasOwnProperty("__dataHasAccessor")||(this.__dataHasAccessor=Object.assign({},this.__dataHasAccessor)),this.__dataHasAccessor[e]||(this.__dataHasAccessor[e]=!0,this._definePropertyAccessor(e,t))}_addPropertyToAttributeMap(e){if(this.hasOwnProperty("__dataAttributes")||(this.__dataAttributes=Object.assign({},this.__dataAttributes)),!this.__dataAttributes[e]){const t=this.constructor.attributeNameForProperty(e);this.__dataAttributes[t]=e}}_definePropertyAccessor(e,t){Object.defineProperty(this,e,{get(){return this._getProperty(e)},set:t?function(){}:function(t){this._setProperty(e,t)}})}constructor(){super(),this.__dataEnabled=!1,this.__dataReady=!1,this.__dataInvalid=!1,this.__data={},this.__dataPending=null,this.__dataOld=null,this.__dataInstanceProps=null,this.__serializing=!1,this._initializeProperties()}ready(){this.__dataReady=!0,this._flushProperties()}_initializeProperties(){for(let e in this.__dataHasAccessor)this.hasOwnProperty(e)&&(this.__dataInstanceProps=this.__dataInstanceProps||{},this.__dataInstanceProps[e]=this[e],delete this[e])}_initializeInstanceProperties(e){Object.assign(this,e)}_setProperty(e,t){this._setPendingProperty(e,t)&&this._invalidateProperties()}_getProperty(e){return this.__data[e]}_setPendingProperty(e,t,n){let r=this.__data[e],i=this._shouldPropertyChange(e,t,r);return i&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),this.__dataOld&&!(e in this.__dataOld)&&(this.__dataOld[e]=r),this.__data[e]=t,this.__dataPending[e]=t),i}_invalidateProperties(){!this.__dataInvalid&&this.__dataReady&&(this.__dataInvalid=!0,je.run(()=>{this.__dataInvalid&&(this.__dataInvalid=!1,this._flushProperties())}))}_enableProperties(){this.__dataEnabled||(this.__dataEnabled=!0,this.__dataInstanceProps&&(this._initializeInstanceProperties(this.__dataInstanceProps),this.__dataInstanceProps=null),this.ready())}_flushProperties(){const e=this.__data,t=this.__dataPending,n=this.__dataOld;this._shouldPropertiesChange(e,t,n)&&(this.__dataPending=null,this.__dataOld=null,this._propertiesChanged(e,t,n))}_shouldPropertiesChange(e,t,n){return Boolean(t)}_propertiesChanged(e,t,n){}_shouldPropertyChange(e,t,n){return n!==t&&(n==n||t==t)}attributeChangedCallback(e,t,n,r){t!==n&&this._attributeToProperty(e,n),super.attributeChangedCallback&&super.attributeChangedCallback(e,t,n,r)}_attributeToProperty(e,t,n){if(!this.__serializing){const r=this.__dataAttributes,i=r&&r[e]||e;this[i]=this._deserializeValue(t,n||this.constructor.typeForProperty(i))}}_propertyToAttribute(e,t,n){this.__serializing=!0,n=arguments.length<3?this[e]:n,this._valueToNodeAttribute(this,n,t||this.constructor.attributeNameForProperty(e)),this.__serializing=!1}_valueToNodeAttribute(e,t,n){const r=this._serializeValue(t);void 0===r?e.removeAttribute(n):e.setAttribute(n,r)}_serializeValue(e){switch(typeof e){case"boolean":return e?"":void 0;default:return null!=e?e.toString():void 0}}_deserializeValue(e,t){switch(t){case Boolean:return null!==e;case Number:return Number(e);default:return e}}}),qe={};let Ye=HTMLElement.prototype;for(;Ye;){let e=Object.getOwnPropertyNames(Ye);for(let t=0;t<e.length;t++)qe[e[t]]=!0;Ye=Object.getPrototypeOf(Ye)}const Ve=le(e=>{const t=Ke(e);return class extends t{static createPropertiesForAttributes(){let e=this.observedAttributes;for(let t=0;t<e.length;t++)this.prototype._createPropertyAccessor(Ne(e[t]))}static attributeNameForProperty(e){return Ie(e)}_initializeProperties(){this.__dataProto&&(this._initializeProtoProperties(this.__dataProto),this.__dataProto=null),super._initializeProperties()}_initializeProtoProperties(e){for(let t in e)this._setProperty(t,e[t])}_ensureAttribute(e,t){const n=this;n.hasAttribute(e)||this._valueToNodeAttribute(n,t,e)}_serializeValue(e){switch(typeof e){case"object":if(e instanceof Date)return e.toString();if(e)try{return JSON.stringify(e)}catch(e){return""}default:return super._serializeValue(e)}}_deserializeValue(e,t){let n;switch(t){case Object:try{n=JSON.parse(e)}catch(t){n=e}break;case Array:try{n=JSON.parse(e)}catch(t){n=null,console.warn("Polymer::Attributes: couldn't decode Array as JSON: "+e)}break;case Date:n=isNaN(e)?String(e):Number(e),n=new Date(n);break;default:n=super._deserializeValue(e,t)}return n}_definePropertyAccessor(e,t){!function(e,t){if(!qe[t]){let n=e[t];void 0!==n&&(e.__data?e._setPendingProperty(t,n):(e.__dataProto?e.hasOwnProperty(JSCompiler_renameProperty("__dataProto",e))||(e.__dataProto=Object.create(e.__dataProto)):e.__dataProto={},e.__dataProto[t]=n))}}(this,e),super._definePropertyAccessor(e,t)}_hasAccessor(e){return this.__dataHasAccessor&&this.__dataHasAccessor[e]}_isPropertyPending(e){return Boolean(this.__dataPending&&e in this.__dataPending)}}}),Ue={"dom-if":!0,"dom-repeat":!0};function $e(e){let t=e.getAttribute("is");if(t&&Ue[t]){let n=e;for(n.removeAttribute("is"),e=n.ownerDocument.createElement(t),n.parentNode.replaceChild(e,n),e.appendChild(n);n.attributes.length;)e.setAttribute(n.attributes[0].name,n.attributes[0].value),n.removeAttribute(n.attributes[0].name)}return e}function Xe(e,t){let n=t.parentInfo&&Xe(e,t.parentInfo);if(!n)return e;for(let e=n.firstChild,r=0;e;e=e.nextSibling)if(t.parentIndex===r++)return e}function Je(e,t,n,r){r.id&&(t[r.id]=n)}function Ge(e,t,n){if(n.events&&n.events.length)for(let r,i=0,s=n.events;i<s.length&&(r=s[i]);i++)e._addMethodEventListenerToNode(t,r.name,r.value,e)}function We(e,t,n){n.templateInfo&&(t._templateInfo=n.templateInfo)}const Ze=le(e=>class extends e{static _parseTemplate(e,t){if(!e._templateInfo){let n=e._templateInfo={};n.nodeInfoList=[],n.stripWhiteSpace=t&&t.stripWhiteSpace||e.hasAttribute("strip-whitespace"),this._parseTemplateContent(e,n,{parent:null})}return e._templateInfo}static _parseTemplateContent(e,t,n){return this._parseTemplateNode(e.content,t,n)}static _parseTemplateNode(e,t,n){let r,i=e;return"template"!=i.localName||i.hasAttribute("preserve-content")?"slot"===i.localName&&(t.hasInsertionPoint=!0):r=this._parseTemplateNestedTemplate(i,t,n)||r,i.firstChild&&(r=this._parseTemplateChildNodes(i,t,n)||r),i.hasAttributes&&i.hasAttributes()&&(r=this._parseTemplateNodeAttributes(i,t,n)||r),r}static _parseTemplateChildNodes(e,t,n){if("script"!==e.localName&&"style"!==e.localName)for(let r,i=e.firstChild,s=0;i;i=r){if("template"==i.localName&&(i=$e(i)),r=i.nextSibling,i.nodeType===Node.TEXT_NODE){let n=r;for(;n&&n.nodeType===Node.TEXT_NODE;)i.textContent+=n.textContent,r=n.nextSibling,e.removeChild(n),n=r;if(t.stripWhiteSpace&&!i.textContent.trim()){e.removeChild(i);continue}}let o={parentIndex:s,parentInfo:n};this._parseTemplateNode(i,t,o)&&(o.infoIndex=t.nodeInfoList.push(o)-1),i.parentNode&&s++}}static _parseTemplateNestedTemplate(e,t,n){let r=this._parseTemplate(e,t);return(r.content=e.content.ownerDocument.createDocumentFragment()).appendChild(e.content),n.templateInfo=r,!0}static _parseTemplateNodeAttributes(e,t,n){let r=!1,i=Array.from(e.attributes);for(let s,o=i.length-1;s=i[o];o--)r=this._parseTemplateNodeAttribute(e,t,n,s.name,s.value)||r;return r}static _parseTemplateNodeAttribute(e,t,n,r,i){return"on-"===r.slice(0,3)?(e.removeAttribute(r),n.events=n.events||[],n.events.push({name:r.slice(3),value:i}),!0):"id"===r&&(n.id=i,!0)}static _contentForTemplate(e){let t=e._templateInfo;return t&&t.content||e.content}_stampTemplate(e){e&&!e.content&&window.HTMLTemplateElement&&HTMLTemplateElement.decorate&&HTMLTemplateElement.decorate(e);let t=this.constructor._parseTemplate(e),n=t.nodeInfoList,r=t.content||e.content,i=document.importNode(r,!0);i.__noInsertionPoint=!t.hasInsertionPoint;let s=i.nodeList=new Array(n.length);i.$={};for(let e,t=0,r=n.length;t<r&&(e=n[t]);t++){let n=s[t]=Xe(i,e);Je(0,i.$,n,e),We(0,n,e),Ge(this,n,e)}return i=i,i}_addMethodEventListenerToNode(e,t,n,r){let i=function(e,t,n){return e=e._methodHost||e,function(t){e[n]?e[n](t,t.detail):console.warn("listener method `"+n+"` not defined")}}(r=r||e,0,n);return this._addEventListenerToNode(e,t,i),i}_addEventListenerToNode(e,t,n){e.addEventListener(t,n)}_removeEventListenerFromNode(e,t,n){e.removeEventListener(t,n)}});let Qe=0;const et={COMPUTE:"__computeEffects",REFLECT:"__reflectEffects",NOTIFY:"__notifyEffects",PROPAGATE:"__propagateEffects",OBSERVE:"__observeEffects",READ_ONLY:"__readOnly"},tt=/[A-Z]/;function nt(e,t){let n=e[t];if(n){if(!e.hasOwnProperty(t)){n=e[t]=Object.create(e[t]);for(let e in n){let t=n[e],r=n[e]=Array(t.length);for(let e=0;e<t.length;e++)r[e]=t[e]}}}else n=e[t]={};return n}function rt(e,t,n,r,i,s){if(t){let o=!1,a=Qe++;for(let l in n)it(e,t,a,l,n,r,i,s)&&(o=!0);return o}return!1}function it(e,t,n,r,i,s,o,a){let l=!1,p=t[o?ve(r):r];if(p)for(let t,d=0,c=p.length;d<c&&(t=p[d]);d++)t.info&&t.info.lastRun===n||o&&!st(r,t.trigger)||(t.info&&(t.info.lastRun=n),t.fn(e,r,i,s,t.info,o,a),l=!0);return l}function st(e,t){if(t){let n=t.name;return n==e||t.structured&&we(n,e)||t.wildcard&&Ce(n,e)}return!0}function ot(e,t,n,r,i){let s="string"==typeof i.method?e[i.method]:i.method,o=i.property;s?s.call(e,e.__data[o],r[o]):i.dynamicFn||console.warn("observer method `"+i.method+"` not defined")}function at(e,t,n){let r=ve(t);if(r!==t){return lt(e,Ie(r)+"-changed",n[t],t),!0}return!1}function lt(e,t,n,r){let i={value:n,queueProperty:!0};r&&(i.path=r),e.dispatchEvent(new CustomEvent(t,{detail:i}))}function pt(e,t,n,r,i,s){let o=(s?ve(t):t)!=t?t:null,a=o?Ee(e,o):e.__data[t];o&&void 0===a&&(a=n[t]),lt(e,i.eventName,a,o)}function dt(e,t,n,r,i){let s=e.__data[t];oe&&(s=oe(s,i.attrName,"attribute",e)),e._propertyToAttribute(t,i.attrName,s)}function ct(e,t,n,r,i){let s=gt(e,t,n,r,i),o=i.methodInfo;e.__dataHasAccessor&&e.__dataHasAccessor[o]?e._setPendingProperty(o,s,!0):e[o]=s}function ht(e,t,n,r,i,s,o){n.bindings=n.bindings||[];let a={kind:r,target:i,parts:s,literal:o,isCompound:1!==s.length};if(n.bindings.push(a),function(e){return Boolean(e.target)&&"attribute"!=e.kind&&"text"!=e.kind&&!e.isCompound&&"{"===e.parts[0].mode}(a)){let{event:e,negate:t}=a.parts[0];a.listenerEvent=e||Ie(i)+"-changed",a.listenerNegate=t}let l=t.nodeInfoList.length;for(let n=0;n<a.parts.length;n++){let r=a.parts[n];r.compoundIndex=n,ut(e,t,a,r,l)}}function ut(e,t,n,r,i){if(!r.literal)if("attribute"===n.kind&&"-"===n.target[0])console.warn("Cannot set attribute "+n.target+' because "-" is not a valid attribute starting character');else{let s=r.dependencies,o={index:i,binding:n,part:r,evaluator:e};for(let n=0;n<s.length;n++){let r=s[n];"string"==typeof r&&(r=Pt(r),r.wildcard=!0),e._addTemplatePropertyEffect(t,r.rootProperty,{fn:ft,info:o,trigger:r})}}}function ft(e,t,n,r,i,s,o){let a=o[i.index],l=i.binding,p=i.part;if(s&&p.source&&t.length>p.source.length&&"property"==l.kind&&!l.isCompound&&a.__isPropertyEffectsClient&&a.__dataHasAccessor&&a.__dataHasAccessor[l.target]){let r=n[t];t=Pe(p.source,l.target,t),a._setPendingPropertyOrPath(t,r,!1,!0)&&e._enqueueClient(a)}else{!function(e,t,n,r,i){i=function(e,t,n,r){if(n.isCompound){let i=e.__dataCompoundStorage[n.target];i[r.compoundIndex]=t,t=i.join("")}"attribute"!==n.kind&&("textContent"!==n.target&&("value"!==n.target||"input"!==e.localName&&"textarea"!==e.localName)||(t=null==t?"":t));return t}(t,i,n,r),oe&&(i=oe(i,n.target,n.kind,t));if("attribute"==n.kind)e._valueToNodeAttribute(t,i,n.target);else{let r=n.target;t.__isPropertyEffectsClient&&t.__dataHasAccessor&&t.__dataHasAccessor[r]?t[et.READ_ONLY]&&t[et.READ_ONLY][r]||t._setPendingProperty(r,i)&&e._enqueueClient(t):e._setUnmanagedPropertyToNode(t,r,i)}}(e,a,l,p,i.evaluator._evaluateBinding(e,p,t,n,r,s))}}function _t(e,t){if(t.isCompound){let n=e.__dataCompoundStorage||(e.__dataCompoundStorage={}),r=t.parts,i=new Array(r.length);for(let e=0;e<r.length;e++)i[e]=r[e].literal;let s=t.target;n[s]=i,t.literal&&"property"==t.kind&&(e[s]=t.literal)}}function mt(e,t,n){if(n.listenerEvent){let r=n.parts[0];e.addEventListener(n.listenerEvent,(function(e){!function(e,t,n,r,i){let s,o=e.detail,a=o&&o.path;a?(r=Pe(n,r,a),s=o&&o.value):s=e.currentTarget[n],s=i?!s:s,t[et.READ_ONLY]&&t[et.READ_ONLY][r]||!t._setPendingPropertyOrPath(r,s,!0,Boolean(a))||o&&o.queueProperty||t._invalidateProperties()}(e,t,n.target,r.source,r.negate)}))}}function yt(e,t,n,r,i,s){s=t.static||s&&("object"!=typeof s||s[t.methodName]);let o={methodName:t.methodName,args:t.args,methodInfo:i,dynamicFn:s};for(let i,s=0;s<t.args.length&&(i=t.args[s]);s++)i.literal||e._addPropertyEffect(i.rootProperty,n,{fn:r,info:o,trigger:i});s&&e._addPropertyEffect(t.methodName,n,{fn:r,info:o})}function gt(e,t,n,r,i){let s=e._methodHost||e,o=s[i.methodName];if(o){let r=e._marshalArgs(i.args,t,n);return o.apply(s,r)}i.dynamicFn||console.warn("method `"+i.methodName+"` not defined")}const bt=[],vt=new RegExp("(\\[\\[|{{)\\s*(?:(!)\\s*)?((?:[a-zA-Z_$][\\w.:$\\-*]*)\\s*(?:\\(\\s*(?:(?:(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*)(?:,\\s*(?:((?:[a-zA-Z_$][\\w.:$\\-*]*)|(?:[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)|(?:(?:'(?:[^'\\\\]|\\\\.)*')|(?:\"(?:[^\"\\\\]|\\\\.)*\")))\\s*))*)?)\\)\\s*)?)(?:]]|}})","g");function wt(e){let t="";for(let n=0;n<e.length;n++){t+=e[n].literal||""}return t}function Ct(e){let t=e.match(/([^\s]+?)\(([\s\S]*)\)/);if(t){let e={methodName:t[1],static:!0,args:bt};if(t[2].trim()){return function(e,t){return t.args=e.map((function(e){let n=Pt(e);return n.literal||(t.static=!1),n}),this),t}(t[2].replace(/\\,/g,"&comma;").split(","),e)}return e}return null}function Pt(e){let t=e.trim().replace(/&comma;/g,",").replace(/\\(.)/g,"$1"),n={name:t,value:"",literal:!1},r=t[0];switch("-"===r&&(r=t[1]),r>="0"&&r<="9"&&(r="#"),r){case"'":case'"':n.value=t.slice(1,-1),n.literal=!0;break;case"#":n.value=Number(t),n.literal=!0}return n.literal||(n.rootProperty=ve(t),n.structured=be(t),n.structured&&(n.wildcard=".*"==t.slice(-2),n.wildcard&&(n.name=t.slice(0,-2)))),n}function xt(e,t,n,r){let i=n+".splices";e.notifyPath(i,{indexSplices:r}),e.notifyPath(n+".length",t.length),e.__data[i]={indexSplices:null}}function St(e,t,n,r,i,s){xt(e,t,n,[{index:r,addedCount:i,removed:s,object:t,type:"splice"}])}const Et=le(e=>{const t=Ze(Ve(e));return class extends t{constructor(){super(),this.__isPropertyEffectsClient=!0,this.__dataCounter=0,this.__dataClientsReady,this.__dataPendingClients,this.__dataToNotify,this.__dataLinkedPaths,this.__dataHasPaths,this.__dataCompoundStorage,this.__dataHost,this.__dataTemp,this.__dataClientsInitialized,this.__data,this.__dataPending,this.__dataOld,this.__computeEffects,this.__reflectEffects,this.__notifyEffects,this.__propagateEffects,this.__observeEffects,this.__readOnly,this.__templateInfo}get PROPERTY_EFFECT_TYPES(){return et}_initializeProperties(){super._initializeProperties(),Tt.registerHost(this),this.__dataClientsReady=!1,this.__dataPendingClients=null,this.__dataToNotify=null,this.__dataLinkedPaths=null,this.__dataHasPaths=!1,this.__dataCompoundStorage=this.__dataCompoundStorage||null,this.__dataHost=this.__dataHost||null,this.__dataTemp={},this.__dataClientsInitialized=!1}_initializeProtoProperties(e){this.__data=Object.create(e),this.__dataPending=Object.create(e),this.__dataOld={}}_initializeInstanceProperties(e){let t=this[et.READ_ONLY];for(let n in e)t&&t[n]||(this.__dataPending=this.__dataPending||{},this.__dataOld=this.__dataOld||{},this.__data[n]=this.__dataPending[n]=e[n])}_addPropertyEffect(e,t,n){this._createPropertyAccessor(e,t==et.READ_ONLY);let r=nt(this,t)[e];r||(r=this[t][e]=[]),r.push(n)}_removePropertyEffect(e,t,n){let r=nt(this,t)[e],i=r.indexOf(n);i>=0&&r.splice(i,1)}_hasPropertyEffect(e,t){let n=this[t];return Boolean(n&&n[e])}_hasReadOnlyEffect(e){return this._hasPropertyEffect(e,et.READ_ONLY)}_hasNotifyEffect(e){return this._hasPropertyEffect(e,et.NOTIFY)}_hasReflectEffect(e){return this._hasPropertyEffect(e,et.REFLECT)}_hasComputedEffect(e){return this._hasPropertyEffect(e,et.COMPUTE)}_setPendingPropertyOrPath(e,t,n,r){if(r||ve(Array.isArray(e)?e[0]:e)!==e){if(!r){let n=Ee(this,e);if(!(e=Te(this,e,t))||!super._shouldPropertyChange(e,t,n))return!1}if(this.__dataHasPaths=!0,this._setPendingProperty(e,t,n))return function(e,t,n){let r=e.__dataLinkedPaths;if(r){let i;for(let s in r){let o=r[s];Ce(s,t)?(i=Pe(s,o,t),e._setPendingPropertyOrPath(i,n,!0,!0)):Ce(o,t)&&(i=Pe(o,s,t),e._setPendingPropertyOrPath(i,n,!0,!0))}}}(this,e,t),!0}else{if(this.__dataHasAccessor&&this.__dataHasAccessor[e])return this._setPendingProperty(e,t,n);this[e]=t}return!1}_setUnmanagedPropertyToNode(e,t,n){n===e[t]&&"object"!=typeof n||(e[t]=n)}_setPendingProperty(e,t,n){let r=this.__dataHasPaths&&be(e),i=r?this.__dataTemp:this.__data;return!!this._shouldPropertyChange(e,t,i[e])&&(this.__dataPending||(this.__dataPending={},this.__dataOld={}),e in this.__dataOld||(this.__dataOld[e]=this.__data[e]),r?this.__dataTemp[e]=t:this.__data[e]=t,this.__dataPending[e]=t,(r||this[et.NOTIFY]&&this[et.NOTIFY][e])&&(this.__dataToNotify=this.__dataToNotify||{},this.__dataToNotify[e]=n),!0)}_setProperty(e,t){this._setPendingProperty(e,t,!0)&&this._invalidateProperties()}_invalidateProperties(){this.__dataReady&&this._flushProperties()}_enqueueClient(e){this.__dataPendingClients=this.__dataPendingClients||[],e!==this&&this.__dataPendingClients.push(e)}_flushProperties(){this.__dataCounter++,super._flushProperties(),this.__dataCounter--}_flushClients(){this.__dataClientsReady?this.__enableOrFlushClients():(this.__dataClientsReady=!0,this._readyClients(),this.__dataReady=!0)}__enableOrFlushClients(){let e=this.__dataPendingClients;if(e){this.__dataPendingClients=null;for(let t=0;t<e.length;t++){let n=e[t];n.__dataEnabled?n.__dataPending&&n._flushProperties():n._enableProperties()}}}_readyClients(){this.__enableOrFlushClients()}setProperties(e,t){for(let n in e)!t&&this[et.READ_ONLY]&&this[et.READ_ONLY][n]||this._setPendingPropertyOrPath(n,e[n],!0);this._invalidateProperties()}ready(){this._flushProperties(),this.__dataClientsReady||this._flushClients(),this.__dataPending&&this._flushProperties()}_propertiesChanged(e,t,n){let r=this.__dataHasPaths;this.__dataHasPaths=!1,function(e,t,n,r){let i=e[et.COMPUTE];if(i){let s=t;for(;rt(e,i,s,n,r);)Object.assign(n,e.__dataOld),Object.assign(t,e.__dataPending),s=e.__dataPending,e.__dataPending=null}}(this,t,n,r);let i=this.__dataToNotify;this.__dataToNotify=null,this._propagatePropertyChanges(t,n,r),this._flushClients(),rt(this,this[et.REFLECT],t,n,r),rt(this,this[et.OBSERVE],t,n,r),i&&function(e,t,n,r,i){let s,o,a=e[et.NOTIFY],l=Qe++;for(let o in t)t[o]&&(a&&it(e,a,l,o,n,r,i)||i&&at(e,o,n))&&(s=!0);s&&(o=e.__dataHost)&&o._invalidateProperties&&o._invalidateProperties()}(this,i,t,n,r),1==this.__dataCounter&&(this.__dataTemp={})}_propagatePropertyChanges(e,t,n){this[et.PROPAGATE]&&rt(this,this[et.PROPAGATE],e,t,n);let r=this.__templateInfo;for(;r;)rt(this,r.propertyEffects,e,t,n,r.nodeList),r=r.nextTemplateInfo}linkPaths(e,t){e=xe(e),t=xe(t),this.__dataLinkedPaths=this.__dataLinkedPaths||{},this.__dataLinkedPaths[e]=t}unlinkPaths(e){e=xe(e),this.__dataLinkedPaths&&delete this.__dataLinkedPaths[e]}notifySplices(e,t){let n={path:""};xt(this,Ee(this,e,n),n.path,t)}get(e,t){return Ee(t||this,e)}set(e,t,n){n?Te(n,e,t):this[et.READ_ONLY]&&this[et.READ_ONLY][e]||this._setPendingPropertyOrPath(e,t,!0)&&this._invalidateProperties()}push(e,...t){let n={path:""},r=Ee(this,e,n),i=r.length,s=r.push(...t);return t.length&&St(this,r,n.path,i,t.length,[]),s}pop(e){let t={path:""},n=Ee(this,e,t),r=Boolean(n.length),i=n.pop();return r&&St(this,n,t.path,n.length,0,[i]),i}splice(e,t,n,...r){let i,s={path:""},o=Ee(this,e,s);return t<0?t=o.length-Math.floor(-t):t&&(t=Math.floor(t)),i=2===arguments.length?o.splice(t):o.splice(t,n,...r),(r.length||i.length)&&St(this,o,s.path,t,r.length,i),i}shift(e){let t={path:""},n=Ee(this,e,t),r=Boolean(n.length),i=n.shift();return r&&St(this,n,t.path,0,0,[i]),i}unshift(e,...t){let n={path:""},r=Ee(this,e,n),i=r.unshift(...t);return t.length&&St(this,r,n.path,0,t.length,[]),i}notifyPath(e,t){let n;if(1==arguments.length){let r={path:""};t=Ee(this,e,r),n=r.path}else n=Array.isArray(e)?xe(e):e;this._setPendingPropertyOrPath(n,t,!0,!0)&&this._invalidateProperties()}_createReadOnlyProperty(e,t){var n;this._addPropertyEffect(e,et.READ_ONLY),t&&(this["_set"+(n=e,n[0].toUpperCase()+n.substring(1))]=function(t){this._setProperty(e,t)})}_createPropertyObserver(e,t,n){let r={property:e,method:t,dynamicFn:Boolean(n)};this._addPropertyEffect(e,et.OBSERVE,{fn:ot,info:r,trigger:{name:e}}),n&&this._addPropertyEffect(t,et.OBSERVE,{fn:ot,info:r,trigger:{name:t}})}_createMethodObserver(e,t){let n=Ct(e);if(!n)throw new Error("Malformed observer expression '"+e+"'");yt(this,n,et.OBSERVE,gt,null,t)}_createNotifyingProperty(e){this._addPropertyEffect(e,et.NOTIFY,{fn:pt,info:{eventName:Ie(e)+"-changed",property:e}})}_createReflectedProperty(e){let t=this.constructor.attributeNameForProperty(e);"-"===t[0]?console.warn("Property "+e+" cannot be reflected to attribute "+t+' because "-" is not a valid starting attribute name. Use a lowercase first letter for the property instead.'):this._addPropertyEffect(e,et.REFLECT,{fn:dt,info:{attrName:t}})}_createComputedProperty(e,t,n){let r=Ct(t);if(!r)throw new Error("Malformed computed expression '"+t+"'");yt(this,r,et.COMPUTE,ct,e,n)}_marshalArgs(e,t,n){const r=this.__data;let i=[];for(let s=0,o=e.length;s<o;s++){let o,a=e[s],l=a.name;if(a.literal?o=a.value:a.structured?(o=Ee(r,l),void 0===o&&(o=n[l])):o=r[l],a.wildcard){let e=0===l.indexOf(t+"."),r=0===t.indexOf(l)&&!e;i[s]={path:r?t:l,value:r?n[t]:o,base:o}}else i[s]=o}return i}static addPropertyEffect(e,t,n){this.prototype._addPropertyEffect(e,t,n)}static createPropertyObserver(e,t,n){this.prototype._createPropertyObserver(e,t,n)}static createMethodObserver(e,t){this.prototype._createMethodObserver(e,t)}static createNotifyingProperty(e){this.prototype._createNotifyingProperty(e)}static createReadOnlyProperty(e,t){this.prototype._createReadOnlyProperty(e,t)}static createReflectedProperty(e){this.prototype._createReflectedProperty(e)}static createComputedProperty(e,t,n){this.prototype._createComputedProperty(e,t,n)}static bindTemplate(e){return this.prototype._bindTemplate(e)}_bindTemplate(e,t){let n=this.constructor._parseTemplate(e),r=this.__templateInfo==n;if(!r)for(let e in n.propertyEffects)this._createPropertyAccessor(e);if(t&&(n=Object.create(n),n.wasPreBound=r,!r&&this.__templateInfo)){let e=this.__templateInfoLast||this.__templateInfo;return this.__templateInfoLast=e.nextTemplateInfo=n,n.previousTemplateInfo=e,n}return this.__templateInfo=n}static _addTemplatePropertyEffect(e,t,n){(e.hostProps=e.hostProps||{})[t]=!0;let r=e.propertyEffects=e.propertyEffects||{};(r[t]=r[t]||[]).push(n)}_stampTemplate(e){Tt.beginHosting(this);let t=super._stampTemplate(e);Tt.endHosting(this);let n=this._bindTemplate(e,!0);if(n.nodeList=t.nodeList,!n.wasPreBound){let e=n.childNodes=[];for(let n=t.firstChild;n;n=n.nextSibling)e.push(n)}return t.templateInfo=n,function(e,t){let{nodeList:n,nodeInfoList:r}=t;if(r.length)for(let t=0;t<r.length;t++){let i=r[t],s=n[t],o=i.bindings;if(o)for(let t=0;t<o.length;t++){let n=o[t];_t(s,n),mt(s,e,n)}s.__dataHost=e}}(this,n),this.__dataReady&&rt(this,n.propertyEffects,this.__data,null,!1,n.nodeList),t}_removeBoundDom(e){let t=e.templateInfo;t.previousTemplateInfo&&(t.previousTemplateInfo.nextTemplateInfo=t.nextTemplateInfo),t.nextTemplateInfo&&(t.nextTemplateInfo.previousTemplateInfo=t.previousTemplateInfo),this.__templateInfoLast==t&&(this.__templateInfoLast=t.previousTemplateInfo),t.previousTemplateInfo=t.nextTemplateInfo=null;let n=t.childNodes;for(let e=0;e<n.length;e++){let t=n[e];t.parentNode.removeChild(t)}}static _parseTemplateNode(e,t,n){let r=super._parseTemplateNode(e,t,n);if(e.nodeType===Node.TEXT_NODE){let i=this._parseBindings(e.textContent,t);i&&(e.textContent=wt(i)||" ",ht(this,t,n,"text","textContent",i),r=!0)}return r}static _parseTemplateNodeAttribute(e,t,n,r,i){let s=this._parseBindings(i,t);if(s){let i=r,o="property";tt.test(r)?o="attribute":"$"==r[r.length-1]&&(r=r.slice(0,-1),o="attribute");let a=wt(s);return a&&"attribute"==o&&e.setAttribute(r,a),"input"===e.localName&&"value"===i&&e.setAttribute(i,""),e.removeAttribute(i),"property"===o&&(r=Ne(r)),ht(this,t,n,o,r,s,a),!0}return super._parseTemplateNodeAttribute(e,t,n,r,i)}static _parseTemplateNestedTemplate(e,t,n){let r=super._parseTemplateNestedTemplate(e,t,n),i=n.templateInfo.hostProps;for(let e in i){ht(this,t,n,"property","_host_"+e,[{mode:"{",source:e,dependencies:[e]}])}return r}static _parseBindings(e,t){let n,r=[],i=0;for(;null!==(n=vt.exec(e));){n.index>i&&r.push({literal:e.slice(i,n.index)});let s=n[1][0],o=Boolean(n[2]),a=n[3].trim(),l=!1,p="",d=-1;"{"==s&&(d=a.indexOf("::"))>0&&(p=a.substring(d+2),a=a.substring(0,d),l=!0);let c=Ct(a),h=[];if(c){let{args:e,methodName:n}=c;for(let t=0;t<e.length;t++){let n=e[t];n.literal||h.push(n)}let r=t.dynamicFns;(r&&r[n]||c.static)&&(h.push(n),c.dynamicFn=!0)}else h.push(a);r.push({source:a,mode:s,negate:o,customEvent:l,signature:c,dependencies:h,event:p}),i=vt.lastIndex}if(i&&i<e.length){let t=e.substring(i);t&&r.push({literal:t})}return r.length?r:null}static _evaluateBinding(e,t,n,r,i,s){let o;return o=t.signature?gt(e,n,r,0,t.signature):n!=t.source?Ee(e,t.source):s&&be(n)?Ee(e,n):e.__data[n],t.negate&&(o=!o),o}}});const Tt=new class{constructor(){this.stack=[]}registerHost(e){if(this.stack.length){this.stack[this.stack.length-1]._enqueueClient(e)}}beginHosting(e){this.stack.push(e)}endHosting(e){let t=this.stack.length;t&&this.stack[t-1]==e&&this.stack.pop()}};const Ot=le(e=>{const t=Ke(e);function n(e){const t=Object.getPrototypeOf(e);return t.prototype instanceof i?t:null}function r(e){if(!e.hasOwnProperty(JSCompiler_renameProperty("__ownProperties",e))){let t=null;if(e.hasOwnProperty(JSCompiler_renameProperty("properties",e))){const n=e.properties;n&&(t=function(e){const t={};for(let n in e){const r=e[n];t[n]="function"==typeof r?{type:r}:r}return t}(n))}e.__ownProperties=t}return e.__ownProperties}class i extends t{static get observedAttributes(){const e=this._properties;return e?Object.keys(e).map(e=>this.attributeNameForProperty(e)):[]}static finalize(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__finalized",this))){const e=n(this);e&&e.finalize(),this.__finalized=!0,this._finalizeClass()}}static _finalizeClass(){const e=r(this);e&&this.createProperties(e)}static get _properties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("__properties",this))){const e=n(this);this.__properties=Object.assign({},e&&e._properties,r(this))}return this.__properties}static typeForProperty(e){const t=this._properties[e];return t&&t.type}_initializeProperties(){this.constructor.finalize(),super._initializeProperties()}connectedCallback(){super.connectedCallback&&super.connectedCallback(),this._enableProperties()}disconnectedCallback(){super.disconnectedCallback&&super.disconnectedCallback()}}return i}),kt=le(e=>{const t=Ot(Et(e));function n(e,t,n,r){n.computed&&(n.readOnly=!0),n.computed&&!e._hasReadOnlyEffect(t)&&e._createComputedProperty(t,n.computed,r),n.readOnly&&!e._hasReadOnlyEffect(t)&&e._createReadOnlyProperty(t,!n.computed),n.reflectToAttribute&&!e._hasReflectEffect(t)&&e._createReflectedProperty(t),n.notify&&!e._hasNotifyEffect(t)&&e._createNotifyingProperty(t),n.observer&&e._createPropertyObserver(t,n.observer,r[n.observer]),e._addPropertyToAttributeMap(t)}function r(e,t,n,r){const i=t.content.querySelectorAll("style"),s=me(t),o=function(e){let t=he(e);return t?ye(t):[]}(n),a=t.content.firstElementChild;for(let n=0;n<o.length;n++){let i=o[n];i.textContent=e._processStyleText(i.textContent,r),t.content.insertBefore(i,a)}let l=0;for(let t=0;t<s.length;t++){let n=s[t],o=i[l];o!==n?(n=n.cloneNode(!0),o.parentNode.insertBefore(n,o)):l++,n.textContent=e._processStyleText(n.textContent,r)}window.ShadyCSS&&window.ShadyCSS.prepareTemplate(t,n)}return class extends t{static get polymerElementVersion(){return"3.0.5"}static _finalizeClass(){super._finalizeClass(),this.hasOwnProperty(JSCompiler_renameProperty("is",this))&&this.is&&this.prototype;const e=((t=this).hasOwnProperty(JSCompiler_renameProperty("__ownObservers",t))||(t.__ownObservers=t.hasOwnProperty(JSCompiler_renameProperty("observers",t))?t.observers:null),t.__ownObservers);var t;e&&this.createObservers(e,this._properties);let n=this.template;n&&("string"==typeof n?(console.error("template getter must return HTMLTemplateElement"),n=null):n=n.cloneNode(!0)),this.prototype._template=n}static createProperties(e){for(let t in e)n(this.prototype,t,e[t],e)}static createObservers(e,t){const n=this.prototype;for(let r=0;r<e.length;r++)n._createMethodObserver(e[r],t)}static get template(){return this.hasOwnProperty(JSCompiler_renameProperty("_template",this))||(this._template=this.prototype.hasOwnProperty(JSCompiler_renameProperty("_template",this.prototype))?this.prototype._template:function(e){let t=null;return e&&(t=ce.import(e,"template")),t}(this.is)||Object.getPrototypeOf(this.prototype).constructor.template),this._template}static set template(e){this._template=e}static get importPath(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_importPath",this))){const e=this.importMeta;if(e)this._importPath=re(e.url);else{const e=ce.import(this.is);this._importPath=e&&e.assetpath||Object.getPrototypeOf(this.prototype).constructor.importPath}}return this._importPath}constructor(){super(),this._template,this._importPath,this.rootPath,this.importPath,this.root,this.$}_initializeProperties(){this.constructor.finalize(),this.constructor._finalizeTemplate(this.localName),super._initializeProperties(),this.rootPath=se,this.importPath=this.constructor.importPath;let e=function(e){if(!e.hasOwnProperty(JSCompiler_renameProperty("__propertyDefaults",e))){e.__propertyDefaults=null;let t=e._properties;for(let n in t){let r=t[n];"value"in r&&(e.__propertyDefaults=e.__propertyDefaults||{},e.__propertyDefaults[n]=r)}}return e.__propertyDefaults}(this.constructor);if(e)for(let t in e){let n=e[t];if(!this.hasOwnProperty(t)){let e="function"==typeof n.value?n.value.call(this):n.value;this._hasAccessor(t)?this._setPendingProperty(t,e,!0):this[t]=e}}}static _processStyleText(e,t){return ne(e,t)}static _finalizeTemplate(e){const t=this.prototype._template;if(t&&!t.__polymerFinalized){t.__polymerFinalized=!0;const n=this.importPath;r(this,t,e,n?te(n):""),this.prototype._bindTemplate(t)}}connectedCallback(){window.ShadyCSS&&this._template&&window.ShadyCSS.styleElement(this),super.connectedCallback()}ready(){this._template&&(this.root=this._stampTemplate(this._template),this.$=this.root.$),super.ready()}_readyClients(){this._template&&(this.root=this._attachDom(this.root)),super._readyClients()}_attachDom(e){if(this.attachShadow)return e?(this.shadowRoot||this.attachShadow({mode:"open"}),this.shadowRoot.appendChild(e),this.shadowRoot):null;throw new Error("ShadowDOM not available. PolymerElement can create dom as children instead of in ShadowDOM by setting `this.root = this;` before `ready`.")}updateStyles(e){window.ShadyCSS&&window.ShadyCSS.styleSubtree(this,e)}resolveUrl(e,t){return!t&&this.importPath&&(t=te(this.importPath)),te(e,t)}static _parseTemplateContent(e,t,n){return t.dynamicFns=t.dynamicFns||this._properties,super._parseTemplateContent(e,t,n)}}});class At{constructor(){this._asyncModule=null,this._callback=null,this._timer=null}setConfig(e,t){this._asyncModule=e,this._callback=t,this._timer=this._asyncModule.run(()=>{this._timer=null,this._callback()})}cancel(){this.isActive()&&(this._asyncModule.cancel(this._timer),this._timer=null)}flush(){this.isActive()&&(this.cancel(),this._callback())}isActive(){return null!=this._timer}static debounce(e,t,n){return e instanceof At?e.cancel():e=new At,e.setConfig(t,n),e}}let Nt="string"==typeof document.head.style.touchAction,It="__polymerGesturesHandled",Lt="__polymerGesturesTouchAction",Mt=["mousedown","mousemove","mouseup","click"],Rt=[0,1,4,2],Dt=function(){try{return 1===new MouseEvent("test",{buttons:1}).buttons}catch(e){return!1}}();function Ht(e){return Mt.indexOf(e)>-1}let Ft=!1;function Bt(e){Ht(e)}!function(){try{let e=Object.defineProperty({},"passive",{get(){Ft=!0}});window.addEventListener("test",null,e),window.removeEventListener("test",null,e)}catch(e){}}();let zt=navigator.userAgent.match(/iP(?:[oa]d|hone)|Android/);const jt=[],Kt={button:!0,input:!0,keygen:!0,meter:!0,output:!0,textarea:!0,progress:!0,select:!0},qt={button:!0,command:!0,fieldset:!0,input:!0,keygen:!0,optgroup:!0,option:!0,select:!0,textarea:!0};function Yt(e){let t=Array.prototype.slice.call(e.labels||[]);if(!t.length){t=[];let n=e.getRootNode();if(e.id){let r=n.querySelectorAll(`label[for = ${e.id}]`);for(let e=0;e<r.length;e++)t.push(r[e])}}return t}let Vt=function(e){let t=e.sourceCapabilities;var n;if((!t||t.firesTouchEvents)&&(e[It]={skip:!0},"click"===e.type)){let t=!1,r=e.composedPath&&e.composedPath();if(r)for(let e=0;e<r.length;e++){if(r[e].nodeType===Node.ELEMENT_NODE)if("label"===r[e].localName)jt.push(r[e]);else if(n=r[e],Kt[n.localName]){let n=Yt(r[e]);for(let e=0;e<n.length;e++)t=t||jt.indexOf(n[e])>-1}if(r[e]===Xt.mouse.target)return}if(t)return;e.preventDefault(),e.stopPropagation()}};function Ut(e){let t=zt?["click"]:Mt;for(let n,r=0;r<t.length;r++)n=t[r],e?(jt.length=0,document.addEventListener(n,Vt,!0)):document.removeEventListener(n,Vt,!0)}function $t(e){let t=e.type;if(!Ht(t))return!1;if("mousemove"===t){let t=void 0===e.buttons?1:e.buttons;return e instanceof window.MouseEvent&&!Dt&&(t=Rt[e.which]||0),Boolean(1&t)}return 0===(void 0===e.button?0:e.button)}let Xt={mouse:{target:null,mouseIgnoreJob:null},touch:{x:0,y:0,id:-1,scrollDecided:!1}};function Jt(e,t,n){e.movefn=t,e.upfn=n,document.addEventListener("mousemove",t),document.addEventListener("mouseup",n)}function Gt(e){document.removeEventListener("mousemove",e.movefn),document.removeEventListener("mouseup",e.upfn),e.movefn=null,e.upfn=null}document.addEventListener("touchend",(function(e){Xt.mouse.mouseIgnoreJob||Ut(!0),Xt.mouse.target=e.composedPath()[0],Xt.mouse.mouseIgnoreJob=At.debounce(Xt.mouse.mouseIgnoreJob,Fe.after(2500),(function(){Ut(),Xt.mouse.target=null,Xt.mouse.mouseIgnoreJob=null}))}),!!Ft&&{passive:!0});const Wt={},Zt=[];function Qt(e){if(e.composedPath){const t=e.composedPath();return t.length>0?t[0]:e.target}return e.target}function en(e){let t,n=e.type,r=e.currentTarget.__polymerGestures;if(!r)return;let i=r[n];if(i){if(!e[It]&&(e[It]={},"touch"===n.slice(0,5))){let t=(e=e).changedTouches[0];if("touchstart"===n&&1===e.touches.length&&(Xt.touch.id=t.identifier),Xt.touch.id!==t.identifier)return;Nt||"touchstart"!==n&&"touchmove"!==n||function(e){let t=e.changedTouches[0],n=e.type;if("touchstart"===n)Xt.touch.x=t.clientX,Xt.touch.y=t.clientY,Xt.touch.scrollDecided=!1;else if("touchmove"===n){if(Xt.touch.scrollDecided)return;Xt.touch.scrollDecided=!0;let n=function(e){let t="auto",n=e.composedPath&&e.composedPath();if(n)for(let e,r=0;r<n.length;r++)if(e=n[r],e[Lt]){t=e[Lt];break}return t}(e),r=!1,i=Math.abs(Xt.touch.x-t.clientX),s=Math.abs(Xt.touch.y-t.clientY);e.cancelable&&("none"===n?r=!0:"pan-x"===n?r=s>i:"pan-y"===n&&(r=i>s)),r?e.preventDefault():an("track")}}(e)}if(t=e[It],!t.skip){for(let n,r=0;r<Zt.length;r++)n=Zt[r],i[n.name]&&!t[n.name]&&n.flow&&n.flow.start.indexOf(e.type)>-1&&n.reset&&n.reset();for(let r,s=0;s<Zt.length;s++)r=Zt[s],i[r.name]&&!t[r.name]&&(t[r.name]=!0,r[n](e))}}}function tn(e,t,n){return!!Wt[t]&&(function(e,t,n){let r=Wt[t],i=r.deps,s=r.name,o=e.__polymerGestures;o||(e.__polymerGestures=o={});for(let t,n,r=0;r<i.length;r++)t=i[r],zt&&Ht(t)&&"click"!==t||(n=o[t],n||(o[t]=n={_count:0}),0===n._count&&e.addEventListener(t,en,Bt(t)),n[s]=(n[s]||0)+1,n._count=(n._count||0)+1);e.addEventListener(t,n),r.touchAction&&sn(e,r.touchAction)}(e,t,n),!0)}function nn(e,t,n){return!!Wt[t]&&(function(e,t,n){let r=Wt[t],i=r.deps,s=r.name,o=e.__polymerGestures;if(o)for(let t,n,r=0;r<i.length;r++)t=i[r],n=o[t],n&&n[s]&&(n[s]=(n[s]||1)-1,n._count=(n._count||1)-1,0===n._count&&e.removeEventListener(t,en,Bt(t)));e.removeEventListener(t,n)}(e,t,n),!0)}function rn(e){Zt.push(e);for(let t=0;t<e.emits.length;t++)Wt[e.emits[t]]=e}function sn(e,t){Nt&&e instanceof HTMLElement&&ze.run(()=>{e.style.touchAction=t}),e[Lt]=t}function on(e,t,n){let r=new Event(t,{bubbles:!0,cancelable:!0,composed:!0});if(r.detail=n,e.dispatchEvent(r),r.defaultPrevented){let e=n.preventer||n.sourceEvent;e&&e.preventDefault&&e.preventDefault()}}function an(e){let t=function(e){for(let t,n=0;n<Zt.length;n++){t=Zt[n];for(let n,r=0;r<t.emits.length;r++)if(n=t.emits[r],n===e)return t}return null}(e);t.info&&(t.info.prevent=!0)}function ln(e,t,n,r){t&&on(t,e,{x:n.clientX,y:n.clientY,sourceEvent:n,preventer:r,prevent:function(e){return an(e)}})}function pn(e,t,n){if(e.prevent)return!1;if(e.started)return!0;let r=Math.abs(e.x-t),i=Math.abs(e.y-n);return r>=5||i>=5}function dn(e,t,n){if(!t)return;let r,i=e.moves[e.moves.length-2],s=e.moves[e.moves.length-1],o=s.x-e.x,a=s.y-e.y,l=0;i&&(r=s.x-i.x,l=s.y-i.y),on(t,"track",{state:e.state,x:n.clientX,y:n.clientY,dx:o,dy:a,ddx:r,ddy:l,sourceEvent:n,hover:function(){return function(e,t){let n=document.elementFromPoint(e,t),r=n;for(;r&&r.shadowRoot&&!window.ShadyDOM;){let i=r;if(r=r.shadowRoot.elementFromPoint(e,t),i===r)break;r&&(n=r)}return n}(n.clientX,n.clientY)}})}function cn(e,t,n){let r=Math.abs(t.clientX-e.x),i=Math.abs(t.clientY-e.y),s=Qt(n||t);!s||qt[s.localName]&&s.hasAttribute("disabled")||(isNaN(r)||isNaN(i)||r<=25&&i<=25||function(e){if("click"===e.type){if(0===e.detail)return!0;let t=Qt(e);if(!t.nodeType||t.nodeType!==Node.ELEMENT_NODE)return!0;let n=t.getBoundingClientRect(),r=e.pageX,i=e.pageY;return!(r>=n.left&&r<=n.right&&i>=n.top&&i<=n.bottom)}return!1}(t))&&(e.prevent||on(s,"tap",{x:t.clientX,y:t.clientY,sourceEvent:t,preventer:n}))}rn({name:"downup",deps:["mousedown","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["down","up"],info:{movefn:null,upfn:null},reset:function(){Gt(this.info)},mousedown:function(e){if(!$t(e))return;let t=Qt(e),n=this;Jt(this.info,(function(e){$t(e)||(ln("up",t,e),Gt(n.info))}),(function(e){$t(e)&&ln("up",t,e),Gt(n.info)})),ln("down",t,e)},touchstart:function(e){ln("down",Qt(e),e.changedTouches[0],e)},touchend:function(e){ln("up",Qt(e),e.changedTouches[0],e)}}),rn({name:"track",touchAction:"none",deps:["mousedown","touchstart","touchmove","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["track"],info:{x:0,y:0,state:"start",started:!1,moves:[],addMove:function(e){this.moves.length>2&&this.moves.shift(),this.moves.push(e)},movefn:null,upfn:null,prevent:!1},reset:function(){this.info.state="start",this.info.started=!1,this.info.moves=[],this.info.x=0,this.info.y=0,this.info.prevent=!1,Gt(this.info)},mousedown:function(e){if(!$t(e))return;let t=Qt(e),n=this,r=function(e){let r=e.clientX,i=e.clientY;pn(n.info,r,i)&&(n.info.state=n.info.started?"mouseup"===e.type?"end":"track":"start","start"===n.info.state&&an("tap"),n.info.addMove({x:r,y:i}),$t(e)||(n.info.state="end",Gt(n.info)),t&&dn(n.info,t,e),n.info.started=!0)};Jt(this.info,r,(function(e){n.info.started&&r(e),Gt(n.info)})),this.info.x=e.clientX,this.info.y=e.clientY},touchstart:function(e){let t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchmove:function(e){let t=Qt(e),n=e.changedTouches[0],r=n.clientX,i=n.clientY;pn(this.info,r,i)&&("start"===this.info.state&&an("tap"),this.info.addMove({x:r,y:i}),dn(this.info,t,n),this.info.state="track",this.info.started=!0)},touchend:function(e){let t=Qt(e),n=e.changedTouches[0];this.info.started&&(this.info.state="end",this.info.addMove({x:n.clientX,y:n.clientY}),dn(this.info,t,n))}}),rn({name:"tap",deps:["mousedown","click","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["click","touchend"]},emits:["tap"],info:{x:NaN,y:NaN,prevent:!1},reset:function(){this.info.x=NaN,this.info.y=NaN,this.info.prevent=!1},mousedown:function(e){$t(e)&&(this.info.x=e.clientX,this.info.y=e.clientY)},click:function(e){$t(e)&&cn(this.info,e)},touchstart:function(e){const t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchend:function(e){cn(this.info,e.changedTouches[0],e)}});const hn=le(e=>class extends e{_addEventListenerToNode(e,t,n){tn(e,t,n)||super._addEventListenerToNode(e,t,n)}_removeEventListenerFromNode(e,t,n){nn(e,t,n)||super._removeEventListenerFromNode(e,t,n)}}),un=/:host\(:dir\((ltr|rtl)\)\)/g,fn=/([\s\w-#\.\[\]\*]*):dir\((ltr|rtl)\)/g,_n=[];let mn=null,yn="";function gn(){yn=document.documentElement.getAttribute("dir")}function bn(e){if(!e.__autoDirOptOut){e.setAttribute("dir",yn)}}function vn(){gn(),yn=document.documentElement.getAttribute("dir");for(let e=0;e<_n.length;e++)bn(_n[e])}const wn=le(e=>{mn||(gn(),mn=new MutationObserver(vn),mn.observe(document.documentElement,{attributes:!0,attributeFilter:["dir"]}));const t=Ve(e);class n extends t{static _processStyleText(e,t){return e=super._processStyleText(e,t),e=this._replaceDirInCssText(e)}static _replaceDirInCssText(e){let t=e;return t=t.replace(un,':host([dir="$1"])'),t=t.replace(fn,':host([dir="$2"]) $1'),e!==t&&(this.__activateDir=!0),t}constructor(){super(),this.__autoDirOptOut=!1}ready(){super.ready(),this.__autoDirOptOut=this.hasAttribute("dir")}connectedCallback(){t.prototype.connectedCallback&&super.connectedCallback(),this.constructor.__activateDir&&(mn&&mn.takeRecords().length&&vn(),_n.push(this),bn(this))}disconnectedCallback(){if(t.prototype.disconnectedCallback&&super.disconnectedCallback(),this.constructor.__activateDir){const e=_n.indexOf(this);e>-1&&_n.splice(e,1)}}}return n.__activateDir=!1,n});function Cn(){document.body.removeAttribute("unresolved")}function Pn(e,t,n){return{index:e,removed:t,addedCount:n}}"interactive"===document.readyState||"complete"===document.readyState?Cn():window.addEventListener("DOMContentLoaded",Cn);function xn(e,t,n,r,i,s){let o,a=0,l=0,p=Math.min(n-t,s-i);if(0==t&&0==i&&(a=function(e,t,n){for(let r=0;r<n;r++)if(!En(e[r],t[r]))return r;return n}(e,r,p)),n==e.length&&s==r.length&&(l=function(e,t,n){let r=e.length,i=t.length,s=0;for(;s<n&&En(e[--r],t[--i]);)s++;return s}(e,r,p-a)),i+=a,s-=l,(n-=l)-(t+=a)==0&&s-i==0)return[];if(t==n){for(o=Pn(t,[],0);i<s;)o.removed.push(r[i++]);return[o]}if(i==s)return[Pn(t,[],n-t)];let d=function(e){let t=e.length-1,n=e[0].length-1,r=e[t][n],i=[];for(;t>0||n>0;){if(0==t){i.push(2),n--;continue}if(0==n){i.push(3),t--;continue}let s,o=e[t-1][n-1],a=e[t-1][n],l=e[t][n-1];s=a<l?a<o?a:o:l<o?l:o,s==o?(o==r?i.push(0):(i.push(1),r=o),t--,n--):s==a?(i.push(3),t--,r=a):(i.push(2),n--,r=l)}return i.reverse(),i}(function(e,t,n,r,i,s){let o=s-i+1,a=n-t+1,l=new Array(o);for(let e=0;e<o;e++)l[e]=new Array(a),l[e][0]=e;for(let e=0;e<a;e++)l[0][e]=e;for(let n=1;n<o;n++)for(let s=1;s<a;s++)if(En(e[t+s-1],r[i+n-1]))l[n][s]=l[n-1][s-1];else{let e=l[n-1][s]+1,t=l[n][s-1]+1;l[n][s]=e<t?e:t}return l}(e,t,n,r,i,s));o=void 0;let c=[],h=t,u=i;for(let e=0;e<d.length;e++)switch(d[e]){case 0:o&&(c.push(o),o=void 0),h++,u++;break;case 1:o||(o=Pn(h,[],0)),o.addedCount++,h++,o.removed.push(r[u]),u++;break;case 2:o||(o=Pn(h,[],0)),o.addedCount++,h++;break;case 3:o||(o=Pn(h,[],0)),o.removed.push(r[u]),u++}return o&&c.push(o),c}function Sn(e,t){return xn(e,0,e.length,t,0,t.length)}function En(e,t){return e===t}function Tn(e){return"slot"===e.localName}class On{static getFlattenedNodes(e){return Tn(e)?(e=e).assignedNodes({flatten:!0}):Array.from(e.childNodes).map(e=>Tn(e)?(e=e).assignedNodes({flatten:!0}):[e]).reduce((e,t)=>e.concat(t),[])}constructor(e,t){this._shadyChildrenObserver=null,this._nativeChildrenObserver=null,this._connected=!1,this._target=e,this.callback=t,this._effectiveNodes=[],this._observer=null,this._scheduled=!1,this._boundSchedule=()=>{this._schedule()},this.connect(),this._schedule()}connect(){Tn(this._target)?this._listenSlots([this._target]):this._target.children&&(this._listenSlots(this._target.children),window.ShadyDOM?this._shadyChildrenObserver=ShadyDOM.observeChildren(this._target,e=>{this._processMutations(e)}):(this._nativeChildrenObserver=new MutationObserver(e=>{this._processMutations(e)}),this._nativeChildrenObserver.observe(this._target,{childList:!0}))),this._connected=!0}disconnect(){Tn(this._target)?this._unlistenSlots([this._target]):this._target.children&&(this._unlistenSlots(this._target.children),window.ShadyDOM&&this._shadyChildrenObserver?(ShadyDOM.unobserveChildren(this._shadyChildrenObserver),this._shadyChildrenObserver=null):this._nativeChildrenObserver&&(this._nativeChildrenObserver.disconnect(),this._nativeChildrenObserver=null)),this._connected=!1}_schedule(){this._scheduled||(this._scheduled=!0,ze.run(()=>this.flush()))}_processMutations(e){this._processSlotMutations(e),this.flush()}_processSlotMutations(e){if(e)for(let t=0;t<e.length;t++){let n=e[t];n.addedNodes&&this._listenSlots(n.addedNodes),n.removedNodes&&this._unlistenSlots(n.removedNodes)}}flush(){if(!this._connected)return!1;window.ShadyDOM&&ShadyDOM.flush(),this._nativeChildrenObserver?this._processSlotMutations(this._nativeChildrenObserver.takeRecords()):this._shadyChildrenObserver&&this._processSlotMutations(this._shadyChildrenObserver.takeRecords()),this._scheduled=!1;let e={target:this._target,addedNodes:[],removedNodes:[]},t=this.constructor.getFlattenedNodes(this._target),n=Sn(t,this._effectiveNodes);for(let t,r=0;r<n.length&&(t=n[r]);r++)for(let n,r=0;r<t.removed.length&&(n=t.removed[r]);r++)e.removedNodes.push(n);for(let r,i=0;i<n.length&&(r=n[i]);i++)for(let n=r.index;n<r.index+r.addedCount;n++)e.addedNodes.push(t[n]);this._effectiveNodes=t;let r=!1;return(e.addedNodes.length||e.removedNodes.length)&&(r=!0,this.callback.call(this._target,e)),r}_listenSlots(e){for(let t=0;t<e.length;t++){let n=e[t];Tn(n)&&n.addEventListener("slotchange",this._boundSchedule)}}_unlistenSlots(e){for(let t=0;t<e.length;t++){let n=e[t];Tn(n)&&n.removeEventListener("slotchange",this._boundSchedule)}}}let kn=[];const An=function(e){kn.push(e)};function Nn(){const e=Boolean(kn.length);for(;kn.length;)try{kn.shift().flush()}catch(e){setTimeout(()=>{throw e})}return e}const In=function(){let e,t;do{e=window.ShadyDOM&&ShadyDOM.flush(),window.ShadyCSS&&window.ShadyCSS.ScopingShim&&window.ShadyCSS.ScopingShim.flush(),t=Nn()}while(e||t)},Ln=Element.prototype,Mn=Ln.matches||Ln.matchesSelector||Ln.mozMatchesSelector||Ln.msMatchesSelector||Ln.oMatchesSelector||Ln.webkitMatchesSelector,Rn=function(e,t){return Mn.call(e,t)};class Dn{constructor(e){this.node=e}observeNodes(e){return new On(this.node,e)}unobserveNodes(e){e.disconnect()}notifyObserver(){}deepContains(e){if(this.node.contains(e))return!0;let t=e,n=e.ownerDocument;for(;t&&t!==n&&t!==this.node;)t=t.parentNode||t.host;return t===this.node}getOwnerRoot(){return this.node.getRootNode()}getDistributedNodes(){return"slot"===this.node.localName?this.node.assignedNodes({flatten:!0}):[]}getDestinationInsertionPoints(){let e=[],t=this.node.assignedSlot;for(;t;)e.push(t),t=t.assignedSlot;return e}importNode(e,t){return(this.node instanceof Document?this.node:this.node.ownerDocument).importNode(e,t)}getEffectiveChildNodes(){return On.getFlattenedNodes(this.node)}queryDistributedElements(e){let t=this.getEffectiveChildNodes(),n=[];for(let r,i=0,s=t.length;i<s&&(r=t[i]);i++)r.nodeType===Node.ELEMENT_NODE&&Rn(r,e)&&n.push(r);return n}get activeElement(){let e=this.node;return void 0!==e._activeElement?e._activeElement:e.activeElement}}class Hn{constructor(e){this.event=e}get rootTarget(){return this.event.composedPath()[0]}get localTarget(){return this.event.target}get path(){return this.event.composedPath()}}Dn.prototype.cloneNode,Dn.prototype.appendChild,Dn.prototype.insertBefore,Dn.prototype.removeChild,Dn.prototype.replaceChild,Dn.prototype.setAttribute,Dn.prototype.removeAttribute,Dn.prototype.querySelector,Dn.prototype.querySelectorAll,Dn.prototype.parentNode,Dn.prototype.firstChild,Dn.prototype.lastChild,Dn.prototype.nextSibling,Dn.prototype.previousSibling,Dn.prototype.firstElementChild,Dn.prototype.lastElementChild,Dn.prototype.nextElementSibling,Dn.prototype.previousElementSibling,Dn.prototype.childNodes,Dn.prototype.children,Dn.prototype.classList,Dn.prototype.textContent,Dn.prototype.innerHTML,function(e,t){for(let n=0;n<t.length;n++){let r=t[n];e[r]=function(){return this.node[r].apply(this.node,arguments)}}}(Dn.prototype,["cloneNode","appendChild","insertBefore","removeChild","replaceChild","setAttribute","removeAttribute","querySelector","querySelectorAll"]),function(e,t){for(let n=0;n<t.length;n++){let r=t[n];Object.defineProperty(e,r,{get:function(){return this.node[r]},configurable:!0})}}(Dn.prototype,["parentNode","firstChild","lastChild","nextSibling","previousSibling","firstElementChild","lastElementChild","nextElementSibling","previousElementSibling","childNodes","children","classList"]),function(e,t){for(let n=0;n<t.length;n++){let r=t[n];Object.defineProperty(e,r,{get:function(){return this.node[r]},set:function(e){this.node[r]=e},configurable:!0})}}(Dn.prototype,["textContent","innerHTML"]);const Fn=function(e){if(!(e=e||document).__domApi){let t;t=e instanceof Event?new Hn(e):new Dn(e),e.__domApi=t}return e.__domApi};let Bn=window.ShadyCSS;const zn=le(e=>{const t=wn(hn(kt(e))),n={x:"pan-x",y:"pan-y",none:"none",all:"auto"};class r extends t{constructor(){super(),this.isAttached,this.__boundListeners,this._debouncers,this._applyListeners()}static get importMeta(){return this.prototype.importMeta}created(){}connectedCallback(){super.connectedCallback(),this.isAttached=!0,this.attached()}attached(){}disconnectedCallback(){super.disconnectedCallback(),this.isAttached=!1,this.detached()}detached(){}attributeChangedCallback(e,t,n,r){t!==n&&(super.attributeChangedCallback(e,t,n,r),this.attributeChanged(e,t,n))}attributeChanged(e,t,n){}_initializeProperties(){let e=Object.getPrototypeOf(this);e.hasOwnProperty("__hasRegisterFinished")||(e.__hasRegisterFinished=!0,this._registered()),super._initializeProperties(),this.root=this,this.created()}_registered(){}ready(){this._ensureAttributes(),super.ready()}_ensureAttributes(){}_applyListeners(){}serialize(e){return this._serializeValue(e)}deserialize(e,t){return this._deserializeValue(e,t)}reflectPropertyToAttribute(e,t,n){this._propertyToAttribute(e,t,n)}serializeValueToAttribute(e,t,n){this._valueToNodeAttribute(n||this,e,t)}extend(e,t){if(!e||!t)return e||t;let n=Object.getOwnPropertyNames(t);for(let r,i=0;i<n.length&&(r=n[i]);i++){let n=Object.getOwnPropertyDescriptor(t,r);n&&Object.defineProperty(e,r,n)}return e}mixin(e,t){for(let n in t)e[n]=t[n];return e}chainObject(e,t){return e&&t&&e!==t&&(e.__proto__=t),e}instanceTemplate(e){let t=this.constructor._contentForTemplate(e);return document.importNode(t,!0)}fire(e,t,n){n=n||{},t=null==t?{}:t;let r=new Event(e,{bubbles:void 0===n.bubbles||n.bubbles,cancelable:Boolean(n.cancelable),composed:void 0===n.composed||n.composed});return r.detail=t,(n.node||this).dispatchEvent(r),r}listen(e,t,n){e=e||this;let r=this.__boundListeners||(this.__boundListeners=new WeakMap),i=r.get(e);i||(i={},r.set(e,i));let s=t+n;i[s]||(i[s]=this._addMethodEventListenerToNode(e,t,n,this))}unlisten(e,t,n){e=e||this;let r=this.__boundListeners&&this.__boundListeners.get(e),i=t+n,s=r&&r[i];s&&(this._removeEventListenerFromNode(e,t,s),r[i]=null)}setScrollDirection(e,t){sn(t||this,n[e]||"auto")}$$(e){return this.root.querySelector(e)}get domHost(){let e=this.getRootNode();return e instanceof DocumentFragment?e.host:e}distributeContent(){window.ShadyDOM&&this.shadowRoot&&ShadyDOM.flush()}getEffectiveChildNodes(){return Fn(this).getEffectiveChildNodes()}queryDistributedElements(e){return Fn(this).queryDistributedElements(e)}getEffectiveChildren(){return this.getEffectiveChildNodes().filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}getEffectiveTextContent(){let e=this.getEffectiveChildNodes(),t=[];for(let n,r=0;n=e[r];r++)n.nodeType!==Node.COMMENT_NODE&&t.push(n.textContent);return t.join("")}queryEffectiveChildren(e){let t=this.queryDistributedElements(e);return t&&t[0]}queryAllEffectiveChildren(e){return this.queryDistributedElements(e)}getContentChildNodes(e){let t=this.root.querySelector(e||"slot");return t?Fn(t).getDistributedNodes():[]}getContentChildren(e){return this.getContentChildNodes(e).filter((function(e){return e.nodeType===Node.ELEMENT_NODE}))}isLightDescendant(e){return this!==e&&this.contains(e)&&this.getRootNode()===e.getRootNode()}isLocalDescendant(e){return this.root===e.getRootNode()}scopeSubtree(e,t){}getComputedStyleValue(e){return Bn.getComputedStyleValue(this,e)}debounce(e,t,n){return this._debouncers=this._debouncers||{},this._debouncers[e]=At.debounce(this._debouncers[e],n>0?Fe.after(n):ze,t.bind(this))}isDebouncerActive(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];return!(!t||!t.isActive())}flushDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.flush()}cancelDebouncer(e){this._debouncers=this._debouncers||{};let t=this._debouncers[e];t&&t.cancel()}async(e,t){return t>0?Fe.run(e.bind(this),t):~ze.run(e.bind(this))}cancelAsync(e){e<0?ze.cancel(~e):Fe.cancel(e)}create(e,t){let n=document.createElement(e);if(t)if(n.setProperties)n.setProperties(t);else for(let e in t)n[e]=t[e];return n}elementMatches(e,t){return Rn(t||this,e)}toggleAttribute(e,t){let n=this;return 3===arguments.length&&(n=arguments[2]),1==arguments.length&&(t=!n.hasAttribute(e)),t?(n.setAttribute(e,""),!0):(n.removeAttribute(e),!1)}toggleClass(e,t,n){n=n||this,1==arguments.length&&(t=!n.classList.contains(e)),t?n.classList.add(e):n.classList.remove(e)}transform(e,t){(t=t||this).style.webkitTransform=e,t.style.transform=e}translate3d(e,t,n,r){r=r||this,this.transform("translate3d("+e+","+t+","+n+")",r)}arrayDelete(e,t){let n;if(Array.isArray(e)){if(n=e.indexOf(t),n>=0)return e.splice(n,1)}else{if(n=Ee(this,e).indexOf(t),n>=0)return this.splice(e,n,1)}return null}_logger(e,t){switch(Array.isArray(t)&&1===t.length&&Array.isArray(t[0])&&(t=t[0]),e){case"log":case"warn":case"error":console[e](...t)}}_log(...e){this._logger("log",e)}_warn(...e){this._logger("warn",e)}_error(...e){this._logger("error",e)}_logf(e,...t){return["[%s::%s]",this.is,e,...t]}}return r.prototype.is="",r});let jn={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,behaviors:!0};function Kn(e,t){if(!e)return t=t;t=zn(t),Array.isArray(e)||(e=[e]);let n=t.prototype.behaviors;return t=function e(t,n){for(let r=0;r<t.length;r++){let i=t[r];i&&(n=Array.isArray(i)?e(i,n):qn(i,n))}return n}(e=function e(t,n,r){n=n||[];for(let i=t.length-1;i>=0;i--){let s=t[i];s?Array.isArray(s)?e(s,n):n.indexOf(s)<0&&(!r||r.indexOf(s)<0)&&n.unshift(s):console.warn("behavior is null, check for missing or 404 import")}return n}(e,null,n),t),n&&(e=n.concat(e)),t.prototype.behaviors=e,t}function qn(e,t){class n extends t{static get properties(){return e.properties}static get observers(){return e.observers}created(){super.created(),e.created&&e.created.call(this)}_registered(){super._registered(),e.beforeRegister&&e.beforeRegister.call(Object.getPrototypeOf(this)),e.registered&&e.registered.call(Object.getPrototypeOf(this))}_applyListeners(){if(super._applyListeners(),e.listeners)for(let t in e.listeners)this._addMethodEventListenerToNode(this,t,e.listeners[t])}_ensureAttributes(){if(e.hostAttributes)for(let t in e.hostAttributes)this._ensureAttribute(t,e.hostAttributes[t]);super._ensureAttributes()}ready(){super.ready(),e.ready&&e.ready.call(this)}attached(){super.attached(),e.attached&&e.attached.call(this)}detached(){super.detached(),e.detached&&e.detached.call(this)}attributeChanged(t,n,r){super.attributeChanged(t,n,r),e.attributeChanged&&e.attributeChanged.call(this,t,n,r)}}n.generatedFrom=e;for(let t in e)if(!(t in jn)){let r=Object.getOwnPropertyDescriptor(e,t);r&&Object.defineProperty(n.prototype,t,r)}return n}const Yn=function(e){let t;return t="function"==typeof e?e:Yn.Class(e),customElements.define(t.is,t),t};function Vn(e,t,n,r,i){let s;i&&(s="object"==typeof n&&null!==n,s&&(r=e.__dataTemp[t]));let o=r!==n&&(r==r||n==n);return s&&o&&(e.__dataTemp[t]=n),o}Yn.Class=function(e,t){e||console.warn("Polymer's Class function requires `info` argument");const n=e.behaviors?Kn(e.behaviors,HTMLElement):zn(HTMLElement),r=qn(e,t?t(n):n);return r.is=e.is,r};const Un=le(e=>class extends e{_shouldPropertyChange(e,t,n){return Vn(this,e,t,n,!0)}}),$n=le(e=>class extends e{static get properties(){return{mutableData:Boolean}}_shouldPropertyChange(e,t,n){return Vn(this,e,t,n,this.mutableData)}});Un._mutablePropertyChange=Vn;let Xn=null;function Jn(){return Xn}Jn.prototype=Object.create(HTMLTemplateElement.prototype,{constructor:{value:Jn,writable:!0}});const Gn=Et(Jn),Wn=Un(Gn);const Zn=Et(class{});class Qn extends Zn{constructor(e){super(),this._configureProperties(e),this.root=this._stampTemplate(this.__dataHost);let t=this.children=[];for(let e=this.root.firstChild;e;e=e.nextSibling)t.push(e),e.__templatizeInstance=this;this.__templatizeOwner&&this.__templatizeOwner.__hideTemplateChildren__&&this._showHideChildren(!0);let n=this.__templatizeOptions;(e&&n.instanceProps||!n.instanceProps)&&this._enableProperties()}_configureProperties(e){if(this.__templatizeOptions.forwardHostProp)for(let e in this.__hostProps)this._setPendingProperty(e,this.__dataHost["_host_"+e]);for(let t in e)this._setPendingProperty(t,e[t])}forwardHostProp(e,t){this._setPendingPropertyOrPath(e,t,!1,!0)&&this.__dataHost._enqueueClient(this)}_addEventListenerToNode(e,t,n){if(this._methodHost&&this.__templatizeOptions.parentModel)this._methodHost._addEventListenerToNode(e,t,e=>{e.model=this,n(e)});else{let r=this.__dataHost.__dataHost;r&&r._addEventListenerToNode(e,t,n)}}_showHideChildren(e){let t=this.children;for(let n=0;n<t.length;n++){let r=t[n];if(Boolean(e)!=Boolean(r.__hideTemplateChildren__))if(r.nodeType===Node.TEXT_NODE)e?(r.__polymerTextContent__=r.textContent,r.textContent=""):r.textContent=r.__polymerTextContent__;else if("slot"===r.localName)if(e)r.__polymerReplaced__=document.createComment("hidden-slot"),r.parentNode.replaceChild(r.__polymerReplaced__,r);else{const e=r.__polymerReplaced__;e&&e.parentNode.replaceChild(r,e)}else r.style&&(e?(r.__polymerDisplay__=r.style.display,r.style.display="none"):r.style.display=r.__polymerDisplay__);r.__hideTemplateChildren__=e,r._showHideChildren&&r._showHideChildren(e)}}_setUnmanagedPropertyToNode(e,t,n){e.__hideTemplateChildren__&&e.nodeType==Node.TEXT_NODE&&"textContent"==t?e.__polymerTextContent__=n:super._setUnmanagedPropertyToNode(e,t,n)}get parentModel(){let e=this.__parentModel;if(!e){let t;e=this;do{e=e.__dataHost.__dataHost}while((t=e.__templatizeOptions)&&!t.parentModel);this.__parentModel=e}return e}dispatchEvent(e){return!0}}Qn.prototype.__dataHost,Qn.prototype.__templatizeOptions,Qn.prototype._methodHost,Qn.prototype.__templatizeOwner,Qn.prototype.__hostProps;const er=Un(Qn);function tr(e,t,n){let r=n.mutableData?er:Qn,i=class extends r{};return i.prototype.__templatizeOptions=n,i.prototype._bindTemplate(e),function(e,t,n,r){let i=n.hostProps||{};for(let t in r.instanceProps){delete i[t];let n=r.notifyInstanceProp;n&&e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:ir(t,n)})}if(r.forwardHostProp&&t.__dataHost)for(let t in i)e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:function(e,t,n){e.__dataHost._setPendingPropertyOrPath("_host_"+t,n[t],!0,!0)}})}(i,e,t,n),i}function nr(e,t,n){let r=n.forwardHostProp;if(r){let i=t.templatizeTemplateClass;if(!i){let e=n.mutableData?Wn:Gn;i=t.templatizeTemplateClass=class extends e{};let s=t.hostProps;for(let e in s)i.prototype._addPropertyEffect("_host_"+e,i.prototype.PROPERTY_EFFECT_TYPES.PROPAGATE,{fn:rr(e,r)}),i.prototype._createNotifyingProperty("_host_"+e)}!function(e,t){Xn=e,Object.setPrototypeOf(e,t.prototype),new t,Xn=null}(e,i),e.__dataProto&&Object.assign(e.__data,e.__dataProto),e.__dataTemp={},e.__dataPending=null,e.__dataOld=null,e._enableProperties()}}function rr(e,t){return function(e,n,r){t.call(e.__templatizeOwner,n.substring("_host_".length),r[n])}}function ir(e,t){return function(e,n,r){t.call(e.__templatizeOwner,e,n,r[n])}}function sr(e,t,n){if(n=n||{},e.__templatizeOwner)throw new Error("A <template> can only be templatized once");e.__templatizeOwner=t;let r=(t?t.constructor:Qn)._parseTemplate(e),i=r.templatizeInstanceClass;i||(i=tr(e,r,n),r.templatizeInstanceClass=i),nr(e,r,n);let s=class extends i{};return s.prototype._methodHost=function(e){let t=e.__dataHost;return t&&t._methodHost||t}(e),s.prototype.__dataHost=e,s.prototype.__templatizeOwner=t,s.prototype.__hostProps=r.hostProps,s=s,s}const or=hn($n(Et(HTMLElement)));customElements.define("dom-bind",class extends or{static get observedAttributes(){return["mutable-data"]}constructor(){super(),this.root=null,this.$=null,this.__children=null}attributeChangedCallback(){this.mutableData=!0}connectedCallback(){this.style.display="none",this.render()}disconnectedCallback(){this.__removeChildren()}__insertChildren(){this.parentNode.insertBefore(this.root,this)}__removeChildren(){if(this.__children)for(let e=0;e<this.__children.length;e++)this.root.appendChild(this.__children[e])}render(){let e;if(!this.__children){if(e=e||this.querySelector("template"),!e){let t=new MutationObserver(()=>{if(e=this.querySelector("template"),!e)throw new Error("dom-bind requires a <template> child");t.disconnect(),this.render()});return void t.observe(this,{childList:!0})}this.root=this._stampTemplate(e),this.$=this.root.$,this.__children=[];for(let e=this.root.firstChild;e;e=e.nextSibling)this.__children[this.__children.length]=e;this._enableProperties()}this.__insertChildren(),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0}))}});class ar{constructor(e){this.value=e.toString()}toString(){return this.value}}function lr(e){if(e instanceof HTMLTemplateElement)return e.innerHTML;if(e instanceof ar)return function(e){if(e instanceof ar)return e.value;throw new Error("non-literal value passed to Polymer's htmlLiteral function: "+e)}(e);throw new Error("non-template value passed to Polymer's html function: "+e)}const pr=function(e,...t){const n=document.createElement("template");return n.innerHTML=t.reduce((t,n,r)=>t+lr(n)+e[r+1],e[0]),n},dr=kt(HTMLElement),cr=$n(dr);class hr extends cr{static get is(){return"dom-repeat"}static get template(){return null}static get properties(){return{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},itemsIndexAs:{type:String,value:"itemsIndex"},sort:{type:Function,observer:"__sortChanged"},filter:{type:Function,observer:"__filterChanged"},observe:{type:String,observer:"__observeChanged"},delay:Number,renderedItemCount:{type:Number,notify:!0,readOnly:!0},initialCount:{type:Number,observer:"__initializeChunking"},targetFramerate:{type:Number,value:20},_targetFrameTime:{type:Number,computed:"__computeFrameTime(targetFramerate)"}}}static get observers(){return["__itemsChanged(items.*)"]}constructor(){super(),this.__instances=[],this.__limit=1/0,this.__pool=[],this.__renderDebouncer=null,this.__itemsIdxToInstIdx={},this.__chunkCount=null,this.__lastChunkTime=null,this.__sortFn=null,this.__filterFn=null,this.__observePaths=null,this.__ctor=null,this.__isDetached=!0,this.template=null}disconnectedCallback(){super.disconnectedCallback(),this.__isDetached=!0;for(let e=0;e<this.__instances.length;e++)this.__detachInstance(e)}connectedCallback(){if(super.connectedCallback(),this.style.display="none",this.__isDetached){this.__isDetached=!1;let e=this.parentNode;for(let t=0;t<this.__instances.length;t++)this.__attachInstance(t,e)}}__ensureTemplatized(){if(!this.__ctor){let e=this.template=this.querySelector("template");if(!e){let e=new MutationObserver(()=>{if(!this.querySelector("template"))throw new Error("dom-repeat requires a <template> child");e.disconnect(),this.__render()});return e.observe(this,{childList:!0}),!1}let t={};t[this.as]=!0,t[this.indexAs]=!0,t[this.itemsIndexAs]=!0,this.__ctor=sr(e,this,{mutableData:this.mutableData,parentModel:!0,instanceProps:t,forwardHostProp:function(e,t){let n=this.__instances;for(let r,i=0;i<n.length&&(r=n[i]);i++)r.forwardHostProp(e,t)},notifyInstanceProp:function(e,t,n){if(function(e,t){return e===t||we(e,t)||Ce(e,t)}(this.as,t)){let r=e[this.itemsIndexAs];t==this.as&&(this.items[r]=n);let i=Pe(this.as,"items."+r,t);this.notifyPath(i,n)}}})}return!0}__getMethodHost(){return this.__dataHost._methodHost||this.__dataHost}__functionFromPropertyValue(e){if("string"==typeof e){let t=e,n=this.__getMethodHost();return function(){return n[t].apply(n,arguments)}}return e}__sortChanged(e){this.__sortFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__filterChanged(e){this.__filterFn=this.__functionFromPropertyValue(e),this.items&&this.__debounceRender(this.__render)}__computeFrameTime(e){return Math.ceil(1e3/e)}__initializeChunking(){this.initialCount&&(this.__limit=this.initialCount,this.__chunkCount=this.initialCount,this.__lastChunkTime=performance.now())}__tryRenderChunk(){this.items&&this.__limit<this.items.length&&this.__debounceRender(this.__requestRenderChunk)}__requestRenderChunk(){requestAnimationFrame(()=>this.__renderChunk())}__renderChunk(){let e=performance.now(),t=this._targetFrameTime/(e-this.__lastChunkTime);this.__chunkCount=Math.round(this.__chunkCount*t)||1,this.__limit+=this.__chunkCount,this.__lastChunkTime=e,this.__debounceRender(this.__render)}__observeChanged(){this.__observePaths=this.observe&&this.observe.replace(".*",".").split(" ")}__itemsChanged(e){this.items&&!Array.isArray(this.items)&&console.warn("dom-repeat expected array for `items`, found",this.items),this.__handleItemPath(e.path,e.value)||(this.__initializeChunking(),this.__debounceRender(this.__render))}__handleObservedPaths(e){if(this.__sortFn||this.__filterFn)if(e){if(this.__observePaths){let t=this.__observePaths;for(let n=0;n<t.length;n++)0===e.indexOf(t[n])&&this.__debounceRender(this.__render,this.delay)}}else this.__debounceRender(this.__render,this.delay)}__debounceRender(e,t=0){this.__renderDebouncer=At.debounce(this.__renderDebouncer,t>0?Fe.after(t):ze,e.bind(this)),An(this.__renderDebouncer)}render(){this.__debounceRender(this.__render),In()}__render(){this.__ensureTemplatized()&&(this.__applyFullRefresh(),this.__pool.length=0,this._setRenderedItemCount(this.__instances.length),this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this.__tryRenderChunk())}__applyFullRefresh(){let e=this.items||[],t=new Array(e.length);for(let n=0;n<e.length;n++)t[n]=n;this.__filterFn&&(t=t.filter((t,n,r)=>this.__filterFn(e[t],n,r))),this.__sortFn&&t.sort((t,n)=>this.__sortFn(e[t],e[n]));const n=this.__itemsIdxToInstIdx={};let r=0;const i=Math.min(t.length,this.__limit);for(;r<i;r++){let i=this.__instances[r],s=t[r],o=e[s];n[s]=r,i?(i._setPendingProperty(this.as,o),i._setPendingProperty(this.indexAs,r),i._setPendingProperty(this.itemsIndexAs,s),i._flushProperties()):this.__insertInstance(o,r,s)}for(let e=this.__instances.length-1;e>=r;e--)this.__detachAndRemoveInstance(e)}__detachInstance(e){let t=this.__instances[e];for(let e=0;e<t.children.length;e++){let n=t.children[e];t.root.appendChild(n)}return t}__attachInstance(e,t){let n=this.__instances[e];t.insertBefore(n.root,this)}__detachAndRemoveInstance(e){let t=this.__detachInstance(e);t&&this.__pool.push(t),this.__instances.splice(e,1)}__stampInstance(e,t,n){let r={};return r[this.as]=e,r[this.indexAs]=t,r[this.itemsIndexAs]=n,new this.__ctor(r)}__insertInstance(e,t,n){let r=this.__pool.pop();r?(r._setPendingProperty(this.as,e),r._setPendingProperty(this.indexAs,t),r._setPendingProperty(this.itemsIndexAs,n),r._flushProperties()):r=this.__stampInstance(e,t,n);let i=this.__instances[t+1],s=i?i.children[0]:this;return this.parentNode.insertBefore(r.root,s),this.__instances[t]=r,r}_showHideChildren(e){for(let t=0;t<this.__instances.length;t++)this.__instances[t]._showHideChildren(e)}__handleItemPath(e,t){let n=e.slice(6),r=n.indexOf("."),i=r<0?n:n.substring(0,r);if(i==parseInt(i,10)){let e=r<0?"":n.substring(r+1);this.__handleObservedPaths(e);let s=this.__itemsIdxToInstIdx[i],o=this.__instances[s];if(o){let n=this.as+(e?"."+e:"");o._setPendingPropertyOrPath(n,t,!1,!0),o._flushProperties()}return!0}}itemForElement(e){let t=this.modelForElement(e);return t&&t[this.as]}indexForElement(e){let t=this.modelForElement(e);return t&&t[this.indexAs]}modelForElement(e){return function(e,t){let n;for(;t;)if(n=t.__templatizeInstance){if(n.__dataHost==e)return n;t=n.__dataHost}else t=t.parentNode;return null}(this.template,e)}}customElements.define(hr.is,hr);class ur extends dr{static get is(){return"dom-if"}static get template(){return null}static get properties(){return{if:{type:Boolean,observer:"__debounceRender"},restamp:{type:Boolean,observer:"__debounceRender"}}}constructor(){super(),this.__renderDebouncer=null,this.__invalidProps=null,this.__instance=null,this._lastIf=!1,this.__ctor=null,this.__hideTemplateChildren__=!1}__debounceRender(){this.__renderDebouncer=At.debounce(this.__renderDebouncer,ze,()=>this.__render()),An(this.__renderDebouncer)}disconnectedCallback(){super.disconnectedCallback(),this.parentNode&&(this.parentNode.nodeType!=Node.DOCUMENT_FRAGMENT_NODE||this.parentNode.host)||this.__teardownInstance()}connectedCallback(){super.connectedCallback(),this.style.display="none",this.if&&this.__debounceRender()}render(){In()}__render(){if(this.if){if(!this.__ensureInstance())return;this._showHideChildren()}else this.restamp&&this.__teardownInstance();!this.restamp&&this.__instance&&this._showHideChildren(),this.if!=this._lastIf&&(this.dispatchEvent(new CustomEvent("dom-change",{bubbles:!0,composed:!0})),this._lastIf=this.if)}__ensureInstance(){let e=this.parentNode;if(e){if(!this.__ctor){let e=this.querySelector("template");if(!e){let e=new MutationObserver(()=>{if(!this.querySelector("template"))throw new Error("dom-if requires a <template> child");e.disconnect(),this.__render()});return e.observe(this,{childList:!0}),!1}this.__ctor=sr(e,this,{mutableData:!0,forwardHostProp:function(e,t){this.__instance&&(this.if?this.__instance.forwardHostProp(e,t):(this.__invalidProps=this.__invalidProps||Object.create(null),this.__invalidProps[ve(e)]=!0))}})}if(this.__instance){this.__syncHostProperties();let t=this.__instance.children;if(t&&t.length){if(this.previousSibling!==t[t.length-1])for(let n,r=0;r<t.length&&(n=t[r]);r++)e.insertBefore(n,this)}}else this.__instance=new this.__ctor,e.insertBefore(this.__instance.root,this)}return!0}__syncHostProperties(){let e=this.__invalidProps;if(e){for(let t in e)this.__instance._setPendingProperty(t,this.__dataHost[t]);this.__invalidProps=null,this.__instance._flushProperties()}}__teardownInstance(){if(this.__instance){let e=this.__instance.children;if(e&&e.length){let t=e[0].parentNode;if(t)for(let n,r=0;r<e.length&&(n=e[r]);r++)t.removeChild(n)}this.__instance=null,this.__invalidProps=null}}_showHideChildren(){let e=this.__hideTemplateChildren__||!this.if;this.__instance&&this.__instance._showHideChildren(e)}}customElements.define(ur.is,ur);let fr=le(e=>{let t=kt(e);return class extends t{static get properties(){return{items:{type:Array},multi:{type:Boolean,value:!1},selected:{type:Object,notify:!0},selectedItem:{type:Object,notify:!0},toggle:{type:Boolean,value:!1}}}static get observers(){return["__updateSelection(multi, items.*)"]}constructor(){super(),this.__lastItems=null,this.__lastMulti=null,this.__selectedMap=null}__updateSelection(e,t){let n=t.path;if("items"==n){let n=t.base||[],r=this.__lastItems;if(e!==this.__lastMulti&&this.clearSelection(),r){let e=Sn(n,r);this.__applySplices(e)}this.__lastItems=n,this.__lastMulti=e}else if("items.splices"==t.path)this.__applySplices(t.value.indexSplices);else{let e=n.slice("items.".length),t=parseInt(e,10);e.indexOf(".")<0&&e==t&&this.__deselectChangedIdx(t)}}__applySplices(e){let t=this.__selectedMap;for(let n=0;n<e.length;n++){let r=e[n];t.forEach((e,n)=>{e<r.index||(e>=r.index+r.removed.length?t.set(n,e+r.addedCount-r.removed.length):t.set(n,-1))});for(let e=0;e<r.addedCount;e++){let n=r.index+e;t.has(this.items[n])&&t.set(this.items[n],n)}}this.__updateLinks();let n=0;t.forEach((e,r)=>{e<0?(this.multi?this.splice("selected",n,1):this.selected=this.selectedItem=null,t.delete(r)):n++})}__updateLinks(){if(this.__dataLinkedPaths={},this.multi){let e=0;this.__selectedMap.forEach(t=>{t>=0&&this.linkPaths("items."+t,"selected."+e++)})}else this.__selectedMap.forEach(e=>{this.linkPaths("selected","items."+e),this.linkPaths("selectedItem","items."+e)})}clearSelection(){this.__dataLinkedPaths={},this.__selectedMap=new Map,this.selected=this.multi?[]:null,this.selectedItem=null}isSelected(e){return this.__selectedMap.has(e)}isIndexSelected(e){return this.isSelected(this.items[e])}__deselectChangedIdx(e){let t=this.__selectedIndexForItemIndex(e);if(t>=0){let e=0;this.__selectedMap.forEach((n,r)=>{t==e++&&this.deselect(r)})}}__selectedIndexForItemIndex(e){let t=this.__dataLinkedPaths["items."+e];if(t)return parseInt(t.slice("selected.".length),10)}deselect(e){let t=this.__selectedMap.get(e);if(t>=0){let n;this.__selectedMap.delete(e),this.multi&&(n=this.__selectedIndexForItemIndex(t)),this.__updateLinks(),this.multi?this.splice("selected",n,1):this.selected=this.selectedItem=null}}deselectIndex(e){this.deselect(this.items[e])}select(e){this.selectIndex(this.items.indexOf(e))}selectIndex(e){let t=this.items[e];this.isSelected(t)?this.toggle&&this.deselectIndex(e):(this.multi||this.__selectedMap.clear(),this.__selectedMap.set(t,e),this.__updateLinks(),this.multi?this.push("selected",t):this.selected=this.selectedItem=t)}}})(dr);class _r extends fr{static get is(){return"array-selector"}}customElements.define(_r.is,_r);const mr=new X;window.ShadyCSS||(window.ShadyCSS={prepareTemplate(e,t,n){},prepareTemplateDom(e,t){},prepareTemplateStyles(e,t,n){},styleSubtree(e,t){mr.processStyles(),T(e,t)},styleElement(e){mr.processStyles()},styleDocument(e){mr.processStyles(),T(document.body,e)},getComputedStyleValue:(e,t)=>O(e,t),flushCustomStyles(){},nativeCss:s,nativeShadow:e,cssBuild:n,disableRuntime:i}),window.ShadyCSS.CustomStyleInterface=mr;const yr=window.ShadyCSS.CustomStyleInterface;class gr extends HTMLElement{constructor(){super(),this._style=null,yr.addCustomStyle(this)}getStyle(){if(this._style)return this._style;const e=this.querySelector("style");if(!e)return null;this._style=e;const t=e.getAttribute("include");return t&&(e.removeAttribute("include"),e.textContent=function(e){let t=e.trim().split(/\s+/),n="";for(let e=0;e<t.length;e++)n+=ge(t[e]);return n}(t)+e.textContent),this.ownerDocument!==window.document&&window.document.head.appendChild(this),this._style}}window.customElements.define("custom-style",gr),zn(HTMLElement).prototype;const br=pr`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;br.setAttribute("style","display: none;"),document.head.appendChild(br.content);var vr=document.createElement("style");if(vr.textContent="[hidden] { display: none !important; }",document.head.appendChild(vr),!window.polymerSkipLoadingFontRoboto){const e=document.createElement("link");e.rel="stylesheet",e.type="text/css",e.crossOrigin="anonymous",e.href="https://fonts.googleapis.com/css?family=Roboto+Mono:400,700|Roboto:400,300,300italic,400italic,500,500italic,700,700italic",document.head.appendChild(e)}const wr=pr`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;wr.setAttribute("style","display: none;"),document.head.appendChild(wr.content);const Cr=pr`
<custom-style>
  <style is="custom-style">
    html {

      /* Material Design color palette for Google products */

      --google-red-100: #f4c7c3;
      --google-red-300: #e67c73;
      --google-red-500: #db4437;
      --google-red-700: #c53929;

      --google-blue-100: #c6dafc;
      --google-blue-300: #7baaf7;
      --google-blue-500: #4285f4;
      --google-blue-700: #3367d6;

      --google-green-100: #b7e1cd;
      --google-green-300: #57bb8a;
      --google-green-500: #0f9d58;
      --google-green-700: #0b8043;

      --google-yellow-100: #fce8b2;
      --google-yellow-300: #f7cb4d;
      --google-yellow-500: #f4b400;
      --google-yellow-700: #f09300;

      --google-grey-100: #f5f5f5;
      --google-grey-300: #e0e0e0;
      --google-grey-500: #9e9e9e;
      --google-grey-700: #616161;

      /* Material Design color palette from online spec document */

      --paper-red-50: #ffebee;
      --paper-red-100: #ffcdd2;
      --paper-red-200: #ef9a9a;
      --paper-red-300: #e57373;
      --paper-red-400: #ef5350;
      --paper-red-500: #f44336;
      --paper-red-600: #e53935;
      --paper-red-700: #d32f2f;
      --paper-red-800: #c62828;
      --paper-red-900: #b71c1c;
      --paper-red-a100: #ff8a80;
      --paper-red-a200: #ff5252;
      --paper-red-a400: #ff1744;
      --paper-red-a700: #d50000;

      --paper-pink-50: #fce4ec;
      --paper-pink-100: #f8bbd0;
      --paper-pink-200: #f48fb1;
      --paper-pink-300: #f06292;
      --paper-pink-400: #ec407a;
      --paper-pink-500: #e91e63;
      --paper-pink-600: #d81b60;
      --paper-pink-700: #c2185b;
      --paper-pink-800: #ad1457;
      --paper-pink-900: #880e4f;
      --paper-pink-a100: #ff80ab;
      --paper-pink-a200: #ff4081;
      --paper-pink-a400: #f50057;
      --paper-pink-a700: #c51162;

      --paper-purple-50: #f3e5f5;
      --paper-purple-100: #e1bee7;
      --paper-purple-200: #ce93d8;
      --paper-purple-300: #ba68c8;
      --paper-purple-400: #ab47bc;
      --paper-purple-500: #9c27b0;
      --paper-purple-600: #8e24aa;
      --paper-purple-700: #7b1fa2;
      --paper-purple-800: #6a1b9a;
      --paper-purple-900: #4a148c;
      --paper-purple-a100: #ea80fc;
      --paper-purple-a200: #e040fb;
      --paper-purple-a400: #d500f9;
      --paper-purple-a700: #aa00ff;

      --paper-deep-purple-50: #ede7f6;
      --paper-deep-purple-100: #d1c4e9;
      --paper-deep-purple-200: #b39ddb;
      --paper-deep-purple-300: #9575cd;
      --paper-deep-purple-400: #7e57c2;
      --paper-deep-purple-500: #673ab7;
      --paper-deep-purple-600: #5e35b1;
      --paper-deep-purple-700: #512da8;
      --paper-deep-purple-800: #4527a0;
      --paper-deep-purple-900: #311b92;
      --paper-deep-purple-a100: #b388ff;
      --paper-deep-purple-a200: #7c4dff;
      --paper-deep-purple-a400: #651fff;
      --paper-deep-purple-a700: #6200ea;

      --paper-indigo-50: #e8eaf6;
      --paper-indigo-100: #c5cae9;
      --paper-indigo-200: #9fa8da;
      --paper-indigo-300: #7986cb;
      --paper-indigo-400: #5c6bc0;
      --paper-indigo-500: #3f51b5;
      --paper-indigo-600: #3949ab;
      --paper-indigo-700: #303f9f;
      --paper-indigo-800: #283593;
      --paper-indigo-900: #1a237e;
      --paper-indigo-a100: #8c9eff;
      --paper-indigo-a200: #536dfe;
      --paper-indigo-a400: #3d5afe;
      --paper-indigo-a700: #304ffe;

      --paper-blue-50: #e3f2fd;
      --paper-blue-100: #bbdefb;
      --paper-blue-200: #90caf9;
      --paper-blue-300: #64b5f6;
      --paper-blue-400: #42a5f5;
      --paper-blue-500: #2196f3;
      --paper-blue-600: #1e88e5;
      --paper-blue-700: #1976d2;
      --paper-blue-800: #1565c0;
      --paper-blue-900: #0d47a1;
      --paper-blue-a100: #82b1ff;
      --paper-blue-a200: #448aff;
      --paper-blue-a400: #2979ff;
      --paper-blue-a700: #2962ff;

      --paper-light-blue-50: #e1f5fe;
      --paper-light-blue-100: #b3e5fc;
      --paper-light-blue-200: #81d4fa;
      --paper-light-blue-300: #4fc3f7;
      --paper-light-blue-400: #29b6f6;
      --paper-light-blue-500: #03a9f4;
      --paper-light-blue-600: #039be5;
      --paper-light-blue-700: #0288d1;
      --paper-light-blue-800: #0277bd;
      --paper-light-blue-900: #01579b;
      --paper-light-blue-a100: #80d8ff;
      --paper-light-blue-a200: #40c4ff;
      --paper-light-blue-a400: #00b0ff;
      --paper-light-blue-a700: #0091ea;

      --paper-cyan-50: #e0f7fa;
      --paper-cyan-100: #b2ebf2;
      --paper-cyan-200: #80deea;
      --paper-cyan-300: #4dd0e1;
      --paper-cyan-400: #26c6da;
      --paper-cyan-500: #00bcd4;
      --paper-cyan-600: #00acc1;
      --paper-cyan-700: #0097a7;
      --paper-cyan-800: #00838f;
      --paper-cyan-900: #006064;
      --paper-cyan-a100: #84ffff;
      --paper-cyan-a200: #18ffff;
      --paper-cyan-a400: #00e5ff;
      --paper-cyan-a700: #00b8d4;

      --paper-teal-50: #e0f2f1;
      --paper-teal-100: #b2dfdb;
      --paper-teal-200: #80cbc4;
      --paper-teal-300: #4db6ac;
      --paper-teal-400: #26a69a;
      --paper-teal-500: #009688;
      --paper-teal-600: #00897b;
      --paper-teal-700: #00796b;
      --paper-teal-800: #00695c;
      --paper-teal-900: #004d40;
      --paper-teal-a100: #a7ffeb;
      --paper-teal-a200: #64ffda;
      --paper-teal-a400: #1de9b6;
      --paper-teal-a700: #00bfa5;

      --paper-green-50: #e8f5e9;
      --paper-green-100: #c8e6c9;
      --paper-green-200: #a5d6a7;
      --paper-green-300: #81c784;
      --paper-green-400: #66bb6a;
      --paper-green-500: #4caf50;
      --paper-green-600: #43a047;
      --paper-green-700: #388e3c;
      --paper-green-800: #2e7d32;
      --paper-green-900: #1b5e20;
      --paper-green-a100: #b9f6ca;
      --paper-green-a200: #69f0ae;
      --paper-green-a400: #00e676;
      --paper-green-a700: #00c853;

      --paper-light-green-50: #f1f8e9;
      --paper-light-green-100: #dcedc8;
      --paper-light-green-200: #c5e1a5;
      --paper-light-green-300: #aed581;
      --paper-light-green-400: #9ccc65;
      --paper-light-green-500: #8bc34a;
      --paper-light-green-600: #7cb342;
      --paper-light-green-700: #689f38;
      --paper-light-green-800: #558b2f;
      --paper-light-green-900: #33691e;
      --paper-light-green-a100: #ccff90;
      --paper-light-green-a200: #b2ff59;
      --paper-light-green-a400: #76ff03;
      --paper-light-green-a700: #64dd17;

      --paper-lime-50: #f9fbe7;
      --paper-lime-100: #f0f4c3;
      --paper-lime-200: #e6ee9c;
      --paper-lime-300: #dce775;
      --paper-lime-400: #d4e157;
      --paper-lime-500: #cddc39;
      --paper-lime-600: #c0ca33;
      --paper-lime-700: #afb42b;
      --paper-lime-800: #9e9d24;
      --paper-lime-900: #827717;
      --paper-lime-a100: #f4ff81;
      --paper-lime-a200: #eeff41;
      --paper-lime-a400: #c6ff00;
      --paper-lime-a700: #aeea00;

      --paper-yellow-50: #fffde7;
      --paper-yellow-100: #fff9c4;
      --paper-yellow-200: #fff59d;
      --paper-yellow-300: #fff176;
      --paper-yellow-400: #ffee58;
      --paper-yellow-500: #ffeb3b;
      --paper-yellow-600: #fdd835;
      --paper-yellow-700: #fbc02d;
      --paper-yellow-800: #f9a825;
      --paper-yellow-900: #f57f17;
      --paper-yellow-a100: #ffff8d;
      --paper-yellow-a200: #ffff00;
      --paper-yellow-a400: #ffea00;
      --paper-yellow-a700: #ffd600;

      --paper-amber-50: #fff8e1;
      --paper-amber-100: #ffecb3;
      --paper-amber-200: #ffe082;
      --paper-amber-300: #ffd54f;
      --paper-amber-400: #ffca28;
      --paper-amber-500: #ffc107;
      --paper-amber-600: #ffb300;
      --paper-amber-700: #ffa000;
      --paper-amber-800: #ff8f00;
      --paper-amber-900: #ff6f00;
      --paper-amber-a100: #ffe57f;
      --paper-amber-a200: #ffd740;
      --paper-amber-a400: #ffc400;
      --paper-amber-a700: #ffab00;

      --paper-orange-50: #fff3e0;
      --paper-orange-100: #ffe0b2;
      --paper-orange-200: #ffcc80;
      --paper-orange-300: #ffb74d;
      --paper-orange-400: #ffa726;
      --paper-orange-500: #ff9800;
      --paper-orange-600: #fb8c00;
      --paper-orange-700: #f57c00;
      --paper-orange-800: #ef6c00;
      --paper-orange-900: #e65100;
      --paper-orange-a100: #ffd180;
      --paper-orange-a200: #ffab40;
      --paper-orange-a400: #ff9100;
      --paper-orange-a700: #ff6500;

      --paper-deep-orange-50: #fbe9e7;
      --paper-deep-orange-100: #ffccbc;
      --paper-deep-orange-200: #ffab91;
      --paper-deep-orange-300: #ff8a65;
      --paper-deep-orange-400: #ff7043;
      --paper-deep-orange-500: #ff5722;
      --paper-deep-orange-600: #f4511e;
      --paper-deep-orange-700: #e64a19;
      --paper-deep-orange-800: #d84315;
      --paper-deep-orange-900: #bf360c;
      --paper-deep-orange-a100: #ff9e80;
      --paper-deep-orange-a200: #ff6e40;
      --paper-deep-orange-a400: #ff3d00;
      --paper-deep-orange-a700: #dd2c00;

      --paper-brown-50: #efebe9;
      --paper-brown-100: #d7ccc8;
      --paper-brown-200: #bcaaa4;
      --paper-brown-300: #a1887f;
      --paper-brown-400: #8d6e63;
      --paper-brown-500: #795548;
      --paper-brown-600: #6d4c41;
      --paper-brown-700: #5d4037;
      --paper-brown-800: #4e342e;
      --paper-brown-900: #3e2723;

      --paper-grey-50: #fafafa;
      --paper-grey-100: #f5f5f5;
      --paper-grey-200: #eeeeee;
      --paper-grey-300: #e0e0e0;
      --paper-grey-400: #bdbdbd;
      --paper-grey-500: #9e9e9e;
      --paper-grey-600: #757575;
      --paper-grey-700: #616161;
      --paper-grey-800: #424242;
      --paper-grey-900: #212121;

      --paper-blue-grey-50: #eceff1;
      --paper-blue-grey-100: #cfd8dc;
      --paper-blue-grey-200: #b0bec5;
      --paper-blue-grey-300: #90a4ae;
      --paper-blue-grey-400: #78909c;
      --paper-blue-grey-500: #607d8b;
      --paper-blue-grey-600: #546e7a;
      --paper-blue-grey-700: #455a64;
      --paper-blue-grey-800: #37474f;
      --paper-blue-grey-900: #263238;

      /* opacity for dark text on a light background */
      --dark-divider-opacity: 0.12;
      --dark-disabled-opacity: 0.38; /* or hint text or icon */
      --dark-secondary-opacity: 0.54;
      --dark-primary-opacity: 0.87;

      /* opacity for light text on a dark background */
      --light-divider-opacity: 0.12;
      --light-disabled-opacity: 0.3; /* or hint text or icon */
      --light-secondary-opacity: 0.7;
      --light-primary-opacity: 1.0;

    }

  </style>
</custom-style>
`;Cr.setAttribute("style","display: none;"),document.head.appendChild(Cr.content);const Pr=pr`
<custom-style>
  <style is="custom-style">
    html {
      /*
       * You can use these generic variables in your elements for easy theming.
       * For example, if all your elements use \`--primary-text-color\` as its main
       * color, then switching from a light to a dark theme is just a matter of
       * changing the value of \`--primary-text-color\` in your application.
       */
      --primary-text-color: var(--light-theme-text-color);
      --primary-background-color: var(--light-theme-background-color);
      --secondary-text-color: var(--light-theme-secondary-color);
      --disabled-text-color: var(--light-theme-disabled-color);
      --divider-color: var(--light-theme-divider-color);
      --error-color: var(--paper-deep-orange-a700);

      /*
       * Primary and accent colors. Also see color.js for more colors.
       */
      --primary-color: var(--paper-indigo-500);
      --light-primary-color: var(--paper-indigo-100);
      --dark-primary-color: var(--paper-indigo-700);

      --accent-color: var(--paper-pink-a200);
      --light-accent-color: var(--paper-pink-a100);
      --dark-accent-color: var(--paper-pink-a400);


      /*
       * Material Design Light background theme
       */
      --light-theme-background-color: #ffffff;
      --light-theme-base-color: #000000;
      --light-theme-text-color: var(--paper-grey-900);
      --light-theme-secondary-color: #737373;  /* for secondary text and icons */
      --light-theme-disabled-color: #9b9b9b;  /* disabled/hint text */
      --light-theme-divider-color: #dbdbdb;

      /*
       * Material Design Dark background theme
       */
      --dark-theme-background-color: var(--paper-grey-900);
      --dark-theme-base-color: #ffffff;
      --dark-theme-text-color: #ffffff;
      --dark-theme-secondary-color: #bcbcbc;  /* for secondary text and icons */
      --dark-theme-disabled-color: #646464;  /* disabled/hint text */
      --dark-theme-divider-color: #3c3c3c;

      /*
       * Deprecated values because of their confusing names.
       */
      --text-primary-color: var(--dark-theme-text-color);
      --default-primary-color: var(--primary-color);
    }
  </style>
</custom-style>`;Pr.setAttribute("style","display: none;"),document.head.appendChild(Pr.content);const xr=document.createElement("template");xr.setAttribute("style","display: none;"),xr.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(xr.content);const Sr={properties:{focused:{type:Boolean,value:!1,notify:!0,readOnly:!0,reflectToAttribute:!0},disabled:{type:Boolean,value:!1,notify:!0,observer:"_disabledChanged",reflectToAttribute:!0},_oldTabIndex:{type:String},_boundFocusBlurHandler:{type:Function,value:function(){return this._focusBlurHandler.bind(this)}}},observers:["_changedControlState(focused, disabled)"],ready:function(){this.addEventListener("focus",this._boundFocusBlurHandler,!0),this.addEventListener("blur",this._boundFocusBlurHandler,!0)},_focusBlurHandler:function(e){this._setFocused("focus"===e.type)},_disabledChanged:function(e,t){this.setAttribute("aria-disabled",e?"true":"false"),this.style.pointerEvents=e?"none":"",e?(this._oldTabIndex=this.getAttribute("tabindex"),this._setFocused(!1),this.tabIndex=-1,this.blur()):void 0!==this._oldTabIndex&&(null===this._oldTabIndex?this.removeAttribute("tabindex"):this.setAttribute("tabindex",this._oldTabIndex))},_changedControlState:function(){this._controlStateChanged&&this._controlStateChanged()}};var Er={"U+0008":"backspace","U+0009":"tab","U+001B":"esc","U+0020":"space","U+007F":"del"},Tr={8:"backspace",9:"tab",13:"enter",27:"esc",33:"pageup",34:"pagedown",35:"end",36:"home",32:"space",37:"left",38:"up",39:"right",40:"down",46:"del",106:"*"},Or={shift:"shiftKey",ctrl:"ctrlKey",alt:"altKey",meta:"metaKey"},kr=/[a-z0-9*]/,Ar=/U\+/,Nr=/^arrow/,Ir=/^space(bar)?/,Lr=/^escape$/;function Mr(e,t){var n="";if(e){var r=e.toLowerCase();" "===r||Ir.test(r)?n="space":Lr.test(r)?n="esc":1==r.length?t&&!kr.test(r)||(n=r):n=Nr.test(r)?r.replace("arrow",""):"multiply"==r?"*":r}return n}function Rr(e,t){return e.key?Mr(e.key,t):e.detail&&e.detail.key?Mr(e.detail.key,t):(n=e.keyIdentifier,r="",n&&(n in Er?r=Er[n]:Ar.test(n)?(n=parseInt(n.replace("U+","0x"),16),r=String.fromCharCode(n).toLowerCase()):r=n.toLowerCase()),r||function(e){var t="";return Number(e)&&(t=e>=65&&e<=90?String.fromCharCode(32+e):e>=112&&e<=123?"f"+(e-112+1):e>=48&&e<=57?String(e-48):e>=96&&e<=105?String(e-96):Tr[e]),t}(e.keyCode)||"");var n,r}function Dr(e,t){return Rr(t,e.hasModifiers)===e.key&&(!e.hasModifiers||!!t.shiftKey==!!e.shiftKey&&!!t.ctrlKey==!!e.ctrlKey&&!!t.altKey==!!e.altKey&&!!t.metaKey==!!e.metaKey)}function Hr(e){return e.trim().split(" ").map((function(e){return function(e){return 1===e.length?{combo:e,key:e,event:"keydown"}:e.split("+").reduce((function(e,t){var n=t.split(":"),r=n[0],i=n[1];return r in Or?(e[Or[r]]=!0,e.hasModifiers=!0):(e.key=r,e.event=i||"keydown"),e}),{combo:e.split(":").shift()})}(e)}))}const Fr={properties:{keyEventTarget:{type:Object,value:function(){return this}},stopKeyboardEventPropagation:{type:Boolean,value:!1},_boundKeyHandlers:{type:Array,value:function(){return[]}},_imperativeKeyBindings:{type:Object,value:function(){return{}}}},observers:["_resetKeyEventListeners(keyEventTarget, _boundKeyHandlers)"],keyBindings:{},registered:function(){this._prepKeyBindings()},attached:function(){this._listenKeyEventListeners()},detached:function(){this._unlistenKeyEventListeners()},addOwnKeyBinding:function(e,t){this._imperativeKeyBindings[e]=t,this._prepKeyBindings(),this._resetKeyEventListeners()},removeOwnKeyBindings:function(){this._imperativeKeyBindings={},this._prepKeyBindings(),this._resetKeyEventListeners()},keyboardEventMatchesKeys:function(e,t){for(var n=Hr(t),r=0;r<n.length;++r)if(Dr(n[r],e))return!0;return!1},_collectKeyBindings:function(){var e=this.behaviors.map((function(e){return e.keyBindings}));return-1===e.indexOf(this.keyBindings)&&e.push(this.keyBindings),e},_prepKeyBindings:function(){for(var e in this._keyBindings={},this._collectKeyBindings().forEach((function(e){for(var t in e)this._addKeyBinding(t,e[t])}),this),this._imperativeKeyBindings)this._addKeyBinding(e,this._imperativeKeyBindings[e]);for(var t in this._keyBindings)this._keyBindings[t].sort((function(e,t){var n=e[0].hasModifiers;return n===t[0].hasModifiers?0:n?-1:1}))},_addKeyBinding:function(e,t){Hr(e).forEach((function(e){this._keyBindings[e.event]=this._keyBindings[e.event]||[],this._keyBindings[e.event].push([e,t])}),this)},_resetKeyEventListeners:function(){this._unlistenKeyEventListeners(),this.isAttached&&this._listenKeyEventListeners()},_listenKeyEventListeners:function(){this.keyEventTarget&&Object.keys(this._keyBindings).forEach((function(e){var t=this._keyBindings[e],n=this._onKeyBindingEvent.bind(this,t);this._boundKeyHandlers.push([this.keyEventTarget,e,n]),this.keyEventTarget.addEventListener(e,n)}),this)},_unlistenKeyEventListeners:function(){for(var e,t,n,r;this._boundKeyHandlers.length;)t=(e=this._boundKeyHandlers.pop())[0],n=e[1],r=e[2],t.removeEventListener(n,r)},_onKeyBindingEvent:function(e,t){if(this.stopKeyboardEventPropagation&&t.stopPropagation(),!t.defaultPrevented)for(var n=0;n<e.length;n++){var r=e[n][0],i=e[n][1];if(Dr(r,t)&&(this._triggerKeyHandler(r,i,t),t.defaultPrevented))return}},_triggerKeyHandler:function(e,t,n){var r=Object.create(e);r.keyboardEvent=n;var i=new CustomEvent(e.event,{detail:r,cancelable:!0});this[t].call(this,i),i.defaultPrevented&&n.preventDefault()}},Br=[[Fr,{properties:{pressed:{type:Boolean,readOnly:!0,value:!1,reflectToAttribute:!0,observer:"_pressedChanged"},toggles:{type:Boolean,value:!1,reflectToAttribute:!0},active:{type:Boolean,value:!1,notify:!0,reflectToAttribute:!0},pointerDown:{type:Boolean,readOnly:!0,value:!1},receivedFocusFromKeyboard:{type:Boolean,readOnly:!0},ariaActiveAttribute:{type:String,value:"aria-pressed",observer:"_ariaActiveAttributeChanged"}},listeners:{down:"_downHandler",up:"_upHandler",tap:"_tapHandler"},observers:["_focusChanged(focused)","_activeChanged(active, ariaActiveAttribute)"],keyBindings:{"enter:keydown":"_asyncClick","space:keydown":"_spaceKeyDownHandler","space:keyup":"_spaceKeyUpHandler"},_mouseEventRe:/^mouse/,_tapHandler:function(){this.toggles?this._userActivate(!this.active):this.active=!1},_focusChanged:function(e){this._detectKeyboardFocus(e),e||this._setPressed(!1)},_detectKeyboardFocus:function(e){this._setReceivedFocusFromKeyboard(!this.pointerDown&&e)},_userActivate:function(e){this.active!==e&&(this.active=e,this.fire("change"))},_downHandler:function(e){this._setPointerDown(!0),this._setPressed(!0),this._setReceivedFocusFromKeyboard(!1)},_upHandler:function(){this._setPointerDown(!1),this._setPressed(!1)},_spaceKeyDownHandler:function(e){var t=e.detail.keyboardEvent,n=Fn(t).localTarget;this.isLightDescendant(n)||(t.preventDefault(),t.stopImmediatePropagation(),this._setPressed(!0))},_spaceKeyUpHandler:function(e){var t=e.detail.keyboardEvent,n=Fn(t).localTarget;this.isLightDescendant(n)||(this.pressed&&this._asyncClick(),this._setPressed(!1))},_asyncClick:function(){this.async((function(){this.click()}),1)},_pressedChanged:function(e){this._changedButtonState()},_ariaActiveAttributeChanged:function(e,t){t&&t!=e&&this.hasAttribute(t)&&this.removeAttribute(t)},_activeChanged:function(e,t){this.toggles?this.setAttribute(this.ariaActiveAttribute,e?"true":"false"):this.removeAttribute(this.ariaActiveAttribute),this._changedButtonState()},_controlStateChanged:function(){this.disabled?this._setPressed(!1):this._changedButtonState()},_changedButtonState:function(){this._buttonStateChanged&&this._buttonStateChanged()}}],Sr,{hostAttributes:{role:"option",tabindex:"0"}}];Yn({_template:pr`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"});export{At as D,Fr as I,Yn as P,Br as a,Ne as b,Be as c,Fn as d,An as e,tn as f,Sr as g,pr as h,ie as u};
