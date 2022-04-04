//init
const app={
    init:()=>{
        document.addEventListener('DOMContentLoaded',app.load);
        console.log('HTML loaded');
    },
    load:()=>{
        console.log('loading');

    },
}

const validate_customer=()=>{
    const email=document.querySelector('.email');
    const password=document.querySelector('.password1');

    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){
        alert('email is not valid')
    }
    if(password.length<5){
        alert('password needs to be at least 5 characters');
    }/*else if(){ //server return error
        alert('wrong credentials')
    }else if(){ //server return 200 OK
        window.location.href="customer.html";
    }*/
}

const validate_employee=()=>{
    const password=document.querySelector('.password2');

    if(password.length<5){
        alert('password needs to be at least 5 characters');
    }/*else if(){ //server return error
        alert('wrong credentials')
    }else if(){ //server return 200 OK
        window.location.href="employee.html";
    }*/
}
const detectProduct=()=>{
    const products=document.querySelectorAll('#pname');
    for(let product of products){
        product.addEventListener('click',(e)=>{
            e.preventDefault();
            const ID=product.children[0].textContent;
            localStorage.setItem('query',ID);
            window.location.href=`http://localhost:8111/product`;
            getProduct();
            //redirect 
        })
    }
}

const getProduct=async()=>{
    const ID=localStorage.getItem('query');
    //fetch data from server
    const response=await fetch(`http://localhost:8111/product/id=${ID}`);
    console.log(response)
    //show product information on product.html
    showProduct(response);
}

const showProduct=(data)=>{
    //build DOM
    const ID=localStorage.getItem('query');
    const detail=document.querySelector('.detailed');
    detail.textContent=ID;
}
app.init();
detectProduct();




