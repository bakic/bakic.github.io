/* Cookie consent + Google Consent Mode v2 for GA4.
   Everything is denied by default. gtag.js is only downloaded after the
   visitor accepts, so nothing reaches Google before an explicit choice. */
(function () {
  var GA_ID = document.currentScript.dataset.ga;
  var KEY = "consent-analytics";

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }

  gtag("consent", "default", {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    wait_for_update: 500
  });
  gtag("set", "ads_data_redaction", true);

  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function write(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var loaded = false;
  function loadGA() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", GA_ID);
  }

  function grant() {
    gtag("consent", "update", { analytics_storage: "granted" });
    loadGA();
  }

  function revoke() {
    gtag("consent", "update", { analytics_storage: "denied" });
    // remove the first-party GA cookies already set
    var host = location.hostname.split(".");
    var domains = [location.hostname, "." + host.slice(-2).join(".")];
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (name === "_ga" || name.indexOf("_ga_") === 0) {
        domains.forEach(function (d) {
          document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + d;
        });
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
      }
    });
  }

  var banner;
  function hide() { if (banner) { banner.remove(); banner = null; } }

  function show() {
    if (banner) return;
    banner = document.createElement("div");
    banner.className = "consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Cookie consent");
    banner.innerHTML =
      '<p>This website uses cookies to analyse traffic and improve your ' +
      'experience. You can accept or decline them, and change your choice ' +
      'at any time from the footer.</p>' +
      '<div class="consent-actions">' +
      '<button type="button" data-choice="denied">Decline</button>' +
      '<button type="button" data-choice="granted">Accept</button>' +
      '</div>';
    banner.addEventListener("click", function (e) {
      var choice = e.target.getAttribute && e.target.getAttribute("data-choice");
      if (!choice) return;
      write(choice);
      if (choice === "granted") grant(); else revoke();
      hide();
    });
    document.body.appendChild(banner);
    var first = banner.querySelector("button");
    if (first) first.focus();
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-consent-open]");
    if (t) { e.preventDefault(); show(); }
  });

  var saved = read();
  if (saved === "granted") grant();
  else if (saved !== "denied") show();
})();
