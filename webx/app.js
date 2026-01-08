const focusButton = document.querySelector("[data-action='toggle']");
const scrollToSection = (selector) => {
  const section = document.querySelector(selector);
  if (!section) {
    return;
  }
  section.scrollIntoView({ behavior: "smooth", block: "start" });
};

focusButton?.addEventListener("click", () => {
  document.body.classList.toggle("focus-mode");
  focusButton.textContent = document.body.classList.contains("focus-mode")
    ? "Modo Expandido"
    : "Modo Foco";
});

document.querySelectorAll("[data-target]").forEach((button) => {
  button.addEventListener("click", () => {
    const target = button.getAttribute("data-target");
    if (target) {
      scrollToSection(target);
    }
  });
});
