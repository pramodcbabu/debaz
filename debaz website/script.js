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

// TVK Executive Portal Modal Functions
function openLoginModal() {
  const modal = document.getElementById("tvkModal");
  if (modal) modal.style.display = "flex";
}

function closeLoginModal() {
  const modal = document.getElementById("tvkModal");
  if (modal) modal.style.display = "none";
}

function handleTvkLogin(e) {
  e.preventDefault();
  const u = document.getElementById("tvkUsername").value;
  const p = document.getElementById("tvkPassword").value;
  if ((u === "tvk_admin" || u === "tvk_leadership" || u === "debaz") && (p === "tvk2026" || p === "debaz2026")) {
    document.getElementById("tvkError").style.display = "none";
    alert("✅ Authentication Successful! Redirecting to TVK Nethra Campaign Suite...");
    window.location.href = "http://localhost:8501";
  } else {
    document.getElementById("tvkError").style.display = "block";
  }
}
