"use strict";

const element = document.getElementById("comment");

var cm_list = [];


function ajax(method, url, body){
    return new Promise(
        function(resolve){
            const xhr = new XMLHttpRequest();

            xhr.onreadystatechange = function(){
                if (xhr.readyState === 4) {
                    resolve(JSON.parse(xhr.responseText));
                }
            }

            xhr.open(method, url);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

            xhr.send(body);
        }
    );
}


function comment(){
    var dummy = ajax("GET", `/comment/get/${idx}`, null);

    dummy.then(function(value){
        cm_list = value;
        render();
    });
}


function render(){
    element.innerHTML = "";

    for(var index in cm_list){
        var cm = cm_list[index];

        var li = document.createElement("li");
        var label = document.createElement("label");
        var span = document.createElement("span");

        li.setAttribute("class", "list-group-item");
        li.setAttribute("id", `cm_area_${cm.comment}`);
        li.setAttribute("data-comment", cm.comment);

        label.setAttribute("class", "col-sm-2");
        label.setAttribute("for", `cm_${cm.comment}`);
        label.setAttribute("data-comment", cm.comment);
        label.appendChild(document.createTextNode(cm.date));

        span.setAttribute("class", "cm");
        span.setAttribute("id", `cm_${cm.comment}`);
        span.setAttribute("data-comment", cm.comment);
        span.appendChild(document.createTextNode(cm.text));

        li.appendChild(label);
        li.appendChild(span);

        element.appendChild(li);

        document.getElementById(`cm_area_${cm.comment}`).addEventListener("click",function(event){
            console.log(event.target.dataset.comment);
            const cm_id = event.target.dataset.comment;
            let password = window.prompt("댓글을 삭제하려면 비밀번호를 입력해주세요");

            if (password.length == 0){
                window.alert("댓글을 입력해주세요");
            }
            else {
                var result = {};
                var dummy = ajax("POST", `/comment/delete/${idx}/${cm_id}`, `password=${password}`);

                dummy.then(function(value){
                    window.alert(value.msg);
                    comment();
                });
            }
        });
    }
}

/* * * * * * * * * * * * * * * * * * */

comment();

document.getElementById("cm_send").addEventListener("click",function(){
    var password = document.getElementById("cm_password").value;
    var content = document.getElementById("cm_content").value;

    var dummy = ajax("POST", `/comment/add/${idx}`, `text=${content}&password=${password}`);
    dummy.then(function(value){
        window.alert(value.msg);
        comment();

        document.getElementById("cm_content").value = "";
    });
});
