/*rotate chevron on click over the whole <li> area
see styles.css for .chevron-rotate and .chevron-rotate.down*/
$("#menu-content li").click(function(){
 $(this).find('i').toggleClass("down")  ;
})
