const input = document.getElementById("input");

input.addEventListener("change",(event)=>{
    const files = changeEvent(event);
    handleUpdate(files);
})

document.addEventListener("dragenter",(event)=>{
    event.preventDefault();
    console.log("dragenter");
    if(event.target.className =="dropbox"){
        event.target.style.background = "#616161";
    }
})



function changeEvent(event){
    const target = event.target;
    return target.files;
}

function handleUpdate(filelist){
    const preview = document.getElementById("dropbox");

    filelist.forEach((file) =>{
        const reader = new FileReader(); // 비동기 적으로 파일의 내용을 읽어들이는 객체
        reader.addEventListener("load", (event)=>{
            const img = el("img",{
                className : "embed-img",
                src: event.target?.result,
            });
            const imgContainer = el("div",{className: "container-img"},img);
            preview.append(imgContainer);
        });
        reader.readAsDataURL(file);
    });

}

function el(nodeName, attributes, ...children){
    const node =
        nodeName ==="fragment"
        ? document.createDocumentFragment() //다른 노드를 담는 임시 컨테이너 역할을 하는 특수 목적의 노드
        : document.createElement(nodeName);


    Object.entries(attributes).forEach(([key, value]) => {
        if(key === "events"){
            Object.entries(value).forEach(([type, listener]) =>{
                node.addEventListener(type, listener);
            }) ;
        }else if (key in node){
            try{
                node[key]= value;
            }catch (err){
                node.setAttribute(key, value);
            }
        } else {
            node.setAttribute(key, value);
        }
    });

    children.forEach((children) => {
        if(typeof childNode === "string"){
            node.appendChild(document.createTextNode(childNode));
        } else{
            node.appendChild(childNode);
        }
    });

    return node;
}