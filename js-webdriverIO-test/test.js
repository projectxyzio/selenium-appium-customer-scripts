const { remote } = require("webdriverio");
const argv = require("yargs").argv;
const fetch = require("node-fetch");
const assert = require("assert");

const userAction = async api_key => {
  const response = await fetch(
    "https://api-dev.headspin.io/v0/devices/automation-config",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + api_key
      }
    }
  );
  const myJson = await response.json();

  var index = [];
  for (var x in myJson) {
    index.push(x);
  }
  i = Math.floor(Math.random() * (index.length - 0 + 1));
  return myJson[index[i]];
};

async function setup() {
  if (argv.key) {
    var api_key = argv.key;
    var target_device = await userAction(api_key);
    const hostname = target_device.driver_url.split("/", 3)[2].split(":")[0];
    const port = target_device.driver_url.split("/", 3)[2].split(":")[1];
    const path = "/v0/" + api_key + "/wd/hub";
    var caps = target_device.capabilities;
    caps["headspin.capture"] = true;
    test(hostname, port, path, caps);
  } else if (argv.url && argv.browser) {
    var url = argv.url;
    var browser = argv.browser;

    const hostname = url.split("/", 3)[2].split(":")[0];
    const port = url.split("/", 3)[2].split(":")[1];
    const path = "/v0/" + url.split("/")[4] + "/wd/hub";

    var caps_2 = {
      "headspin:initialScreenSize": {
        width: 1920,
        height: 1080
      },
      browserName: browser,
      "headspin.capture": true
    };

    if (argv.ver) {
      caps_2["browserVersion"] = argv.ver;
      test(hostname, port, path, caps_2);
    } else {
      test(hostname, port, path, caps_2);
    }
  }
}

async function test(hostname, port, path, caps) {
  const browser = await remote({
    protocol: "https",
    hostname: hostname,
    port: Number(port),
    path: path,
    logLevel: "trace",
    capabilities: caps
  });

  await browser.url("https://powerbi.microsoft.com/en-us/landing/signin/");
  const inputElem = await browser.$(".medium-centered a");
  await inputElem.click();

  (await browser.$("#i0116")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  const signIn = await browser.$("#i0116");
  await signIn.setValue("scott@headspin.io");

  const nextButton = await browser.$("#idSIButton9");
  await nextButton.click();

  await browser.pause(1000);

  (await browser.$("#i0118")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  const passWord = await browser.$("#i0118");
  await passWord.setValue("BriSugi12!");

  (await browser.$("#idSIButton9")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });

  const signinButton = await browser.$("#idSIButton9");
  await signinButton.click();

  await browser.pause(500);

  await signinButton.click();

  const title = await browser.getTitle();

  assert.ok(title.includes("Power"));

  //////////////////////////////////////////////////////

  (await browser.$("span=Favorites")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  (await browser.$("span=Favorites")).click();

  (await browser.$("span=Recent")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  (await browser.$("span=Recent")).click();

  (await browser.$("span=Apps")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  (await browser.$("span=Apps")).click();

  (await browser.$("span=Shared with me")).waitForExist({
    timeout: 10000,
    timeoutMsg: "Element never found"
  });
  (await browser.$("span=Shared with me")).click();

  await browser.pause(3000);

  await browser.deleteSession();
}

setup().catch(e => console.error(e));
