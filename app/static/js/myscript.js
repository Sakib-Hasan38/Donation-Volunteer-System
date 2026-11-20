$(document).ready(function(){
    $('#mytable').DataTable();


const btn = document.querySelector('#btn-sidebar');
const sidebar = document.querySelector('.sidebar');

if (btn && sidebar){
    btn.onclick = function(){
        sidebar.classList.toggle('active');
    };
}
});
