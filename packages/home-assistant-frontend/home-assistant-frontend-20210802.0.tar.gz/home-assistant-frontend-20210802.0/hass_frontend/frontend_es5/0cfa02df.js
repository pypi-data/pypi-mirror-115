(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8251],{98251:function(e,t){"use strict";function n(e){return(n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}Object.defineProperty(t,"__esModule",{value:!0});var r=new WeakMap,o=new WeakMap;function i(e){var t=r.get(e);return console.assert(null!=t,"'this' is expected an Event object, but got",e),t}function l(e){null==e.passiveListener?e.event.cancelable&&(e.canceled=!0,"function"==typeof e.event.preventDefault&&e.event.preventDefault()):"undefined"!=typeof console&&"function"==typeof console.error&&console.error("Unable to preventDefault inside passive event listener invocation.",e.passiveListener)}function u(e,t){r.set(this,{eventTarget:e,event:t,eventPhase:2,currentTarget:e,canceled:!1,stopped:!1,immediateStopped:!1,passiveListener:null,timeStamp:t.timeStamp||Date.now()}),Object.defineProperty(this,"isTrusted",{value:!1,enumerable:!0});for(var n=Object.keys(t),o=0;o<n.length;++o){var i=n[o];i in this||Object.defineProperty(this,i,a(i))}}function a(e){return{get:function(){return i(this).event[e]},set:function(t){i(this).event[e]=t},configurable:!0,enumerable:!0}}function s(e){return{value:function(){var t=i(this).event;return t[e].apply(t,arguments)},configurable:!0,enumerable:!0}}function c(e){if(null==e||e===Object.prototype)return u;var t=o.get(e);return null==t&&(t=function(e,t){var n=Object.keys(t);if(0===n.length)return e;function r(t,n){e.call(this,t,n)}r.prototype=Object.create(e.prototype,{constructor:{value:r,configurable:!0,writable:!0}});for(var o=0;o<n.length;++o){var i=n[o];if(!(i in e.prototype)){var l="function"==typeof Object.getOwnPropertyDescriptor(t,i).value;Object.defineProperty(r.prototype,i,l?s(i):a(i))}}return r}(c(Object.getPrototypeOf(e)),e),o.set(e,t)),t}function p(e){return i(e).immediateStopped}function f(e,t){i(e).passiveListener=t}u.prototype={get type(){return i(this).event.type},get target(){return i(this).eventTarget},get currentTarget(){return i(this).currentTarget},composedPath:function(){var e=i(this).currentTarget;return null==e?[]:[e]},get NONE(){return 0},get CAPTURING_PHASE(){return 1},get AT_TARGET(){return 2},get BUBBLING_PHASE(){return 3},get eventPhase(){return i(this).eventPhase},stopPropagation:function(){var e=i(this);e.stopped=!0,"function"==typeof e.event.stopPropagation&&e.event.stopPropagation()},stopImmediatePropagation:function(){var e=i(this);e.stopped=!0,e.immediateStopped=!0,"function"==typeof e.event.stopImmediatePropagation&&e.event.stopImmediatePropagation()},get bubbles(){return Boolean(i(this).event.bubbles)},get cancelable(){return Boolean(i(this).event.cancelable)},preventDefault:function(){l(i(this))},get defaultPrevented(){return i(this).canceled},get composed(){return Boolean(i(this).event.composed)},get timeStamp(){return i(this).timeStamp},get srcElement(){return i(this).eventTarget},get cancelBubble(){return i(this).stopped},set cancelBubble(e){if(e){var t=i(this);t.stopped=!0,"boolean"==typeof t.event.cancelBubble&&(t.event.cancelBubble=!0)}},get returnValue(){return!i(this).canceled},set returnValue(e){e||l(i(this))},initEvent:function(){}},Object.defineProperty(u.prototype,"constructor",{value:u,configurable:!0,writable:!0}),"undefined"!=typeof window&&void 0!==window.Event&&(Object.setPrototypeOf(u.prototype,window.Event.prototype),o.set(window.Event.prototype,u));var v=new WeakMap;function y(e){return null!==e&&"object"===n(e)}function d(e){var t=v.get(e);if(null==t)throw new TypeError("'this' is expected an EventTarget object, but got another value.");return t}function b(e,t){Object.defineProperty(e,"on".concat(t),function(e){return{get:function(){for(var t=d(this).get(e);null!=t;){if(3===t.listenerType)return t.listener;t=t.next}return null},set:function(t){"function"==typeof t||y(t)||(t=null);for(var n=d(this),r=null,o=n.get(e);null!=o;)3===o.listenerType?null!==r?r.next=o.next:null!==o.next?n.set(e,o.next):n.delete(e):r=o,o=o.next;if(null!==t){var i={listener:t,listenerType:3,passive:!1,once:!1,next:null};null===r?n.set(e,i):r.next=i}},configurable:!0,enumerable:!0}}(t))}function g(e){function t(){h.call(this)}t.prototype=Object.create(h.prototype,{constructor:{value:t,configurable:!0,writable:!0}});for(var n=0;n<e.length;++n)b(t.prototype,e[n]);return t}function h(){if(!(this instanceof h)){if(1===arguments.length&&Array.isArray(arguments[0]))return g(arguments[0]);if(arguments.length>0){for(var e=new Array(arguments.length),t=0;t<arguments.length;++t)e[t]=arguments[t];return g(e)}throw new TypeError("Cannot call a class as a function")}v.set(this,new Map)}h.prototype={addEventListener:function(e,t,n){if(null!=t){if("function"!=typeof t&&!y(t))throw new TypeError("'listener' should be a function or an object.");var r=d(this),o=y(n),i=(o?Boolean(n.capture):Boolean(n))?1:2,l={listener:t,listenerType:i,passive:o&&Boolean(n.passive),once:o&&Boolean(n.once),next:null},u=r.get(e);if(void 0!==u){for(var a=null;null!=u;){if(u.listener===t&&u.listenerType===i)return;a=u,u=u.next}a.next=l}else r.set(e,l)}},removeEventListener:function(e,t,n){if(null!=t)for(var r=d(this),o=(y(n)?Boolean(n.capture):Boolean(n))?1:2,i=null,l=r.get(e);null!=l;){if(l.listener===t&&l.listenerType===o)return void(null!==i?i.next=l.next:null!==l.next?r.set(e,l.next):r.delete(e));i=l,l=l.next}},dispatchEvent:function(e){if(null==e||"string"!=typeof e.type)throw new TypeError('"event.type" should be a string.');var t=d(this),n=e.type,r=t.get(n);if(null==r)return!0;for(var o=function(e,t){return new(c(Object.getPrototypeOf(t)))(e,t)}(this,e),l=null;null!=r;){if(r.once?null!==l?l.next=r.next:null!==r.next?t.set(n,r.next):t.delete(n):l=r,f(o,r.passive?r.listener:null),"function"==typeof r.listener)try{r.listener.call(this,o)}catch(u){"undefined"!=typeof console&&"function"==typeof console.error&&console.error(u)}else 3!==r.listenerType&&"function"==typeof r.listener.handleEvent&&r.listener.handleEvent(o);if(p(o))break;r=r.next}return f(o,null),function(e,t){i(e).eventPhase=t}(o,0),function(e,t){i(e).currentTarget=t}(o,null),!o.defaultPrevented}},Object.defineProperty(h.prototype,"constructor",{value:h,configurable:!0,writable:!0}),"undefined"!=typeof window&&void 0!==window.EventTarget&&Object.setPrototypeOf(h.prototype,window.EventTarget.prototype),t.defineEventAttribute=b,t.EventTarget=h,t.default=h,e.exports=h,e.exports.EventTarget=e.exports.default=h,e.exports.defineEventAttribute=b}}]);
//# sourceMappingURL=0cfa02df.js.map