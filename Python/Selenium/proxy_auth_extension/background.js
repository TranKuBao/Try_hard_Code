
var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "116.105.33.18",
        port: parseInt("22953")
      },
      bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "tmproxyLUf2H",
            password: "3VlALyLoLy"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
    