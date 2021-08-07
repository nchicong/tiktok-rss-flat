var userTitleNodes = document.querySelectorAll(".user-title");

var list = "";
for (var i = 0; i < userTitleNodes.length; i++) {
  list += userTitleNodes[i].textContent + "\n";
}