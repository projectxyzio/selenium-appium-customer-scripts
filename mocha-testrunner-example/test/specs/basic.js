const assert = require("assert");

describe("Microsoft PowerBI Test", () => {
  it("should sign in", () => {
    browser.url("https://powerbi.microsoft.com/en-us/landing/signin/");
   
    browser.$("*=Sign").click();

    const username = browser.$("#i0116")
    username.waitForEnabled({timeout: 5000})
    username.setValue("scott@headspin.io");

    const nextButton = browser.$("#idSIButton9")
    nextButton.waitForClickable({timeout: 5000})
    nextButton.click();

    browser.pause(1000);

    const password = browser.$("#i0118")
    password.waitForEnabled({timeout: 5000})
    password.setValue("BriSugi12!");

    
    const signInButton = browser.$("#idSIButton9")
    signInButton.waitForClickable({timeout: 5000})
    signInButton.click();

    browser.pause(1000);

    const yesButton = browser.$("#idSIButton9")
    yesButton.waitForClickable({timeout: 5000})
    yesButton.click();

    browser.pause(2000);

    const title = browser.getUrl();
    assert.strictEqual(
      title,
      "https://app.powerbi.com/home?noSignUpCheck=1"
    );

  });

  it("should launch recent dashbaord", () => {
    
    const recentPage = browser.$("span=Recent")
    recentPage.waitForEnabled({timeout: 5000})
    recentPage.click()

    const retailPage = browser.$("span=Retail Analysis Sample")
    retailPage.waitForEnabled({timeout: 5000})
    retailPage.click();

    const homePage = browser.$(".home")
    homePage.waitForEnabled({timeout: 5000})
    homePage.click();

    const widgetTitle = browser.$(".widget-title")
    widgetTitle.waitForExist({timeout: 5000})
    const title = widgetTitle.getText();

    browser.pause(5000);

    assert.ok(title.includes("Scott"));
  });

  it("should naviagte to apps page", () => {
    const appPage = browser.$("span=Apps")
    appPage.waitForEnabled({timeout: 5000})
    appPage.click();
    const title = browser.$(".title")
    title.waitForExist({timeout: 3000})
    const refTitle = title.getText();
    assert.strictEqual(refTitle, "You don't have any apps yet");
  });

  it("should interact with search bar", () => {
    
    browser.waitUntil(() => browser.$(".searchBox").isEnabled() === true, {
      timeout: 5000,
      timeoutMsg: "element was ever enabled"
    });
    
    browser.$(".searchBox input").setValue("This is a test search");
    
    const elem = browser.$(".empty-search-img");
    assert.ok(elem.isExisting({timeout: 5000}));
  });

  it("should navigate to favorites", () => {
    const favoritesPage = browser.$('span=Favorites')
    favoritesPage.waitForEnabled({timeout: 5000})
    favoritesPage.click();
    browser.pause(500);
    const elem = browser.$('.noFavTitle');
    assert.ok(elem.isExisting({timeout: 5000}));
  })
});
