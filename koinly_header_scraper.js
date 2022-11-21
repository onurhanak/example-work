const puppeteer = require("puppeteer-extra");
const fs = require("fs");

// add stealth plugin and use defaults. This will help us go undetected
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

// get the current working directory, useful to write shortcuts
const workingDirectory = __dirname;

// program to solve captcha
const captchaPath = "--load-extension=" + workingDirectory + "/captcha";

// get credentials from argv
emailAddress = process.argv[2];
password = process.argv[3];

// main function
async function main() {
  // start puppeteer and add captcha extension
  puppeteer
    .launch({
      headless: false,
      args: [captchaPath],
    })
    .then(async (browser) => {

      console.log("\nGetting data from Koinly");
      const page = await browser.newPage();

      // go to login page
      await page.goto("https://app.koinly.io/login/");

      // sleep for a while
      await new Promise(resolve => setTimeout(resolve, 10000));

      // locate input fields and enter credentials
      let input = await page.waitForSelector('input[type="email"]');
      let pw_input = await page.waitForSelector('input[type="password"]');

      await input.type(emailAddress);
      await pw_input.type(password);

      await page.$eval("button[type=submit]", (el) => el.click());

      await new Promise(resolve => setTimeout(resolve, 3000));

      // find captcha frame and locate the solver button and click it
      try {
        var frames = await page.frames();
        var myframe = frames.find((f) =>
          f.url().includes("recaptcha/api2/bframe")
        );
        var btn = await myframe.waitForSelector("#solver-button");

        await btn.click();
        

        // monitor requests so that we can find the api request and hijack it
        await page.on("request", async (request) => {
          // Ignore OPTIONS requests
          if (request.url().includes("assets?per_page=400")) {
            console.log("\n We got the request url: ", request.url());
            var headers = request.headers();
            if ("x-auth-token" in headers) {
              const page = await browser.newPage();
              await page.setExtraHTTPHeaders(headers);

              await page.goto("https://api.koinly.io/api/assets?per_page=400");

              // write assets data to file for python to use
              jsonData = await page.evaluate(() => {
                return document.querySelector("body").innerText;
              });
              dataPath = workingDirectory + "/tmp/data.json";
              fs.writeFileSync(dataPath, jsonData);

              console.log(
                "\nGot the data from Koinly. Switching back to Python."
              );

              await browser.close();
            }
          }
        });
      } catch (e) {
        console.log(e);
        console.log("Could not find captcha frame.");

        await page.reload();
        // monitor requests so that we can find the api request and hijack it
        await page.on("request", async (request) => {
          // Ignore OPTIONS requests
          if (request.url().includes("assets?per_page=400")) {
            console.log("\n We got the request url: ", request.url());
            var headers = request.headers();
            if ("x-auth-token" in headers) {
              const page = await browser.newPage();
              await page.setExtraHTTPHeaders(headers);

              await page.goto("https://api.koinly.io/api/assets?per_page=400");

              // write assets data to file for python to use
              jsonData = await page.evaluate(() => {
                return document.querySelector("body").innerText;
              });
              dataPath = workingDirectory + "/tmp/data.json";
              fs.writeFileSync(dataPath, jsonData);

              console.log(
                "\nGot the data from Koinly. Switching back to Python."
              );

              await browser.close();
            }
          }
        });
      }
    });
}

main();
