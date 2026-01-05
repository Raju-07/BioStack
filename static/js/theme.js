const toggleBtn = document.getElementById("themeToggle");
const body = document.body;

toggleBtn.addEventListener("click", () => {
  const theme = body.getAttribute("data-theme");
  body.setAttribute("data-theme", theme === "dark" ? "light" : "dark");
});
