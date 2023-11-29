var to = parseInt(document.getElementById("age_to").value);
var from = parseInt(document.getElementById("age_from").value);
if (from == NaN && to == NaN) {
  document.getElementById("seach_button").setAttribute("disabled", true);
} else if (from != NaN && to != NaN && to < from) {
  document.getElementById("inputError").innerHTML =
    "Age to should be greater than from";
  document.getElementById("seach_button").setAttribute("disabled", true);
} else {
  document.getElementById("inputError").innerHTML = "";
  document.getElementById("seach_button").removeAttribute("disabled");
}

document.getElementById("age_from").addEventListener("change", (event) => {
  document.getElementById("inputError").innerHTML = "";
  var from = parseInt(event.target.value);
  var to = parseInt(document.getElementById("age_to").value);
  if (to != NaN && to < from) {
    document.getElementById("inputError").innerHTML =
      "Age to should be greater than from";
    document.getElementById("seach_button").setAttribute("disabled", true);
  } else {
    document.getElementById("inputError").innerHTML = "";
    document.getElementById("seach_button").removeAttribute("disabled");
  }
});

document.getElementById("age_to").addEventListener("change", (event) => {
  document.getElementById("inputError").innerHTML = "";
  var to = parseInt(event.target.value);
  var from = parseInt(document.getElementById("age_from").value);
  if (from != NaN && to < from) {
    document.getElementById("inputError").innerHTML =
      "Age to should be greater than from";
    document.getElementById("seach_button").setAttribute("disabled", true);
  } else {
    document.getElementById("inputError").innerHTML = "";
    document.getElementById("seach_button").removeAttribute("disabled");
  }
});
