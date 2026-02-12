document.addEventListener("DOMContentLoaded", function() {
    const memoForm = document.getElementById("memo-form");
    const authorInput = document.getElementById("author");
    const contentInput = document.getElementById("content");
    //const memoInput = document.getElementById("memo-input");
    //const memoList = document.getElementById("memo-list");  


    memoForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // 폼 제출 기본 동작 방지   
        const author = authorInput.value.trim();
        const content = contentInput.value.trim();
        if (!(author && content)) {
            alert("작성자와 메모 내용을 모두 입력해주세요.");
            return;
        }
        alert(author + ':' + content);
        
        const result= await fetch('/memo',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  
            },
            body: JSON.stringify({ author, content })  
        })
        const data = await result.json();
        console.log('서버 응답:', data);
        alert(data.message);
        authorInput.value = '';
        contentInput.value = '';
    });
})