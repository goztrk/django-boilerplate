(function SiteInit() {
  const Site = {
    init: function () {},
  };

  window.Site =
    window.Site !== undefined ? Object.assign(window.Site, Site) : Site;

  Site.init();
})();
