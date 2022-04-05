//init
const app={
    init:()=>{
        document.addEventListener('DOMContentLoaded',app.load);
        console.log('HTML loaded');
    },
    load:()=>{
        console.log('loading');
        let page=document.body.id;
        switch(page){
            case 'index':
                add_cart();
                delete_cart();
            case 'checkout':
                show_order();
                setOrder();
        }   
    },
}

const add_cart=()=>{
    const buttons=document.querySelectorAll('.add-shopping');
    let selection=''
    for(let button of buttons){
        button.addEventListener('click',()=>{
            alert('item has been added to your shopping cart!');
            selection=button.parentNode.parentNode.childNodes[1].textContent;
            localStorage.setItem('product',selection);
        })
    }
}

const delete_cart=()=>{
    const buttons=document.querySelectorAll('.delete-shopping');
    for(let button of buttons){
        button.addEventListener('click',()=>{
            let item=localStorage.getItem('product');
            if(!item){
                alert('there is nothing to delete! your shopping cart is empty ');
                return;
            }
            let selection='';
            localStorage.setItem('product',selection);
            alert('item has been deleted from your shopping cart!');
        })
    }
}
const show_order=()=>{
    const shipping_info=document.querySelector('.detail');
    let order_div=document.createElement('h3');
    if(shipping_info) shipping_info.appendChild(order_div)
    let items=localStorage.getItem('product');
    if(items){
        order_div.innerText=items;
    }else{
        order_div.innerText='Your shoppping cart is empty'
    }
}

const setOrder=()=>{
    const product=document.querySelector('#set-item')
    const confirm=document.querySelector('.confirm');
    confirm.addEventListener(('click'),()=>{
        let item=localStorage.getItem('product');
        if(item){
            product.value=item;
            console.log('value set!')
        }
    })
}

const payNow=()=>{
    const pay=document.querySelector('#paynow');
    pay.addEventListener(('click',(e)=>{
        e.preventDefault();
    }))
}

app.init();

//delete_cart();
//show_order();
//checkPaymant();




