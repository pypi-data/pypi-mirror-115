(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6478],{23682:(t,e,n)=>{"use strict";function s(t,e){if(e.length<t)throw new TypeError(t+" argument"+(t>1?"s":"")+" required, but only "+e.length+" present")}n.d(e,{Z:()=>s})},90394:(t,e,n)=>{"use strict";function s(t){if(null===t||!0===t||!1===t)return NaN;var e=Number(t);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}n.d(e,{Z:()=>s})},59699:(t,e,n)=>{"use strict";n.d(e,{Z:()=>a});var s=n(90394),r=n(39244),i=n(23682),o=36e5;function a(t,e){(0,i.Z)(2,arguments);var n=(0,s.Z)(e);return(0,r.Z)(t,n*o)}},39244:(t,e,n)=>{"use strict";n.d(e,{Z:()=>o});var s=n(90394),r=n(34327),i=n(23682);function o(t,e){(0,i.Z)(2,arguments);var n=(0,r.Z)(t).getTime(),o=(0,s.Z)(e);return new Date(n+o)}},93752:(t,e,n)=>{"use strict";n.d(e,{Z:()=>i});var s=n(34327),r=n(23682);function i(t){(0,r.Z)(1,arguments);var e=(0,s.Z)(t);return e.setHours(23,59,59,999),e}},70390:(t,e,n)=>{"use strict";n.d(e,{Z:()=>r});var s=n(93752);function r(){return(0,s.Z)(Date.now())}},61334:(t,e,n)=>{"use strict";function s(){var t=new Date,e=t.getFullYear(),n=t.getMonth(),s=t.getDate(),r=new Date(0);return r.setFullYear(e,n,s-1),r.setHours(23,59,59,999),r}n.d(e,{Z:()=>s})},59429:(t,e,n)=>{"use strict";n.d(e,{Z:()=>i});var s=n(34327),r=n(23682);function i(t){(0,r.Z)(1,arguments);var e=(0,s.Z)(t);return e.setHours(0,0,0,0),e}},27088:(t,e,n)=>{"use strict";n.d(e,{Z:()=>r});var s=n(59429);function r(){return(0,s.Z)(Date.now())}},83008:(t,e,n)=>{"use strict";function s(){var t=new Date,e=t.getFullYear(),n=t.getMonth(),s=t.getDate(),r=new Date(0);return r.setFullYear(e,n,s-1),r.setHours(0,0,0,0),r}n.d(e,{Z:()=>s})},34327:(t,e,n)=>{"use strict";n.d(e,{Z:()=>r});var s=n(23682);function r(t){(0,s.Z)(1,arguments);var e=Object.prototype.toString.call(t);return t instanceof Date||"object"==typeof t&&"[object Date]"===e?new Date(t.getTime()):"number"==typeof t||"[object Number]"===e?new Date(t):("string"!=typeof t&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},85415:(t,e,n)=>{"use strict";n.d(e,{q:()=>s,w:()=>r});const s=(t,e)=>t<e?-1:t>e?1:0,r=(t,e)=>s(t.toLowerCase(),e.toLowerCase())},11950:(t,e,n)=>{"use strict";n.d(e,{l:()=>s});const s=async(t,e)=>new Promise((n=>{const s=e(t,(t=>{s(),n(t)}))}))},57066:(t,e,n)=>{"use strict";n.d(e,{Lo:()=>o,IO:()=>a,qv:()=>c,sG:()=>_});var s=n(95282),r=n(85415),i=n(38346);const o=(t,e)=>t.callWS({type:"config/area_registry/create",...e}),a=(t,e,n)=>t.callWS({type:"config/area_registry/update",area_id:e,...n}),c=(t,e)=>t.callWS({type:"config/area_registry/delete",area_id:e}),u=t=>t.sendMessagePromise({type:"config/area_registry/list"}).then((t=>t.sort(((t,e)=>(0,r.q)(t.name,e.name))))),l=(t,e)=>t.subscribeEvents((0,i.D)((()=>u(t).then((t=>e.setState(t,!0)))),500,!0),"area_registry_updated"),_=(t,e)=>(0,s.B)("_areaRegistry",u,l,t,e)},81582:(t,e,n)=>{"use strict";n.d(e,{LZ:()=>s,pB:()=>r,SO:()=>i,iJ:()=>o,Nn:()=>a,Ny:()=>c,T0:()=>u});const s=2143==n.j?["migration_error","setup_error","setup_retry"]:null,r=t=>t.callApi("GET","config/config_entries/entry"),i=(t,e,n)=>t.callWS({type:"config_entries/update",entry_id:e,...n}),o=(t,e)=>t.callApi("DELETE",`config/config_entries/entry/${e}`),a=(t,e)=>t.callApi("POST",`config/config_entries/entry/${e}/reload`),c=(t,e)=>t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:"user"}),u=(t,e)=>t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:null})},57292:(t,e,n)=>{"use strict";n.d(e,{jL:()=>o,t1:()=>a,q4:()=>l});var s=n(95282),r=n(91741),i=n(38346);const o=(t,e,n)=>t.name_by_user||t.name||n&&((t,e)=>{for(const n of e||[]){const e="string"==typeof n?n:n.entity_id,s=t.states[e];if(s)return(0,r.C)(s)}})(e,n)||e.localize("ui.panel.config.devices.unnamed_device"),a=(t,e,n)=>t.callWS({type:"config/device_registry/update",device_id:e,...n}),c=t=>t.sendMessagePromise({type:"config/device_registry/list"}),u=(t,e)=>t.subscribeEvents((0,i.D)((()=>c(t).then((t=>e.setState(t,!0)))),500,!0),"device_registry_updated"),l=(t,e)=>(0,s.B)("_dr",c,u,t,e)},55424:(t,e,n)=>{"use strict";n.d(e,{Bm:()=>y,o1:()=>p,iK:()=>g,rl:()=>h,ZC:()=>b,_Z:()=>v,Jj:()=>w,UB:()=>Z});var s=n(59699),r=n(27088),i=n(83008),o=n(70390),a=n(61334),c=n(95282),u=n(11950),l=n(81582),_=n(74186),d=n(58763);const f=[],y=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),p=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),g=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),h=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),m=t=>t.callWS({type:"energy/info"}),b=t=>t.callWS({type:"energy/get_prefs"}),v=async(t,e)=>{const n=t.callWS({type:"energy/save_prefs",...e});return S(t),n},w=t=>{const e={};for(const n of t.energy_sources)n.type in e?e[n.type].push(n):e[n.type]=[n];return e},S=t=>{f.forEach((e=>{const n=Z(t,{key:e});n.clearPrefs(),n._active&&n.refresh()}))},Z=(t,e={})=>{let n="_energy";if(e.key){if(!e.key.startsWith("energy_"))throw new Error("Key need to start with energy_");n=`_${e.key}`}if(t.connection[n])return t.connection[n];f.push(e.key||"energy");const y=(0,c._)(t.connection,n,(async()=>{if(y.prefs||(y.prefs=await b(t)),y._refreshTimeout&&clearTimeout(y._refreshTimeout),y._active&&(!y.end||y.end>new Date)){const t=new Date;t.getMinutes()>20&&t.setHours(t.getHours()+1),t.setMinutes(20),y._refreshTimeout=window.setTimeout((()=>y.refresh()),t.getTime()-Date.now())}return(async(t,e,n,r)=>{const[i,o,a]=await Promise.all([(0,l.pB)(t),(0,u.l)(t.connection,_.LM),m(t)]),c=i.find((t=>"co2signal"===t.domain));let f;if(c)for(const e of o){if(e.config_entry_id!==c.entry_id)continue;const n=t.states[e.entity_id];if(n&&"%"===n.attributes.unit_of_measurement){f=n.entity_id;break}}const y=[];void 0!==f&&y.push(f);for(const t of e.energy_sources)if("solar"!==t.type){for(const e of t.flow_from){y.push(e.stat_energy_from),e.stat_cost&&y.push(e.stat_cost);const t=a.cost_sensors[e.stat_energy_from];t&&y.push(t)}for(const e of t.flow_to){y.push(e.stat_energy_to),e.stat_compensation&&y.push(e.stat_compensation);const t=a.cost_sensors[e.stat_energy_to];t&&y.push(t)}}else y.push(t.stat_energy_from);return{start:n,end:r,info:a,prefs:e,stats:await(0,d.dL)(t,(0,s.Z)(n,-1),r,y),co2SignalConfigEntry:c,co2SignalEntity:f}})(t,y.prefs,y.start,y.end)})),p=y.subscribe;y.subscribe=t=>{const e=p(t);return y._active++,()=>{y._active--,y._active<1&&(clearTimeout(y._refreshTimeout),y._refreshTimeout=void 0),e()}},y._active=0,y.prefs=e.prefs;const g=new Date;y.start=g.getHours()>0?(0,r.Z)():(0,i.Z)(),y.end=g.getHours()>0?(0,o.Z)():(0,a.Z)();const h=()=>{y._updatePeriodTimeout=window.setTimeout((()=>{y.start=(0,r.Z)(),y.end=(0,o.Z)(),h()}),(0,s.Z)((0,o.Z)(),1).getTime()-Date.now())};return h(),y.clearPrefs=()=>{y.prefs=void 0},y.setPeriod=(t,e)=>{var n;y.start=t,y.end=e,y._updatePeriodTimeout&&(clearTimeout(y._updatePeriodTimeout),y._updatePeriodTimeout=void 0),y.start.getTime()===(0,r.Z)().getTime()&&(null===(n=y.end)||void 0===n?void 0:n.getTime())===(0,o.Z)().getTime()&&h()},y}},74186:(t,e,n)=>{"use strict";n.d(e,{eD:()=>o,Mw:()=>a,vA:()=>c,L3:()=>u,Nv:()=>l,z3:()=>_,LM:()=>y});var s=n(95282),r=n(91741),i=n(38346);const o=(t,e)=>e.find((e=>t.states[e.entity_id]&&"battery"===t.states[e.entity_id].attributes.device_class)),a=(t,e)=>e.find((e=>t.states[e.entity_id]&&"battery_charging"===t.states[e.entity_id].attributes.device_class)),c=(t,e)=>{if(e.name)return e.name;const n=t.states[e.entity_id];return n?(0,r.C)(n):null},u=(t,e)=>t.callWS({type:"config/entity_registry/get",entity_id:e}),l=(t,e,n)=>t.callWS({type:"config/entity_registry/update",entity_id:e,...n}),_=(t,e)=>t.callWS({type:"config/entity_registry/remove",entity_id:e}),d=t=>t.sendMessagePromise({type:"config/entity_registry/list"}),f=(t,e)=>t.subscribeEvents((0,i.D)((()=>d(t).then((t=>e.setState(t,!0)))),500,!0),"entity_registry_updated"),y=(t,e)=>(0,s.B)("_entityRegistry",d,f,t,e)},58763:(t,e,n)=>{"use strict";n.d(e,{vq:()=>c,_J:()=>u,Nu:()=>_,uR:()=>d,dL:()=>f,Kj:()=>y,q6:()=>p,Nw:()=>g,m2:()=>m});var s=n(29171),r=n(22311),i=n(91741);const o=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],c=(t,e,n,s,r=!1,i,o=!0)=>{let a="history/period";return n&&(a+="/"+n.toISOString()),a+="?filter_entity_id="+e,s&&(a+="&end_time="+s.toISOString()),r&&(a+="&skip_initial_state"),void 0!==i&&(a+=`&significant_changes_only=${Number(i)}`),o&&(a+="&minimal_response"),t.callApi("GET",a)},u=(t,e,n,s)=>t.callApi("GET",`history/period/${e.toISOString()}?end_time=${n.toISOString()}&minimal_response${s?`&filter_entity_id=${s}`:""}`),l=(t,e)=>t.state===e.state&&(!t.attributes||!e.attributes||a.every((n=>t.attributes[n]===e.attributes[n]))),_=(t,e,n)=>{const c={},u=[];if(!e)return{line:[],timeline:[]};e.forEach((e=>{if(0===e.length)return;const o=e.find((t=>t.attributes&&"unit_of_measurement"in t.attributes));let a;a=o?o.attributes.unit_of_measurement:{climate:t.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:t.config.unit_system.temperature}[(0,r.N)(e[0])],a?a in c?c[a].push(e):c[a]=[e]:u.push(((t,e,n)=>{const r=[],o=n.length-1;for(const i of n)r.length>0&&i.state===r[r.length-1].state||(i.entity_id||(i.attributes=n[o].attributes,i.entity_id=n[o].entity_id),r.push({state_localize:(0,s.D)(t,i,e),state:i.state,last_changed:i.last_changed}));return{name:(0,i.C)(n[0]),entity_id:n[0].entity_id,data:r}})(n,t.locale,e))}));return{line:Object.keys(c).map((t=>((t,e)=>{const n=[];for(const t of e){const e=t[t.length-1],s=(0,r.N)(e),c=[];for(const e of t){let t;if(o.includes(s)){t={state:e.state,last_changed:e.last_updated,attributes:{}};for(const n of a)n in e.attributes&&(t.attributes[n]=e.attributes[n])}else t=e;c.length>1&&l(t,c[c.length-1])&&l(t,c[c.length-2])||c.push(t)}n.push({domain:s,name:(0,i.C)(e),entity_id:e.entity_id,states:c})}return{unit:t,identifier:e.map((t=>t[0].entity_id)).join(""),data:n}})(t,c[t]))),timeline:u}},d=(t,e)=>t.callWS({type:"history/list_statistic_ids",statistic_type:e}),f=(t,e,n,s)=>t.callWS({type:"history/statistics_during_period",start_time:e.toISOString(),end_time:null==n?void 0:n.toISOString(),statistic_ids:s}),y=t=>{if(!t||t.length<2)return null;const e=t[t.length-1].sum;if(null===e)return null;const n=t[0].sum;return null===n?e:e-n},p=(t,e)=>{let n=null;for(const s of e){if(!(s in t))continue;const e=y(t[s]);null!==e&&(null===n?n=e:n+=e)}return n},g=(t,e)=>t.some((t=>null!==t[e])),h=t=>{let e=null,n=null;for(const s of t){if(0===s.length)continue;const t=new Date(s[0].start);null!==e?t<n&&(e=s[0].start,n=t):(e=s[0].start,n=t)}return e},m=(t,e)=>{let n=null;if(0===e.length)return null;const s=(t=>{const e=[],n=t.map((t=>[...t]));for(;n.some((t=>t.length>0));){const t=h(n);let s=0;for(const e of n){if(0===e.length)continue;if(e[0].start!==t)continue;const n=e.shift();n.sum&&(s+=n.sum)}e.push({start:t,sum:s})}return e})(e),r=[...t];let i=null;for(const e of s){if(new Date(e.start)>=new Date(t[0].start))break;i=e.sum}for(;r.length>0;){if(!s.length)return n;if(s[0].start!==r[0].start){new Date(s[0].start)<new Date(r[0].start)?s.shift():r.shift();continue}const t=s.shift(),e=r.shift();if(null!==i){const s=t.sum-i;null===n?n=s*(e.mean/100):n+=s*(e.mean/100)}i=t.sum}return n}},38926:(t,e,n)=>{"use strict";n.d(e,{VG:()=>_,AP:()=>y});var s=n(58831),r=n(22311),i=n(91741);var o=n(85415),a=n(5986),c=n(41499);const u=new Set(["automation","configurator","device_tracker","geo_location","persistent_notification","zone"]),l=new Set(["mobile_app"]),_=(t,e,n=!1)=>{const r=[],o=[],a=e.title?`${e.title} `:void 0;for(const[e,u]of t){const t=(0,s.M)(e);if("alarm_control_panel"===t){const t={type:"alarm-panel",entity:e};r.push(t)}else if("camera"===t){const t={type:"picture-entity",entity:e};r.push(t)}else if("climate"===t){const t={type:"thermostat",entity:e};r.push(t)}else if("humidifier"===t){const t={type:"humidifier",entity:e};r.push(t)}else if("light"===t&&n){const t={type:"light",entity:e};r.push(t)}else if("media_player"===t){const t={type:"media-control",entity:e};r.push(t)}else if("plant"===t){const t={type:"plant-status",entity:e};r.push(t)}else if("weather"===t){const t={type:"weather-forecast",entity:e,show_forecast:!1};r.push(t)}else if("sensor"===t&&(null==u?void 0:u.attributes.device_class)===c.A);else{let t;const n=a&&u&&(t=(0,i.C)(u))!==a&&t.startsWith(a)?{entity:e,name:d(t.substr(a.length))}:e;o.push(n)}}return o.length>0&&r.unshift({type:"entities",entities:o,...e}),r},d=t=>{return(e=t.substr(0,t.indexOf(" "))).toLowerCase()!==e?t:t[0].toUpperCase()+t.slice(1);var e},f=(t,e,n,c,u,l)=>{const d=(t=>{const e=[],n={};return Object.keys(t).forEach((r=>{const i=t[r];"group"===(0,s.M)(r)?e.push(i):n[r]=i})),e.forEach((t=>t.attributes.entity_id.forEach((t=>{delete n[t]})))),{groups:e,ungrouped:n}})(u);d.groups.sort(((t,e)=>l[t.entity_id]-l[e.entity_id]));const f={};Object.keys(d.ungrouped).forEach((t=>{const e=d.ungrouped[t],n=(0,r.N)(e);n in f||(f[n]=[]),f[n].push(e.entity_id)}));let y=[];d.groups.forEach((t=>{y=y.concat(_(t.attributes.entity_id.map((t=>[t,u[t]])),{title:(0,i.C)(t),show_header_toggle:"hidden"!==t.attributes.control}))})),Object.keys(f).sort().forEach((e=>{y=y.concat(_(f[e].sort(((t,e)=>(0,o.q)((0,i.C)(u[t]),(0,i.C)(u[e])))).map((t=>[t,u[t]])),{title:(0,a.Lh)(t,e)}))}));const p={path:e,title:n,cards:y};return c&&(p.icon=c),p},y=(t,e,n,s,i,o)=>{const a=((t,e)=>{const n={},s=new Set(e.filter((t=>l.has(t.platform))).map((t=>t.entity_id)));return Object.keys(t).forEach((e=>{const i=t[e];u.has((0,r.N)(i))||s.has(i.entity_id)||(n[e]=t[e])})),n})(s,n),c={};Object.keys(a).forEach((t=>{const e=a[t];e.attributes.order&&(c[t]=e.attributes.order)}));const d=((t,e,n,s)=>{const r={...s},i=[];for(const s of t){const t=[],o=new Set(e.filter((t=>t.area_id===s.area_id)).map((t=>t.id)));for(const e of n)(o.has(e.device_id)&&!e.area_id||e.area_id===s.area_id)&&e.entity_id in r&&(t.push(r[e.entity_id]),delete r[e.entity_id]);t.length>0&&i.push([s,t])}return{areasWithEntities:i,otherEntities:r}})(t,e,n,a),y=f(i,"default_view","Home",undefined,d.otherEntities,c),p=[];if(d.areasWithEntities.forEach((([t,e])=>{p.push(..._(e.map((t=>[t.entity_id,t])),{title:t.name}))})),o){const t=o.energy_sources.find((t=>"grid"===t.type));t&&t.flow_from.length>0&&p.push({title:"Energy distribution today",type:"energy-distribution",linkDashboard:!0})}return y.cards.unshift(...p),y}},76478:(t,e,n)=>{"use strict";n.r(e),n.d(e,{OriginalStatesStrategy:()=>_});var s=n(4915),r=n(11950),i=n(57066),o=n(57292),a=n(55424),c=n(74186),u=n(38926);let l=!1;class _{static async generateView(t){const e=t.hass;if(e.config.state===s.UE)return{cards:[{type:"starting"}]};if(e.config.safe_mode)return{cards:[{type:"safe-mode"}]};l||(l=!0,(0,i.sG)(e.connection,(()=>{})),(0,o.q4)(e.connection,(()=>{})),(0,c.LM)(e.connection,(()=>{})));const[n,_,d,f,y]=await Promise.all([(0,r.l)(e.connection,i.sG),(0,r.l)(e.connection,o.q4),(0,r.l)(e.connection,c.LM),e.loadBackendTranslation("title"),(0,a.ZC)(e).catch((()=>{}))]),p=(0,u.AP)(n,_,d,e.states,f,y);return e.config.components.includes("geo_location")&&p&&p.cards&&p.cards.push({type:"map",geo_location_sources:["all"]}),0===p.cards.length&&p.cards.push({type:"empty-state"}),p}static async generateDashboard(t){return{title:t.hass.config.location_name,views:[{strategy:{type:"original-states"}}]}}}}}]);
//# sourceMappingURL=e4280328.js.map