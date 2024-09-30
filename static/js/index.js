let prevScrollPosition = window.scrollY;

window.addEventListener("scroll", function() {
    const header = document.getElementsByTagName("header")[0];
    const logo = document.getElementsByClassName("logo")[0];
    const scrollPosition = window.scrollY;
    
    if (scrollPosition > 0) {
        // Shrink the element as you scroll down
        header.style.padding = "0px 10%";
        logo.style.height = "45px";
        logo.style.marginLeft = "30px";
    } else {
        // Restore the element to its original size when at the top
        header.style.padding = "2px 10%";
        logo.style.height = "60px";
        logo.style.marginLeft = "0";
    }

    // if (prevScrollPosition - scrollPosition > 0 && scrollPosition <= 100) {
    //     header.style.padding = "2px 10%";
    //     logo.style.height = "60px";
    //     logo.style.marginLeft = "0";
    // }

    prevScrollPosition = scrollPosition;
});
