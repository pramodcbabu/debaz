const menuButton = document.querySelector(".menu-button");
const siteNav = document.querySelector(".site-nav");

menuButton?.addEventListener("click", () => {
  const isOpen = siteNav.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
});

siteNav?.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    siteNav.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
  }
});
