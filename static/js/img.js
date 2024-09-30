let elems = document.querySelectorAll(".img");

elems.forEach(elem => {
    let img = elem.getElementsByTagName("img")[0];

    let a = document.createElement("a");

    a.setAttribute("class", "popup_link");
    a.setAttribute("href", img.getAttribute("alt"));
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");

    a.setHTMLUnsafe("Go to source <i class=\"material-icons\" style=\"font-size: inherit; position: absolute; top: 5px; left: 75px;\">call_made</i>");

    elem.appendChild(a);
});