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

app.init();




