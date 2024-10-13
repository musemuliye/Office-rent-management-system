const shrink_btn = document.querySelector(".shrink-btn");
const sidebar_links = document.querySelectorAll(
  "a.orent__nav__link:not(.orent__nav__link_dd),a.orent__nav__dropdown-item"
);
const theme_selector = document.getElementById("theme-selector");
const orentNavBar = document.getElementById("orentNavBar");

const themes = {
  light: {
    name: "theme_light",
    icon: "orent-logos_black.png",
    selectorIcon: "bi bi-brightness-high",
  },
  dark: {
    name: "theme_dark",
    icon: "orent-logos_white.png",
    selectorIcon: "bi bi-moon-stars",
  },
};
const DEFAULT_THEME = "dark";

const applayTheme = (themeName, init = false) => {
  console.log("Active theme: " + themeName);
  const theme = themes[themeName];
  const iconLink = document.getElementById("orentIcon");
  localStorage.setItem("orent_active_theme", themeName);
  const classToToggle = init && themeName == DEFAULT_THEME ? "" : "dark-layout";
  theme_selector.classList.toggle(classToToggle);
  document.body.classList.toggle("dark-layout");
  document.querySelector("#theme-selector i").className = theme.selectorIcon;
};
const initTheme = () => {
  const activeThemeT =
    localStorage.getItem("orent_active_theme") || DEFAULT_THEME;
  if (activeThemeT != DEFAULT_THEME) {
    applayTheme(activeThemeT, true);
  }
};

initTheme();

theme_selector.addEventListener("click", (e) => {
  e.preventDefault();
  const themeName = theme_selector.classList.contains("dark-layout")
    ? "light"
    : "dark";
  applayTheme(themeName);
});

shrink_btn.addEventListener("click", (e) => {
  e.preventDefault();
  document.body.classList.toggle("shrink");
});

/*==================== Set Navbar active links ====================*/
function changeLink() {
  //Remove current active links
  const sidebar_sub_link_active = orentNavBar.querySelectorAll("a.active");
  sidebar_sub_link_active.forEach((activeLink) =>
    activeLink.classList.remove("active")
  );

  //Set current link as active
  this.classList.add("active");

  //Set parent link active for drodown links
  if (this.classList.contains("orent__nav__dropdown-item")) {
    const parentElement = this.closest(".orent__nav__dropdown");
    parentDD = parentElement
      ? parentElement.querySelector(".orent__nav__link")
      : null;
    if (parentDD) {
      parentDD.classList.add("active");
    }
    this.classList.add("active");
  }
}

sidebar_links.forEach((link) => link.addEventListener("click", changeLink));

/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) => {
  const toggleBtn = document.getElementById(headerToggle),
    nav = document.getElementById(navbarId);

  // Validate that variables exist
  if (toggleBtn && nav) {
    toggleBtn.addEventListener("click", () => {
      nav.classList.toggle("orent-mobile-show-nav-mobile");
    });
  }
};
showMenu("orent-header-toggle", "orentNavBar");

/*==================== Control Navbar dropdown slide ====================*/
$(".orent__nav__dropdown > a").click(function (e) {
  e.preventDefault();
  $(".orent__nav__dropdown-collapse").slideUp(350);

  if ($(this).parent().hasClass("nav__dropdown-active")) {
    $(".orent__nav__dropdown").removeClass("nav__dropdown-active");
    $(this).parent().removeClass("active");
  } else {
    $(".orent__nav__dropdown").removeClass("nav__dropdown-active");
    $(this).next(".orent__nav__dropdown-collapse").slideDown(350);
    $(this).parent().addClass("nav__dropdown-active");
  }
});
