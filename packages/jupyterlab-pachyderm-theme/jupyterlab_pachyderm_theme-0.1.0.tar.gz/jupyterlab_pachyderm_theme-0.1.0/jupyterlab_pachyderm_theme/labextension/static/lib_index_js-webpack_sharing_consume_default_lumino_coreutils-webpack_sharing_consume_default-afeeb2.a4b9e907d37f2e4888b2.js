"use strict";
(self["webpackChunk_pachyderm_jupyterlab_pachyderm_theme"] = self["webpackChunk_pachyderm_jupyterlab_pachyderm_theme"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-afeeb2"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/polling */ "./node_modules/@lumino/polling/dist/index.es6.js");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);



/**
 * The interval in milliseconds before recover options appear during splash.
 */
const SPLASH_RECOVER_TIMEOUT = 12000;
/**
 * The command IDs used by the apputils plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.loadState = 'apputils:load-statedb';
    CommandIDs.print = 'apputils:print';
    CommandIDs.reset = 'apputils:reset';
    CommandIDs.resetOnLoad = 'apputils:reset-on-load';
    CommandIDs.runFirstEnabled = 'apputils:run-first-enabled';
})(CommandIDs || (CommandIDs = {}));
let head = document.head || document.getElementsByTagName('head')[0];
function changeFavicon(src) {
    let link = document.createElement('link'), oldLink = document.getElementById('dynamic-favicon');
    link.id = 'dynamic-favicon';
    link.rel = 'icon';
    link.type = 'image/x-icon';
    link.href = src;
    if (oldLink) {
        head.removeChild(oldLink);
    }
    head.appendChild(link);
}
/**
 * A splash screen for pachyderm
 */
const splash = {
    id: '@pachyderm/jupyterlab-pachyderm-theme:plugin',
    autoStart: true,
    // requires: [ITranslator],
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ISplashScreen,
    activate: (app
    // translator: ITranslator
    ) => {
        // const trans = translator.load('jupyterlab');
        const { commands, restored } = app;
        changeFavicon('https://www.pachyderm.com/favicons/favicon.ico');
        const splash = document.createElement('div');
        splash.id = 'pachyderm-splash';
        const logo = document.createElement('div');
        logo.id = 'pachyderm-logo';
        splash.appendChild(logo);
        const graphic = document.createElement('div');
        logo.appendChild(graphic);
        graphic.className = 'logoGraphic';
        const graphicTop = document.createElement('div');
        graphic.appendChild(graphicTop);
        graphicTop.className = 'graphicTop';
        const graphicMid = document.createElement('div');
        graphic.appendChild(graphicMid);
        graphicMid.className = 'graphicMid';
        const graphicBot = document.createElement('div');
        graphic.appendChild(graphicBot);
        graphicBot.className = 'graphicBot';
        const text = document.createElement('div');
        logo.appendChild(text);
        text.className = 'logoText';
        const pachyderm = document.createElement('h1');
        pachyderm.innerHTML = 'Pachyderm';
        text.appendChild(pachyderm);
        const labs = document.createElement('h2');
        labs.innerHTML = 'Labs';
        text.appendChild(labs);
        // Create debounced recovery dialog function.
        let dialog;
        const recovery = new _lumino_polling__WEBPACK_IMPORTED_MODULE_1__.Throttler(async () => {
            if (dialog) {
                return;
            }
            dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
                title: 'Loading...',
                body: `The loading screen is taking a long time. 
Would you like to clear the workspace or keep waiting?`,
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Keep Waiting' }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: 'Clear Workspace' })
                ]
            });
            try {
                const result = await dialog.launch();
                dialog.dispose();
                dialog = null;
                if (result.button.accept && commands.hasCommand(CommandIDs.reset)) {
                    return commands.execute(CommandIDs.reset);
                }
                // Re-invoke the recovery timer in the next frame.
                requestAnimationFrame(() => {
                    // Because recovery can be stopped, handle invocation rejection.
                    void recovery.invoke().catch(_ => undefined);
                });
            }
            catch (error) {
                /* no-op */
            }
        }, { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' });
        // Return ISplashScreen.
        let splashCount = 0;
        return {
            show: () => {
                splash.classList.remove('splash-fade');
                splashCount++;
                console.log('adding');
                document.body.appendChild(splash);
                // Because recovery can be stopped, handle invocation rejection.
                void recovery.invoke().catch(_ => undefined);
                return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(async () => {
                    await restored;
                    if (--splashCount === 0) {
                        void recovery.stop();
                        if (dialog) {
                            dialog.dispose();
                            dialog = null;
                        }
                        splash.classList.add('splash-fade');
                        window.setTimeout(() => {
                            document.body.removeChild(splash);
                        }, 200);
                    }
                });
            }
        };
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (splash);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-afeeb2.a4b9e907d37f2e4888b2.js.map