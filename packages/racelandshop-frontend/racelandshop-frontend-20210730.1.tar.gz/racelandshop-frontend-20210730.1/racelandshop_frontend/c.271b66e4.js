import{a9 as e,aa as a,$ as s,ab as r,ac as u}from"./main-adfe0fa2.js";async function i(i,o,n){const t=new e("updateLovelaceResources"),l=await a(i),d="/racelandshopfiles/"+o.full_name.split("/")[1],c=s({repository:o,version:n}),p=l.find(e=>e.url.includes(d));t.debug({namespace:d,url:c,exsisting:p}),p&&p.url!==c?(t.debug("Updating exsusting resource for "+d),await r(i,{url:c,resource_id:p.id,res_type:p.type})):l.map(e=>e.url).includes(c)||(t.debug(`Adding ${c} to Lovelace resources`),await u(i,{url:c,res_type:"module"}))}export{i as u};
