const categories = document.querySelectorAll('.categoryBtn')

categories.forEach((category)=>{
    category.addEventListener('click',async (e)=>{
        window.location.href=`/blogs?category=${e.target.dataset.category}&page=1`
    })
})