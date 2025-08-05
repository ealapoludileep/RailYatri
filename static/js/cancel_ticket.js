document.getElementById("reset-db").addEventListener("click", (event) => {
  console.log("Reseting database");
  fetch("/railway/reset-db")
});
