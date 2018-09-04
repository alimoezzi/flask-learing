const a=document.querySelectorAll('input')
for (let i = 0; i < a.length; i++) {
    a[i].removeAttribute('required')
}