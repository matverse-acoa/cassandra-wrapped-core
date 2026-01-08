const focusButton = document.querySelector("[data-action='toggle']");
const primaryAction = document.querySelector(".primary");
const secondaryAction = document.querySelector(".secondary");

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

primaryAction?.addEventListener("click", () => {
  scrollToSection("#overview");
});

secondaryAction?.addEventListener("click", () => {
  scrollToSection("#metrics");
});
